#!/usr/bin/env python3
"""Restore verified inert repository bytes from the Lucifer Markdown handoff.

No network, subprocess, Git, evaluation, import of bundled code, or installation.
Run only in a trusted private parent directory; concurrent hostile writers are
outside this portable utility's threat model. Integrity hashes are not signatures.
"""
import argparse
import base64
import binascii
import hashlib
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

MAX_DOCUMENT = 12 * 1024 * 1024
MAX_COMPRESSED = 4 * 1024 * 1024
MAX_JSON = 8 * 1024 * 1024
MAX_TOTAL = 32 * 1024 * 1024
MAX_FILE = 1024 * 1024
MAX_FILES = 2048
MAX_BLOBS = 1024
MEMORY_LIMIT = 128 * 1024 * 1024
META_KEYS = {
    'schema', 'encoding', 'created_date', 'compressed_bytes',
    'compressed_sha256', 'json_bytes', 'json_sha256', 'base64_characters',
    'file_count', 'unique_blobs', 'total_file_bytes', 'max_file_bytes',
    'file_manifest_sha256', 'candidate_fingerprint', 'canonical_path',
    'canonical_sha256', 'canonical_bytes', 'extractor_sha256',
}
REQUIRED = {'README.md', 'start here.md', 'goal.md', 'AGENTS.md', 'persona.md',
            'tools/restore_singlefile.py', 'workflow/state.json',
            'workflow/review-files.json', 'workflow/input-manifest.json'}
RESERVED = {'con', 'prn', 'aux', 'nul', 'clock$'} | {
    f'{prefix}{digit}' for prefix in ('com', 'lpt') for digit in range(1, 10)
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical_json(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key')
        result[key] = value
    return result


def read_json(data):
    def reject_constant(value):
        raise ValueError('Nonstandard JSON constant: ' + value)
    def bounded_int(value):
        digits = value[1:] if value.startswith('-') else value
        require(len(digits) <= 16, 'JSON integer exceeds digit limit')
        return int(value)
    def reject_float(value):
        raise ValueError('Floating-point values are not part of the transport schema')
    return json.loads(data.decode('utf-8'), object_pairs_hook=unique_object,
                      parse_constant=reject_constant, parse_int=bounded_int,
                      parse_float=reject_float)


def valid_hash(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def integer(value, minimum, maximum, label):
    require(type(value) is int and minimum <= value <= maximum,
            'Invalid bounded integer: ' + label)


def block(document, label, language, ticks=3):
    # Split marker literals so this program does not duplicate live delimiters.
    prefix = b'<!-- LUCIFER:' + label.encode('ascii')
    begin = prefix + b':BEGIN -->'
    end = prefix + b':END -->'
    starts = list(re.finditer(rb'^' + re.escape(begin) + rb'\r?\n', document, re.M))
    ends = list(re.finditer(rb'^' + re.escape(end) + rb'(?:\r?\n|\Z)', document, re.M))
    require(len(starts) == len(ends) == 1, 'Missing or duplicate block: ' + label)
    require(starts[0].end() < ends[0].start(), 'Reversed block: ' + label)
    lines = document[starts[0].end():ends[0].start()].splitlines(keepends=True)
    require(len(lines) >= 2, 'Empty fenced block: ' + label)
    fence = b'`' * ticks
    require(lines[0].rstrip(b'\r\n') == fence + language.encode('ascii'),
            'Invalid opening fence: ' + label)
    require(lines[-1].rstrip(b'\r\n') == fence, 'Invalid closing fence: ' + label)
    return b''.join(lines[1:-1])


def validate_path(relative):
    require(isinstance(relative, str) and 0 < len(relative) <= 240,
            'Invalid path length or type')
    require(re.fullmatch(r'[A-Za-z0-9._ /-]+', relative) is not None,
            'Nonportable path characters')
    parts = relative.split('/')
    require(all(p and p not in ('.', '..') for p in parts), 'Unsafe path component')
    require(not relative.startswith('/') and PurePosixPath(relative).as_posix() == relative,
            'Path must be normalized and relative')
    for part in parts:
        require(not part.endswith(('.', ' ')), 'Trailing dot/space in path')
        require(part.casefold().split('.')[0].rstrip(' ') not in RESERVED,
                'Reserved device path')
        require(part.casefold() != '.git', 'Git metadata is not a payload file')
    return parts


def decode_document(document):
    require(len(document) <= MAX_DOCUMENT, 'Document exceeds hard size limit')
    terminal = b'<!-- LUCIFER:HANDOFF:' + b'END -->'
    require(document.rstrip().endswith(terminal) and
            len(re.findall(rb'^' + re.escape(terminal) + rb'(?:\r?\n|\Z)', document, re.M)) == 1,
            'Missing or duplicate final handoff marker')
    metadata = read_json(block(document, 'METADATA', 'json'))
    require(isinstance(metadata, dict) and set(metadata) == META_KEYS,
            'Unsupported metadata schema fields')
    require(metadata['schema'] == 'lucifer-singlefile-v1', 'Unsupported metadata version')
    require(metadata['encoding'] == 'base64-xz-json-content-addressed-v1',
            'Unsupported payload encoding')
    require(isinstance(metadata['created_date'], str) and
            re.fullmatch(r'\d{4}-\d{2}-\d{2}', metadata['created_date']) is not None,
            'Invalid preparation date')
    for key in ('compressed_sha256', 'json_sha256', 'file_manifest_sha256',
                'candidate_fingerprint', 'canonical_sha256', 'extractor_sha256'):
        require(valid_hash(metadata[key]), 'Invalid hash: ' + key)
    bounds = {
        'compressed_bytes': (1, MAX_COMPRESSED), 'json_bytes': (1, MAX_JSON),
        'base64_characters': (4, 4 * ((MAX_COMPRESSED + 2) // 3)),
        'file_count': (1, MAX_FILES), 'unique_blobs': (1, MAX_BLOBS),
        'total_file_bytes': (1, MAX_TOTAL), 'max_file_bytes': (1, MAX_FILE),
        'canonical_bytes': (1, MAX_FILE),
    }
    for key, (low, high) in bounds.items():
        integer(metadata[key], low, high, key)
    require(metadata['canonical_path'] == 'persona.md', 'Unexpected canonical path')
    encoded = block(document, 'PAYLOAD', 'base64')
    require(re.fullmatch(rb'[A-Za-z0-9+/=\r\n \t]+', encoded) is not None,
            'Invalid base64 alphabet')
    compact = re.sub(rb'[\r\n \t]', b'', encoded)
    require(len(compact) == metadata['base64_characters'], 'Base64 length mismatch')
    require(len(compact) == 4 * ((metadata['compressed_bytes'] + 2) // 3),
            'Inconsistent encoded size')
    compressed = base64.b64decode(compact, validate=True)
    require(len(compressed) == metadata['compressed_bytes'] and
            digest(compressed) == metadata['compressed_sha256'], 'Compressed payload mismatch')
    decoder = lzma.LZMADecompressor(format=lzma.FORMAT_XZ, memlimit=MEMORY_LIMIT)
    raw = decoder.decompress(compressed, max_length=MAX_JSON + 1)
    require(len(raw) <= MAX_JSON and decoder.eof and not decoder.unused_data,
            'Incomplete, concatenated, trailing or oversized XZ stream')
    require(len(raw) == metadata['json_bytes'] and digest(raw) == metadata['json_sha256'],
            'Decoded JSON mismatch')
    bundle = read_json(raw)
    require(isinstance(bundle, dict) and set(bundle) == {'schema', 'files', 'blobs'} and
            bundle['schema'] == 'lucifer-repository-bundle-v1', 'Unsupported bundle schema')
    files, encoded_blobs = bundle['files'], bundle['blobs']
    require(isinstance(files, list) and len(files) == metadata['file_count'], 'File count mismatch')
    require(isinstance(encoded_blobs, dict) and len(encoded_blobs) == metadata['unique_blobs'],
            'Unique blob count mismatch')
    require(digest(canonical_json(files)) == metadata['file_manifest_sha256'],
            'File manifest mismatch')
    paths, folded, directories, sizes, total = [], {}, set(), {}, 0
    for entry in files:
        require(isinstance(entry, dict) and set(entry) == {'path', 'mode', 'bytes', 'sha256'},
                'Unsupported file entry schema')
        parts = validate_path(entry['path'])
        require(entry['mode'] in ('100644', '100755'), 'Unsupported Git mode')
        integer(entry['bytes'], 0, MAX_FILE, 'file bytes')
        require(valid_hash(entry['sha256']), 'Invalid file hash')
        for depth in range(1, len(parts) + 1):
            current = '/'.join(parts[:depth])
            key = current.casefold()
            require(key not in folded or folded[key] == current, 'Case-colliding path')
            folded[key] = current
        directories.update('/'.join(parts[:depth]) for depth in range(1, len(parts)))
        require(entry['sha256'] not in sizes or sizes[entry['sha256']] == entry['bytes'],
                'Same hash has inconsistent file sizes')
        sizes[entry['sha256']] = entry['bytes']
        total += entry['bytes']
        paths.append(entry['path'])
    require(paths == sorted(paths) and len(paths) == len(set(paths)),
            'Unsorted or duplicate file paths')
    require(not set(paths).intersection(directories), 'File/directory collision')
    require(REQUIRED.issubset(paths), 'Missing required repository files')
    require(total == metadata['total_file_bytes'] and total <= MAX_TOTAL, 'Total bytes mismatch')
    require(max(sizes.values()) == metadata['max_file_bytes'], 'Maximum file size mismatch')
    require(set(encoded_blobs) == set(sizes), 'Missing or unreferenced content blob')
    blobs = {}
    for sha, value in encoded_blobs.items():
        require(valid_hash(sha) and isinstance(value, str), 'Invalid blob entry')
        require(len(value) == 4 * ((sizes[sha] + 2) // 3), 'Blob encoded length mismatch')
        data = base64.b64decode(value, validate=True)
        require(len(data) == sizes[sha] and digest(data) == sha, 'Blob hash/size mismatch')
        blobs[sha] = data
    entries = {entry['path']: entry for entry in files}
    canonical = blobs[entries['persona.md']['sha256']]
    require(digest(canonical) == metadata['canonical_sha256'] and
            len(canonical) == metadata['canonical_bytes'], 'Canonical specification mismatch')
    require(block(document, 'CANONICAL', 'markdown', ticks=6) == canonical,
            'Plaintext canonical projection differs from restored bytes')
    extractor = blobs[entries['tools/restore_singlefile.py']['sha256']]
    require(digest(extractor) == metadata['extractor_sha256'] and
            block(document, 'EXTRACTOR', 'python') == extractor,
            'Extractor projection mismatch')
    state = read_json(blobs[entries['workflow/state.json']['sha256']])
    manifest = read_json(blobs[entries['workflow/input-manifest.json']['sha256']])
    require(isinstance(state, dict) and isinstance(manifest, dict) and
            state.get('candidate_fingerprint') == manifest.get('fingerprint') == metadata['candidate_fingerprint'],
            'Preparation fingerprint mismatch')
    return metadata, files, blobs


def is_link_or_reparse(path):
    try:
        info = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400))


def restore(metadata, files, blobs, destination):
    destination = Path(os.path.abspath(os.fspath(destination)))
    require(destination.parent.is_dir(), 'Choose an existing private parent directory')
    require(not any(is_link_or_reparse(path) for path in [destination, *destination.parents]),
            'Symlink/junction/reparse destination path is unsupported')
    require(not os.path.lexists(destination), 'Destination already exists; never overwrite it')
    if os.name == 'nt':
        require(max(len(str(destination.joinpath(*entry['path'].split('/')))) for entry in files) < 248,
                'Choose a shorter Windows destination path')
    destination.mkdir(mode=0o700, exist_ok=False)
    # All payload validation happened before this exclusive mkdir. An I/O failure
    # leaves this newly reserved partial directory for inspection; it is not reused.
    for entry in files:
        target = destination.joinpath(*entry['path'].split('/'))
        target.parent.mkdir(parents=True, exist_ok=True)
        require(not any(is_link_or_reparse(path) for path in [target, *target.parents]),
                'Destination changed to a link during restoration')
        with target.open('xb') as handle:
            handle.write(blobs[entry['sha256']])
        if os.name != 'nt':
            target.chmod(0o700 if entry['mode'] == '100755' else 0o600)
        actual = target.read_bytes()
        require(len(actual) == entry['bytes'] and digest(actual) == entry['sha256'],
                'Written file readback mismatch')
    actual_paths = {p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_file()}
    require(actual_paths == {entry['path'] for entry in files}, 'Restored inventory mismatch')
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('handoff', type=Path)
    parser.add_argument('destination', type=Path, nargs='?')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    try:
        require(args.verify_only or args.destination is not None, 'Provide a new destination or --verify-only')
        with args.handoff.open('rb') as handle:
            document = handle.read(MAX_DOCUMENT + 1)
        metadata, files, blobs = decode_document(document)
        destination = None if args.verify_only else restore(metadata, files, blobs, args.destination)
        print(json.dumps({
            'status': 'VERIFIED' if args.verify_only else 'RESTORED_AND_READ_BACK',
            'destination': None if destination is None else str(destination),
            'file_count': len(files), 'unique_blobs': len(blobs),
            'total_file_bytes': metadata['total_file_bytes'],
            'payload_sha256': metadata['compressed_sha256'],
            'candidate_fingerprint': metadata['candidate_fingerprint'],
            'canonical_path': None if destination is None else str(destination / 'persona.md'),
            'canonical_sha256': metadata['canonical_sha256'],
            'remote_created': False, 'reviews_executed': False, 'personalization_installed': False,
        }, ensure_ascii=False, indent=2))
    except (ValueError, OSError, EOFError, RecursionError, binascii.Error, lzma.LZMAError) as exc:
        print(json.dumps({'status': 'FAILED', 'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

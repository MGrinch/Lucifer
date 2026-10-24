"""Inert transport fixtures; these are not model reviews or installation tests."""
import base64
import hashlib
import importlib.util
import json
import lzma
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'tools' / 'restore_singlefile.py'
SPEC = importlib.util.spec_from_file_location('lucifer_restore_transport', SCRIPT)
transport = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(transport)
FINGERPRINT = '1' * 64


def fixture():
    return {
        'README.md': b'Transport fixture only.\n',
        'start here.md': b'Start fixture.\n',
        'goal.md': b'Goal fixture.\n',
        'AGENTS.md': b'No active real task.\n',
        'persona.md': b'Original Unicode: \xd0\x9b\xd1\x8e\xd1\x86\xd0\xb8\xd1\x84\xd0\xb5\xd1\x80\r\nSecond line.\r\n',
        'tools/restore_singlefile.py': SCRIPT.read_bytes(),
        'workflow/state.json': json.dumps({'candidate_fingerprint': FINGERPRINT}).encode(),
        'workflow/input-manifest.json': json.dumps({'fingerprint': FINGERPRINT}).encode(),
        'workflow/review-files.json': b'{"schema":1,"files":[]}\n',
    }


def bundle_for(content):
    blobs, files = {}, []
    for path, data in sorted(content.items()):
        sha = hashlib.sha256(data).hexdigest()
        blobs[sha] = base64.b64encode(data).decode('ascii')
        files.append({'path': path, 'mode': '100644', 'bytes': len(data), 'sha256': sha})
    return {'schema': 'lucifer-repository-bundle-v1', 'files': files, 'blobs': blobs}


def fenced(label, language, body, ticks=3):
    marker = b'<!-- LUCIFER:' + label.encode()
    return (marker + b':BEGIN -->\n' + b'`' * ticks + language.encode() + b'\n' +
            body + b'`' * ticks + b'\n' + marker + b':END -->\n')


def document_for(content=None, mutate=None, raw_override=None, concatenate=False, metadata_override=None):
    content = fixture() if content is None else content
    bundle = bundle_for(content)
    if mutate:
        mutate(bundle)
    raw = transport.canonical_json(bundle) if raw_override is None else raw_override
    compressed = lzma.compress(raw, format=lzma.FORMAT_XZ)
    if concatenate:
        compressed += lzma.compress(b'another stream')
    encoded = base64.b64encode(compressed)
    files = bundle['files']
    metadata = {
        'schema': 'lucifer-singlefile-v1', 'encoding': 'base64-xz-json-content-addressed-v1',
        'created_date': '2026-10-24', 'compressed_bytes': len(compressed),
        'compressed_sha256': transport.digest(compressed), 'json_bytes': len(raw),
        'json_sha256': transport.digest(raw), 'base64_characters': len(encoded),
        'file_count': len(files), 'unique_blobs': len(bundle['blobs']),
        'total_file_bytes': sum(x['bytes'] for x in files),
        'max_file_bytes': max(x['bytes'] for x in files),
        'file_manifest_sha256': transport.digest(transport.canonical_json(files)),
        'candidate_fingerprint': FINGERPRINT, 'canonical_path': 'persona.md',
        'canonical_sha256': transport.digest(content['persona.md']),
        'canonical_bytes': len(content['persona.md']),
        'extractor_sha256': transport.digest(content['tools/restore_singlefile.py']),
    }
    if metadata_override:
        metadata.update(metadata_override)
    return (b'# Inert fixture\n' +
            fenced('METADATA', 'json', transport.canonical_json(metadata) + b'\n') +
            fenced('EXTRACTOR', 'python', content['tools/restore_singlefile.py']) +
            fenced('CANONICAL', 'markdown', content['persona.md'], ticks=6) +
            fenced('PAYLOAD', 'base64', encoded + b'\n') +
            b'<!-- LUCIFER:HANDOFF:END -->\n')


class SingleFileTransportTests(unittest.TestCase):
    def test_roundtrip_exact_bytes_with_crlf_and_unicode(self):
        content = fixture()
        metadata, files, blobs = transport.decode_document(document_for(content))
        with tempfile.TemporaryDirectory() as temporary:
            dest = transport.restore(metadata, files, blobs, Path(temporary) / 'Lucifer')
            self.assertEqual({p.relative_to(dest).as_posix(): p.read_bytes()
                              for p in dest.rglob('*') if p.is_file()}, content)

    def test_existing_empty_or_nonempty_destination_is_never_overwritten(self):
        metadata, files, blobs = transport.decode_document(document_for())
        with tempfile.TemporaryDirectory() as temporary:
            dest = Path(temporary) / 'existing'
            dest.mkdir()
            with self.assertRaisesRegex(ValueError, 'already exists'):
                transport.restore(metadata, files, blobs, dest)
            marker = dest / 'preserve.txt'
            marker.write_bytes(b'untouched')
            with self.assertRaisesRegex(ValueError, 'already exists'):
                transport.restore(metadata, files, blobs, dest)
            self.assertEqual(marker.read_bytes(), b'untouched')

    def test_corrupt_compressed_digest_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Compressed payload mismatch'):
            transport.decode_document(document_for(metadata_override={'compressed_sha256': '0' * 64}))

    def test_duplicate_marker_rejected(self):
        doc = document_for()
        extra = b'<!-- LUCIFER:METADATA:BEGIN -->\n'
        with self.assertRaisesRegex(ValueError, 'duplicate block'):
            transport.decode_document(extra + doc)

    def test_missing_final_marker_rejected(self):
        with self.assertRaisesRegex(ValueError, 'final handoff marker'):
            transport.decode_document(document_for().rsplit(b'<!-- LUCIFER:HANDOFF:', 1)[0])

    def test_unsafe_and_nonportable_paths_rejected(self):
        for path in ('../escape', '/absolute', 'a//b', 'a/./b', 'a\\b', 'C:/bad',
                     'CON.md', 'lpt1.txt', 'CON .txt', 'NUL .md', 'COM1 .txt',
                     'LPT9 .json', 'bad./file', 'bad /file', '.git/config'):
            with self.subTest(path=path):
                content = fixture()
                content[path] = b'unsafe'
                with self.assertRaises(ValueError):
                    transport.decode_document(document_for(content))

    def test_case_and_file_directory_collisions_rejected(self):
        for additions in ({'readme.md': b'collision'}, {'Tree/a': b'a', 'tree/b': b'b'},
                          {'item': b'file', 'item/child': b'child'}):
            with self.subTest(additions=list(additions)):
                content = fixture()
                content.update(additions)
                with self.assertRaises(ValueError):
                    transport.decode_document(document_for(content))

    def test_unsupported_symlink_mode_rejected(self):
        def mutate(bundle):
            bundle['files'][0]['mode'] = '120000'
        with self.assertRaisesRegex(ValueError, 'Unsupported Git mode'):
            transport.decode_document(document_for(mutate=mutate))

    def test_extra_unreferenced_blob_rejected(self):
        def mutate(bundle):
            data = b'unreferenced'
            bundle['blobs'][transport.digest(data)] = base64.b64encode(data).decode()
        with self.assertRaisesRegex(ValueError, 'unreferenced content blob'):
            transport.decode_document(document_for(mutate=mutate))

    def test_blob_hash_mismatch_rejected(self):
        def mutate(bundle):
            entry = next(x for x in bundle['files'] if x['path'] == 'README.md')
            bundle['blobs'][entry['sha256']] = base64.b64encode(b'x' * entry['bytes']).decode()
        with self.assertRaisesRegex(ValueError, 'Blob hash/size mismatch'):
            transport.decode_document(document_for(mutate=mutate))

    def test_duplicate_json_key_rejected(self):
        raw = transport.canonical_json(bundle_for(fixture()))
        raw = b'{"schema":"ignored",' + raw[1:]
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON key'):
            transport.decode_document(document_for(raw_override=raw))

    def test_oversized_integer_and_float_rejected(self):
        with self.assertRaisesRegex(ValueError, 'integer exceeds digit limit'):
            transport.read_json(b'{"integer":' + b'1' * 20000 + b'}')
        with self.assertRaisesRegex(ValueError, 'Floating-point values'):
            transport.read_json(b'{"unexpected":1.25}')

    def test_concatenated_xz_stream_rejected(self):
        with self.assertRaisesRegex(ValueError, 'concatenated'):
            transport.decode_document(document_for(concatenate=True))

    def test_bounded_decompression_rejects_excess_output(self):
        raw = b' ' * (transport.MAX_JSON + 1)
        with self.assertRaisesRegex(ValueError, 'oversized XZ stream'):
            transport.decode_document(document_for(raw_override=raw, metadata_override={'json_bytes': 1}))

    def test_boolean_numeric_metadata_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Invalid bounded integer'):
            transport.decode_document(document_for(metadata_override={'file_count': True}))

    def test_plaintext_and_extractor_projection_corruption_rejected(self):
        for original, replacement, expected in [
            (b'Original Unicode:', b'Altered_ Unicode:', 'Plaintext canonical projection'),
            (b'No network, subprocess, Git, evaluation,', b'XX network, subprocess, Git, evaluation,', 'Extractor projection mismatch')
        ]:
            with self.subTest(expected=expected):
                doc = document_for()
                self.assertEqual(doc.count(original), 1)
                with self.assertRaisesRegex(ValueError, expected):
                    transport.decode_document(doc.replace(original, replacement, 1))

    def test_symlink_parent_is_not_followed(self):
        metadata, files, blobs = transport.decode_document(document_for())
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            real = base / 'real'
            real.mkdir()
            link = base / 'link'
            try:
                link.symlink_to(real, target_is_directory=True)
            except OSError as exc:
                self.skipTest('Host cannot create a test symlink: ' + str(exc))
            with self.assertRaisesRegex(ValueError, 'Symlink/junction/reparse'):
                transport.restore(metadata, files, blobs, link / 'Lucifer')
            self.assertEqual(list(real.iterdir()), [])


if __name__ == '__main__':
    unittest.main()

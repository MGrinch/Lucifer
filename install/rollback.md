# Rollback and partial completion

Before changing a user-controlled instruction/configuration field, retain its exact previous value and scope in a protected private backup. Do not commit account exports, full memories, credentials or recordings into the review repository.

If the new candidate causes a material regression, restore only the affected managed contribution or field after comparing current state with the expected installed value. Preserve unrelated changes made since the backup. An old backup is not permission to reset a whole account or device.

Record the rollback operation and readback. Reopen the affected behavioral tests. Keep the failed candidate and its evidence for diagnosis, without promoting it as the current installed state.

If a write outcome is unknown, inspect the destination before repeating it. If a device is offline or a control is unsupported, retain prepared payloads and explicit status. Distinguish `PREPARED`, `APPLIED`, `READBACK_VERIFIED`, `BEHAVIOR_VERIFIED`, `VOICE_VERIFIED`, `PENDING_USER_SAVE`, `UNREACHABLE` and `UNSUPPORTED_AUTOMATION_ROUTE` using the canonical ledger.

A partially applied deployment can be a valid supported result. It must be called partial for the uncovered scope. Never replace unknowns with success to close the task.

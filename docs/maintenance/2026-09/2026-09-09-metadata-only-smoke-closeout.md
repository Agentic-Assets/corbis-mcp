# Metadata-only OAuth smoke correction

Date: 2026-09-09. Branch: `fix/corbis-mcp-metadata-only-smoke`.
Base: `f18976b72fde28ff6bec10bb3d5413194f67dce1`.
Implementation: `a23f746b0b521cfa57b3feb02e940bf675998a06`.

## Problem and correction

PR #15 used a real `tools/call` to test the authentication boundary. If
authentication regressed, that request could invoke a tool before observing the
unexpected response. The repository requires smoke probes to remain
metadata-only. The coordinator confirmed the late
[P1 review finding](https://github.com/Agentic-Assets/corbis-mcp/pull/15#discussion_r3972968366)
and superseded the earlier refutation.

The probe now sends one unauthenticated `tools/list` request, with no tool name
or arguments. It retains the exact HTTP 401 and Bearer discovery challenge
requirements, JSON/event-stream Accept header, metadata validation, no-redirect
checks, bounded reads, and credential exclusion. Even an unexpected anonymous
HTTP 200 stops the probe without an authentication or tool-call attempt.

The earlier documentation-only correction `d3e1cb4` was preserved as cherry-pick
`91a182c` before this change. The superseded branch must remain until this
replacement is merged and its content is preserved.

## Verification and live blocker

- Python 3.14.5: 45 offline tests pass with
  `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --release`.
- Ruff 0.16.4: `ruff check --no-cache tests/validate_package.py` passes.
- `git diff --check` passes.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --release --smoke`
  at `2026-09-09T21:04:28.852344+00:00` passed all 45 tests, then failed the live
  gate: unauthenticated `tools/list` returned HTTP 200, expected 401.
- A separate credential-free structural readback returned JSON-RPC `result`
  containing `tools` and `_meta`, with 36 tool descriptions and no Bearer
  challenge. No tool was invoked and no tool contents were persisted.

The service owns this contract mismatch. The source task reported it to the
coordinator and did not weaken the required assertion or alter the application.
This record does not claim the live gate or release acceptance has passed.

## Evidence boundaries

The source-package offline checks pass. The live metadata-only auth-boundary
gate remains blocked as recorded above. This work does not register a client,
authenticate, invoke a tool, change production, promote Marketplace content,
or submit/publish a directory entry. Direct-client OAuth acceptance and release
evidence remain separate.

See [follow-up candidates](2026-09-09-metadata-only-smoke-forward-queue.md).

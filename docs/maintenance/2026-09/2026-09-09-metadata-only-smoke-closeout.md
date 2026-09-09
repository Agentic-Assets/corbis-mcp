# Metadata-only OAuth smoke correction

Date: 2026-09-09. Branch: `fix/corbis-mcp-metadata-only-smoke`.
Base: `f18976b72fde28ff6bec10bb3d5413194f67dce1`.
Final implementation: `c58e740cffc634935ae0cf56e46605b17b371856`.

## Problem and correction

PR #15 used a real `tools/call` to test the authentication boundary. If
authentication regressed, that request could invoke a tool before observing the
unexpected response. The repository requires smoke probes to remain
metadata-only. The coordinator confirmed the late
[P1 review finding](https://github.com/Agentic-Assets/corbis-mcp/pull/15#discussion_r3972968366)
and superseded the earlier refutation.

The final probe sends only five unauthenticated GET requests: base endpoint
metadata, root and path-specific protected-resource metadata, and both
authorization-server aliases. It retains exact resource/issuer/endpoint checks,
DCR, authorization-code and refresh grants, response type `code`, PKCE `S256`,
strict JSON parsing, no redirects, bounded reads, and credential exclusion.
There is no POST, tool request, client registration, or authentication attempt.
The application and Marketplace own protected-request HTTP 401 and Bearer
challenge guards. Source smoke does not validate those guards.

The earlier documentation-only correction `d3e1cb4` was preserved as cherry-pick
`91a182c` before this change. The superseded branch must remain until this
replacement is merged and its content is preserved.

## Verification

- Python 3.14.5: 38 offline tests pass (15 package, 23 metadata/transport tests) with
  `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --release`.
- Ruff 0.16.4: `ruff check --no-cache tests/validate_package.py` passes.
- `git diff --check` passes.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --release --smoke`
  on the final implementation at `2026-09-09T21:08:01.350330+00:00` passed all
  38 tests and all five GET probes with HTTP 200 and valid metadata.
- Regression tests assert exactly those five GET URLs, absent request bodies,
  absent credentials, and immediate failure on an unexpected base HTTP 401
  without following its challenge or sending any POST.
- Reviewed validator SHA-256:
  `0b07781c08bd84e966c18a345def78183e429e5c32b2f85893baa61b6cc5a26d`.

## Contract decision

An intermediate `tools/list` probe required HTTP 401 and failed live at
`2026-09-09T21:04:28.852344+00:00`. A structural readback showed HTTP 200 with
the public tool catalog, not an authentication error. Historical application
evidence already recorded public listing. The coordinator explicitly narrowed
source smoke to GET metadata rather than changing application behavior to fit
a source test. This resolves the intermediate mismatch by correcting ownership
and scope; it does not claim a service authentication repair.

## Evidence boundaries

The source-package offline checks and live GET metadata probes pass. This work does not register a client,
authenticate, invoke a tool, change production, promote Marketplace content,
or submit/publish a directory entry. Direct-client OAuth acceptance and release
evidence remain separate.

See [follow-up candidates](2026-09-09-metadata-only-smoke-forward-queue.md).

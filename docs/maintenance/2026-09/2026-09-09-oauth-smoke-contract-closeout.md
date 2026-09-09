# OAuth smoke contract closeout

Date: 2026-09-09. Branch: `fix/corbis-mcp-oauth-smoke-contract`.
Base: `292ec29b6a9468dbfe07f0359f43eaa6f63c70b2`.
Implementation: `223826361a9b4b5b89d70d7098e644cd6918a42d`.

This record describes the original PR #15 implementation and its historical
readback. Its real-tool probe is superseded by the
[metadata-only correction](2026-09-09-metadata-only-smoke-closeout.md), which
uses unauthenticated `tools/list` and cannot invoke an application tool.

## Change

The old live probe checked two metadata documents without asserting the OAuth
contract. The replacement checks the endpoint, requires a Bearer challenge on
an unauthenticated `get_data_freshness` call, validates the challenged and both
protected-resource discovery paths, and checks both authorization-server
discovery aliases. The POST advertises both JSON and event-stream responses.

Metadata must identify the exact resource and issuer, advertise same-origin
HTTPS authorization/token/registration endpoints, authorization-code and refresh
grants, response type `code`, and PKCE `S256`. The probe rejects redirects,
duplicate JSON members, nonfinite JSON constants, malformed challenges, invalid
scopes, and bodies above 1 MiB. Quoted pairs are decoded exactly once. Reads use
a 15-second socket timeout; streams close on success, HTTP errors, and failed
reads. Environment proxies and their credentials are excluded.

This is a Corbis service contract, not a general OAuth validator. Both the RFC
path-specific authorization discovery route and the root compatibility alias
returned HTTP 200 in the live readback, so both are required. Removing an alias
requires a deliberate contract change rather than silently skipping a 404.
The existing package descriptors and public assets are unchanged.

## Proof

On the implementation commit, Python 3.14.5:

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --release --smoke`:
  44 tests passed (15 package tests and 29 OAuth regression tests, with additional
  parameterized cases); release-material structural validation passed.
- Live probe at `2026-09-09T20:52:24.578294+00:00`: endpoint HTTP 200;
  unauthenticated `get_data_freshness` HTTP 401 with Bearer discovery challenge;
  challenged, root, and path-specific protected-resource metadata HTTP 200;
  both authorization-server aliases HTTP 200 with all required fields valid.
- `ruff check --no-cache tests/validate_package.py`: passed with Ruff 0.16.4.
- `git diff --check`: passed. Python source compiled without writing bytecode.
- Dependency/secret review: standard library only; no manifests, dependencies,
  credentials, cookies, authorization headers, or runtime configuration added.

Primary protocol references checked during implementation:
[MCP authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization),
[MCP transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports),
and [HTTP quoted strings](https://www.rfc-editor.org/rfc/rfc9110.html#section-5.6.4).
Exact Corbis endpoint paths and the second discovery alias are service-specific
requirements verified live, not additional requirements imposed by MCP.

## Independent review

The independent reviewer ran the 44 offline tests and completed adversarial and
security review of file SHA-256
`9befe1d9d8448b50bffdee97d9e1bdc7a7286eb860e1f93e6a433ed0954474d9`.
No actionable findings remain in that file.

That statement records the local review at the time. The later GitHub P1
[metadata-only finding](https://github.com/Agentic-Assets/corbis-mcp/pull/15#discussion_r3972968366)
was initially refuted against the original task wording, then confirmed by the
coordinating task. The follow-up correction restores the repository's
metadata-only boundary. The initial refutation is superseded.

Confirmed and fixed: escaped quoted-string parsing; probe tool and Accept
header; required response type; missing authorization discovery alias;
nonfinite JSON rejection; escaped Latin-1 header bytes; and transport failures
while reading HTTP error bodies. Each has deterministic regression coverage.

Refuted concerns: nested duplicate members already fail closed, redirect
following was already disabled, the exact URL guard rejects changed URLs,
responses were already bounded, and environment proxy credentials were already
excluded. Regression tests now cover those boundaries explicitly.

## State and separate gates

Implementation and local proof are complete. The PR carries current GitHub gate
and review intake evidence. The coordinating task owns the merge decision and
execution under its applicable instructions. This task performs verification
and worktree cleanup; the PR records the resulting merge state.

Source-package tests and live unauthenticated readback passed. No authenticated
OAuth flow, direct-client acceptance, source release, Marketplace promotion or
admission, deployment, or public-directory submission/publication was performed.
The live test establishes responses at the time checked, not deployment identity
or whether a rejected request reached internal dispatch. Client validators were
not rerun because no descriptor changed and this is not a release candidate.

The saved main checkout was not edited. Worktree removal and final branch/PR
state are reported in the task and PR closeout after the final push.

See [the separate follow-up candidates](2026-09-09-oauth-smoke-contract-forward-queue.md).

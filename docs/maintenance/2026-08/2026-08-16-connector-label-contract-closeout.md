# Corbis MCP connector-label contract closeout (2026-08-16)

**Branch:** `fix/corbis-mcp-label-identity`

**Base:** `origin/main` at `d96a9c7520ab3d572e5510e9cf5a257a444df21f`

**Implementation commit:**
`97739287e07eda7649178e4a9b6c97160e755068`

**State at this record:** `0.1.3` is an untagged source candidate. No
Marketplace payload, Corbis Research configuration, production service,
OAuth setting, direct-client acceptance record, or attestation was changed.

## Goal

Keep the connector's human-facing name as `Corbis` while retaining the
collision-safe technical MCP identifier `corbis-mcp`. Make that distinction
explicit and resistant to a future source regression without inventing a
client-specific server-label field.

## What changed

- Retained `Corbis` in the supported Claude `displayName` and Codex
  `interface.displayName` fields.
- Retained `corbis-mcp` in the Claude, Codex, and Cursor `mcpServers` maps.
- Added static checks for title-case human-facing display labels, separate
  technical identifiers, current release-material versioning, and absence of
  unsupported per-server display-label fields.
- Added source and acceptance guidance that requires recorded post-install
  settings-label readback for every tested client route.
- Reframed the public README around Corbis, cited research, Research Insights,
  and Open Datasets. Release operations, tag history, server identifiers, and
  test commands remain in maintainer documentation.
- Corrected the stale source record: `v0.1.2` is an annotated SSH-signed tag
  that points to `d96a9c7520ab3d572e5510e9cf5a257a444df21f`; its signer trust
  is not verified because GitHub reports `unknown_key`. Marketplace has an
  immutable payload promoted from that tag, which remains distinct from
  acceptance, admission, attestation, and production proof.

## Decision and evidence

The `corbis` MCP server key cannot safely be reused. Corbis Research currently
uses it for the same universal endpoint, and the historical `v0.1.0`
thin-connector installation resolved to Corbis Research instead of this
connector. The technical key remains `corbis-mcp` until a coordinated,
evidence-backed identity migration is authorized.

Current official client documentation supports plugin-level display names for
Claude and Codex, but does not document a source-controlled per-server label
for these MCP maps. The MCP protocol may carry `serverInfo` metadata, but the
production application owns that metadata and client rendering is not inferred
from source validation.

The requested Corbis Plugin screenshots were not added. On 2026-08-16, each
showed the stale `400,079` corpus figure, while the live Corbis page showed
`423,715+`. Repository policy prohibits reusing a stale corpus figure; the
downloaded, untracked copies were removed without a commit. A refreshed or
approved redacted public asset is required before adding a product screenshot.

Follow-on independent README review confirmed and corrected one public-copy
issue: earlier wording could imply that every compatible client already
accepted the connection and sign-in flow. The final README makes availability
conditional on the workspace and account. The reviewer also raised broader
Research Insights and Open Datasets wording; an independent skeptic refuted
that concern against the current official product pages.

Independent adversarial review confirmed that this source candidate does not
change a post-install settings row when that client renders the MCP map key.
The candidate is therefore a source-contract and evidence improvement, not a
claim that the reported client label is fixed. The client/application route is
explicitly deferred below.

## Verification

At implementation commit
`97739287e07eda7649178e4a9b6c97160e755068`:

- `git diff --check` passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py` passed: 14
  tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --release`
  passed: 14 tests.
- `claude plugin validate --strict` passed against a staging directory
  containing the Claude descriptor. The full repository invocation remains
  expected to fail strictly because the required root `CLAUDE.md` bridge is
  not a plugin component.
- JSON parsing passed for all three client manifests.

These checks do not establish OAuth, MCP runtime initialization, tool access,
production deployment/readback, client settings-label behavior, Marketplace
admission, or publication.

## Independent review

- Security review found no security or package-boundary issue in the changed
  descriptors, tests, documentation, or maintenance records.
- Adversarial finder and independent skeptic both confirmed the settings-label
  limitation described above. It is a scope boundary, not a source defect that
  can be safely patched with an undocumented field or a colliding identifier.

## Remaining gates

1. Obtain Cayman approval before merge.
2. Verify the exact merged head, then obtain explicit authorization for a new
   trusted signed annotated `v0.1.3` tag. Do not move or replace `v0.1.2`.
3. Promote only that new immutable source tag in the separate Marketplace
   repository, then regenerate digest-bound evidence.
4. Run clean-profile Claude Code, Codex CLI, and Cursor acceptance. Record the
   plugin-card name and post-install settings label separately for each client.
5. Keep production endpoint/OAuth, Marketplace admission and attestation, and
   public-directory publication as separate authorized gates.

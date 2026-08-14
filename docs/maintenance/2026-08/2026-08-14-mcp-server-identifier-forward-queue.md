# Forward queue after Corbis MCP server-identifier fix (2026-08-14)

Candidate work surfaced during the `0.1.1` source fix. This is a menu, not an
authorization.

## Release validation

- **Repeat clean-client acceptance from a new immutable snapshot** (confidence:
  verified requirement; priority: high)
  After a signed `v0.1.1` tag and new exact-digest preview exist, collect
  Claude Code, Codex CLI, and Cursor acceptance separately. Use clean profiles
  so a prior `corbis` registration cannot mask a descriptor error.

- **Configure local SSH tag verification** (confidence: verified local gap;
  priority: medium)
  Install the trusted maintainer allowed-signers file through the authorized
  signing workflow, then rerun `git tag -v <tag>`. Do not add signer material
  to this source repository.

## Hardening

- **Keep the package/server-ID separation test** (confidence: implemented
  control; priority: high)
  Retain the assertion that package ID `corbis` and MCP server identifier
  `corbis-mcp` differ. This prevents the client-name collision from returning
  in a future descriptor refactor.

- **Reconcile the Marketplace allowlist before promotion** (confidence:
  verified requirement; priority: high)
  Marketplace promotion must consume the exact tagged `0.1.1` snapshot under
  its current policy. Do not modify that control plane from this repository.

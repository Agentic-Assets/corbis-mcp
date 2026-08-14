# Corbis MCP server-identifier closeout (2026-08-14)

**Branch:** `fix/corbis-mcp-server-identifier`

**Base:** `origin/main` at `ef1c48a715ef8e8a45971e257331aab9d2004d01`

**Commit:** branch head at closeout; see Git history for the immutable commit
identifier.

**State at this record:** `0.1.1` is an untagged source candidate. No
Marketplace, Corbis Research, production-service, client-profile, or
attestation material was changed.

## Goal

Make the thin connector independently installable in Codex after the signed
`v0.1.0` snapshot used the same MCP server identifier as the separate Corbis
Research package.

## What changed

- The descriptor map key for Claude Code, Codex, and Cursor is now
  `corbis-mcp`.
- Package manifests retain package ID `corbis`, display name `Corbis`, and the
  fixed endpoint `https://www.corbis.ai/api/mcp/universal`.
- The package version is consistently `0.1.1`; the changelog records this as an
  untagged patch candidate.
- Static tests now assert that the MCP server identifier differs from the
  package ID and that every descriptor uses only `corbis-mcp`.

## Evidence and decision

The signed `v0.1.0` tag points to
`ef1c48a715ef8e8a45971e257331aab9d2004d01` (tag object
`1f1de0d`). A real Codex CLI installation during the external preview found a
duplicate `corbis` server name and resolved to the already installed
`corbis-research@agentic-assets` configuration. That result is not thin
connector Codex acceptance.

`corbis-mcp` is the narrow fix because it changes only the local MCP server
map key. It deliberately does not rename the source package, Marketplace
selector `corbis@agentic-assets`, source payload path, or service endpoint.

## Remaining gates

1. Review and merge this branch with Cayman approval.
2. Verify the exact remote `main` commit, then have the configured trusted
   signing authority create and verify a signed annotated `v0.1.1` tag on that
   reachable commit. Do not reuse `v0.1.0`.
3. In the separate Marketplace repository, promote only the immutable `v0.1.1`
   tagged snapshot and generate a new exact-digest preview.
4. Use clean client profiles to record real Claude Code, Codex CLI, and Cursor
   local acceptance evidence for that exact digest. The Codex profile must not
   retain a legacy `corbis` alias.
5. Complete Marketplace proof binding, atomic admission, externally controlled
   attestation, release gate, production readback, and any public publication
   as separate, authorized activities.

## Local signing limitation

`git tag -v v0.1.0` displayed an SSH signature envelope but this machine cannot
complete trust verification because `gpg.ssh.allowedSignersFile` is not
configured to an existing allowed-signers file. This is a local verification
configuration gap, not permission to tag or a substitute for signer approval.

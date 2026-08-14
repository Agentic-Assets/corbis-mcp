# Changelog

All notable changes to this source package are documented here.

## Unreleased

- Added initial Claude Code, Codex, and Cursor descriptors for the Corbis
  remote MCP endpoint.
- Added portable static package validation and an opt-in metadata smoke check.
- Hardened release-material validation to reject symlinked paths, malformed
  PNG streams, invalid decoded layouts, and invalid PNG filter bytes.
- Added the empty `provenance.json` required by the Marketplace allowlist. It
  contains no release tag, payload digest, client evidence, or attestation
  data.

No source release tag, Marketplace artifact, direct-client acceptance record,
or public-directory listing has been created.

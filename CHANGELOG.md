# Changelog

All notable changes to this source package are documented here.

## 0.1.2 - 2026-08-14

- Corrected the source-package release record after the signed `v0.1.1` tag.
- Bumped all client descriptors to patch-release version `0.1.2` so they are
  distinguishable from the immutable `v0.1.1` snapshot.

This source release record does not assert a signed `v0.1.2` tag. It does not
establish direct-client acceptance, a Marketplace artifact or admission, or a
public-directory listing.

## 0.1.1 - 2026-08-14

- Changed the thin connector MCP server identifier from `corbis` to
  `corbis-mcp` in all client descriptors to avoid a collision with the
  separately installed `corbis-research@agentic-assets` configuration.
- Bumped all client descriptors to patch-release version `0.1.1`.

The signed annotated `v0.1.1` tag object
`ff16d89bf37f291cd643711233ed255f934dc446` points to source commit
`3fb5b4659ed971f409c0d70135d654f21da4db08`, which is reachable from `main`.
The source tag does not establish direct-client acceptance,
Marketplace artifact or admission, or public-directory listing.

## 0.1.0 - 2026-08-14

- Added initial Claude Code, Codex, and Cursor descriptors for the Corbis
  remote MCP endpoint.
- Added portable static package validation and an opt-in metadata smoke check.
- Hardened release-material validation to reject symlinked paths, malformed
  PNG streams, invalid decoded layouts, and invalid PNG filter bytes.
- Added the empty `provenance.json` required by the Marketplace allowlist. It
  contains no release tag, payload digest, client evidence, or attestation
  data.
- Added concise MIT license, security-reporting, and support documents for the
  source package.

The signed `v0.1.0` source tag is historical only. Its Codex installation
resolved to the separate Corbis Research configuration because both used the
`corbis` MCP server identifier, so it is not thin-connector Codex acceptance.

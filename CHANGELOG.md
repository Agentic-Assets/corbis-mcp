# Changelog

All notable changes to this source package are documented here.

## 0.1.5 - Unreleased

- Declared `https://www.corbis.ai` as the canonical homepage in every client
  descriptor and as Codex `interface.websiteURL`, so the Codex plugin details
  view has the supported metadata needed to display the Corbis website instead
  of “Unavailable”.
- Added static regression coverage for the shared homepage and Codex website
  metadata.
- Bumped all client descriptors to patch-release version `0.1.5`.

## 0.1.4 - Unreleased

- Replaced the Codex plugin icon with the exact Corbis Research icon and
  declared it through the supported Codex `interface.composerIcon` field.
- Added a static regression check for the approved icon digest and manifest
  reference so Marketplace promotions retain the same card icon.
- Bumped all client descriptors to patch-release version `0.1.4`.

## 0.1.3 - Unreleased

- Retained `Corbis` as the human-facing plugin and connector label in the
  supported Claude and Codex display-name fields, while preserving
  `corbis-mcp` as the collision-safe MCP server identifier.
- Added source documentation and static regression coverage that distinguish
  human-facing display labels from package and MCP identifiers. The tests
  reject unsupported per-server display-label fields rather than silently
  relying on them.
- Reframed the public README around Corbis, cited research, Research Insights,
  and Open Datasets; release operations and technical identifiers remain in
  maintainer documentation.
- Added the user-supplied Corbis landing-page image, a fresh Research Insights
  image, and the requested public Open Datasets image to the public README.
- Bumped all client descriptors to patch-release version `0.1.3`.

This candidate does not change the `mcpServers` map key. A client that renders
that key in its server settings may still show `corbis-mcp`; no supported
source-descriptor field controls that rendering. Native client acceptance must
record the actual settings label before a source release is proposed.

## 0.1.2 - 2026-08-14

- Corrected the source-package release record after the signed `v0.1.1` tag.
- Bumped all client descriptors to patch-release version `0.1.2` so they are
  distinguishable from the immutable `v0.1.1` snapshot.

The annotated `v0.1.2` tag object
`6219c55ee79eb0031ea73bfe167a08dac39c202e` peels to source commit
`d96a9c7520ab3d572e5510e9cf5a257a444df21f`. Its SSH signature is present,
but GitHub reported the signing key as unknown on 2026-08-16, so this record
does not assert trusted signature verification. The source tag does not
establish direct-client acceptance, Marketplace admission, or a
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

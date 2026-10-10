# Changelog

All notable changes to this plugin are documented here.

## Unreleased

- Added a 512 px PNG of the Corbis mark for directory listings and replaced the 48 px Codex and Cursor icon with it.

## 0.3.1

- Add OpenAI listing copy, conversation starters, review cases and release notes, with all-supported-countries targeting.
- Link the synthetic reference-audit PDF and BibTeX fixtures used by the review case.
- Keep the Codex interface aligned and raise compatible host manifest versions together.

## 0.3.0 - 2026-10-02

- Added a portable OpenAI plugin manifest and Streamable HTTP connection descriptor alongside the existing client manifests.
- Added onboarding that guides account connection, source inspection, and workflow selection.
- Added metadata for a hosted Corbis research workspace with sidebar and conversation entrypoints and paper mentions on compatible hosts.
- Kept research authorization and account permissions in the Corbis connector. Workspace preferences apply to the current session.
- Clarified host support, source inspection, and the distinction between a direct MCP connection and an installed plugin.

## 0.2.0 - 2026-09-29

- Added three skills (`literature-review`, `citations`, `paper-review`) that turn the
  Corbis connector into cited research workflows for finance, real estate, and
  economics.
- Added Codex and Cursor manifests alongside the existing Claude manifest, all three
  pointing at one shared `.mcp.json` (server key `corbis`, production endpoint).
- Consolidated the plugin under a single name and repository: `corbis` at
  `Agentic-Assets/corbis-mcp`. The prior Claude-only `corbis-research-skills`
  plugin and its separate repository are retired; neither was ever listed in a
  directory.
- Bumped all client descriptors to `0.2.0`.

## 0.1.6 and earlier (connector-only, pre-skills)

- Declared the public privacy policy, terms, license, and logo metadata each client
  descriptor requires for a directory listing.
- Declared `https://www.corbis.ai` as the canonical homepage in every client
  descriptor.
- Set the Corbis icon through each client's supported icon field.
- Distinguished the human-facing `Corbis` display label from the MCP server
  identifier used in client settings.
- Added the initial Claude Code, Codex, and Cursor descriptors for the Corbis
  remote MCP endpoint, static package validation, an opt-in metadata smoke
  check, and MIT license, security-reporting, and support documents.

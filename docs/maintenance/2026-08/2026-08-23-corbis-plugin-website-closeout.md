# Corbis MCP plugin website metadata closeout (2026-08-23)

**Branch:** `fix/corbis-plugin-website`

**Base:** `origin/main` at `e5a2707c3be328578e74d3a974b6df9b3696fb85`

**Implementation commit:**
`3def95d79529c986ddfec2070c39eb870d6c7eec`

**State at this record:** source-package metadata correction only. It is not
direct-client acceptance, Marketplace promotion or admission, production
readback, or directory publication.

## What changed

- Added `https://www.corbis.ai` as the canonical `homepage` value in the
  Claude, Codex, and Cursor client descriptors.
- Added the supported Codex `interface.websiteURL` value. This is the metadata
  the Codex and ChatGPT plugin detail surface uses for its Website row.
- Bumped all three descriptors to `0.1.5` and added static regression checks
  for the shared homepage and Codex presentation URL.

## Verification

- A signed-out `https://corbis.ai` request redirected to the canonical
  `https://www.corbis.ai/` page, which returned HTTP 200.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py` passed: 15
  tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --release`
  passed: 15 tests.
- `claude plugin validate .` passed with its known root `CLAUDE.md` bridge
  warning.
- `git diff --check` passed.

## Boundaries

The Codex and ChatGPT plugin detail surface shares the Codex descriptor, so
the supported `interface.websiteURL` is included there. The common `homepage`
field is included in Claude and Cursor descriptors. Static validation does not
prove that a distinct client cache, ChatGPT web or mobile, Claude Desktop,
Cowork, or Cursor workspace has refreshed and rendered the new metadata.

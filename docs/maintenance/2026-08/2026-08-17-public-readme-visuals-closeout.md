# Corbis MCP public README visuals closeout (2026-08-17)

**Branch:** `docs/corbis-readme-visuals`

**Base:** `origin/main` at `493b06d31f532af12294646812eb25ad33e661db`

**Implementation commit:** `d239004da5ec47b85f4afee41ec1aa6049c9d8de`

**State at this record:** documentation and public image assets only. This is
not a source release, client acceptance record, Marketplace promotion, or
production claim.

**Draft PR:** `https://github.com/Agentic-Assets/corbis-mcp/pull/11`

## What changed

- Added a current Corbis landing-page visual to the public README.
- Added a current Research Insights visual to the public README.
- Added the requested public Open Datasets visual from
  `Agentic-Assets/Corbis-Plugin` `origin/master`.
- Added a static README contract requiring the three public visuals to remain
  linked from the page.

## Asset evidence

The Corbis landing page was opened through `agent-browser` on 2026-08-17 and
captured at the original `1943 x 1252` viewport. The visual shows the then-live
`423,715+` corpus figure.

Research Insights was opened through `agent-browser` on the same date and
captured at the original `1384 x 1257` viewport. It shows the then-live
`423,715` total-publications figure.

The Open Datasets asset is an exact copy of
`images/corbis-datasets.png` from `Agentic-Assets/Corbis-Plugin`
`origin/master`, Git blob `44f24fc683c22917de747002a76cc01222b901e7`, at
`1383 x 1133`. It contains no corpus total. It was copied at the user's
explicit request and remains a public product visual only, not a transfer of
the separate research-workflow package.

The old Corbis Plugin landing-page and Research Insights screenshots were not
reused because they visibly showed the stale `400,079` corpus figure. The
fresh screenshots preserve the requested dimensions and page areas without
repeating that stale claim.

## Verification

At source commit `714b9d5a4bb140d84d375f38bea6529a48562ffb`:

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py` passed: 15
  tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --release`
  passed: 15 tests.
- `git diff --check origin/main...HEAD` passed.
- Independent copy, asset-provenance, and security reviews found no remaining
  package-boundary or stale-figure issue. They confirmed that the fresh hero is
  deliberately not the old byte-identical image.

These checks do not establish direct-client acceptance, OAuth, MCP runtime
initialization, Marketplace admission, source release, or production readback.

The separate `0.1.3` source candidate still requires Cayman approval before
merge, explicit authorization for a trusted signed tag, and a later immutable
Marketplace promotion with its own evidence.

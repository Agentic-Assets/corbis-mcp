# Corbis MCP plugin icon closeout (2026-08-23)

**Branch:** `fix/corbis-plugin-icon`

**Base:** `origin/main` at `5c6e59ead02a9fc47281e0902f71f2021b6781a9`

**Implementation commit:** `14feb2e55fe76b12f442e537fa3c2d547ac25a13`

**State at this record:** source-package correction only. It is not direct
client acceptance, a source release tag, Marketplace promotion or admission,
or production readback.

## What changed

- Replaced `assets/icon.png` with the exact Corbis Research icon from
  `Agentic-Assets/Corbis-Plugin` `origin/master` at
  `ca45471aece6b96c376ee1459336fb2646c67365`.
- Added Codex `interface.composerIcon` metadata pointing to that contained
  asset so the package card can render it.
- Added static regression coverage for the asset reference and SHA-256 digest.
- Bumped the three descriptors to `0.1.4`.

## Asset evidence

The source and destination icon are byte-identical 48 x 48 RGBA PNG files.
Their SHA-256 is
`80188a21893d91b9e18f603bce504df80f85ad068bed06cb25a0de9d87545984`.
Only the public icon asset was copied. No Corbis Research workflows, skills,
agents, tools, application code, or private material entered this package.

## Verification

On the implementation candidate:

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py` passed: 15
  tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --release`
  passed: 15 tests.
- The unauthenticated `--smoke` endpoint and protected-resource metadata
  probes both returned HTTP 200. They did not authenticate or invoke tools.
- `claude plugin validate .` passed with its known warning that the mandatory
  root `CLAUDE.md` bridge is not plugin context. Strict mode fails solely on
  that warning; the bridge remains required by repository governance.
- `git diff --check` passed.
- Independent adversarial and security reviews found no confirmed issues.

The pending Marketplace update must promote the merged, signed source release
through its normal one-way workflow. A static asset check cannot prove a client
has refreshed a cached installed-plugin card.

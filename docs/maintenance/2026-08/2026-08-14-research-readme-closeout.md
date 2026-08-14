# Corbis MCP research-focused README closeout (2026-08-14)

**Branch:** `docs/corbis-mcp-research-readme`

**Base:** `main` at `364d891db87d923152e2d03e50b1d2fbaba76bdd`

**State at this record:** user-facing README revision verified locally and
awaiting review. No release, client acceptance, Marketplace, or deployment
claim is created by this documentation change.

## What changed

- Reworked `README.md` around the Corbis Plugin's centered header, compact
  badges, navigation, divider, research-facing introduction, and centered
  footer.
- Kept the connector's own boundary intact: its remote endpoint, OAuth-first
  connection model, account-scoped authorization, source-only status, and
  release gates remain explicit.
- Omitted Corbis Research Plugin skills, commands, workflows, WRDS guidance,
  installers, tool lists, data credentials, and Marketplace-install claims.

## Hero image decision

The requested exact Corbis Plugin hero screenshot was not added. Its displayed
corpus count is stale relative to the live Corbis page checked on this date.
See `2026-08-14-readme-hero-image-blocker.md` for the source blob, verified
live count, and required owner action.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py` passed 14
  tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --release`
  passed its unit tests then failed as designed because `LICENSE`,
  `SECURITY.md`, and `SUPPORT.md` remain founder-gated.
- `git diff --check` passed.

## Left to the operator

Approve a newly captured, claim-current Corbis landing-page image if the README
must have a screenshot hero. Do not use the stale Plugin asset. A future
Marketplace promotion would require its separate owner to add any approved new
asset to the exact allowlist before promotion.

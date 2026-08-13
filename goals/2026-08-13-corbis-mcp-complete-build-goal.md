# Codex Goal - Complete Corbis MCP connector

## Goal

Deliver the minimal root-level `corbis` connector for
`https://www.corbis.ai/api/mcp/universal`, its authorized readiness work, and,
when release authority is granted, an immutable `corbis@agentic-assets`
Marketplace artifact with digest-bound evidence. Source validation, client
acceptance, Marketplace admission, production deployment, and directory
publication are separate states. Finish independent work and report any missing
approval, credential, signing, production, or platform gate without claiming a
release.

## Boundaries

Read `AGENTS.md`, `docs/00-start-here.md`, and the numbered design documents.
`corbis-mcp` owns only three client descriptors, `.mcp.json`, `mcp.json`,
approved assets, public material, and tests. Do not add server/proxy code, a
static tool list, credentials, user data, caches, query-string secrets, or sync.

`agentic-assets-app` owns the server, OAuth, authorization, tools, and
deployment. Do not copy private Corbis Research material. Use Marketplace only
for policy, promotion, evidence, attestation, and catalogs. Never push a
default branch, merge, change visibility, deploy, publish, or use reviewer
credentials without explicit authority.

## Iteration Policy

Reconcile branches, PRs, endpoint/OAuth metadata, application readiness,
Marketplace main, and current schemas before coding. Record dates and SHAs;
plans are not live proof. Work in focused branches. Build consistent `corbis`
metadata, the exact HTTPS endpoint, no embedded credential, factual
entitlement-aware copy, and approved public material using current scaffolds
and validators.

Resolve or refute the application's nested market-ranking output-schema audit
with producer-derived tests. In Marketplace, implement `corbis-mcp-v1` and a
`corbis` policy for root source `.`, narrow allowlist, containment,
symlink/traversal protection, policy-driven evidence, and staged promotion.
Exclude AGENTS, maintainer docs, and tests. Promote exact signed-tag blobs, not
a mutable checkout. Validate, inspect diffs, update evidence, and seek review.

## Verification

Add portable descriptor tests: common metadata/version, exact HTTPS endpoint,
no placeholders, local/private paths, credentials, or undeclared files, plus
assets and links. Run Claude strict, Codex, and Cursor validators,
secret/dependency review, clean direct-install/OAuth, and Inspector-equivalent
initialization, tool, invalid-input, authentication, authorization, and bounded
result tests. Record client, host, route, tag/commit, digest, and evidence.

Run application MCP schema/annotation/transport, lint, type, docs, and
sufficient build/test checks. Run Marketplace fixtures, preflight, preview,
digest-bound Claude Code and Codex CLI proof, admission, attestation, and final
gate. Browser-check public routes signed out. A validator or catalog row never
proves a client, directory, or production route.

## Deliverables

- Source-package PR with working descriptors/MCP files, approved materials and
  assets, tests, changelog, and install/support/security documentation.
- Application evidence resolving readiness findings and live readback when
  deployment is authorized.
- Marketplace PR with profile, policy, promotion, provenance, evidence,
  admission, and attestation when release authority is granted.
- Updated closeout/forward queue and a final report separating source,
  production, Marketplace, client, directory, and blocked states.

## Blocked Stop Condition

Stop only after safe independent work is exhausted and a missing founder
decision, reviewer access, signing/deployment/OAuth authority, platform
permission, or unfixable security/review/client/release gate prevents progress.
Report evidence, completed work, affected state, and smallest next decision.
Never mark complete because a budget ends, branch/PR exists, validator passes,
or a Marketplace entry appears.

# Corbis MCP source handoff

**Date:** 2026-08-13

**Audience:** the coding agent and maintainer building the first Corbis MCP
source package

**Status:** the initial thin source package merged through PR #2 at
`ec00b9252366601acd916d0a464e8d0eb18ffaee`. It has not been tagged, accepted
through a native client, promoted to the Marketplace, or released.

**Execution goal:** for the full build, readiness, Marketplace, and publication
contract, read
[`goals/2026-08-13-corbis-mcp-complete-build-goal.md`](../goals/2026-08-13-corbis-mcp-complete-build-goal.md)
after this document. The goal does not replace its explicit approval gates.

## One-sentence decision

`Agentic-Assets/corbis-mcp` is the sole editable source for the thin Corbis
connector, and `corbis@agentic-assets` will later be a separately promoted,
immutable Marketplace snapshot of a signed source release.

## Start with these truths

- The only intended remote endpoint is
  `https://www.corbis.ai/api/mcp/universal`.
- The wrapper is packaging and transparency around that endpoint. It must not
  contain or reimplement server code, OAuth logic, authorization, entitlements,
  tool implementations, private research workflows, or a static copy of the
  server's tools.
- The production application, `Agentic-Assets/agentic-assets-app`, remains the
  endpoint authority. Its readiness work is not production proof until it is
  independently reviewed, merged, deployed, and read back live.
- The Corbis Research Plugin is an intentionally different private product. Do
  not turn this minimal connector into a research toolkit.
- This repository is still private. Public visibility is a later human gate,
  not an implementation side effect.

## Current implementation checkpoint

- The source package contains separate Claude Code, Codex, and Cursor
  descriptors, the two client-specific MCP configuration files, `README.md`,
  `CHANGELOG.md`, a root-package guard, and a separate unauthenticated endpoint
  metadata smoke option.
- Its implementation-time checks, the release-material gate, and the separate
  application-readiness observation are recorded in
  [`docs/maintenance/2026-08/2026-08-13-connector-implementation-evidence.md`](maintenance/2026-08/2026-08-13-connector-implementation-evidence.md).
- No approved public assets, final public license, public security or support
  route, source release tag, Marketplace payload, native-client acceptance, or
  public-directory listing exists.

The Marketplace profile is being prepared separately. It still cannot admit
this connector until the source has the required public release material, a
signed source tag, and digest-bound Codex CLI, Claude Code, and Cursor local
acceptance evidence.

The checkpoint is source-package validation only. It is not a supported direct
installation route or proof of OAuth, tool invocation, production readiness,
Marketplace admission, or directory publication.

## Expected content of a reviewable source-package PR

Build only the thin, root-level package described in
[the implementation plan](01-build-plan.md):

- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`
- `.cursor-plugin/plugin.json`
- `.mcp.json` and `mcp.json`
- approved public assets
- `README.md`, `CHANGELOG.md`, `LICENSE`, `SECURITY.md`, and `SUPPORT.md`
  because the Marketplace v1 allowlist requires a separate support document
- portable manifest and endpoint smoke tests

The exact file list and public text must be reviewed against current client
schemas, the approved license, brand assets, support contact, and live public
web routes. Do not create placeholders and call the package release-ready.

## Do not build these things

- A local MCP server, API proxy, application code, database access, or OAuth
  callback handler.
- Skills, agents, commands, hooks, WRDS tooling, a corpus, or project
  scaffolding from Corbis Research.
- Credentials, reviewer accounts, source code from the private application,
  user data, client caches, or a custom browser UI.
- Marketplace catalog entries, Marketplace provenance, Marketplace evidence,
  or an automatic sync. Those belong in the Marketplace only after the source
  release and direct-client evidence gates.

## Required sequence

1. Read [`../AGENTS.md`](../AGENTS.md), then this document and the three
   numbered design documents.
2. Reconcile source-repository state, production endpoint metadata, application
   readiness, and client schema/validator requirements. Treat all prior
   observations as historical until rechecked.
3. Resolve the founder-gated public decisions listed in
   [the decision register](04-source-record.md#open-human-gates). Do not guess
   a license, support address, final public copy, or visibility setting.
4. Implement the minimal package on a feature branch, with machine-checkable
   contracts and no secrets.
5. Run local validation, including `python3 tests/validate_package.py --release`,
   and clean direct-install/OAuth tests. The release-material mode is expected
   to fail until structural public materials exist; it does not grant founder
   approval. Record exact
   versions, commands, environment boundaries, and outcomes.
6. Obtain review and the separate approvals required for merge, source release,
   production deployment, and any public visibility or directory action.
7. Only after a reviewed, signed annotated source tag and direct-client evidence
   may the Marketplace team start its separate `corbis@agentic-assets` process.

## Important non-equivalences

| Evidence | Does prove | Does not prove |
| --- | --- | --- |
| JSON or plugin validator passes | The tested descriptor meets that validator's current syntax rules | OAuth works, production tools work, a directory accepts the package, or another client accepts it |
| A source-package release tag exists | The reviewed source release can be considered for promotion | Marketplace policy, payload promotion, Marketplace admission, or client acceptance |
| Direct Codex CLI or Claude Code acceptance | That named direct route accepted the tested release | Desktop, web, mobile, Cowork, Cursor Team Marketplace, or public directory acceptance |
| Marketplace catalog admission | A digest-bound promoted artifact is cataloged | Any client refreshed, installed, authenticated, or invoked it successfully |
| Production endpoint returns a tool list | The endpoint responded for the tested principal | Every entitlement, tool, output, OAuth flow, or directory route is healthy |

## Verification record required for a source-package PR

Before opening the source-package PR, leave a short evidence record that says:

- which source and application commits were inspected;
- the current endpoint and OAuth discovery readback, without recording tokens;
- which client schemas and validators were used and their versions;
- which public support, privacy, terms, and documentation URLs were actually
  verified while signed out;
- the separate application's producer-derived nested market-ranking proof and
  whether it has been independently reviewed, merged, deployed, and read back
  live.

The final bullet is an application gate, not permission to change the
application from this repository. Route any application remediation through its
own repository and review path.

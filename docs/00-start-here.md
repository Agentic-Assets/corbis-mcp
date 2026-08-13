# Corbis MCP source handoff

**Date:** 2026-08-13

**Audience:** the coding agent and maintainer building the first Corbis MCP
source package

**Status:** implementation planning is complete. This repository deliberately
contains documentation only; it is not yet an installable or released plugin.

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

## What to build in the first source-package PR

Build only the thin, root-level package described in
[the implementation plan](01-build-plan.md):

- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`
- `.cursor-plugin/plugin.json`
- `.mcp.json` and `mcp.json`
- approved public assets
- `README.md`, `CHANGELOG.md`, `LICENSE`, `SECURITY.md`, and either an approved
  `SUPPORT.md` or an approved public support section in the README
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
5. Run local validation and clean direct-install/OAuth tests. Record exact
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

## First verification checkpoint

Before opening the source-package PR, leave a short evidence record that says:

- which source and application commits were inspected;
- the current endpoint and OAuth discovery readback, without recording tokens;
- which client schemas and validators were used and their versions;
- which public support, privacy, terms, and documentation URLs were actually
  verified while signed out;
- whether the application readiness candidate's open audit signal about nested
  market-ranking output must be resolved before treating it as launch-ready.

The final bullet is a handoff risk, not a request to change the application
from this repository. Route any application remediation to its own repository
and review path.

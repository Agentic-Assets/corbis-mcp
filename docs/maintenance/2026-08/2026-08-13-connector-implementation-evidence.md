# Corbis MCP connector implementation evidence (2026-08-13)

**Source branch:** `feat/corbis-mcp-connector`

**Source base / remote branch head before this working-tree change:**
`099492d07ba29aa2b105894700affd9b1096b4b1`

**Purpose:** record implementation-time observations and local validation. This
is not a source release, direct-client acceptance record, production
acceptance record, Marketplace admission, or directory publication record.

## Source package work completed

- Added independent Claude Code, Codex, and Cursor manifests at version
  `0.1.0`.
- Added the Codex-specific `.mcp.json` and the Cursor-specific `mcp.json`
  `mcpServers` maps. Both name `corbis` and point exactly to
  `https://www.corbis.ai/api/mcp/universal`.
- Kept the Claude HTTP configuration inline in its own manifest. The client
  adapters remain separate files and acceptance lanes, so one parser contract
  cannot prove another client's installation or OAuth behavior.
- Added `tests/validate_package.py`, a Python-standard-library static contract
  check with an explicit, separate unauthenticated metadata smoke option. It
  rejects caches, build artifacts, runtime/dependency manifests, and
  undeclared root-level package components. It also scans the candidate public
  package text for placeholders, credential-like values, and local or private
  paths without scanning excluded maintainer material.
- Updated the README to describe the source package's current proof boundary.

No server implementation, OAuth callback, static tool catalog, credential,
client registration, Marketplace control-plane artifact, or automatic sync was
added.

## Local evidence

All observations below were made on 2026-08-13 in this workspace.

| Check | Result | Scope proved |
| --- | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py` | Passed, 10 tests | Descriptor parsing, shared metadata/version, exact endpoint, contained paths, no placeholders, unsafe URLs, credential fields, undeclared manifest components, candidate public package text, and prohibited local artifacts |
| `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --smoke` | Passed at `2026-08-13T11:19:48Z` | Anonymous GET availability for the exact endpoint and protected-resource metadata only |
| JSON parse for the five JSON files | Passed | JSON syntax only |
| Claude Code `2.1.231`, staged-payload `claude plugin validate <payload> --strict` | Passed | The isolated Claude connector payload's strict manifest validation |
| Claude Code strict validation at repository root | Blocked only by the company-required root `CLAUDE.md` bridge, which Claude reports is not a plugin component | This is a source-repository layout warning, not a connector manifest failure. The future Marketplace allowlist excludes maintainer material. |
| Codex CLI `0.147.0` | No generic `codex plugin validate` command exposed; an ephemeral `mcp_servers.corbis.url` configuration resolved as streamable HTTP at the exact endpoint | The separate Codex configuration received non-persistent parsing validation. It did not validate a plugin `.mcp.json` file, native plugin installation, or OAuth. |
| Cursor `3.15.19` | No generic platform CLI validator exposed | The Cursor descriptor received JSON and portable-contract validation. Native local load remains untested. |
| Added-file secret scan and dependency inventory | No credential pattern or runtime dependency found | Static source review only |

The latest metadata smoke probe returned HTTP 200 from the endpoint and its
protected-resource metadata document. It used no token, did not begin OAuth,
and did not invoke a tool.

## Adversarial review reconciliation

A focused read-only review identified two potential packaging concerns. The
cache and build-artifact gap was confirmed and addressed with the source-tree
guard and `.gitignore` rule above. The reviewer also questioned the Codex
`.mcp.json` shape and the absence of a `type` field. The current official Codex
MCP page documents `config.toml` with an `mcp_servers` table, but does not
define a plugin `.mcp.json` schema. The connector and Marketplace profile now
use the Marketplace's established `mcpServers` adapter convention and lock it
with exact portable checks. This is not official native-plugin acceptance;
that acceptance, including OAuth, remains an unperformed release gate.

## Endpoint and OAuth discovery observation

Anonymous discovery identified the protected resource as the configured HTTPS
endpoint, with an authorization server under `https://www.corbis.ai/api/mcp`.
The public metadata advertises authorization-code and refresh-token grants,
dynamic client registration, and PKCE `S256`. This is discovery evidence only.
It does not validate consent, redirect handling, resource binding, scope
reduction, refresh, revocation, or any client-specific OAuth flow.

## Application-readiness reconciliation

The current `Agentic-Assets/agentic-assets-app` default branch was observed at
`ab3ea384b14e56c8abef781b276819009b7f235b`; GitHub reported a production
deployment for that SHA. The live endpoint and OAuth discovery documents were
also reachable at the time of this record.

That deployment must not be used as evidence that the endpoint is ready for a
directory or connector release:

- Current `main` still lacks advertised output schemas for the five
  market-ranking tools named in the source handoff's known gap.
- Draft application PR [#1589](https://github.com/Agentic-Assets/agentic-assets-app/pull/1589)
  remains open at `74d5e6ee1a7383a9ea2de393bc0c288ef4af089c` with no GitHub
  check runs recorded during this reconciliation.
- The draft's `ScreenMarketsOutput` does describe the producer's nested
  `components` object, including value, percentile, weighted contribution,
  weight, and direction. The producer implementation has the same fields.
- A separate local follow-up branch based on that draft head,
  `fix/corbis-mcp-screen-output-contract`, now contains commit
  `c85d1e16b`. It safe-parses an actual `screenMarkets` result with
  `ScreenMarketsOutput` and asserts the producer's exact nested component
  values. On 2026-08-13, its focused Vitest file passed 26 tests, and
  `pnpm lint`, `pnpm type-check`, and `pnpm exec next build --webpack` exited
  successfully. The build emitted environment-dependent Supabase, auth, and
  pricing fallback warnings while rendering static pages; it did not use
  production credentials or constitute live acceptance.

This is producer-to-schema validation in an isolated local application branch.
It is not a change to draft PR #1589, a reviewed application change, a merge,
or production deployment evidence.

Application remediation and its test run belong in `agentic-assets-app`; this
source repository did not change that application.

## Marketplace reconciliation

`Agentic-Assets/Agentic-Assets-Marketplace` default branch was observed at
`2728bf631e9e076e1822b9977e3f3191683110c7`. A separate open Marketplace PR
now prepares a `corbis` policy, `corbis-mcp-v1` profile, root-payload
promotion, and staged-payload validation. It has no merged control-plane
profile, staged `plugins/corbis/` snapshot, digest-bound client evidence,
catalog admission, or attestation.

The Marketplace profile must merge before a separate promotion branch can
verify a signed source tag against the live policy. Promotion, evidence,
admission, and attestation remain explicit human-gated steps.

## Open gates and next evidence

1. Founder decision on final public license, security reporting route, support
   channel, approved assets, and final public copy.
2. A public source-repository / directory decision. The source repository was
   still private during this reconciliation. Public support, contact, and
   security routes were not verified as package-ready.
3. A decision to integrate the local producer-derived `screenMarkets`
   nested-ranking contract test with the application readiness work, followed
   by application review, merge, deployment, and live readback.
4. Controlled reviewer authorization for native Claude Code, Codex CLI, and
   Cursor local installation/OAuth, plus Inspector-equivalent authentication,
   authorization, invalid-input, and bounded-result checks. No reviewer
   credentials were used.
5. Explicit source-review, merge, and signed annotated tag authorization.
6. A merged Marketplace policy/profile, signed-tag promotion, digest-bound
   Claude Code, Codex CLI, and Cursor local evidence, admission, and
   attestation.
7. Separate Anthropic, OpenAI, and Cursor directory permissions, submission,
   review, and publication. A local validator or descriptor does not establish
   any of these states.

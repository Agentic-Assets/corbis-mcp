# Corbis MCP source repository instructions

Read `~/AGENTS.md` first. This repository is the canonical editable source for
the thin **Corbis** remote-MCP connector. It is not the Corbis application,
the Corbis Research toolkit, or the Agentic Assets Marketplace.

## Start here

Read these files before changing the package:

1. [`docs/00-start-here.md`](docs/00-start-here.md)
2. [`docs/01-build-plan.md`](docs/01-build-plan.md)
3. [`docs/02-marketplace-release-contract.md`](docs/02-marketplace-release-contract.md)
4. [`docs/03-security-and-acceptance.md`](docs/03-security-and-acceptance.md)
5. [`docs/04-source-record.md`](docs/04-source-record.md)

The documents distinguish verified facts from future gates. Revalidate
time-sensitive platform requirements, endpoint metadata, repository state, and
application readiness before acting on them.

## Ownership boundary

- This repository owns only the public-facing, root-level connector package:
  three client descriptors, two MCP descriptors, approved public assets,
  documentation, license, security/support material, changelog, and package
  tests.
- `Agentic-Assets/agentic-assets-app` remains the only owner of the production
  MCP server, tool catalog, OAuth, authorization, subscriptions, data access,
  result contracts, monitoring, and deployment.
- `Agentic-Assets/Corbis-Plugin` remains a separate private research-workflow
  product. Do not copy its skills, agents, commands, hooks, WRDS workflows,
  generated files, or private research material here.
- `Agentic-Assets/Agentic-Assets-Marketplace` is a private distribution
  control plane. It later receives an allowlisted immutable snapshot of a
  signed release from this repository. It is never an editable mirror or a
  substitute source of truth.

## Non-negotiable package rules

- The remote endpoint is `https://www.corbis.ai/api/mcp/universal`. Keep it in
  descriptors without query-string credentials, tokens, client secrets, or
  session data. OAuth is the default connection path.
- Do not implement, proxy, duplicate, or hard-code a Corbis tool catalog in
  this repository. The live server selects tools and enforces authorization for
  the authenticated principal.
- Keep client adapters distinct. A descriptor that parses locally is not proof
  that another client, a directory, or a Marketplace route accepted it.
- Keep the source package intentionally small. Do not add application code,
  skills, commands, agents, hooks, mutable dependencies, private source code,
  user data, reviewer credentials, client caches, or local configuration.
- Do not put API keys in URLs. Any future unattended-client guidance must use
  a secure header or environment-variable mechanism approved by the service
  owner.
- Treat all public copy as a capability claim. Do not state that every account
  receives every tool, quote a corpus size from memory, or claim a client,
  directory, production deployment, or Marketplace route works without the
  corresponding recorded evidence.

## Working and release rules

- Never push directly to `main`. Use a focused `feat/*`, `fix/*`, `docs/*`, or
  `chore/*` branch, validate the smallest sufficient scope, and open a draft
  PR for review.
- Before a source release, run the current official plugin validators, manifest
  and endpoint smoke checks, a secret/dependency review, and clean-install
  OAuth acceptance checks. Record exact commands, versions, and outcomes.
- Public visibility, final public license, publisher and support identity,
  merge, signed release-tag publication, production deployment, directory
  submission, and Marketplace admission are explicit human gates. A successful
  local check does not authorize any of them.
- A Marketplace promotion may use only a reviewed signed annotated source tag.
  It verifies the signature, tag object, peeled commit, default-branch
  reachability, allowlist, and payload digest. Do not run an automatic sync or
  manually edit a promoted `plugins/corbis` snapshot.

## Required skills and review

For non-trivial package work, refresh and use the applicable MCP-builder,
testing-strategy, security-review, agentic-assets-expert, and
agentic-assets-brand-kit guidance. Use the current official client validators
instead of copying a historical manifest example. Complete an adversarial and
security review before any release-candidate decision.

### Project-local client guidance

- **Plugin Structure** guides the Claude descriptor and `.claude-plugin/`
  layout.
- **plugin-creator** guides `.codex-plugin/plugin.json`; do not use its
  scaffold or local-Marketplace generator in this root-level source package.
- **chatgpt-apps** provides docs-first ChatGPT MCP compatibility and submission
  guidance. This connector remains tool-only: it does not authorize a local
  server, widget, or static tool surface.

These skills supplement, never replace, the current official client schemas,
validators, and distinct acceptance evidence for each client.

## Before declaring work complete

Report separately:

1. Source-package tests and static validation.
2. Direct-client acceptance for the exact source release.
3. Marketplace promotion, evidence, and admission for the exact payload digest.
4. Production deployment and live endpoint readback.
5. Public-directory submission and publication.

Do not collapse any of these into a single "released" claim.

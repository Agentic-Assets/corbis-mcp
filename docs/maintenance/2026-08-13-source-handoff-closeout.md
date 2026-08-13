# Corbis MCP source handoff closeout (2026-08-13)

**Branch:** `docs/corbis-mcp-build-handoff`

**Base:** `main` at `28cd4c172cf86877b9fa8b7580ac2ffb7fdd539c`

**Implementation commit:** `3f9f2bcd8d353fb9456db0e19ad018a6d40a2874`
(`docs(corbis): add source package handoff`)

**State at this record:** committed locally on the documentation branch. No
push, pull request, merge, visibility change, release tag, production change,
Marketplace action, or directory submission is claimed by this record.

## Goal

Move the founder-selected source and Marketplace decisions into the empty
`corbis-mcp` source repository, so a future coding agent can build the minimal
connector without re-deriving its ownership boundaries, proof requirements, or
approval gates.

## What shipped

- Root [`AGENTS.md`](../../AGENTS.md) establishes this repository as the sole
  editable thin connector source and prevents application, research-toolkit, and
  Marketplace-control-plane scope drift.
- Root [`README.md`](../../README.md) gives the current source-package status,
  remote endpoint, and source-handoff entry point without representing the
  repository as released.
- [`docs/00-start-here.md`](../00-start-here.md) gives a cold-start coding
  agent the selected model, required sequence, explicit non-equivalences, and
  first verification checkpoint.
- [`docs/01-build-plan.md`](../01-build-plan.md) specifies the root package
  tree, descriptor constraints, tests, exclusions, and phased source-release
  plan.
- [`docs/02-marketplace-release-contract.md`](../02-marketplace-release-contract.md)
  makes the later `corbis@agentic-assets` snapshot one-way, signed-tag,
  allowlisted, digest-bound, and evidence-gated.
- [`docs/03-security-and-acceptance.md`](../03-security-and-acceptance.md)
  records the OAuth, secret, public-copy, protocol, and separate-client proof
  boundaries.
- [`docs/04-source-record.md`](../04-source-record.md) records decisions,
  source planning provenance, known gaps, human gates, and current primary
  references.

## Verification

The following checks were run against the content committed in `3f9f2bc`:

- `git diff --check` passed before the commit.
- Every referenced local handoff file and local Markdown target was checked for
  existence before the commit.
- The official MCP, OpenAI, Anthropic, and Claude Code reference URLs listed in
  `docs/04-source-record.md` resolved when checked on 2026-08-13.
- `git status --short --branch` was clean immediately after the implementation
  commit.

There is no runnable source package yet, so no plugin validator, client
installation, OAuth, MCP Inspector, test suite, Marketplace preflight, or
production acceptance result is claimed.

## Decisions preserved

- `corbis-mcp` is the editable root-level source; it does not grow a duplicate
  `plugin/` layout for Marketplace convenience.
- `corbis@agentic-assets` is later promoted from an exact signed source tag;
  it is not a fork or automatic mirror.
- Client validation, direct-client acceptance, Marketplace admission,
  production deployment, and public-directory publication remain separate
  proofs.
- The current application readiness candidate must be independently reconciled
  and deployed before this source package can be represented as endpoint-ready.

## Deliberately deferred

- The actual package descriptors, assets, public license/support/security
  materials, and tests are intentionally not created here.
- Final public copy, brand assets, support identity, license, visibility,
  release tag, and publication decisions remain founder gates.
- The Marketplace control-plane profile, policy, root-payload support,
  promotion, evidence, admission, and attestation remain separate work in the
  Marketplace repository.

## Left to the operator

Choose whether to push this local documentation branch and open a draft PR.
Before source-package implementation begins, authorize or decide the public
materials enumerated in `docs/04-source-record.md`, and route any application
readiness remediation through `agentic-assets-app` rather than this repository.

# Forward queue after Corbis MCP source handoff (2026-08-13)

Candidate work surfaced while creating the source handoff. This is a menu, not
a roadmap. Revalidate every item against the current source repository,
production service, Marketplace control plane, official platform requirements,
and founder authorization before acting.

## Hardening

- **Add a source-package contract test suite**
  (confidence: required future implementation work; priority: high)
  Once descriptors exist, add portable tests for JSON parsing, shared metadata,
  exact endpoint configuration, relative asset paths, release-version drift,
  placeholder URLs, and secret/query-string rejection. Keep a live endpoint
  smoke test separate and explicit about whether it ran.

- **Exercise root-payload containment in the Marketplace**
  (confidence: verified control-plane gap; priority: high)
  Before allowing promotion, implement and test `source_payload_root: "."`
  using exact committed blobs, strict allowlists, symlink/traversal rejection,
  and fixtures with unrelated source documents. Assert that `AGENTS.md`,
  maintainer docs, and tests cannot enter `plugins/corbis/`.

- **Add a source-to-payload consistency fixture**
  (confidence: required future implementation work; priority: high)
  Test that all three promoted client descriptors and both MCP descriptors
  carry the signed release version, approved endpoint, and only
  package-root-relative references after promotion.

## Correctness and security

- **Reconcile the application nested-ranking output-schema audit**
  (confidence: focused audit signal; priority: high)
  The application candidate has a supported nested market-ranking producer
  shape that appears narrower than the advertised output schema. Fix or
  explicitly refute it in `agentic-assets-app`, with producer-derived tests,
  before relying on its MCP readiness claims.

- **Run the production OAuth and threat-model review**
  (confidence: verified release requirement; priority: high)
  After approved deployment and reviewer-account access, evaluate dynamic
  registration, PKCE, consent, redirect validation, refresh behavior, resource
  binding, scope minimization, and tool authorization without committing
  credentials or user data.

- **Create a public-material review gate**
  (confidence: required future implementation work; priority: medium)
  Before source visibility, review every public source file for private
  application details, sensitive operational material, incorrect capability
  claims, corpus counts, support links, and license/brand consistency.

## Marketplace and client acceptance

- **Implement the minimal `corbis-mcp-v1` profile**
  (confidence: founder-selected required distribution lane; priority: high)
  Add a policy-driven profile distinct from Corbis Research. Require exact
  digest-bound Claude Code and Codex CLI evidence, retain separate Cursor
  adapter validation, and do not claim Cursor Team Marketplace acceptance.

- **Capture clean direct-client and Marketplace evidence separately**
  (confidence: verified launch requirement; priority: high)
  Record client version, host, installation route, source tag/commit, payload
  digest, OAuth outcome, representative tool behavior, and known untested
  routes. A direct CLI success must not be reused as desktop, Cowork, mobile,
  public-directory, or Team Marketplace proof.

## Documentation and process

- **Decide the public support surface**
  (confidence: founder-gated decision; priority: medium)
  Choose a public `SUPPORT.md` versus an approved README support section only
  after the contact and live support route are approved. Include only the
  chosen file in the Marketplace allowlist.

- **Refresh official schemas immediately before implementation**
  (confidence: time-sensitive requirement; priority: high)
  Use current OpenAI, Anthropic, Claude Code, Codex, Cursor, and MCP primary
  documentation and validators. Do not copy this handoff's historical examples
  as live schema authority.

# Corbis MCP decision and source record

**Record date:** 2026-08-13

This is the durable handoff record for the first source-package implementation.
It is not a release record and must be revalidated before any visibility,
submission, deployment, or Marketplace action.

## Recorded decisions

| Decision | Status | Meaning |
| --- | --- | --- |
| Canonical editable source | Decided | `Agentic-Assets/corbis-mcp` |
| Package ID | Decided | `corbis` |
| Display name | Decided | `Corbis` |
| Publisher | Decided | `Agentic Assets` |
| Remote endpoint | Decided | `https://www.corbis.ai/api/mcp/universal` |
| Private Marketplace selector | Decided, not admitted | `corbis@agentic-assets` |
| Source payload layout | Decided | One root-level thin package, not a duplicate `plugin/` subtree |
| Marketplace artifact | Decided | One-way, signed-tag, allowlisted immutable snapshot at `plugins/corbis/` |
| Automatic synchronization | Rejected | No source-to-Marketplace automatic mirror or GitHub Action |
| Corbis Research reuse | Rejected | No skills, agents, commands, hooks, workflows, WRDS material, or research package copied into this connector |

## Current source-repository state

The original 2026-08-13 initial-seed observation is historical. The first thin
source-package implementation at `2f0cf5832645ad5fea64582aafd04b07b4d61416`
merged through PR #2 at
`ec00b9252366601acd916d0a464e8d0eb18ffaee` on private `main`. It adds the
three client descriptors, two client-specific MCP configuration files,
public-facing source documentation, `CHANGELOG.md`, a source-tree ignore
guard, and portable static and opt-in metadata-smoke checks.

Its implementation-time validation and the exact boundaries of the companion
application test are recorded in
[`docs/maintenance/2026-08/2026-08-13-connector-implementation-evidence.md`](maintenance/2026-08/2026-08-13-connector-implementation-evidence.md).
The merged source is not a signed source release and proves neither native-
client acceptance nor a public installation route. Re-read the remote default
branch, current visibility, branches, pull requests, and signed tags before
any release action.

## Upstream planning sources transferred into this handoff

This repository consolidates the decisions and implementation contract from
the following Marketplace planning artifacts at commit
`e7ede61f6050a3ed9b35f690baf7674052965bcf` on branch
`docs/corbis-public-mcp-publication-plan`:

- `docs/2026-08-05-corbis-public-mcp-plugin-publication-plan.md`
- `docs/maintenance/2026-08-13-corbis-public-mcp-plan-closeout.md`
- `docs/maintenance/2026-08-13-corbis-public-mcp-plan-forward-queue.md`

These local documents are the implementation-oriented source handoff. The
Marketplace repository remains authoritative for its own policy, promotion,
evidence, attestation, and catalog implementation.

## Standards to revalidate at implementation time

Platform forms, schemas, eligibility, and client behavior are intentionally not
frozen in this repository. Re-read the current primary documentation before
building, validating, or submitting:

- [Model Context Protocol tools specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
- [Model Context Protocol security best practices](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices)
- [OpenAI plugin architecture](https://developers.openai.com/plugins/concepts/plugins)
- [OpenAI MCP server guidance](https://developers.openai.com/plugins/build/mcp-server)
- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [Codex MCP configuration](https://developers.openai.com/codex/extend/mcp)
- [Anthropic connector implementation guidance](https://claude.com/docs/connectors/building/mcp)
- [Anthropic plugin submission guidance](https://claude.com/docs/plugins/submit)
- [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)

Use the current official scaffold and validators rather than treating a
historical descriptor example as a schema contract.

## Production application dependency

The relevant application readiness candidate was recorded as:

- repository: `Agentic-Assets/agentic-assets-app`;
- branch: `fix/corbis-mcp-directory-readiness`;
- candidate commit: `74d5e6ee1a7383a9ea2de393bc0c288ef4af089c`;
- draft PR: `https://github.com/Agentic-Assets/agentic-assets-app/pull/1589`;
- historical state at handoff: not merged and not deployed.

Do not treat those values as current. Reconcile them with the live repository
and production endpoint before relying on any endpoint, documentation, OAuth,
tool-schema, or support-route claim.

## Open human gates

The implementation agent must not silently choose or perform any of the
following:

- final public license;
- final publisher/support contact and support channel;
- approved public brand assets and public copy;
- public source-repository visibility;
- merge to `main`;
- signed source release tag publication;
- production deployment, OAuth configuration, entitlement, or tool-surface
  changes;
- use of controlled reviewer accounts or credentials;
- OpenAI or Anthropic submission, publication, and launch communication; or
- Marketplace promotion, admission, attestation, or client-support claim.

An approval for source-package implementation does not imply any of these
authorizations.

## Known implementation and evidence gaps

- The source repository has descriptors, the empty allowlisted
  `provenance.json`, candidate Corbis image assets copied from the production
  application's default branch, and a portable static test suite. The image
  assets still require public-release approval. The repository has no final
  public license, public security or support material, source release tag, or
  direct-client acceptance evidence.
- Marketplace main contained the `corbis` policy and `corbis-mcp-v1` profile
  at `9af39cab5b1ff5e415c6ac50bd790aa107aa5ef0` on 2026-08-14. There is no
  promoted payload, catalog entry, digest-bound evidence, or signed
  attestation.
- Public-directory eligibility, forms, permissions, and client support may
  change. Re-read official documentation immediately before submission.
- The application candidate still requires an integration decision for local
  producer-to-schema test commit `c85d1e16b`, independent review, merge,
  deployment, and live readback.

## Deferred work menu

### High priority: source package and production proof

- Resolve the open public-material decisions, review the existing source
  package, and obtain the explicit signed-tag authorization.
- Decide whether to integrate local application test commit `c85d1e16b` with
  the readiness candidate, then complete its independent review, merge,
  deployment, and live readback before running a redacted authenticated
  per-tool acceptance matrix and signed-out support/documentation route checks
  against the deployed endpoint.
- Run an OAuth and threat-model review for dynamic registration, PKCE, refresh,
  resource binding, scopes, redirect URIs, and reviewer-account handling.

### High priority: required private Marketplace lane

- Revalidate the merged dedicated `corbis-mcp-v1` Marketplace profile and
  root-payload promotion support, including containment and allowlist tests,
  before a source tag is proposed.
- Promote only a signed source tag, bind Claude Code, Codex CLI, and Cursor
  local proof to the resulting digest, then admit and attest
  `corbis@agentic-assets`.

### Medium priority: public discovery and wider clients

- Revalidate OpenAI and Anthropic directory rules and submit only after their
  account/permission, source-visibility, and reviewer requirements are met.
- Test each additional client route separately. Do not infer desktop, mobile,
  Cowork, ChatGPT, Codex desktop, or Cursor Team Marketplace acceptance from a
  direct CLI check.

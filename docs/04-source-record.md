# Corbis MCP decision and source record

**Record date:** 2026-08-16

This is the durable handoff record for the first source-package implementation.
It is not a release record and must be revalidated before any visibility,
submission, deployment, or Marketplace action.

## Recorded decisions

| Decision | Status | Meaning |
| --- | --- | --- |
| Canonical editable source | Decided | `Agentic-Assets/corbis-mcp` |
| Package ID | Decided | `corbis` |
| MCP server identifier | Decided | `corbis-mcp`, distinct from the package ID and the Corbis Research server identifier `corbis` |
| Human-facing plugin display label | Decided | `Corbis` in the supported Claude and Codex display-name fields |
| MCP settings label | Client-dependent | A client may render the technical `mcpServers` key; this source package has no supported per-server display-label field |
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
That historical source was superseded by signed `v0.1.0` on
`ef1c48a715ef8e8a45971e257331aab9d2004d01`. Its Codex installation resolved
to the separately installed Corbis Research server because both descriptors
used the `corbis` MCP server identifier; it is not valid thin-connector Codex
acceptance. The functional correction in the later `v0.1.1` signed annotated
tag is the thin connector server identifier `corbis-mcp`; the release also
updates its matching descriptors, validation, and release records. Its remote
tag object is
`ff16d89bf37f291cd643711233ed255f934dc446`; it peels to
`3fb5b4659ed971f409c0d70135d654f21da4db08`, which is reachable from `main`.
Neither source tag is direct-client acceptance. The later `v0.1.2` tag object
`6219c55ee79eb0031ea73bfe167a08dac39c202e` peels to current `main` commit
`d96a9c7520ab3d572e5510e9cf5a257a444df21f`. It has an SSH signature, but
GitHub reported the signer as `unknown_key` on 2026-08-16; do not describe it
as trusted-verified. Marketplace promoted its immutable source payload digest
`1b94a0e92112cb6a22a947a0bb19e64675342445d0f2ad61ea540fae7eecd9ef` on
2026-08-15. That promotion is not client acceptance, admission, attestation,
or production proof.

The `0.1.3` source candidate preserves `corbis-mcp` as the technical server
identifier and reinforces `Corbis` as the supported human-facing plugin label.
It documents the current client limitation: a settings surface that renders
the MCP map key cannot be changed by an unsupported source-descriptor field.
Re-read the remote default branch, current visibility, branches, pull requests,
and signed tags before any further release action.

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
  application's default branch, a portable static test suite, and concise MIT
  license, security, and support documents. `v0.1.0` is a signed historical
  source tag, but it has no valid thin-connector direct-client acceptance
  evidence because of the MCP server-name collision. The `v0.1.1` tag fixes
  that descriptor collision, but it also has no recorded direct-client
  acceptance evidence. `v0.1.2` has an SSH signature whose trust could not be
  verified with the available signer configuration, and it likewise has no
  recorded direct-client acceptance evidence.
- Marketplace contains the immutable payload promoted from `v0.1.2`, but its
  source promotion does not supply a verified client settings-label readback,
  digest-bound direct-client acceptance, admission, or signed attestation.
- Current client schemas do not provide a supported source-controlled
  per-server label field. A source release cannot honestly claim the post-
  installation settings label is `Corbis` until each applicable client route
  demonstrates that behavior. The application owner may separately assess MCP
  `serverInfo` metadata, but that is not a source-package change.
- Public-directory eligibility, forms, permissions, and client support may
  change. Re-read official documentation immediately before submission.
- The application candidate still requires an integration decision for local
  producer-to-schema test commit `c85d1e16b`, independent review, merge,
  deployment, and live readback.

## Deferred work menu

### High priority: source package and production proof

- Obtain explicit authorization before creating a new trusted signed source tag
  for the `0.1.3` candidate. Preserve the tag-object and peeled-commit SHAs and
  verify the signer with the configured trust material.
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
  before promoting any later signed source tag.
- Promote only an immutable signed source tag, bind Claude Code, Codex CLI,
  and Cursor local proof to the resulting digest, then admit and attest
  `corbis@agentic-assets`.

### Medium priority: public discovery and wider clients

- Revalidate OpenAI and Anthropic directory rules and submit only after their
  account/permission, source-visibility, and reviewer requirements are met.
- Test each additional client route separately. Do not infer desktop, mobile,
  Cowork, ChatGPT, Codex desktop, or Cursor Team Marketplace acceptance from a
  direct CLI check.

# Corbis source-to-Marketplace release contract

## Purpose

This document prevents two different distribution jobs from being confused:

- `Agentic-Assets/corbis-mcp` is the sole editable source package.
- `corbis@agentic-assets` is the future private Marketplace package.

The Marketplace package is an immutable, allowlisted snapshot of a specific
signed source release. It is not a fork, development checkout, Git submodule,
branch reference, or automatic mirror. A source commit, a Marketplace release,
and public-directory publication are independent state transitions.

## Required source-to-payload mapping

| Source fact | Marketplace fact |
| --- | --- |
| Source repository | `https://github.com/Agentic-Assets/corbis-mcp.git` |
| Source payload root | `.` (the package is intentionally root-level) |
| Future Marketplace payload path | `plugins/corbis/` |
| Future Marketplace selector | `corbis@agentic-assets` |
| Required source input | A reviewed, signed annotated tag on a reachable source commit |
| Required artifact identity | The promoted payload digest, bound to source tag and commit |

## Prerequisites before a Marketplace attempt

All of these must exist before an operator tries to admit `corbis`:

The control-plane observations in items 3 through 6 were read from Marketplace
main `9af39cab5b1ff5e415c6ac50bd790aa107aa5ef0` on 2026-08-14. They are
historical observations, not authorization or a substitute for immediate live
revalidation before a promotion.

1. A reviewed source package on an approved source release, with a signed
   annotated tag and recorded tag-object and peeled-commit SHAs.
2. Current direct-client acceptance evidence for the exact source release.
   The required evidence lanes are Claude Code, Codex CLI, and Cursor local.
3. Marketplace main already has a dedicated `corbis-mcp-v1` remote-MCP profile
   that does not reuse Corbis Research. Revalidate it before promotion.
4. Marketplace main already has the `corbis` policy that pins the source
   repository, `main`, source root `.`, target `plugins/corbis/`, trusted
   signer baseline, presentation metadata, source exclusions, allowlist, and
   evidence profile. Revalidate the policy and its signer baseline immediately
   before a promotion branch verifies a source tag.
5. Marketplace main already has promotion support that reads exact committed
   source blobs from root `.`, with containment, traversal, symlink, and
   unrelated-file tests. It must not copy from a mutable working tree.
6. Marketplace main already uses policy-driven acceptance surfaces. The first
   Corbis profile requires `claude_code`, `codex_cli`, and `cursor_local`
   evidence on the exact payload digest. Cursor local acceptance is not
   evidence of Cursor Team Marketplace acceptance.

No root Marketplace catalog entry belongs in the repository before these
prerequisites and evidence are met.

## Minimal promotion allowlist

The Marketplace policy should name exact paths from the signed source tag. The
expected initial set is:

```text
.claude-plugin/plugin.json
.codex-plugin/plugin.json
.cursor-plugin/plugin.json
.mcp.json
mcp.json
assets/icon.png
assets/logo.png
assets/logo-dark.png
README.md
CHANGELOG.md
LICENSE
SECURITY.md
SUPPORT.md
provenance.json
```

If public documentation moves below a dedicated path, add only the named
released documents after review. Do not widen the allowlist by copying all
`docs/` content.

The policy must exclude, at a minimum:

```text
.git/
.gitignore
AGENTS.md
docs/00-start-here.md
docs/01-build-plan.md
docs/02-marketplace-release-contract.md
docs/03-security-and-acceptance.md
docs/04-source-record.md
docs/maintenance/
tests/
local caches, editor state, credentials, tokens, sessions, logs, and secrets
application source, private sources, research workflows, mutable dependencies
```

The source documentation and AGENTS file are maintainer material. They may
remain in the source repository, but they are not installable Marketplace
payload files. The source policy, not an informal convention, must enforce the
exclusion list.

## One-way release sequence

1. Review and merge the source package through the normal source-repository
   branch process after the required authorization.
2. Create and verify a real signed annotated final `vX.Y.Z` tag on a commit
   reachable from `main`. Record the remote tag-object SHA, peeled commit SHA,
   signature verification, and default-branch reachability.
3. On a separate Marketplace `chore/*` branch, promote only allowlisted exact
   blobs from that immutable tag into a staged `plugins/corbis/` payload. Do
   not add a root catalog entry at this point.
4. Run Marketplace preflight and generate a disposable exact-digest preview.
5. Obtain real Claude Code, Codex CLI, and Cursor local acceptance evidence,
   then commit immutable proof records bound to that exact payload digest.
6. Admit atomically only after all required proof records pass. The admission
   may add the three root adapters, each pointing only to `./plugins/corbis`.
7. Create and sign an attestation using externally controlled trust material,
   then run the Marketplace release gate and review the Marketplace branch.
8. State only the client support that the evidence proves. Production
   deployment/live readback, public visibility, and directory publication
   remain separate gates.

## Update and rollback rules

- Every Marketplace update starts with a strictly newer reviewed signed source
  release and fresh evidence for the newly promoted digest.
- Never edit the admitted snapshot directly, replace it manually, or sync it
  from an untagged source branch.
- Do not infer a client cache refresh, an in-place downgrade, a desktop route,
  Cowork, or Cursor Team Marketplace acceptance from the initial direct-client
  checks.
- Treat rollback as an explicit operator/runbook decision. Do not delete an
  admitted payload to simulate a rollback.

## Separation from public discovery

The private Marketplace makes the approved snapshot available to its permitted
Marketplace users. It does not make Corbis publicly discoverable and does not
replace the separate OpenAI or Anthropic submission/review/publication paths.

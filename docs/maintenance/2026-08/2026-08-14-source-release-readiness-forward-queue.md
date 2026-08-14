# Forward queue after Corbis MCP source-release readiness (2026-08-14)

Candidate work surfaced during the source-readiness branch. This is a menu, not
an authorization. Revalidate each item against current policy and owner
approval before acting.

## Release blockers

- **Approve public release materials** (confidence: verified blocker; priority:
  high)
  Obtain authoritative `LICENSE`, `SECURITY.md`, and `SUPPORT.md` content,
  including the publisher, disclosure process, and support route. Do not infer
  these from another product or add a placeholder.

- **Approve candidate public assets** (confidence: verified human gate;
  priority: high)
  Confirm that the three assets copied from the public Corbis application are
  authorized for this connector's public source release before the release gate
  is considered satisfied.

## Hardening

- **Bind public asset provenance to an owner-approved record** (confidence:
  verified improvement; priority: medium)
  Once approved, record the asset owner, approved source paths, and content
  hashes in a reviewed public-material decision rather than relying on a
  one-time implementation closeout.

- **Add an approved-client acceptance harness** (confidence: verified gap;
  priority: high)
  After controlled reviewer accounts and client routes are available, automate
  only non-secret setup checks and retain separate evidence for Claude Code,
  Codex CLI, and Cursor local acceptance. Keep this distinct from endpoint
  health and from Marketplace proof binding.

## Process

- **Revalidate Marketplace policy immediately before promotion** (confidence:
  verified requirement; priority: high)
  Re-read live Marketplace `main`, its Corbis allowlist, signer baseline, and
  promotion commands after the final source tag is created. The 2026-08-14
  readback is historical evidence, not current authorization.

- **Preserve the release-material failure mode** (confidence: implemented
  control; priority: medium)
  Keep `tests/validate_package.py --release` as a release gate that fails closed
  when a required public artifact is missing, malformed, symlinked, or outside
  the source boundary.

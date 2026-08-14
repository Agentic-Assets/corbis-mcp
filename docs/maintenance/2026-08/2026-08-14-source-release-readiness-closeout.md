# Corbis MCP source-release-readiness closeout (2026-08-14)

**Branch:** `feat/corbis-mcp-source-release-readiness`

**Base:** `origin/main` at `657b7176f8e03ae83b684ee80b1827418b1b164c`

**Implementation commits:** `7c09976cc65b842ebcaf740c6c2dd065910be7ad`
and `102c4c7883e899a652c16a76c74674eaa42d3505`

**State at this record:** source hardening is committed locally. The public
release-material gate is intentionally blocked. No source tag, Marketplace
promotion, client-acceptance evidence, admission, attestation, deployment, or
public-directory publication is claimed.

## Goal

Prepare the thin source package for a future private Marketplace promotion
without crossing into Marketplace control-plane work or the production
application.

## What shipped

- `7c09976` adds the allowlisted empty `provenance.json`, repairs the canonical
  root `CLAUDE.md` bridge, updates public package and Marketplace-contract
  documentation, and hardens the static release-material validator.
- The validator now requires an exact source-package boundary, regular required
  files, a fixed HTTPS endpoint, credential-free descriptors, and structurally
  sound PNG assets. It rejects bad zlib streams, unsafe decoded sizes, invalid
  PNG filter bytes, absent indexed palettes, and oversized indexed palettes.
- `102c4c7` fixes the indexed-palette bit-depth edge case identified by final
  adversarial review and adds a regression test.
- `assets/icon.png`, `assets/logo.png`, and `assets/logo-dark.png` are copied
  from the public asset paths on `Agentic-Assets/agentic-assets-app` `main` at
  `3b9504304e90a00c723dd878e15554ca1ed5d9da`, as authorized for this task.
  Their source paths are respectively `public/android-chrome-512x512.png`,
  `public/logo/corbis-v4-navy.png`, and `public/logo/corbis-v4-light.png`.
  They remain candidate public assets pending the product owner's approval.
- Read-only Marketplace-policy reconciliation used Marketplace `main`
  `9af39cab5b1ff5e415c6ac50bd790aa107aa5ef0` on 2026-08-14. No Marketplace
  file or catalog entry was changed.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py` passed 14
  tests on the implementation branch.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --release`
  passed its 14 tests and then failed as designed because `LICENSE`,
  `SECURITY.md`, and `SUPPORT.md` are absent.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --smoke`
  observed HTTP 200 for the public endpoint and protected-resource metadata.
  A credential-free JSON-RPC `tools/list` health probe also returned HTTP 200.
  These are endpoint-health observations only, not client acceptance,
  authorization, Marketplace admission, or production-release proof.
- `claude --version` reported `2.1.232`. `claude plugin validate` with
  `--strict` passed for an allowlisted staged payload. Strict validation of the
  repository root warns about the required root `CLAUDE.md` bridge, so the root
  is not a valid Claude plugin staging shape by design.
- Codex CLI exposed plugin installation and marketplace commands but no generic
  plugin-validation command. Cursor was not available for headless native
  acceptance. No native client acceptance was performed.
- `git diff --check` passed before the implementation commits. The final
  source security scan `d04a550a-0c23-412a-b556-16b036a0e1e9` reviewed
  `657b717..102c4c7`, found zero reportable findings, and generated its report
  outside this repository. The final adversarial review found the indexed
  palette defect, which `102c4c7` resolves; the re-review found no remaining
  confirmed source or Marketplace-contract defect.

## Decisions preserved

- Do not create placeholder legal terms, security contacts, support promises,
  or a public asset approval. The release validator remains failing until
  verified authority supplies them.
- The source `provenance.json` is an empty required source file. It does not
  record a tag, commit, payload digest, evidence, admission, or attestation.
- The source handoff is one-way: a reviewed signed annotated tag can later be
  promoted as an exact allowlisted snapshot. Client acceptance, atomic
  admission, externally trusted attestation, production readback, and public
  publication remain separate gates.

## Left to the operator

1. Approve the final public license terms, security disclosure contact and
   process, support contact and route, and use of the candidate public assets.
2. After those materials are committed and review is complete, merge the source
   branch, verify its exact remote `main` SHA, and have the configured trusted
   signing authority create and verify a signed annotated final tag, for
   example `git tag -s -a v0.1.0 <verified-main-sha> -m 'Corbis MCP 0.1.0'`.
   Do not create that tag without the authority and verification.
3. In the separate Marketplace repository, promote only that immutable signed
   tag, generate an exact-digest disposable preview, obtain real Claude Code,
   Codex CLI, and Cursor local acceptance evidence, commit digest-bound proofs,
   admit atomically, create a signer-controlled attestation, and run the
   Marketplace release gate.

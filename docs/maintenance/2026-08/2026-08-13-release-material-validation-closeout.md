# Release-material validation closeout (2026-08-13)

**Branch:** `docs/corbis-mcp-current-state`

**Base:** `ec00b9252366601acd916d0a464e8d0eb18ffaee` (`origin/main`)

**Implementation commits:**

- `4ffc266aa114e2f4eb95734ab1f8d5a2b80b8830` — validate compressed PNG
  release assets.
- `24668242f8fef56bcfbfcd67bf75cd087a600a09` — verify PNG decoded scanline
  size.

## Goal

Fix the release-material validator so a structurally framed PNG cannot pass
solely because its chunks and CRCs are valid.

## Completed work

- The validator now requires a complete, single zlib stream across consecutive
  `IDAT` chunks, rejects trailing compressed data and unknown critical chunks,
  and bounds decoded output to 64 MiB.
- It validates IHDR color/depth/method fields and requires the decoded byte
  count to match the IHDR dimensions for both non-interlaced and Adam7 images.
- Regression coverage includes split IDAT streams, corrupt and trailing zlib
  data, and a 1×1 RGBA image with too-short decompressed scanlines.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py` — passed,
  12 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --release` —
  failed as expected because the founder-gated `LICENSE`, `SECURITY.md`,
  `SUPPORT.md`, and brand assets do not exist.
- `git diff --check` — passed.
- Two repository-only Codex Security diff scans completed with no findings:
  `6c4cc63b-b147-4d1e-8942-4a64fdb97955` and
  `dbd1832a-baf8-4f26-930d-7c1a4e4c296b`.
- An independent adversarial review identified the short-scanline gap; the
  second implementation commit and regression test resolve it.

## Decision record

The validator intentionally remains a standard-library structural gate. It
does not make a human approval, client acceptance, source tag, deployment, or
publication claim.

## Left to the operator

Final public material, source release, and all direct-client acceptance remain
separate human-gated work. The branch is pending its final documentation commit
and push; merge requires the explicit Cayman approval phrase.

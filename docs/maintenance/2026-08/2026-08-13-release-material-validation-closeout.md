# Release-material validation closeout (2026-08-13)

**Branch:** `docs/corbis-mcp-current-state`

**Base:** `ec00b9252366601acd916d0a464e8d0eb18ffaee` (`origin/main`)

**Implementation commits:**

- `4ffc266aa114e2f4eb95734ab1f8d5a2b80b8830` — validate compressed PNG
  release assets.
- `24668242f8fef56bcfbfcd67bf75cd087a600a09` — verify PNG decoded scanline
  size.
- `5f5abe6254b02b2dbbc88337fd5bdb55e7202bad` — reject symlinked release
  asset directories.

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
- Every component of each required release-material path must now be a real
  in-tree path, so a symlinked `assets/` directory cannot make external files
  appear to be signed release assets.

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
- The final open PR review thread concerning a symlinked `assets/` directory
  was addressed by `5f5abe6254b02b2dbbc88337fd5bdb55e7202bad`; static
  validation still passes. The existing `--release` invocation continues to
  fail as expected while founder-gated public material is absent.

## Decision record

The validator intentionally remains a standard-library structural gate. It
does not make a human approval, client acceptance, source tag, deployment, or
publication claim.

## Left to the operator

Final public material, source release, and all direct-client acceptance remain
separate human-gated work. Merge requires the explicit Cayman approval phrase.

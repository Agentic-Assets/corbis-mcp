# Corbis MCP public release-materials closeout (2026-08-14)

**Branch:** `docs/corbis-mcp-research-readme`

**Base:** `main` at `364d891db87d923152e2d03e50b1d2fbaba76bdd`

**State at this record:** the source package has required license, security,
and support files and passes its structural release-material gate. It is not a
tagged release, Marketplace artifact, admitted plugin, client-acceptance
record, production readback, or public-directory publication.

## Materials added

- `LICENSE` copies the MIT license from `Agentic-Assets/Corbis-Plugin` `master`
  commit `ca45471aece6b96c376ee1459336fb2646c67365`, root `LICENSE`, blob
  `d7bd8173005d2f6328120e789a93fd8541dc4648`.
- `SUPPORT.md` uses `corbis@agenticassets.ai`, the canonical public Corbis
  support contact from `Agentic-Assets/agentic-assets-app` `main` commit
  `3b9504304e90a00c723dd878e15554ca1ed5d9da`,
  `lib/constants/support-contact.ts`, blob
  `df0e87fc0ef4470e5c041c7b9d3ab7ab0ff4fe3f`.
- `SECURITY.md` uses private reporting through `security@agenticassets.ai`,
  matching the Corbis security information sheet in
  `Agentic-Assets/CRE_EQUIRE` `main` commit
  `d123efb8a5ebfcb53617994fafafa7fa143dab1b`,
  `docs/soc2-compliance/security-information-sheet-corbis.md`, blob
  `19f74305ceee06f3d07d5b069aefd7838fd1032d`.

The support and security files make no response-time, bounty, disclosure-scope,
or service-level promise. They prohibit sending credentials, tokens, or client
data by email.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py` passed 14
  tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --release`
  passed 14 tests and the release-material gate.
- `git diff --check` passed.

## Remaining gates

- Approve the candidate public brand assets and a current README screenshot if
  one is desired.
- Merge the reviewed source change, create and verify a real signed annotated
  tag with the configured signing authority, then complete separate client
  acceptance and Marketplace promotion, proof, admission, and attestation
  gates.

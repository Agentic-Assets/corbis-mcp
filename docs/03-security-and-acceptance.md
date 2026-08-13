# Corbis MCP security and acceptance plan

## Security model

The source package exposes client metadata and a remote endpoint reference. It
does not authenticate a user, authorize a tool, proxy requests, or store data.
Those decisions remain in the production Corbis application. Keeping that
boundary intact is the principal security property of this repository.

The implementation must preserve these invariants:

- No token, API key, client secret, session, OAuth registration secret, or
  reviewer credential is committed, logged, or placed in a URL.
- OAuth remains the default connection route. The package does not introduce a
  callback handler or change redirect-URI, PKCE, consent, refresh, resource
  binding, or scope behavior.
- The wrapper never bypasses server-side authorization or converts a denied
  tool into a local fallback.
- Tool availability is dynamic and account-scoped. The package does not
  promise a fixed tool count, universal premium access, or elevated scope.
- Public copy is narrow and factual. Treat documentation, descriptors, asset
  metadata, tool descriptions, and links as part of the security boundary.

The MCP specification requires servers to validate inputs, apply access
controls, rate limit invocation, and sanitize outputs. Those are application
responsibilities to evaluate in the production readiness lane, not features to
reimplement in this package. If the wrapper changes its scope in a way that
needs any server-side behavior, stop and create a separately authorized
application change.

## Source-package review checklist

### Secrets and supply chain

- Scan the complete candidate tree, including history introduced by the branch,
  for credentials, private URLs, tokens, session values, test accounts, copied
  environment files, and client caches.
- Prefer static JSON and approved image/document assets. Introduce no runtime
  dependency, executable, installer, network proxy, or generated blob without
  an approved reason and dependency review.
- Ensure every local file reference is relative, contained in the package, and
  included in the intended source-release review.

### Endpoint and OAuth metadata

- Require HTTPS for the production MCP endpoint and every OAuth-related public
  URL. Reject `javascript:`, `data:`, `file:`, local-host, private-network, and
  shell-invoked URL paths in descriptors or documentation.
- Verify protected-resource and authorization-server metadata immediately
  before direct-client tests. Do not record tokens or reproduce authentication
  responses containing user data in the repository.
- Exercise the real client's OAuth route with a controlled reviewer account
  only after approval. Confirm consent, redirect, PKCE, resource binding,
  reduced-scope behavior, refresh/revocation behavior where applicable, and
  failure handling without placing sensitive evidence in Git.

### Public-copy and data minimization

- Never quote the Corbis corpus size from memory. If a public figure is needed,
  fetch it from corbis.ai during the publication task and cite that live
  observation.
- Do not paste client data, contracts, partner identities, reviewer
  credentials, private tool samples, prompt contents, or raw results into the
  README, release notes, issue, PR, evidence, or public assets.
- Do not cite a support or documentation URL until it works in a signed-out
  browser. Do not use a login redirect or a visually successful 200 page that
  actually says documentation was not found.

## Acceptance matrix

Record every result against the exact source commit/release tag, descriptor
version, endpoint, client version, operating system/host, authentication state,
adapter/installation route, test prompt or operation class, result, and
evidence location. Redact user and credential data.

| Lane | Before source release | Before Marketplace admission | What it does not establish |
| --- | --- | --- | --- |
| Static package tests | Required | Re-run through staged payload validation | Server health or client acceptance |
| Claude strict validation | Required | Required for promoted descriptor | Claude Desktop, Cowork, or directory publication |
| Codex package validation | Required | Required for promoted descriptor | Codex desktop or public-directory publication |
| Cursor schema/direct adapter check | Recommended if descriptor is shipped | Required for adapter validation if cataloged | Cursor Team Marketplace acceptance |
| MCP Inspector or protocol client | Required against the selected endpoint | Re-run when source/endpoint changes | OAuth experience in every native client |
| Controlled direct Claude Code acceptance | Required evidence lane | Required and digest-bound | Claude Desktop, Cowork, web/mobile, or directory acceptance |
| Controlled direct Codex CLI acceptance | Required evidence lane | Required and digest-bound | Codex desktop, ChatGPT, or directory acceptance |
| Marketplace isolated preview | Not applicable | Required | A client refreshed or installed the root catalog entry |
| Marketplace admission and attestation | Not applicable | Required after evidence | Public discovery or untested client support |

## Production readiness dependency

The source package must not be represented as production-ready merely because
its static files are valid. The endpoint itself needs its own independent
application review, merge, deployment, OAuth validation, per-tool acceptance
matrix, output-contract checks, and live readback.

At the time this handoff was prepared, the application readiness work was a
draft candidate rather than a merged deployment. A focused follow-up on local
application branch `fix/corbis-mcp-screen-output-contract` added commit
`c85d1e16b`, which safe-parses an actual `screenMarkets` producer result with
the registered `ScreenMarketsOutput` schema and asserts the nested ranking
components. This establishes a local producer-to-schema check only. It is not
part of draft PR #1589, a reviewed application change, a merge, deployment, or
production readback. The remaining application gate belongs to
`agentic-assets-app`; it neither expands this wrapper nor authorizes a change
from this repository.

## Required review outcomes

Before a source tag or Marketplace admission is proposed, preserve:

1. Static and validator results, including versions.
2. A secret and dependency review with findings and resolutions.
3. A focused MCP/OAuth threat model and adversarial review.
4. Direct-client acceptance evidence and all known untested routes.
5. The exact application deployment/readback boundary.
6. The source tag, source commit, promoted payload digest, and signed
   Marketplace attestation once the Marketplace lane is authorized.

An unresolved high-severity security finding, unsupported public claim,
unreviewed server-side change, or missing required evidence blocks release.

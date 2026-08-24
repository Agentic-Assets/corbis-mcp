# Corbis MCP public-directory submission forward queue (2026-08-24)

Companion to
`2026-08-24-public-directory-submission-readiness-closeout.md`. Items are
ordered by dependency. Owners: founder items require Cayman; application
items belong to `Agentic-Assets/agentic-assets-app`; package items belong to
this repository.

## Founder gates (portal logins, approvals, credentials)

1. Review and merge `docs/corbis-directory-submission-readiness` (explicit
   "merge to main" authorization). Then create the signed annotated `v0.1.6`
   tag, publish a GitHub Release, and register the ed25519 signing key
   (`SHA256:xOXGnzSe+yV+WuNI13VbBfVTZstn4diio62sWBZglFU`) on the
   `agenticassets` GitHub account.
2. Provision a fully populated reviewer test account without MFA and write
   the access steps outside Git.
3. Submit Lane A (Anthropic plugin directory) and Lane B (Anthropic
   Connectors Directory) from a claude.ai Team or Enterprise Owner login, or
   Lane A alone from Console. Accept the Anthropic Software Directory Terms.
4. Submit Lane D at `https://cursor.directory/plugins/new` and
   `https://cursor.com/marketplace/publish`; accept the Cursor Publisher
   Terms.
5. Complete OpenAI identity verification under `Agentic Assets`, confirm
   `api.apps.write`, then run Lane C once the application items below ship.
6. Decide whether to publish to the open MCP Registry (optional; secondary
   discovery only).

## Application follow-ups (`agentic-assets-app`)

1. Resolve the conflict on draft PR #1589 or re-cut the `/support` page so
   `https://www.corbis.ai/support` returns 200 signed out; then update the
   support URL in every listing and in the Codex descriptor if a
   `supportURL` field becomes documented.
2. Add an explicit `openWorldHint` to every MCP tool annotation (OpenAI
   requires an explicit value per tool; Anthropic accepts the current
   annotations).
3. Add a route that serves the OpenAI domain-verification token as plain
   text at `/.well-known/openai-apps-challenge` (token supplied by the portal
   at submission time; must return only the token).
4. Optional: advertise client ID metadata document support
   (`client_id_metadata_document_supported: true` with `none` in
   `token_endpoint_auth_methods_supported`) so directory clients stop
   registering a new DCR client per connection.
5. Confirm tool results stay within the claude.ai and Desktop limits
   (150,000 characters, 300 seconds).

## Package follow-ups (this repository)

1. After each listing is live, add a maintenance record with the observed
   card label, install route, client version, and OAuth result per lane, then
   update `README.md` install guidance to reference the directory routes.
2. Promote `v0.1.6` into `Agentic-Assets-Marketplace` only through the signed
   tag and the existing promotion procedure.
3. If any portal requires metadata the descriptors cannot express, record it
   in the closeout rather than adding undocumented fields.

## Not started, by design

- No portal form was opened or submitted (browser extension unavailable).
- No reviewer credentials, tokens, or session data were created or stored.
- No change was made to the private Marketplace snapshot or to `main`.

# Corbis MCP public-directory submission readiness closeout (2026-08-24)

**Branch:** `docs/corbis-directory-submission-readiness`

**Base:** `origin/main` at `34c9494eb474156bec60769806d9c7a06e8af4e1`

**State at this record:** readiness reconciliation, descriptor metadata fixes,
and a paste-ready submission packet. It is not a directory submission, a
directory listing, a source release tag, Marketplace admission, or production
proof. Every platform observation below is dated 2026-08-24 and must be
rechecked before any later submission action.

## Objective

Make the thin Corbis connector discoverable inside the native plugin and
connector directories that Claude Code, Claude Desktop/claude.ai, Codex, and
Cursor users browse in-app, instead of relying on the GitHub repository or the
private `corbis@agentic-assets` Marketplace snapshot.

## One-screen summary

- Every native directory (Anthropic plugin directory, Anthropic Connectors
  Directory, OpenAI universal Plugins Directory, Cursor Marketplace, Cursor
  Directory) is a logged-in portal submission by a founder. None accepts a
  pull request, an email, or an unauthenticated API call, and none can be
  driven from this repository. The Claude-in-Chrome extension was not
  connected in this session, so no portal form was opened or submitted.
- The package and the live endpoint already satisfy the published technical
  criteria that can be checked signed out: OAuth 2.1 with dynamic client
  registration and PKCE S256, protected-resource metadata that matches the
  endpoint, Streamable HTTP, 35 titled tools with `readOnlyHint` or
  `destructiveHint`, tool names at most 25 characters, live privacy, terms,
  and documentation routes, and a public MIT repository that passes
  `claude plugin validate`.
- Three application-side gaps remain for specific lanes: no
  `/.well-known/openai-apps-challenge` route (OpenAI domain verification), no
  `openWorldHint` on any tool (OpenAI asks for an explicit value on every
  tool), and `/support` still 404 because application draft PR #1589 is
  unmerged and now conflicts with `main`.
- This branch adds the documented Codex `privacyPolicyURL` and
  `termsOfServiceURL` interface fields and the documented Cursor `license`
  and `logo` fields, bumps descriptors to `0.1.6`, and extends the static
  validator. The private Marketplace snapshot stays at `0.1.5` until a signed
  tag is promoted.

## Reconciled source and endpoint state

- `Agentic-Assets/corbis-mcp` is PUBLIC with an MIT license. `main` is
  `34c9494eb474156bec60769806d9c7a06e8af4e1`; on `main` all three descriptors
  carry version `0.1.5`, and `CHANGELOG.md` lists `0.1.5` as unreleased. This
  branch moves the descriptors to `0.1.6` (unreleased).
- Annotated tags `v0.1.0`, `v0.1.1`, and `v0.1.2` exist. Each carries an SSH
  signature from the ed25519 key with fingerprint
  `SHA256:xOXGnzSe+yV+WuNI13VbBfVTZstn4diio62sWBZglFU` (the local
  `Agentic-Assets GitHub` key, loaded in the agent). GitHub still reports the
  `v0.1.2` tag as `unknown_key` because that key is not registered as a
  signing key on the `agenticassets` account. No `v0.1.3` through `v0.1.6`
  tag and no GitHub Release exists.
- The private Marketplace `plugins/corbis` snapshot on
  `Agentic-Assets-Marketplace` main `eb08113a6a7a26cfad0c30b144b68e7c61d21a10`
  carries descriptor version `0.1.5`.
- Before this branch's edits: `PYTHONDONTWRITEBYTECODE=1 python3
  tests/validate_package.py` passed (15 tests); `--release` passed (15
  tests); `--smoke` passed with endpoint HTTP 200 and protected-resource
  metadata HTTP 200, without authenticating or invoking tools.
  `claude plugin validate .` (Claude Code 2.1.241) passed with the known root
  `CLAUDE.md` bridge warning; `--strict` fails solely on that warning, and the
  bridge remains required by repository governance. Anthropic's current
  submission guidance states that warnings do not fail validation and that the
  review pipeline runs the same non-strict check.
- Validation of this branch's edited tree is recorded under "Validation of
  this branch" below.
- Local client versions: Claude Code 2.1.241, codex-cli 0.147.0,
  cursor-agent 2026.08.11.

### Live endpoint readback (signed out, 2026-08-24)

- `GET /.well-known/oauth-protected-resource/api/mcp/universal` and the root
  protected-resource document returned HTTP 200 with resource
  `https://www.corbis.ai/api/mcp/universal`, authorization server
  `https://www.corbis.ai/api/mcp`, seven `read:*` scopes, and header bearer
  auth.
- `GET /.well-known/oauth-authorization-server` returned HTTP 200 with
  authorization, token, and dynamic registration endpoints, `code` response
  type, `authorization_code` and `refresh_token` grants, public-client token
  auth (`none`), and PKCE `S256`. The document does not advertise
  `client_id_metadata_document_supported`, so Anthropic and OpenAI clients
  will use dynamic client registration and register a new client per fresh
  connection.
- An unauthenticated `initialize` POST returned HTTP 200 with
  `serverInfo.name` `Corbis MCP Server`, version `2.0.0`, a 512 x 512 PNG icon
  at `https://www.corbis.ai/icons/icon-512x512.png`, and instructions to
  discover tools dynamically through `tools/list`.
- An unauthenticated `tools/list` POST (metadata only; no tool was invoked)
  returned HTTP 200 with 35 tools. Every tool has a `title`; 34 declare
  `readOnlyHint: true`; `confirm_academic_identity` declares
  `readOnlyHint: false` and `destructiveHint: true`; no tool declares
  `openWorldHint`; the longest tool name is 25 characters. Tool families
  observed: paper search and details, literature retrieval and positioning,
  evidence packs, FRED macro series, market and CRE market data, CRE listings,
  comps, and operating data, REIT transaction cap rates, citation export,
  rendering, formatting, and BibTeX verification, dataset search, academic
  identity, research pulse, data freshness, and document retrieval. This is
  the signed-out catalog on one date, not a promise of which tools a given
  account receives.
- `GET /.well-known/mcp/server-card.json` returned HTTP 200 and advertises
  streamable HTTP, OAuth 2 and API-key authentication, the two OAuth metadata
  documents, and documentation at `https://www.corbis.ai/docs/mcp-guide`.
- `GET /.well-known/openai-apps-challenge` returned HTTP 404 (no OpenAI
  domain-verification challenge is deployed, and a remote search of
  `agentic-assets-app` `main` finds no such route).

### Public route readback (signed out, 2026-08-24)

| Route | Result |
| --- | --- |
| `https://www.corbis.ai/privacy` | HTTP 200 |
| `https://www.corbis.ai/terms` | HTTP 200 |
| `https://www.corbis.ai/docs` | HTTP 200 |
| `https://www.corbis.ai/docs/mcp` | HTTP 200 |
| `https://www.corbis.ai/docs/mcp-guide` | HTTP 200 |
| `https://www.corbis.ai/contact` | HTTP 200 |
| `https://www.corbis.ai/support` | HTTP 404 |
| `https://www.corbis.ai/icons/icon-512x512.png` | advertised by the server; 512 x 512 PNG |
| `https://www.agenticassets.ai/privacy` | HTTP 200 |
| `https://www.agenticassets.ai/terms` | HTTP 200 |

Application draft PR `Agentic-Assets/agentic-assets-app#1589`
(`fix/corbis-mcp-directory-readiness`, last updated 2026-08-13) remains OPEN,
unmerged, and reported `CONFLICTING` against `main`
(`e115847e1565f54c38ae4fa093956b8cb3b8f403` on 2026-08-24). It is the change
that adds the public `/support` page. Separate MCP fixes merged on 2026-08-23
(`#1644`, `#1645`, `#1647`, `#1648`) but their deployment state was not read
back from this repository. The support contact used in this package is
`corbis@agenticassets.ai` (`SUPPORT.md`) and the security intake is
`security@agenticassets.ai` (`SECURITY.md`).

### Directory presence readback (2026-08-24)

- `anthropics/claude-plugins-community` marketplace (2,282 plugins) and
  `anthropics/claude-plugins-official` (286 plugins): no `corbis` entry.
- MCP Registry (`registry.modelcontextprotocol.io`): no `corbis` entry.
- Cursor Marketplace public payload (239 listings, 34 of them MCP-only): no
  `corbis` entry.
- OpenAI `openai/plugins` (`openai-curated`, 180 vendored entries): no
  `corbis` entry.

## Platform submission paths (verified 2026-08-24)

Each lane below records the mechanism, the requirements this package already
meets, the requirements that still need a founder or an application change,
and the observable proof that a listing exists. Source URLs were fetched on
2026-08-24; portal pages behind login were not rendered.

### Lane A. Anthropic plugin directory (Claude Code, Cowork, Claude Desktop and claude.ai Customize > Plugins)

- Mechanism: in-product submission portal, no PR path. Team or Enterprise
  Owner: `https://claude.ai/admin-settings/directory/submissions/plugins/new`.
  Individual author through Console: `https://platform.claude.com/plugins/submit`
  (HTTP 200 signed out; the form itself requires login). Guidance:
  `https://claude.com/docs/plugins/submit`.
- Requirements met: public GitHub repository, `claude plugin validate` passes
  (warning only), remote-MCP-only plugin is an accepted shape, OAuth is the
  connection path, support contact and privacy policy exist.
- Outcome shape: accepted plugins are mirrored into
  `anthropics/claude-plugins-community` (read-only mirror, nightly sync,
  automated screening on updates) and install with
  `/plugin install corbis@claude-community`. Inclusion in the curated
  `claude-plugins-official` marketplace is at Anthropic's discretion and has
  no application.
- Founder actions: sign in as an Owner of the Agentic Assets claude.ai
  organization (or Console), submit the repository URL and the packet fields,
  accept the Anthropic Software Directory Terms.
- Proof of listing: a `corbis` row in
  `anthropics/claude-plugins-community/.claude-plugin/marketplace.json` and a
  successful `/plugin install corbis@claude-community` on a clean machine.

### Lane B. Anthropic Connectors Directory (claude.ai, Claude Desktop, mobile, Cowork; Claude Code via `claude mcp add`)

- Mechanism: in-product portal only,
  `https://claude.ai/admin-settings/directory/submissions/new`, available to
  Owners and Primary Owners of a Team or Enterprise organization (Enterprise
  can delegate through a custom role). Escalations:
  `mcp-review@anthropic.com`. Guidance:
  `https://claude.com/docs/connectors/building/submission` and
  `https://claude.com/docs/connectors/building/review-criteria`. The legacy
  `clau.de/mcp-directory-submission` short link now redirects to the portal.
- Portal steps and fields (from the published guidance): Introduction (remote
  servers only); Connection (HTTPS server URL, transport, same URL for every
  user); Tools (synced automatically from the live server, grouped by
  read-only and write annotations); Listing (name at most 100 characters,
  tagline at most 55, description at most 2,000, one to five categories,
  documentation URL, privacy policy URL, support contact, icon, permanent URL
  slug); Use cases; Company; Authentication (OAuth with DCR is supported out
  of the box); Data handling; Test and launch (reviewer test-account
  instructions, confirmation that every tool was exercised); Compliance
  (seven acknowledgments); Review.
- Requirements met by the live endpoint: `title` on every tool and
  `readOnlyHint` or `destructiveHint` where applicable; tool names under 64
  characters; no catch-all HTTP tool observed; Streamable HTTP; OAuth 2.1 with
  DCR and PKCE S256; protected-resource `resource` equal to the registered URL;
  the registered host is `www.corbis.ai` directly, so no cross-host redirect
  drops the `Authorization` header; first-party API on a matching domain;
  public documentation and privacy policy live.
- Requirements needing a founder: a fully populated reviewer test account
  with step-by-step access instructions; confirmation that every tool was run
  end to end (MCP Inspector or a custom connector in Claude) before
  submission; the seven policy acknowledgments; a decision on the permanent
  slug (recommended: `corbis`).
- Advisory application follow-ups (not blockers): Anthropic recommends
  client ID metadata documents over DCR for directory traffic because DCR
  registers a new client on every fresh connection; confirm results stay under
  the 150,000-character and 300-second limits for claude.ai and Desktop.
- Outcome shape: automated policy scan, then a Community listing by default;
  Anthropic may escalate to Verified review. No review SLA is published.
  Listing URL `https://claude.ai/directory/connectors/<slug>`; the same
  catalog serves claude.ai, Cowork, Desktop, mobile, and Claude Code. Tool
  changes do not require resubmission.
- Proof of listing: the directory card visible under Customize > Connectors
  in a signed-in claude.ai account, and `claude mcp add --transport http
  corbis https://www.corbis.ai/api/mcp/universal` completing OAuth on a clean
  machine.

### Lane C. OpenAI universal Plugins Directory (Codex CLI, Codex app, ChatGPT)

- Mechanism: OpenAI Platform portal `https://platform.openai.com/plugins`
  (HTTP 403 signed out), Create plugin, "With MCP", enter the production MCP
  URL, Scan Tools, complete the tabs, Submit for review, then an explicit
  Publish after approval. Guidance:
  `https://developers.openai.com/plugins/deploy/submission`,
  `https://developers.openai.com/plugins/deploy/submission-errors`, and
  `https://developers.openai.com/plugins/deploy/app-review`. There is no PR
  path: `openai/plugins` (the `openai-curated` marketplace shown as "Codex
  official") has pull requests and issues disabled and is hand-committed by
  OpenAI staff. An MCP-only plugin is an explicitly accepted shape, and the
  portal reads the endpoint directly rather than this repository.
- Requirements met: production HTTPS endpoint; OAuth 2.1 with PRM, DCR, and
  PKCE S256; `readOnlyHint` and `destructiveHint` present; website, privacy,
  and terms URLs live; 48 x 48 PNG icon in the package (minimum accepted
  size) and a 512 x 512 PNG served by the application.
- Requirements needing a founder: an OpenAI organization with the
  `api.apps.write` permission and completed individual or business identity
  verification under the exact publisher name `Agentic Assets`; a project
  without EU data residency; a reviewer demo account without MFA, SMS, or
  email confirmation; at least five positive and three negative test cases;
  a demo recording of the main use cases; per-tool annotation justifications;
  policy attestations; a support URL (use `https://www.corbis.ai/contact`
  until `/support` ships).
- Requirements needing an application change: serve the portal-issued token
  as plain text at `https://www.corbis.ai/.well-known/openai-apps-challenge`
  (returns 404 today; the token only exists after the portal issues it), and
  declare an explicit `openWorldHint` on every tool (absent today).
- Outcome shape: review status by email; after approval the plugin is
  discoverable by direct link and name search in the universal directory used
  by ChatGPT and Codex; main-page placement is OpenAI-selected. Whether a
  portal-published plugin is also vendored into the Codex CLI's offline
  `openai-curated` snapshot is not documented; treat that placement as not
  guaranteed. The MCP origin cannot change after publication.
- Proof of listing: the directory listing URL issued by the portal, a
  `codex plugin add corbis` (or `/plugins` browser install) from the universal
  directory on a clean machine, and OAuth completing.
- Fallback today (not public discovery): `codex plugin marketplace add
  Agentic-Assets/Agentic-Assets-Marketplace` then
  `codex plugin add corbis@agentic-assets`, which installs the private
  Marketplace snapshot (`0.1.5`).

### Lane D. Cursor (Customize > Plugins, `/add-plugin`, cursor.directory)

- Two surfaces exist. Official Cursor Marketplace: publisher application at
  `https://cursor.com/marketplace/publish` (login required; fields: owner,
  organization name, kebab-case organization handle, website, contact email,
  absolute logotype URL, description, public GitHub repository URL; posts to
  `/api/marketplace/publish-application`; acceptance of the Publisher Terms
  at `https://cursor.com/marketplace-publisher-terms`, last updated
  2026-05-06). Cursor Directory: `https://cursor.directory/plugins/new`
  (sign in with GitHub or Google, paste the repository URL, automatic
  detection of `.cursor-plugin/plugin.json` and `mcp.json`, automated
  security scan, optional "Verified by Cursor Directory" request). Cursor
  staff wrote on 2026-07-07 that the directory is the intended listing
  surface going forward and that general marketplace submissions were being
  wound down, but the official docs still point at the marketplace form and
  the form still accepts applications. Submit to both.
- Requirements met: MIT license (permissive licenses only); free plugin;
  remote-MCP-only plugins are listed today (34 of 239); manifest `name` is
  kebab-case; `logo` and `license` now declared in `.cursor-plugin/plugin.json`;
  OAuth with DCR needs no static `auth` block; privacy and terms pages live;
  README documents usage.
- Requirements needing a founder: a Cursor login for the marketplace form and
  a GitHub or Google login for the directory; the organization handle
  (recommended `@agentic-assets`); the absolute logotype URL
  (`https://www.corbis.ai/icons/icon-512x512.png`); acceptance of the
  Publisher Terms.
- Unverified: whether a Cursor Directory listing (verified or not) appears in
  Cursor's in-app plugin browser. One publisher reported on the Cursor forum
  that a directory-published plugin did not appear in the in-app search. The
  marketplace pins a commit SHA and every update is manually re-reviewed
  ("request a re-index").
- Proof of listing: a `corbis` entry in the `https://cursor.com/marketplace`
  payload with `PLUGIN_LIFECYCLE_STATE_PUBLIC_LISTED`, `/add-plugin corbis`
  succeeding in Cursor, and OAuth completing.
- Fallback today (not discovery): the install deeplink
  `cursor://anysphere.cursor-deeplink/mcp/install?name=corbis-mcp&config=eyJ1cmwiOiJodHRwczovL3d3dy5jb3JiaXMuYWkvYXBpL21jcC91bml2ZXJzYWwifQ%3D%3D`
  or a manual `mcp.json` entry with the endpoint URL.

### Lane E. MCP Registry (optional; does not surface in Claude, Cursor, or Codex)

- Anthropic states that publishing to the open MCP Registry or
  `modelcontextprotocol/servers` does not surface a server in Claude; Cursor
  and Codex do not consume it either. It feeds the GitHub MCP Registry and VS
  Code's gallery, so it is a secondary discovery channel.
- Mechanism: `mcp-publisher init`, `mcp-publisher login github` (device flow,
  founder browser action) for the `io.github.agentic-assets/*` namespace, or
  a DNS TXT record on `corbis.ai` for `ai.corbis/*`, then
  `mcp-publisher publish`. A remote-only `server.json` needs only name, title,
  description, version, websiteUrl, repository, and a `streamable-http`
  remote. Versions are immutable.
- Not started; listed in the forward queue as optional.

## Submission packet (paste-ready; verify each URL signed out on the day)

- Name: `Corbis`
- Slug or handle: `corbis` (Anthropic slug is permanent); Cursor
  organization handle `@agentic-assets`.
- Tagline (55 max): `Evidence-grounded finance and real estate research`
- Short description (30 max, OpenAI): `Evidence-grounded research`
  (alternate: `Research-grounded finance data`)
- Description (under 2,000 characters):

  Corbis connects your AI workspace to research-grounded finance, real
  estate, and economics intelligence. Search peer-reviewed and industry
  research, retrieve paper details and evidence packs, and export citations
  in APA, MLA, Chicago, or BibTeX. Pull macroeconomic series, metro and
  commercial real estate market indicators, listings, comparables, and
  operating benchmarks, and screen or compare markets directly in
  conversation. Every result carries its source so analysts, investors, and
  academics can stand behind the answer. Corbis is built by finance
  professors at Agentic Assets for private equity, commercial real estate,
  asset management, investment banking, and academic research teams. Connect
  with your Corbis account through OAuth. Tool availability depends on the
  authenticated account and service authorization.

- Categories: Anthropic (pick up to five from the portal list): Financial
  services, Data, Education, Productivity. OpenAI (one): `Education &
  Research` (alternate `Finance` or `Data & Analytics`). Cursor assigns its
  own categories; suggest Research and Finance & Legal.
- Website: `https://www.corbis.ai`
- Documentation: `https://www.corbis.ai/docs/mcp-guide`
- Privacy policy: `https://www.corbis.ai/privacy`
- Terms: `https://www.corbis.ai/terms`
- Support: `https://www.corbis.ai/contact` and `corbis@agenticassets.ai`
  (switch to `https://www.corbis.ai/support` once it is live signed out)
- Security contact: `security@agenticassets.ai`
- Repository: `https://github.com/Agentic-Assets/corbis-mcp`
- Icon: `assets/icon.png` (48 x 48 PNG, approved Corbis Research icon) and
  `https://www.corbis.ai/icons/icon-512x512.png` (512 x 512 PNG) for forms
  that want a larger or absolute logotype URL.
- Developer and company: `Agentic Assets` (Agentic Assets LLC),
  `https://www.agenticassets.ai`; primary contact Dr. Cayman Seagraves,
  `cayman@agenticassets.ai`.
- Connection: `https://www.corbis.ai/api/mcp/universal`, Streamable HTTP,
  every user connects to the same URL.
- Authentication: OAuth 2.1 with dynamic client registration and PKCE S256;
  authorization server metadata at
  `https://www.corbis.ai/.well-known/oauth-authorization-server`; protected
  resource metadata at
  `https://www.corbis.ai/.well-known/oauth-protected-resource/api/mcp/universal`.
- Data access: reads research, market, and dataset content from Corbis's
  own first-party API. One tool (`confirm_academic_identity`) writes a
  confirmation to the user's own account, so declare "reads and writes" if
  the form asks. No health data, no sponsored content, no third-party API
  proxying.
- What users need first: a Corbis account at `https://www.corbis.ai`. Tool
  availability depends on the account's plan and authorization.
- Primary use cases: (1) find and cite peer-reviewed evidence for a memo,
  paper, or investment thesis; (2) pull macro, metro, and commercial real
  estate market data with comparables and benchmarks; (3) format, verify,
  and export citations for research output.
- Starter prompts (128 characters max each): `Find peer-reviewed evidence on
  cap rate compression and summarize the findings with citations.`;
  `Compare office market fundamentals for Miami and Atlanta and flag the key
  risks.`; `Verify these BibTeX entries and export them in APA format.`
- Reviewer test account: founder-provisioned, fully populated, no MFA or
  email confirmation at sign-in, with written steps from account creation
  through OAuth consent to a successful tool call. Never store the
  credentials in this repository.
- OpenAI test cases (draft): positive: search papers on a finance topic and
  return cited results; retrieve details for a returned paper; fetch a FRED
  series by search; compare two metro markets; export citations in BibTeX.
  Negative: request a paper by a malformed identifier (expect a clear
  validation error); request a tool outside the account's authorization
  (expect a permission error, not a fallback); prompt the connector to reveal
  another user's data (expect refusal).

## Founder runbook (ordered)

1. Merge this branch after review (`merge to main` authorization), then
   create and push the signed annotated `v0.1.6` tag and a GitHub Release, and
   register the ed25519 signing key on the `agenticassets` GitHub account so
   the tag shows as verified.
2. Provision the reviewer test account and write the access steps (kept
   outside Git).
3. Lane A: submit the repository at
   `https://claude.ai/admin-settings/directory/submissions/plugins/new` or
   `https://platform.claude.com/plugins/submit`. Record the confirmation.
4. Lane B: submit the connector at
   `https://claude.ai/admin-settings/directory/submissions/new` with the
   packet above. Record the confirmation and the slug.
5. Lane D: submit at `https://cursor.directory/plugins/new` and at
   `https://cursor.com/marketplace/publish`. Record both confirmations.
6. Lane C: in `https://platform.openai.com/plugins`, create the plugin, run
   Scan Tools, copy the domain-verification token, hand it to the
   `agentic-assets-app` change that serves it at
   `/.well-known/openai-apps-challenge`, deploy, verify, record the demo,
   enter test cases, submit. Requires `openWorldHint` on every tool first.
7. Read each listing back signed out and from a clean client install, and
   record the observed card label, install command, and OAuth result per lane
   in a new maintenance record before any public "available in" claim.

## Validation of this branch

Run on this branch's edited tree (macOS host, 2026-08-24):

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py`: 15 tests, OK.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_package.py --release`: 15
  tests, OK.
- `claude plugin validate .` (Claude Code 2.1.241): passed with the single
  root `CLAUDE.md` bridge warning; `--strict` fails only on that warning.
- `--smoke` ran earlier the same day, before the edits (endpoint HTTP 200,
  protected-resource metadata HTTP 200). The edits do not change the endpoint
  reference, so the probe was not repeated.
- The exact commit is recorded in the pull request for this branch.

## Session closeout (2026-08-24)

Branch `docs/corbis-directory-submission-readiness` off `main` at `34c9494`.

Commits:

- `1b35300` fix: add Corbis privacy, terms, license, and logo metadata
- `119f198` docs: record public-directory submission readiness
- the commit that adds this section (decision record only)

State: pushed; draft PR #14 is open against `main`. Merge, the `v0.1.6`
signed tag, Marketplace promotion, and every portal submission remain founder
gates (Linear AGENTIC-2488). Application follow-ups are AGENTIC-2489.

### Decisions and rejected alternatives

- Portal submission was not attempted through a signed-in browser session.
  The Claude-in-Chrome extension reported "not connected" on repeated
  attempts, and using a founder's saved browser profile or credentials is
  outside agent authority. Rejected: driving `agent-browser` against a copied
  Chrome profile.
- No pull request to `openai/plugins` or `anthropics/claude-plugins-community`.
  OpenAI keeps pull requests disabled on its directory repository and vendors
  entries by hand, and the Anthropic community mirror is populated from portal
  submissions. Rejected: opening a speculative PR that would be closed.
- Only documented descriptor fields were added (Codex
  `interface.privacyPolicyURL` and `interface.termsOfServiceURL`; Cursor
  `license` and `logo`). Rejected: adding OpenAI-portal-only values such as
  the 30-character short description to `.codex-plugin/plugin.json`, because
  the Codex manifest schema does not carry them; they live in the packet.
- `openWorldHint` and the `/.well-known/openai-apps-challenge` route were
  routed to `agentic-assets-app` rather than emulated here. The server owns
  tool annotations and public routes; this package never carries a tool
  catalog.
- No Linear repository label was invented for `corbis-mcp`. The gate issue
  carries only `Needs Cayman` and `Human-Signoff`; the app issue carries the
  existing `Agentic-Assets/agentic-assets-app` label.
- Cursor Directory (`cursor.directory/plugins/new`) is the primary Cursor
  lane and the Marketplace publish form is secondary, following the
  2026-07-07 staff statement recorded in Lane D. In-app visibility of
  directory listings is still unverified.

### Deliberately deferred

- The `v0.1.6` signed tag, GitHub Release, and Marketplace promotion wait for
  merge approval.
- `--smoke` was not re-run after the descriptor edits because the endpoint
  reference did not change.
- MCP Registry publication (Lane E) is optional and needs a founder GitHub
  device-flow login.

## Boundaries

- Nothing in this record is a directory submission or listing. Each platform
  lane records a separate submission event, review outcome, and observed
  listing before any public availability claim.
- The repository CLAUDE.md bridge is retained; strict validation remains an
  advisory check, not a release blocker, under current Anthropic guidance.
- Reviewer test-account credentials, portal sign-ins, domain-verification
  deployments, identity verification, terms acceptance, and signing-key
  registration are founder-controlled actions and were not performed by this
  session.
- The signed-out `tools/list` readback is metadata only; no tool was invoked
  and no account was authenticated.

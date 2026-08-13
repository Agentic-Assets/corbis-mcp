# First Corbis MCP source-package plan

**Status:** design and implementation plan, not release authorization

## Objective

Create a minimal, cross-client connector package named **Corbis** that gives a
client one remote-MCP configuration for the production Corbis endpoint. The
production server, not this package, remains authoritative for authentication,
tool discovery, authorization, subscriptions, data, and results.

## Scope boundary

| Own here | Do not own here |
| --- | --- |
| Client descriptors, endpoint configuration, approved brand assets, public setup and support documentation, license/security material, changelog, and tests | Tool code, server transport, OAuth implementation, API clients, private application source, user data, research agents/skills/commands/hooks, data pipelines, or Marketplace catalogs |

The package must remain useful as a connector without implying that it is the
full Corbis Research Plugin or that every account has identical access.

## Target root tree

```text
corbis-mcp/
├── .claude-plugin/
│   └── plugin.json
├── .codex-plugin/
│   └── plugin.json
├── .cursor-plugin/
│   └── plugin.json
├── .mcp.json
├── mcp.json
├── assets/
│   ├── icon.png
│   ├── logo.png
│   └── logo-dark.png
├── docs/
│   └── ...planning and maintainer material...
├── tests/
│   └── manifest-and-endpoint-smoke.<chosen-test-extension>
├── AGENTS.md
├── CHANGELOG.md
├── LICENSE
├── README.md
├── SECURITY.md
└── SUPPORT.md                     # or an approved README support section
```

Only add a file when a supported client, release check, or public user needs
it. A root-level source package is intentional. Do not add a duplicate
`plugin/` subtree merely for a future Marketplace tool.

## Descriptor contract

### Shared invariants

Every descriptor must use the same:

- package ID: `corbis`;
- display name: `Corbis`;
- publisher: `Agentic Assets`;
- release version: one approved plain SemVer value with no drift across
  descriptors;
- repository URL: `https://github.com/Agentic-Assets/corbis-mcp`;
- public home/support/security URLs after they are approved and verified;
- license identifier matching the approved `LICENSE` file; and
- factual, entitlement-aware descriptions.

Do not claim client support that has not been tested. Do not leave temporary
URLs, generated timestamps, boilerplate about a local runtime, or a generic
research-toolkit inventory in the final descriptors.

### MCP configuration

Both `.mcp.json` and `mcp.json` must configure the named server `corbis` as
HTTP at:

```text
https://www.corbis.ai/api/mcp/universal
```

The configuration must contain no query parameters carrying credentials, no
embedded bearer tokens, no client secret, and no local executable. OAuth is the
default client path. If a client needs an alternate credential mechanism later,
document only a service-owner-approved header/environment mechanism and test it
outside version control.

### Client-specific work

- Use the then-current Claude schema and `claude plugin validate --strict` for
  `.claude-plugin/plugin.json`.
- Use the current official Codex plugin-creation and validation workflow for
  `.codex-plugin/plugin.json` and its reference to `.mcp.json`.
- Use Cursor's current closed plugin schema for
  `.cursor-plugin/plugin.json` and its reference to `mcp.json`.
- Keep the files deliberately independent even where their metadata overlaps.
  Do not assume a passing adapter is transferable to another client.

## Public documentation contract

The public README must state what Corbis is, the remote-MCP connection model,
the supported direct installation routes that have actual evidence, OAuth as
the normal authentication path, account-dependent tool availability, and clear
support/security links. It must not describe private app internals or the
Corbis Research workflow package.

Before citing them, browser-verify public support, privacy, terms, and MCP
documentation routes while signed out. A route that redirects to sign-in or
renders a not-found page is not valid submission or support material. The
application candidate previously proposed fixes for public support and MCP
documentation, but no source-package document may rely on them until the
approved deployment is live and independently read back.

Public copy, assets, license, support contact, and launch jurisdictions require
the approvals listed in [the source record](04-source-record.md#open-human-gates).

## Tests and review gates

The initial PR must add portable tests that, at a minimum:

1. Parse every descriptor as its declared data format.
2. Assert shared metadata consistency and release-version consistency.
3. Assert both MCP descriptors name `corbis`, use HTTPS, and exactly use the
   approved endpoint without an embedded credential or query string.
4. Reject placeholder URLs, private repository URLs, local paths, and
   unapproved component references.
5. Confirm every declared local asset and documentation link exists.
6. Confirm the package contains none of the explicitly prohibited categories
   listed below.
7. Keep an endpoint smoke test distinct from static tests. It must avoid
   collecting credentials and must record whether a live network probe ran.

Then run, record, and review:

- the official Claude strict validator;
- the current official Codex validator;
- the applicable Cursor schema validator;
- a secret scan and dependency review;
- a clean direct installation and OAuth flow for the supported direct routes;
- MCP Inspector or equivalent protocol validation against the exact production
  endpoint, including authentication boundaries and representative tools; and
- a focused security and adversarial review.

Do not make a source release tag merely because static files parse.

## Explicit exclusions

The following are out of scope for the first package and must be rejected in
review unless a new approved decision changes the scope:

- application/server source, reverse proxies, database clients, deployment
  configuration, and API keys;
- private Corbis Research skills, agents, commands, hooks, workflows, WRDS
  material, generated indexes, corpora, or research scaffolding;
- credentials, OAuth registration secrets, browser sessions, reviewer accounts,
  tokens, user data, logs, and local caches;
- a hard-coded tool list, tool entitlements, pricing logic, or a claim that
  installation grants access to all tools;
- automated Marketplace synchronization, Marketplace catalog adapters, or
  Marketplace admission artifacts; and
- unreviewed dependencies or a local executable MCP server.

## Implementation phases

### Phase A: revalidate before coding

Read the current source branch and `origin/main`, inspect current platform
schemas and validators, and verify the production endpoint/OAuth metadata
without credentials. Reconcile the pending application readiness PR and its
review state. Record what is observation versus what is an approval.

### Phase B: construct the minimal package

Use the current official scaffold as a starting point, then keep only the
approved files in the target tree. Build common metadata from one reviewed
source within the repository so the three descriptors cannot drift. Do not
write a server implementation.

### Phase C: prove the source package

Run the static tests, client validators, secret/dependency checks, and clean
direct-install/OAuth tests. Capture the source commit, validator versions,
client version/host, test outcome, and any unmet route. Open a reviewable
feature-branch PR.

### Phase D: make a release candidate

After code review and explicit merge/release authorization, publish a signed
annotated tag such as `vX.Y.Z`. Preserve the tag-object SHA, peeled commit SHA,
signature verification, and default-branch reachability. This tag is the only
permitted input to later Marketplace promotion.

### Phase E: hand off to the Marketplace

Follow [the one-way Marketplace contract](02-marketplace-release-contract.md).
The Marketplace implementation has its own policy/profile work and must not
admit or catalog `corbis` before digest-bound client evidence exists.

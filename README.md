<div align="center">

# Corbis MCP

**Connect research-first Corbis to an MCP-compatible AI assistant for
finance, real estate, and economics research.**

[![Remote MCP connector](https://img.shields.io/badge/Corbis-Remote%20MCP-102A43)](https://www.corbis.ai/)
[![Research-first AI](https://img.shields.io/badge/Research-first%20AI-Cited%20answers-167C80)](https://www.corbis.ai/)
[![Source package status](https://img.shields.io/badge/Status-Source%20package%20only-486581)](docs/04-source-record.md)

[corbis.ai](https://www.corbis.ai/) | [What is Corbis](#what-is-corbis) | [This connector](#what-this-connector-is) | [How it works](#how-it-works) | [Source verification](#verify-the-source-package) | [Release status](#release-status)

[![Corbis wordmark](assets/logo.png)](https://www.corbis.ai/)

</div>

---

## What is Corbis

[Corbis](https://www.corbis.ai/) is a research-first AI platform for finance,
real estate, and economics. It gives professionals and researchers cited
answers with sources they can inspect before relying on them.

This repository is not the Corbis application or the private Corbis Research
Plugin. It is the small public-facing connector package that will eventually
let approved MCP clients reach Corbis through one remote endpoint.

## What This Connector Is

Corbis MCP supplies separate configuration descriptors for Claude Code, Codex,
and Cursor. Each descriptor identifies the same remote endpoint:

```text
https://www.corbis.ai/api/mcp/universal
```

The connector has separate human-facing and technical identities:

| Purpose | Value |
| --- | --- |
| Human-facing connector label | `Corbis` |
| Package identifier | `corbis` |
| Technical MCP server identifier | `corbis-mcp` |
| Marketplace selector | `corbis@agentic-assets` |

Every descriptor uses the stable `corbis-mcp` server identifier under its
`mcpServers` key. It is intentionally distinct from the package name
`corbis` and the Marketplace selector, so it does not collide with the
separate Corbis Research MCP configuration. Claude and Codex expose supported
plugin display-name fields set to `Corbis`. Their MCP server maps, and Cursor's
current MCP configuration, do not provide a supported per-server display-label
field. A client that displays the map key in server settings may therefore
show `corbis-mcp`; this package must not add an undocumented field or rename
the key to recreate the known collision.

OAuth is the normal authentication path. The Corbis service, not this package,
decides which tools an authenticated account may use and enforces authorization
for each request.

The connector does not contain a local server, research workflows, tool
catalog, API key, client secret, user data, or private application code.

## How It Works

1. An MCP client reads its client-specific Corbis descriptor.
2. The client connects to the fixed HTTPS Corbis endpoint and follows the
   service-controlled authentication path.
3. Corbis returns only the tools and data authorized for that account.

That separation matters: a valid descriptor or responsive endpoint does not
prove that a particular client has accepted the package, completed OAuth, or
received access to every Corbis capability.

## What Is Included

| Component | Purpose |
| --- | --- |
| `.claude-plugin/plugin.json` | Claude Code descriptor |
| `.codex-plugin/plugin.json` and `.mcp.json` | Codex descriptor and remote MCP configuration |
| `.cursor-plugin/plugin.json` and `mcp.json` | Cursor descriptor and remote MCP configuration |
| `assets/` | Candidate Corbis icon and wordmark assets |
| `tests/validate_package.py` | Static package, release-material, and opt-in endpoint checks |

## Support and Security

For help, contact [corbis@agenticassets.ai](mailto:corbis@agenticassets.ai).
For private vulnerability reporting, follow [SECURITY.md](SECURITY.md). Do not
send credentials, tokens, or client data to either route.

## Connection Status

The signed `v0.1.0` source tag remains a historical snapshot, but its Codex
install resolved to the separate Corbis Research configuration because both
used the `corbis` server identifier. The signed `v0.1.1` tag corrects that
collision by using `corbis-mcp`; its tag object
`ff16d89bf37f291cd643711233ed255f934dc446` points to source commit
`3fb5b4659ed971f409c0d70135d654f21da4db08` on `main`.

The `v0.1.2` source tag is annotated and peels to
`d96a9c7520ab3d572e5510e9cf5a257a444df21f`. Its SSH signature could not be
trusted-verified on 2026-08-16 because the signing key was unknown. Neither
the `v0.1.1` nor the `v0.1.2` tag proves that any native client accepted the
connector. No Marketplace admission or public-directory listing is claimed.

For the full Corbis research experience, visit [corbis.ai](https://www.corbis.ai/).
The private Corbis Research Plugin is a separate product and is intentionally
not bundled here.

## Verify the Source Package

Run the static contract locally:

```sh
python3 tests/validate_package.py
```

The release-material gate verifies regular, non-empty public license, security,
support, and PNG brand assets. It correctly fails until every approved public
material exists:

```sh
python3 tests/validate_package.py --release
```

The separate endpoint probe is opt-in:

```sh
python3 tests/validate_package.py --smoke
```

It checks anonymous endpoint and protected-resource metadata availability only.
It does not authenticate or invoke tools.

## Release Status

The source package includes concise license, security, and support materials.
The `v0.1.2` source snapshot was promoted into an immutable Marketplace
payload, but that promotion does not establish client acceptance, admission,
attestation, production readback, or public publication. A future source
release must be reviewed, signed with a trusted key, and tested in each
supported client. That client evidence must include the actual connector label
shown in settings, not only the Marketplace or plugin card title.

See the [source record](docs/04-source-record.md),
[security and acceptance plan](docs/03-security-and-acceptance.md), and
[Marketplace release contract](docs/02-marketplace-release-contract.md) for
the exact boundaries.

---

<div align="center">

**Built by [Corbis](https://www.corbis.ai/) from [Agentic Assets](https://www.agenticassets.ai/)**

[corbis.ai](https://www.corbis.ai/) | [Source record](docs/04-source-record.md) | [Security and acceptance](docs/03-security-and-acceptance.md) | [Marketplace contract](docs/02-marketplace-release-contract.md)

</div>

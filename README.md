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

Every descriptor uses the stable `corbis-mcp` server identifier under its
`mcpServers` key. It is intentionally distinct from the package name
`corbis` and the future Marketplace selector `corbis@agentic-assets`, so it
does not collide with the separate Corbis Research MCP configuration.

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
used the `corbis` server identifier. This `0.1.1` source candidate changes the
thin connector to `corbis-mcp`; it has not yet been tagged or accepted by any
client. No Marketplace admission or public-directory listing exists. Do not
treat this repository as proof that any client has installed or accepted
Corbis MCP.

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

The source package now includes concise license, security, and support
materials. Candidate public-asset approval, a reviewed signed source tag,
independent direct-client acceptance, Marketplace promotion, digest-bound
evidence, admission, externally trusted attestation, production readback, and
public publication are all separate steps.

See the [source record](docs/04-source-record.md),
[security and acceptance plan](docs/03-security-and-acceptance.md), and
[Marketplace release contract](docs/02-marketplace-release-contract.md) for
the exact boundaries.

---

<div align="center">

**Built by [Corbis](https://www.corbis.ai/) from [Agentic Assets](https://www.agenticassets.ai/)**

[corbis.ai](https://www.corbis.ai/) | [Source record](docs/04-source-record.md) | [Security and acceptance](docs/03-security-and-acceptance.md) | [Marketplace contract](docs/02-marketplace-release-contract.md)

</div>

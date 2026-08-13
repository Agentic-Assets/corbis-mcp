# Corbis MCP

Canonical source for the minimal Corbis remote-MCP connector.

The connector will point supported clients to the Corbis production MCP
endpoint. It will not contain the Corbis service implementation, research
workflows, credentials, or a fixed copy of the server's tool catalog. Tool
availability remains governed by the authenticated account and the production
service.

The repository contains the initial client descriptors and portable static
checks. It is not a released plugin and must not be presented as a supported
direct installation route. The intended private Marketplace package is
`corbis@agentic-assets`, promoted only as an immutable snapshot of a reviewed
signed source release. Marketplace availability, direct-client acceptance,
public visibility, and directory publication are separate milestones.

## Intended endpoint

`https://www.corbis.ai/api/mcp/universal`

OAuth is the intended default authentication flow. No API key, bearer token,
or client secret belongs in this repository or in an endpoint URL.

## Current package boundary

- Claude Code uses `.claude-plugin/plugin.json` and its inline Claude-specific
  remote configuration.
- Codex uses `.codex-plugin/plugin.json` and the Codex-specific `mcp_servers`
  configuration in `.mcp.json`.
- Cursor uses `.cursor-plugin/plugin.json` and `mcp.json`.

The descriptors contain no tool list, credentials, local executable, or OAuth
client registration. Tool availability and authorization remain service-side
and account-dependent.

Run the static package contract locally with:

```sh
python3 tests/validate_package.py
```

The separate release-readiness gate adds the founder-approved public license,
security, support, and brand-asset requirements. It intentionally fails until
those decisions and materials exist:

```sh
python3 tests/validate_package.py --release
```

The separately opt-in endpoint probe is:

```sh
python3 tests/validate_package.py --smoke
```

It checks only anonymous endpoint and protected-resource metadata availability.
It neither authenticates nor invokes a tool.

## Project status

No source release tag, Marketplace payload, client-acceptance record, or
public-directory listing exists. The release-readiness gate is currently
expected to fail because final public license, support, security, and brand
asset material remains subject to the explicit gates in the
[source record](docs/04-source-record.md).

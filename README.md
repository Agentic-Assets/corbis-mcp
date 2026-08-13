# Corbis MCP

Canonical source for the minimal Corbis remote-MCP connector.

The connector will point supported clients to the Corbis production MCP
endpoint. It will not contain the Corbis service implementation, research
workflows, credentials, or a fixed copy of the server's tool catalog. Tool
availability remains governed by the authenticated account and the production
service.

This repository is currently a build handoff, not a released plugin. The
implementation agent should begin with [the source handoff](docs/00-start-here.md).
The intended private Marketplace package is `corbis@agentic-assets`, promoted
only as an immutable snapshot of a reviewed signed source release. Marketplace
availability, direct-client acceptance, public visibility, and directory
publication are separate milestones.

## Intended endpoint

`https://www.corbis.ai/api/mcp/universal`

OAuth is the intended default authentication flow. No API key, bearer token,
or client secret belongs in this repository or in an endpoint URL.

## Project status

No installable source package, Marketplace payload, client-acceptance record,
or public-directory listing exists yet. See [the source record](docs/04-source-record.md)
for the exact boundaries and revalidation requirements.

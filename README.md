# Corbis plugin

Corbis is a research workspace for finance, real estate, and economics from Agentic Assets. This plugin connects a compatible AI workspace to the Corbis research connector and adds three skills that turn Corbis tools into cited research workflows. The skills instruct the model to cite only papers and data that Corbis returns in the conversation or that you supply, so each claim can be traced to a source.

## Skills

- **literature-review** (`/corbis:literature-review`): cited literature reviews, "what does research say about" questions, claim checks against published papers, and positioning a paper against related work.
- **citations** (`/corbis:citations`): verify and correct BibTeX, flag references that cannot be matched, format citations in APA, MLA, Chicago, or Harvard style, and export BibTeX, Markdown, or JSON.
- **paper-review** (`/corbis:paper-review`): referee-style reports and technical audits of a manuscript you provide, with literature positioning and missing-reference checks.

Narrow questions get a quick answer that uses at most five Corbis tool calls, followed by an offer to run the full workflow. Ask for a full review, report, or audit to run the complete procedure.

## Connect

This plugin ships the same Corbis connector and skills to three platforms. Skills only change how a client that reads `SKILL.md` files, such as Claude Code, claude.ai, Cowork, Codex, or Cursor, guides a research task; the connector and its tools work in every client that supports remote MCP.

- **Claude (claude.ai and Cowork):** once the plugin is listed in the Claude directory, install it, open its Connectors tab, connect Corbis, and sign in with your Corbis account.
- **Claude Code:** install the plugin, run `/mcp`, choose `corbis`, and complete the browser sign-in. If you prefer a key to browser sign-in, create a personal MCP API key in Corbis Settings and follow the Claude Code steps in the [Corbis MCP guide](https://www.corbis.ai/docs/mcp-guide). Use this instead of the plugin's connection, not alongside it. Send the key only in an `Authorization` header, never in the URL, and keep it out of shell history and shared files.
- **Codex:** install the plugin from a configured Codex marketplace, or point Codex at this repository directly. Codex reads the connector from `.codex-plugin/plugin.json` and completes the same OAuth sign-in as Claude Code.
- **Cursor:** install the plugin from the Cursor marketplace, or add it from this repository under Cursor Settings, MCP. Cursor is an OAuth-only client for this connector; sign in when prompted.
- **ChatGPT chat:** ChatGPT chat does not read plugin skills. Connect the Corbis MCP connector directly from ChatGPT's connector settings to reach the same tools; the literature-review, citations, and paper-review skills apply only to clients that read `SKILL.md` files.

If the Corbis connector is already added another way, such as a custom connector or a manual server entry, the client sees the same tools twice. Keep one connection: disable the extra entry from that client's MCP or connector settings.

## Plans

Every skill works on standard Corbis plans. A few optional steps (managed literature synthesis, scored claim verification, and scored referee and audit evaluations) use premium tools that are available on enterprise plans. Without them, the skill says so once and finishes with the standard tools. Tool calls use Corbis credits. Current plans and credit costs: https://www.corbis.ai/pricing

## Data and privacy

The plugin is instructions and connector metadata only: it contains no hooks, scripts, or local servers, and its one connection is the Corbis research connector at www.corbis.ai. It stores nothing. When a skill runs, your research questions, the manuscript excerpts or summaries a tool call needs, and the BibTeX entries you ask it to verify are sent to your Corbis account at www.corbis.ai. Privacy policy: https://www.corbis.ai/privacy

## Scope and limits

Corbis is strongest in finance, real estate, economics, and adjacent business research. Outputs are research aids: check the cited sources before relying on them, and treat the results as inputs to your own judgment, not as investment, legal, or tax advice.

## Support and license

Support: corbis@agenticassets.ai. To report a security issue privately, follow [SECURITY.md](SECURITY.md).

The plugin files in this repository are MIT licensed. The Corbis service is proprietary and governed by its terms: https://www.corbis.ai/terms

## Source

Agentic Assets publishes this repository from its internal source, and each release replaces its contents. To report a problem or suggest a change, open an issue here or email corbis@agenticassets.ai; changes are made in the source and arrive in the next release.

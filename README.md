# Corbis plugin

Corbis is a research workspace for finance, real estate, and economics from Agentic Assets. This plugin connects a compatible AI workspace to the Corbis research connector and adds skills that turn Corbis tools into cited research workflows. Compatible OpenAI hosts can also open a research workspace from the sidebar or beside a conversation, search papers, inspect sources, and export citations. The skills instruct the model to cite only papers and data that Corbis returns in the conversation or that you supply, so each claim can be traced to a source.

## Skills

- **onboarding** (`/corbis:onboarding` where the host exposes skill commands): connect Corbis, inspect a first paper, and choose a research workflow.
- **literature-review** (`/corbis:literature-review`): cited literature reviews, "what does research say about" questions, claim checks against published papers, and positioning a paper against related work.
- **citations** (`/corbis:citations`): verify and correct BibTeX, flag references that cannot be matched, format citations in APA, MLA, Chicago, or Harvard style, and export BibTeX, Markdown, or JSON.
- **paper-review** (`/corbis:paper-review`): referee-style reports and technical audits of a manuscript you provide, with literature positioning and missing-reference checks.

Narrow questions get a quick answer that uses at most five Corbis tool calls, followed by an offer to run the full workflow. Ask for a full review, report, or audit to run the complete procedure.

## Connect

This plugin packages the same Corbis connector and skills for Claude, Codex, Cursor, and OpenAI plugin hosts. Skill loading and native UI depend on the host. Ordinary Corbis tools remain available through compatible remote MCP connections.

- **Claude (claude.ai and Cowork):** once the plugin is listed in the Claude directory, install it, open its Connectors tab, connect Corbis, and sign in with your Corbis account.
- **Claude Code:** install the plugin, run `/mcp`, choose `corbis`, and complete the browser sign-in. If you prefer a key to browser sign-in, create a personal MCP API key in Corbis Settings and follow the Claude Code steps in the [Corbis MCP guide](https://www.corbis.ai/docs/mcp-guide). Use this instead of the plugin's connection, not alongside it. Send the key only in an `Authorization` header, never in the URL, and keep it out of shell history and shared files.
- **Codex:** install the plugin from a configured Codex marketplace, or point Codex at this repository directly. Codex reads the connector from `.codex-plugin/plugin.json` and completes the same OAuth sign-in as Claude Code.
- **Cursor:** install the plugin from the Cursor marketplace, or add it from this repository under Cursor Settings, MCP. Cursor is an OAuth-only client for this connector; sign in when prompted.
- **OpenAI plugin hosts:** install the portable Corbis plugin from your host's available plugin source, then connect the Corbis account when prompted. On supported hosts, open Corbis from the sidebar or conversation panel. Paper mentions depend on desktop host support. Availability differs by host, plan, and workspace policy; see the [OpenAI extensions guide](https://developers.openai.com/plugins/build/extensions).
- **A direct ChatGPT MCP connection:** reaches Corbis tools without proving the packaged skills or native entrypoints are installed. Use the complete plugin for hosts that support bundled skills.

If the Corbis connector is already added another way, such as a custom connector or a manual server entry, the client sees the same tools twice. Keep one connection: disable the extra entry from that client's MCP or connector settings.

## Plans

Every skill works on standard Corbis plans. A few optional steps (managed literature synthesis, scored claim verification, and scored referee and audit evaluations) use premium tools that are available on enterprise plans. Without them, the skill says so once and finishes with the standard tools. Tool calls use Corbis credits. Current plans and credit costs: https://www.corbis.ai/pricing

## Data and privacy

The package contains instructions and connector metadata. It runs no hooks, scripts, or local servers. The research workspace is served by the Corbis connector at www.corbis.ai and uses that connection for research calls. Research questions, manuscript excerpts or summaries a tool call needs, and BibTeX entries you ask it to verify are sent to your Corbis account. Workspace preferences apply to the current session; account preferences remain in [Corbis Settings](https://www.corbis.ai/settings). Privacy policy: https://www.corbis.ai/privacy

Paper selections stay in the workspace until you choose **Compare in conversation** to add source context and request a comparison. Search results and metadata do not establish that a claim is supported by the paper's full text. Native plugin settings and file editing are not included.

## Scope and limits

Corbis is strongest in finance, real estate, economics, and adjacent business research. Outputs are research aids: check the cited sources before relying on them, and treat the results as inputs to your own judgment, not as investment, legal, or tax advice.

## Support and license

Support: corbis@agenticassets.ai. To report a security issue privately, follow [SECURITY.md](SECURITY.md).

The plugin files in this repository are MIT licensed. The Corbis service is proprietary and governed by its terms: https://www.corbis.ai/terms

## Source

Agentic Assets publishes this repository from its internal source, and each release replaces its contents. To report a problem or suggest a change, open an issue here or email corbis@agenticassets.ai; changes are made in the source and arrive in the next release.

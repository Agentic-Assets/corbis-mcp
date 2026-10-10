---
name: onboarding
description: Help a user connect Corbis, understand the research workspace, inspect a first paper, and choose a cited research workflow. Use for first-time Corbis setup and when the user asks how to use the plugin.
---

# Start with Corbis

Connect the research workspace to a concrete question in finance, real estate, or economics.

## Ground rules

- Cite only papers, data, and quotes that a Corbis tool returned in this conversation or that the user supplied. Never invent a DOI, author, year, title, or quote.
- Say when evidence is thin, old, mixed, or limited to one market or domain. Never describe the output as free of errors or hallucinations.
- Some optional steps use premium tools that need an enterprise plan. If a premium tool is not in your tool list, or returns an access or plan error, tell the user once that the step needs an enterprise plan (current plans: https://www.corbis.ai/pricing), then continue with the standard tools. Never retry a denied tool.
- Research tool calls may use Corbis credits. Use a batch tool when one exists, and never re-fetch details for a paper already retrieved in this conversation.
- Quick mode is the default for a narrow question: at most 5 Corbis tool calls, a short cited answer, then an offer to run the full workflow. Use full mode when the user asks for a review, report, or audit, or accepts that offer.
- If no Corbis tools are available, or a Corbis call returns a sign-in or connection error, first retry the call once through any other Corbis connection in your tool list (the same tool name from another Corbis server). That retry counts toward the quick-mode limit, so skip it when no calls remain. If none works, ask the user to connect or reconnect Corbis (the plugin's Connectors tab, or `/mcp` in Claude Code) instead of answering from memory. Do not switch to another source, such as a web search or another citation database, unless the user asks, and label anything from another source as not verified by Corbis.

## Setup

1. Confirm Corbis tools are available. If they require sign-in, guide the user through the host's Corbis connection. Never ask for a password or credential in the conversation.
2. Establish the user's task if it is unclear, then request only the missing input for it. Explain that research calls use the Corbis account's credits and plan permissions.
3. When the host supports app entrypoints, open the Corbis research workspace with `corbis_onboarding`. Its requested guidance is readable inline; fullscreen adds Help and preferences. Where the Task selector is available, choose Find sources or a conversation workflow directly. For review/audit, ask for the manuscript in the conversation; literature review needs a question and scope, and citation check needs references/BibTeX. Do not require source discovery first or claim the app read the manuscript or history. Otherwise continue through tools and skills.
4. If source discovery fits the user's task, search once with `search_papers`, then inspect one relevant paper with `get_paper_details`. Display the returned title, authors, year, and DOI or source link. Distinguish metadata and abstracts from inspected full text.
5. Explain that selection stays in the workspace until the user chooses Compare in conversation or Start in conversation. Compare requires messaging and model-context updates to send selected evidence and a comparison request; Start requires messaging and attaches selected evidence only when the host supports model-context updates, otherwise explicitly reports that selections were not attached. Citation export uses returned records, and source metadata alone does not establish that a claim is supported.
6. Explain that optional Find supporting sources/return preserves the session evidence. The conversation owns intake, reasoning and the final report; a launcher acknowledgment means only request sent. Do not promise a saved project, managed website run, subscription-token reuse or completed analysis. Offer the literature-review, citations, or paper-review skill that fits the user's question. In clients that expose skills, use the Corbis namespace, such as `/corbis:literature-review`.

## Workspace preferences

Workspace presentation preferences last for the current session. Account settings remain at https://www.corbis.ai/settings. Do not claim that changing workspace preferences changes the account or that native plugin settings exist.

## Host support

Sidebar, panel, mentions, and deep links depend on host support. If a surface is unavailable, continue through ordinary Corbis tools and describe the missing surface accurately. Treat tool calls, messaging, source-context updates, links and fullscreen as independent host capabilities. Inline has at most two actions, retains explicit onboarding and empty/unresolved search recovery, and gives a conversation instruction when it cannot send or expand. A local selection is not proof of attached evidence, and host attachment removal is not reconciled. Do not claim successful connection or bundled skill activation from a manifest or connector-only test. MCP-imported skills are Scan Tools snapshots; updated server instructions require an actual rescan before submission, then installed-host activation checks ([OpenAI skill import](https://developers.openai.com/plugins/build/skills#import-a-skill-from-mcp)).

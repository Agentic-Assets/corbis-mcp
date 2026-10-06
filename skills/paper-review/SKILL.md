---
name: paper-review
description: Use for any request to review, critique, or give feedback on a research paper, draft, or manuscript in finance, real estate, economics, or urban studies, including quick feedback on its biggest problems or weaknesses, a referee report, a pre-submission check, or a technical audit. Produces referee-style reviews with literature positioning and reference checks from the Corbis research connector.
---

# Paper review

Review a manuscript the user provides, the way a careful referee would, and ground literature and reference findings in Corbis sources.

## Ground rules

- Cite only papers, data, and quotes that a Corbis tool returned in this conversation or that the user supplied. Never invent a DOI, author, year, title, or quote.
- Say when evidence is thin, old, mixed, or limited to one market or domain. Never describe the output as free of errors or hallucinations.
- Some optional steps use premium tools that need an enterprise plan. If a premium tool is not in your tool list, or returns an access or plan error, tell the user once that the step needs an enterprise plan (current plans: https://www.corbis.ai/pricing), then continue with the standard tools. Never retry a denied tool.
- Research tool calls may use Corbis credits. Use a batch tool when one exists, and never re-fetch details for a paper already retrieved in this conversation.
- Quick mode is the default for a narrow question: at most 5 Corbis tool calls, a short cited answer, then an offer to run the full workflow. Use full mode when the user asks for a review, report, or audit, or accepts that offer.
- If no Corbis tools are available, or a Corbis call returns a sign-in or connection error, first retry the call once through any other Corbis connection in your tool list (the same tool name from another Corbis server). That retry counts toward the quick-mode limit, so skip it when no calls remain. If none works, ask the user to connect or reconnect Corbis (the plugin's Connectors tab, or `/mcp` in Claude Code) instead of answering from memory. Do not switch to another source, such as a web search or another citation database, unless the user asks, and label anything from another source as not verified by Corbis.

## Before you start

- You need the manuscript. If none is attached, ask for it. Never review from a title or abstract alone and present it as a paper review.
- Pick the review type from the request:
  - **Referee report:** overall assessment, recommendation, must-address issues, and additional comments.
  - **Technical audit:** specific technical findings, each with an exact quote from the manuscript.
  - Ask only if the request fits both.
- Send Corbis short search queries and summaries, not the full manuscript text.

## Quick (a request for fast feedback, or top issues)

1. Read the manuscript.
2. Report the five most important issues. For each: location (section, page, table, or equation), the problem, why it matters, and a concrete fix. For a technical audit, include the exact quote.
3. Corbis calls are optional here (at most 5). Use one `literature_retrieve` call only if an issue depends on related work.
4. Offer the full review.

## Full review

If your client can read MCP resources, read `docs://workflow-packs/referee-report` (referee report) or `docs://workflow-packs/technical-audit` (technical audit) first; use its phases and contracts, and do not create local files or subagents. Otherwise follow `references/referee-report-phases.md` or `references/technical-audit-phases.md`.

Evidence tools during the phases:

- Related and missing literature: `literature_retrieve` or `search_papers` with short queries built from the research question, then `get_paper_details_batch` on the papers you keep, at most 25 IDs per call.
- Bibliography health (technical audit): `verify_bibtex` on the manuscript's references when the user supplies BibTeX.
- Reference list for papers you cite in the report: `render_citations`.

Deliver the report in the template from the phase reference.

## Scored evaluation (enterprise upgrade)

After the local report, on enterprise plans:

- Referee report: call `referee_report_evaluate` with the summary contract in `references/referee-report-phases.md`.
- Technical audit: call `technical_audit_evaluate` with the findings contract in `references/technical-audit-phases.md`.

If the tool is unavailable or denied, deliver the local report labeled "Local review" and note once that the scored evaluation needs an enterprise plan.

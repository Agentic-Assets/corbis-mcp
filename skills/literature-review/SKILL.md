---
name: literature-review
description: Cited literature reviews, claim checks, and paper positioning in finance, real estate, and economics using the Corbis research connector. Use when the user asks for a literature review, asks what research says about a topic, wants to find papers on a question, asks whether a claim is supported by research, asks where their paper fits in the literature, or asks about research gaps.
---

# Literature review

Answer research questions with papers that Corbis retrieves, and keep every claim traceable to a returned source.

## Ground rules

- Cite only papers, data, and quotes that a Corbis tool returned in this conversation or that the user supplied. Never invent a DOI, author, year, title, or quote.
- Say when evidence is thin, old, mixed, or limited to one market or domain. Never describe the output as free of errors or hallucinations.
- Some optional steps use premium tools that need an enterprise plan. If a premium tool is not in your tool list, or returns an access or plan error, tell the user once that the step needs an enterprise plan (current plans: https://www.corbis.ai/pricing), then continue with the standard tools. Never retry a denied tool.
- Research tool calls may use Corbis credits. Use a batch tool when one exists, and never re-fetch details for a paper already retrieved in this conversation.
- Quick mode is the default for a narrow question: at most 5 Corbis tool calls, a short cited answer, then an offer to run the full workflow. Use full mode when the user asks for a review, report, or audit, or accepts that offer.
- If no Corbis tools are available, or a Corbis call returns a sign-in or connection error, first retry the call once through any other Corbis connection in your tool list (the same tool name from another Corbis server). That retry counts toward the quick-mode limit, so skip it when no calls remain. If none works, ask the user to connect or reconnect Corbis (the plugin's Connectors tab, or `/mcp` in Claude Code) instead of answering from memory. Do not switch to another source, such as a web search or another citation database, unless the user asks, and label anything from another source as not verified by Corbis.

## Choose the task

- **Research question or review:** follow Quick or Full below.
- **"Is this claim supported?":** follow Claim check.
- **"Where does my paper fit?" or "What are the gaps?":** follow Positioning.

## Quick (narrow question)

1. Call `literature_retrieve` with the question as `researchQuestion` and a low `perQueryLimit`; set `includeAbstracts` if you expect to need abstracts. Pass a journal constraint as `journalNames` and a year window as `minYear` and `maxYear`, and never drop a constraint to widen results. The tool has no field filter: state a field or market constraint in `researchQuestion` and set aside returned papers outside it.
2. If the returned metadata and any requested abstract snippets are not enough, call `get_paper_details_batch` once on the three to eight most relevant papers.
3. Answer in a few short paragraphs with author-year citations, then list the sources (authors, year, title, journal, DOI or link exactly as returned).
4. Offer the full literature review.

## Full review

If your client can read MCP resources, read `docs://workflow-packs/literature-search` first and follow it where it adds detail: use its phases and contracts, and do not create local files or subagents.

1. Restate the question, field, time window, and constraints. Ask one clarifying question only if the scope is ambiguous enough to change the search.
2. Call `literature_retrieve` once per distinct sub-question (usually one to three calls). Do not re-run it with paraphrases of the same query.
3. Call `get_paper_details_batch` on the papers you keep, at most 25 IDs per call; split a larger set into batches.
4. When the question maps to specific journals, call `top_cited_articles` once for field context.
5. Write the review using `references/output-format.md`.
6. If the user wants the references as a file, call `export_citations` (BibTeX, Markdown, or JSON). For a named citation style (APA, MLA, Chicago, or Harvard), call `format_citation` with that style using the metadata already returned by `get_paper_details_batch`; say that formatting does not re-verify it. For a Markdown or BibTeX reference list instead of a named style, use `render_citations`.

Managed synthesis upgrade: if the user asks Corbis to write the synthesis itself, `literature_search` can replace steps 2 to 5 on enterprise plans; if it is unavailable or denied, run the steps above. When `literature_search` does run, call `get_paper_details_batch` before step 6 on the papers you cite whose full metadata it did not return, at most 25 IDs per call.

## Claim check

1. Call `evidence_pack` with the claim, plus any paper IDs already retrieved in this conversation.
2. `evidence_pack` returns abstract-level evidence, not a verdict. Report which returned papers appear to bear on the claim and in which direction, labeled as abstract-level leads, or say the evidence is insufficient. Do not call the claim supported or contradicted unless you inspected the relevant paper with `get_paper_details_batch` (or the user supplied its text); otherwise say that confirming it needs a closer read. Cite each paper you rely on and quote only text the tool returned.
3. Scored verification upgrade: on enterprise plans, `claim_verification` gives a scored verdict. Offer it only after the Tier 1 answer, and follow the ground rules if it is unavailable or denied.

## Positioning

1. Ask for the paper's abstract if the user has not supplied one, or condense it into a contribution statement of a few sentences: `literature_positioning`'s input has a short length cap.
2. Call `literature_positioning` with that text to find the closest papers. Its results are candidate positioning hints, not verified distinctions: inspect the closest papers with `get_paper_details_batch` before stating how the contribution differs.
3. For gaps and open questions, call `research_opportunity_map` on the topic.
4. Report the closest papers, the claimed difference, and where the difference is weak. Label any difference you did not check against an inspected paper as an unverified candidate. `research_opportunity_map` returns candidate leads only: present its gaps as unverified candidates, or confirm the ones that matter with `literature_retrieve` or `get_paper_details_batch` before calling a gap supported. Mark any gap you infer beyond the returned evidence as your own judgment.

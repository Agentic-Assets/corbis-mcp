---
name: citations
description: Use for academic citation requests, including citing or formatting a paper or article in APA, MLA, Chicago, or Harvard style (even a single one), fixing or checking BibTeX, verifying references or a bibliography, auditing a .bib file, or exporting citations as BibTeX, Markdown, or JSON. Verifies, corrects, formats, and exports references with the Corbis research connector.
---

# Citations

Check references against the Corbis paper index and format them without adding anything the tools did not return.

## Ground rules

- Cite only papers, data, and quotes that a Corbis tool returned in this conversation or that the user supplied. Never invent a DOI, author, year, title, or quote.
- Say when evidence is thin, old, mixed, or limited to one market or domain. Never describe the output as free of errors or hallucinations.
- Some optional steps use premium tools that need an enterprise plan. If a premium tool is not in your tool list, or returns an access or plan error, tell the user once that the step needs an enterprise plan (current plans: https://www.corbis.ai/pricing), then continue with the standard tools. Never retry a denied tool.
- Each Corbis tool call uses credits. Use a batch tool when one exists, and never re-fetch details for a paper already retrieved in this conversation.
- Quick mode is the default for a narrow question: at most 5 Corbis tool calls, a short cited answer, then an offer to run the full workflow. Use full mode when the user asks for a review, report, or audit, or accepts that offer.
- If no Corbis tools are available, or a Corbis call returns a sign-in or connection error, first retry the call once through any other Corbis connection in your tool list (the same tool name from another Corbis server). That retry counts toward the quick-mode limit, so skip it when no calls remain. If none works, ask the user to connect or reconnect Corbis (the plugin's Connectors tab, or `/mcp` in Claude Code) instead of answering from memory. Do not switch to another source, such as a web search or another citation database, unless the user asks, and label anything from another source as not verified by Corbis.

## Quick: verify BibTeX

1. Take the BibTeX the user pasted or uploaded. If they gave formatted references instead, ask whether to convert them to BibTeX entries first, and convert only the fields they wrote.
2. Call `verify_bibtex`, setting `maxEntries` to the number of entries you have, up to the tool's maximum. A bibliography that needs more than one call to cover, staying within 5 total Corbis tool calls, can split across calls in quick mode; a bibliography that needs more than 5 calls does not fit quick mode, so say so and offer full mode instead.
3. Compare the tool's total entry count against how many it actually checked, then report every entry in one of four groups:
   - **Matched:** the entry agrees with the index.
   - **Corrected:** list each changed field as old value and new value. An `author` correction is only a first-author surname hint, not a full author list: keep the user's `author` field and flag the mismatch instead of replacing it.
   - **Unverifiable:** no confident match. Keep the user's entry as written and say what is missing or ambiguous. Never fill in guessed fields.
   - **Not checked:** any entry beyond what the tool actually verified. Never silently drop these.
4. Give one corrected BibTeX block that uses only the tool's corrections (except `author` hints, per step 3) and the user's original fields.
5. Offer to format or export the verified list.

## Full: verify, then format or export

1. Run Quick steps 1 to 4, except that full mode has no 5-call cap: keep calling `verify_bibtex` in batches at the entry cap until every entry is checked, then report all of them.
2. For matched and corrected entries, call `render_citations` with the matched work IDs or DOIs that `verify_bibtex` returned, in the requested format (BibTeX, Markdown, or JSON). Its `exports` already hold the file content and a suggested filename, built from full corpus metadata including complete author lists: give those to the user as the file, exactly as returned, without editing them. Any BibTeX you compose (such as the corrected block from Quick step 4) uses only fields the user supplied or a tool returned in this conversation: never add a volume, issue, pages, publisher, or any other field from memory. Use `export_citations` only for metadata the user supplied, never to rebuild records from rendered text.
3. For a named style (APA, MLA, Chicago, or Harvard), first call `get_paper_details_batch` on the matched IDs or DOIs, at most 25 per call, because `verify_bibtex` returns match IDs and correction notes, not full records. Then call `format_citation` with that style and the returned metadata, at most 50 papers per call, and combine the results in order. For an entry with no match, use only complete metadata the user supplied, and say that formatting supplied fields does not verify them.
4. Keep unverifiable entries out of verified output and list them separately for the user to fix.

## Single citation

For one paper in a named style ("cite this in APA"): call `format_citation` with that style, using the metadata a Corbis tool already returned if the paper came from Corbis in this conversation, or the metadata the user gave otherwise. For a Markdown or BibTeX reference on a paper that came from Corbis, use `render_citations` instead. Either way that is one tool call.

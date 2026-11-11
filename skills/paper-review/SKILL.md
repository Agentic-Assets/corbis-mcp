---
name: paper-review
description: Use for any request to review, critique, or give feedback on a research paper, draft, or manuscript in finance, real estate, economics, or urban studies, including quick feedback on its biggest problems, a referee report, a pre-submission check, or a technical audit. Also use when the user already has a referee report or review draft and wants it verified, fact-checked against the manuscript, tightened, or checked for overstatement, even if they only say "check my review" or "make sure this report is right". Produces referee-style reviews and verified report revisions, with literature positioning and reference checks from the Corbis research connector.
---

# Paper review

Review a manuscript the way a careful referee would, or verify and tighten a referee report the user already has. Ground literature and reference findings in Corbis sources. Every factual statement in the final report should trace to the manuscript, its supplement, or a cited source.

## Ground rules

- Cite only papers, data, and quotes that a Corbis tool returned in this conversation, that the user supplied, or that you confirmed with the registry check below. Never invent a DOI, author, year, title, or quote.
- Say when evidence is thin, old, mixed, or limited to one market or domain. Never describe the output as free of errors or hallucinations.
- Some optional steps use premium tools that need an enterprise plan. If a premium tool is not in your tool list, or returns an access or plan error, tell the user once that the step needs an enterprise plan (current plans: the Corbis pricing page), then continue with the standard tools. Never retry a denied tool.
- Research tool calls may use Corbis credits. Use a batch tool when one exists, and never re-fetch details for a paper already retrieved in this conversation.
- Quick mode is the default for a narrow question: at most 5 Corbis tool calls, a short cited answer, then an offer to run the full workflow. Use full mode when the user asks for a review, report, or audit, or accepts that offer.
- If no Corbis tools are available, or a Corbis call returns a sign-in or connection error, first retry the call once through any other Corbis connection in your tool list (the same tool name from another Corbis server). That retry counts toward the quick-mode limit, so skip it when no calls remain. If none works, ask the user to connect or reconnect Corbis (the plugin's Connectors tab, or `/mcp` in Claude Code) instead of answering from memory. Do not switch to another source, such as a web search or another citation database, unless the user asks. Crossref is the named exception, and only as the registry check below states: a DOI the user supplied or a Corbis tool returned, when the metadata looks wrong or the record is missing, one fetch per cited paper, labeled "confirmed by Crossref", never a DOI from memory. Label anything else from another source as not verified by Corbis.
- Registry check: when a DOI from the user's material or a Corbis record has metadata that looks wrong (authors, year, title), or its paper is missing from Corbis, and you have a web-fetch tool, you may look up that DOI at Crossref (https://api.crossref.org/works/ followed by the DOI), once per cited paper, without asking. Label the result as confirmed by Crossref, not by Corbis. Never look up a DOI you recall from memory. Without a web-fetch tool, mark the paper as not verified.

## Before you start

- You need the manuscript. If it is missing, ask. Ask for a supplement or appendix only when the manuscript cites one that was not provided; many checkable claims live there. Never review from a title or abstract alone and present it as a paper review.
- Read any journal context the user gives (scope, word limit, article type). A request that suits a long journal article can be wrong for a short letter, so let the venue shape what you ask the authors to add to the main text versus the supplement.
- Pick the mode from the request. Ask only if it truly fits more than one:
  - **Quick:** the five most important issues.
  - **Referee report:** a full report for the editor and authors.
  - **Technical audit:** specific technical findings, each with an exact quote.
  - **Verify a report:** the user has a draft report and wants it checked against the paper, fixed where wrong, and possibly tightened. Phrases like "double check", "verify", "make sure we're not overstating", or "don't change much" signal this mode.
- Note how much change the user wants. "It's already in good shape" or "don't change much" means fix verified errors and imprecision only, and list everything else as optional suggestions for the user to decide on.
- Send Corbis short search queries and summaries, not the full manuscript text.
- When you can run code, convert PDF and Word inputs to plain text once (for example `pdftotext -layout` or `pandoc -t plain`) so you can search them. Absence claims and quotes are only as good as your search.

## Quick

1. Read the manuscript.
2. Report the five most important issues. For each: location (section, page, table, or equation), the problem, why it matters, and a concrete fix.
3. Corbis calls are optional here (at most 5). Use one `literature_retrieve` call only if an issue depends on related work.
4. Offer the full review.

## Full review (referee report or technical audit)

Follow `references/referee-report-phases.md` for a referee report or `references/technical-audit-phases.md` for a technical audit. Those files are the long form. `docs://workflow-packs/referee-report` and `docs://workflow-packs/technical-audit` are the short host contract for a client that never sees this skill. Each phase file lists what that pack leaves out.

Evidence tools during the phases:

- Related and missing literature: `literature_retrieve` or `search_papers` with short queries built from the research question, then `get_paper_details_batch` on the papers you keep, at most 25 IDs per call.
- Bibliography health (technical audit): `verify_bibtex` on the manuscript's references when the user supplies BibTeX.
- Reference list for papers you cite in the report: `render_citations`.

Before delivering, run the verification pass in `references/report-verification.md` and the calibration pass in `references/calibration-checklist.md` on your own draft. A fresh draft fails the same ways a user's draft does. Deliver the report in the template from the phase reference, or in the user's own structure when they have one.

## Verify a report

Follow `references/report-verification.md` for the claim ledger, arithmetic, edit rules, and the verification log. Follow `references/calibration-checklist.md` for tone, overstatement, and trimming. In short:

1. Work from copies. When you work with files, never edit the user's files in place: save each revision as a new version (for example `_v2`, `_v3`) next to the original. In a chat without file access, return the revised text in your reply.
2. If there are several versions of the report, compare them first, ignoring formatting, so you know which text is current and whether older copies differ in substance.
3. Build a claim ledger: one row for every number, quote, location reference, absence claim, characterization of the authors or of a cited paper, and policy claim in the report.
4. Check each row against the source. Recompute every derived number, in a short script when you can run code. The claim-type table is in `references/report-verification.md`.
5. Run the calibration pass in `references/calibration-checklist.md`.
6. Write the new version with the smallest edits that fix what you confirmed, plus a verification log of what changed, why, and what you checked and left alone.

## Second reader (when subagents are available)

For a full report or a verification, a second reader catches what the first misses. If your client can run subagents, start two independent reviewers in parallel, a fact-checker and a calibration reviewer, using the briefs in `references/report-verification.md`. Give them the file paths (or the pasted text) and the brief, not your conclusions, so they are not anchored on your reading.

Treat what they return as candidates. Re-check each one against the source before you edit; reviewers can be wrong, especially about cited papers they could not open. Record what you accepted, what you rejected, and why. Without subagents, run the fact-check and the calibration checklist as two separate passes.

## Citations

- Look up every DOI the report cites with `get_paper_details_batch`, in as few calls as possible.
- Corbis metadata can be wrong: online-first years differ from print years, and author disambiguation can attach a different person with a similar name. When a record looks off, or a cited paper is missing from Corbis, use the Crossref check in the ground rules.
- Check titles word for word. A dropped word in a title is a real error.

## Deliverables

- The report, in Markdown or the user's format. When the user works in Word and you can create files, also produce a `.docx`; if a document skill or tool is available, use it, and look over the rendered pages before handing it over.
- For a verification, the verification log (template in `references/report-verification.md`) and any arithmetic script you ran.

Keep process notes (tool limits, what you could not verify, "local review") out of a referee report. Put them in the verification log and your reply, because the editor forwards that report to the authors. For a technical audit, say in your reply, not in the report body, that this is a local review. Missing files, appendices, code, or data stay in the audit's Limitations section.

## Scored evaluation (enterprise upgrade)

After the local report, on enterprise plans:

- Referee report: call `referee_report_evaluate` with the summary contract in `references/referee-report-phases.md`. The sealed markdown is an extra artifact. It must not replace the verified local report.
- Technical audit: call `technical_audit_evaluate` with the findings contract in `references/technical-audit-phases.md`.

If the tool is unavailable or denied, deliver the local report and say once, in your reply rather than inside the report, that this is a local review and the scored evaluation needs an enterprise plan.

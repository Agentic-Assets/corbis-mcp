# Referee report phases

This file is the long form for a host that has the paper-review skill. The MCP resource `docs://workflow-packs/referee-report` is the short host contract for a client that never sees these files.

The pack leaves out or compresses the following:

- Synthesis here keeps major comments to the few questions that decide the recommendation, usually three to five. The pack's synthesis line stops at candidate concerns and assessment summaries.
- Each major comment here uses a bold question heading, locations, evidence paragraphs, and a Resolution line. The pack states that shape in one sentence.
- The confidential note here is two or three sentences on fit and severity, then what you checked yourself, such as recomputed table means. The pack asks for fit, severity, and what you checked yourself.
- Policy and journal claims, the claim ledger, file versioning, and the second-reader briefs are in `references/report-verification.md`. Trimming and tone rules are in `references/calibration-checklist.md`. The pack's verify list is the short check only.

## Phases

1. **Intake:** title, research question, contribution claim, target venue if given, and which files you have (main text, appendix, tables, code, data).
2. **Literature position:** compare the contribution claim with nearby papers from Corbis. Note closely related papers the manuscript does not cite.
3. **Mechanism and contribution:** is the main idea stated clearly, is it new relative to phase 2, and does it matter to the field.
4. **Design and data:** identification, measurement, sample construction, data limits, and alternative explanations.
5. **Results and interpretation:** do tables, figures, and robustness checks support the stated claims, and are magnitudes interpreted.
6. **Writing and presentation:** organization, undefined terms, and reader friction.
7. **Synthesis:** merge phase notes into ranked concerns. Keep the major comments to the few questions that decide the recommendation, usually three to five.
8. **Verify and calibrate:** before delivering, run `references/report-verification.md` and `references/calibration-checklist.md` on the draft.

## Concern format

Work notes for each concern: phase, severity (high, medium, or low), the issue stated plainly, where it appears, why it matters, and a concrete suggested resolution. Literature concerns in the report name papers that Corbis returned. A paper confirmed only in Crossref may appear in the report when labeled "confirmed by Crossref", and stays out of `citationEvidence`.

In the report itself, write each major comment as:

- **A bold heading phrased as the question**, followed by its locations in parentheses: main-text sections, supplement sections and tables. Cite the table each quoted number comes from.
- **Evidence paragraphs** with numbers taken from the paper. Credit any caveat the authors already make.
- ***Resolution:*** the concrete request. Mark which parts are optional, and say whether each can be done from stored outputs or needs new work.

Severity labels stay in your notes. Editors read the ordering, not the labels.

## Report template

Use the user's existing structure when they have one. Otherwise:

```markdown
**Referee Report**
*<Journal, if given>*
Manuscript <ID, if given>
"<Title>"

## Summary and Recommendation
One paragraph on what the paper does, one on the headline results with numbers, and one with the recommendation and what the required changes would clarify.

## Contribution
Position against the closest literature (with links), what is new, and what the paper should add to the comparison.

## Major Comments
Numbered, in the format above.

## Minor Comments
Numbered, one or two sentences each. Group related small requests, such as several abstract fixes, as bullets under one item.

## Source Appendix
Full references for every paper cited in the report, with DOIs.
```

Deliver a **confidential note to the editor** as a separate block after the report, for the journal's confidential-comments field: two or three sentences on fit and severity, then what you checked yourself (for example, recomputed table means). It never goes inside the report the authors receive.

Keep process notes (tool limitations, "Local review", what you could not verify) out of the report. They go in your reply and the verification log, because the editor forwards the report to the authors.

## Scored evaluation input (enterprise)

`referee_report_evaluate` takes summaries, not the manuscript. Include only citation evidence that came from Corbis tools. The sealed markdown is an extra artifact. It must not replace the verified local report.

```json
{
  "manuscriptTitle": "Optional title",
  "assessmentSummaries": [
    { "phase": "Design and data", "summary": "Concise local assessment.", "keyConcerns": ["Optional short concern"] }
  ],
  "candidateConcerns": [
    {
      "id": "concern-1",
      "phase": "Results and interpretation",
      "severity": "high",
      "issue": "Specific concern stated plainly.",
      "whyItMatters": "Why a reader or editor should care.",
      "suggestedResolution": "Concrete revision request.",
      "evidenceSummary": "Brief local evidence summary.",
      "citationRefs": ["paper-1"]
    }
  ],
  "citationEvidence": [
    {
      "id": "paper-1",
      "title": "Paper title",
      "authors": ["Author"],
      "year": 2025,
      "journal": "Journal",
      "doi": "10.xxxx/example",
      "url": "https://doi.org/10.xxxx/example",
      "summary": "Why this evidence matters."
    }
  ]
}
```

# Referee report phases

Condensed from the Corbis resource `docs://workflow-packs/referee-report`. If your client can read MCP resources, that resource is the fuller version.

## Phases

1. **Intake:** title, research question, contribution claim, target venue if given, and which files you have (main text, appendix, tables, code, data).
2. **Literature position:** compare the contribution claim with nearby papers from Corbis. Note closely related papers the manuscript does not cite.
3. **Mechanism and contribution:** is the main idea stated clearly, is it new relative to phase 2, and does it matter to the field.
4. **Design and data:** identification, measurement, sample construction, data limits, and alternative explanations.
5. **Results and interpretation:** do tables, figures, and robustness checks support the stated claims, and are magnitudes interpreted.
6. **Writing and presentation:** organization, undefined terms, and reader friction.
7. **Synthesis:** merge phase notes into ranked concerns.

## Concern format

Each concern: phase, severity (high, medium, or low), the issue stated plainly, where it appears, why it matters, and a concrete suggested resolution. Literature concerns name papers that Corbis returned.

## Report template

```markdown
# Referee Report

## Manuscript
Title and one-sentence summary.

## Recommendation
Accept, minor revisions, or major revisions, with one sentence of reasoning.

## Summary Assessment
Contribution, strengths, and main reservations.

## Must-Address Issues
Numbered concerns in the concern format above.

## Additional Comments
Lower-priority notes on clarity, framing, and presentation.

## Literature and Positioning
Papers from Corbis with full references.

## Limitations
Missing appendices, data, or code. Label the report "Local review" when no scored evaluation ran.
```

## Scored evaluation input (enterprise)

`referee_report_evaluate` takes summaries, not the manuscript. Include only citation evidence that came from Corbis tools.

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

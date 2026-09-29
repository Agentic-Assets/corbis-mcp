# Technical audit phases

Condensed from the Corbis resource `docs://workflow-packs/technical-audit`. If your client can read MCP resources, that resource is the fuller version.

## Phases

1. **Intake:** title, files, target venue, methods, tables, figures, appendices, code, and data availability.
2. **Claim map:** list the paper's core claims and the evidence each one relies on.
3. **Method and identification:** assumptions, research design, controls, timing, and alternative explanations.
4. **Data and measurement:** sample construction, variable definitions, exclusions, and missing data.
5. **Results:** table logic, figure interpretation, robustness, and consistency across sections.
6. **References and citations:** support for cited claims and bibliography health. Use `verify_bibtex` when the user supplies BibTeX.
7. **Synthesis:** merge phase notes into candidate findings.

## Finding format

Every finding needs: severity (critical, major, moderate, or minor), category, a short title, location, the exact quote from the manuscript, the problem, why the quote supports the finding, and a concrete fix. Drop any finding you cannot tie to an exact quote.

## Report template

```markdown
# Technical Audit Report

## Manuscript
Title and one-sentence summary.

## Summary
Overview of the findings and the limits of the review.

## Detailed Findings
Each finding: severity, category, location, quote, issue, evidence, and suggested fix.

## Dropped Candidates
Candidates left out and why.

## Limitations
Missing files, appendices, code, or data. Label the report "Local review" when no scored evaluation ran.
```

## Scored evaluation input (enterprise)

`technical_audit_evaluate` takes candidate findings, not the manuscript.

```json
{
  "manuscriptTitle": "Optional title",
  "candidateFindings": [
    {
      "id": "finding-1",
      "category": "Method and identification",
      "severity": "major",
      "title": "Short finding title",
      "location": "Section 3.2, paragraph 4",
      "verbatimQuote": "Exact quoted text from the manuscript.",
      "problem": "What is technically wrong or underspecified.",
      "evidence": "Why the quote supports the finding.",
      "suggestedFix": "Concrete revision request."
    }
  ]
}
```

# Verifying a referee report

Use this when the user already has a report (theirs, or a draft you wrote) and wants it checked against the manuscript and improved without being rewritten.

## 1. Set up

- Keep the inputs untouched. When you work with files, copy them into one folder and work only on new versions. In a chat without file access, quote the current text and return revised text in your reply.
- When you can run code, extract searchable text once, for example `pdftotext -layout paper.pdf paper.txt`, `pandoc supplement.docx -t plain --wrap=none -o supplement.txt`, and `pandoc report.docx -t markdown -o report.md`.
- If there are several report versions (for example a Word file and a newer Markdown file), compare them after normalizing quotes, escapes and list markers. Tell the user whether they differ in substance or only in formatting, and work from the latest.

## 2. Claim ledger

Go through the report sentence by sentence. Each checkable statement becomes one row:

| Type | Example from a report | How to check |
|---|---|---|
| Number | "a 6 percent rent decline (standard error 0.05)" | find the table cell |
| Derived number | "about a third of the total effect" | recompute from the table values |
| Quote | "reform timing was exogenous" | exact-match search |
| Location | "(Section 3.2; Table A4)" | does each location hold the material? |
| Absence | "Table A2 lists the variable but the appendix never reports it" | full-text search for the term and its synonyms |
| Author characterization | "the conclusion nonetheless states that..." | did the authors already caveat it? |
| Cited-paper characterization | "this paper does not vary the treatment timing" | the cited paper's abstract |
| Policy | "does not meet the journal's data policy" | policy text the user supplied, or the publisher's page if the user allows a web lookup |
| Feasibility | "can be done with existing estimates, not new data" | does every required request really qualify? |

Keep a "verified as written" list as well as a "changed" list. The user wants to know what was checked, not only what was fixed.

## 3. Arithmetic

When you can run code, write a short script that types in the table values the report relies on and prints each derived figure next to the report's figure. Otherwise show the arithmetic in the log. Cover:

- means computed from cell values;
- differences against reported contrasts;
- shares and ratios;
- interval width ratios when the report compares intervals.

Differences within the rounding of the inputs are fine; say so rather than "correcting" them.

## 4. Edit rules

- Make the smallest edit that fixes the confirmed problem, and keep the user's voice and structure.
- When a claim cannot be verified, either soften it to what you can show or move it into the log as an open question. Never leave it as if it were checked.
- When you add support for a claim, keep it to one clause.
- Re-read every edited sentence in context. Edits introduce new mistakes: a stray comma, a broken cross-reference, a renumbered list that another comment still points to.

## 5. Independent reviewer briefs

When your client can run subagents, give each reviewer the file paths (or the pasted text) and the brief below, not your findings.

**Fact-checker brief.** Check every number (recompute derived ones and show the arithmetic), every quote, every section or table reference, every absence claim (search the full text), and every description of the design against the manuscript and supplement. Do not assess external literature. Return findings most serious first, each with: the exact report text, what is wrong, the evidence quoted with its location, a minimal corrected wording, a severity (error, imprecise, or nitpick), and your confidence. End with a "checked and correct" list. Do not edit files.

**Calibration brief.** You are a senior referee reviewing a colleague's draft before it goes to the editor. The draft is in good shape, so this is a light pass, not a rewrite. Flag:

- (A) overstatement: claims or characterizations stronger than the manuscript supports, required requests that should be optional, harsh wording;
- (B) over-explaining: restatements, repeated points across comments, explanations the editor does not need.

For each item give the exact text, the problem, the evidence (for A), a minimal replacement or "delete", and a priority (should-fix or optional). Never propose deleting a request, number or citation. Do not edit files.

## 6. Verification log template

```markdown
# <Manuscript ID> referee report: verification log

Checked <date>. Sources: <files>. Report checked: <file and version>.

## Result
One paragraph: errors found (or none), how many wording changes, and whether the recommendation changed.

## Changes in <new version>
| # | Location | Before | Issue | After |

## Verified as written
Grouped by report section; one line per claim with its source location.

## Citations
| Citation | Corbis | Crossref | Status |

## Reviewer findings not applied
Each with a one-line reason.

## Optional points not added
Suggestions the user may want, left out because the brief was light-touch.
```

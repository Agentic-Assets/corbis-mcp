# Public skills collection observation

`skills-sh-collection.yml` checks the public skills.sh collection after each
push to the default branch and on manual dispatch. Pull requests run
only the observer's tests. Results and the checked commit appear in the GitHub
Actions run log. The check derives expected names from `skills/*/SKILL.md` in
the checked-out commit. It makes no skill installations and uses no token.

The observer accepts only the source collection's recognizable heading and
skill-link paths. All expected links observed is `visible`. A recognizable page
missing expected links is `pending`; inaccessible, redirected, rate-limited,
oversized, or unrecognized pages are `unknown`. Pending and unknown retry a
bounded number of times and then fail the workflow so a later manual run
remains visible. A delayed result can resolve without a new release;
a failed workflow does not roll back a published commit.

This is an observation of the rendered public collection, whose HTML structure
may change without notice. It does not establish that skill content matches the
checked commit, that search returns a skill, that every viewer sees the same
result, or that an MCP client is connected. A page layout change must be
investigated rather than treated as an empty or complete catalog. Check the
release owner guidance for authenticated catalog or revision verification.

Run locally from the repository root:

```sh
python3 -m unittest discover -s .github/tests -p 'test_*.py'
python3 .github/scripts/check_skills_sh_collection.py --source Agentic-Assets/corbis-mcp
```

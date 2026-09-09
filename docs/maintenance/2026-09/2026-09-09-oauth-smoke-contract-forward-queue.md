# OAuth smoke follow-up candidates

Date: 2026-09-09. These are suggestions, not authorization or a parallel queue.
Code and review proof remain in the repository and its PR.

Historical follow-up record for PR #15. The
[metadata-only correction](2026-09-09-metadata-only-smoke-closeout.md) supersedes
the original real-tool probe and owns the current source-smoke scope.

- **P1, acceptance (verified scope gap):** At a separately authorized release,
  run clean-client OAuth acceptance against the exact signed source release.
  This smoke test checks unauthenticated discovery and advertised DCR/PKCE/grants;
  it does not register a client, obtain or refresh a token, or verify entitlements.
- **P2, compatibility (deliberate contract):** If the service intentionally removes
  its root authorization-discovery alias, review client compatibility before
  changing this smoke contract. Both aliases returned valid HTTP 200 metadata on
  2026-09-09, and a future 404 currently fails the test.

No unresolved code-review defect is deferred to this list. Source release,
Marketplace admission, deployment, and public-directory work retain their own
evidence and human gates.

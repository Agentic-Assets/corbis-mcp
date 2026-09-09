# Metadata-only smoke follow-up candidates

Date: 2026-09-09. Suggestions only; the repository/PR and coordinator own work.

- **P1, service contract (verified mismatch):** Reconcile whether unauthenticated
  `tools/list` should return a public catalog or HTTP 401 with discovery
  metadata. The requested source contract requires 401; production returned
  HTTP 200 on 2026-09-09. Resolve this explicitly before merging the replacement.
- **P2, client acceptance (separate gate):** Verify authenticated clean-client
  connection and tool access against the exact source release. Metadata-only
  probes cannot establish token issuance, refresh, or entitlement enforcement.

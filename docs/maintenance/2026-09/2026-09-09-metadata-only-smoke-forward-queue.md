# Metadata-only smoke follow-up candidates

Date: 2026-09-09. Suggestions only; the repository/PR and coordinator own work.

- **P1, separate auth coverage (ownership decision):** Keep protected-request
  HTTP 401 and Bearer discovery challenge tests in the application and Marketplace.
  The source package validates GET discovery metadata only. Public `tools/list`
  responses are not evidence of an authentication regression.
- **P2, client acceptance (separate gate):** Verify authenticated clean-client
  connection and tool access against the exact source release. Metadata-only
  probes cannot establish token issuance, refresh, or entitlement enforcement.

# Forward queue after Corbis MCP connector-label contract (2026-08-16)

Candidate work surfaced during the `0.1.3` source candidate. This is a menu,
not an authorization.

## Evaluation

- **Publish a current public product image** (confidence: verified gap;
  priority: high)
  Use a source-approved or live-derived image that does not contain the stale
  `400,079` corpus figure. Verify any displayed corpus number against the live
  Corbis page immediately before committing it to this public source package.

- **Capture exact client label readbacks** (confidence: verified release gap;
  priority: high)
  In clean Claude Code, Codex CLI, and Cursor profiles, record the Marketplace
  or plugin-card title and the post-install MCP settings label separately for
  the exact signed source tag and promoted payload digest. Do not infer one
  label from another.

- **Evaluate production `serverInfo` metadata in the application lane**
  (confidence: verified ownership boundary; priority: high)
  The production application owns MCP initialization metadata. Its owner can
  determine whether it emits a title that the relevant clients render, then
  test that behavior with controlled clients. This source repository must not
  proxy or hard-code server metadata.

## Hardening

- **Keep the label and identifier regression contract** (confidence:
  implemented control; priority: high)
  Retain the static assertions that `Corbis` is title case in supported display
  fields and that `corbis-mcp` remains distinct in MCP maps. Do not accept an
  undocumented display-label field simply to change a settings surface.

- **Establish trusted SSH tag verification** (confidence: verified local and
  remote gap; priority: high)
  Configure authorized maintainer signer material outside this repository, then
  verify the next candidate tag's signature, tag object, peeled commit, and
  default-branch reachability before Marketplace promotion.

## Process

- **Require a client-schema evidence review before any new display field**
  (confidence: verified requirement; priority: medium)
  If a client adds documented server-level display metadata, cite the primary
  schema, add a narrow static contract, and demonstrate the exact label in the
  corresponding clean client before release.

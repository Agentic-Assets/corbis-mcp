# Maintenance records

This directory preserves dated internal closeouts and forward queues. It is not
part of the public connector package or its future Marketplace payload.

## Layout

- Store records in `YYYY-MM/` directories, using their existing
  `YYYY-MM-DD-<subject>-<type>.md` filenames.
- Keep one closeout record and, where useful, one forward queue per substantive
  branch or work session.
- Link the date, branch, commits, verification, decisions, deferred work, and
  human gates in the closeout. Keep the forward queue as a prioritized menu,
  not an execution authorization.
- Do not rename records solely to change their category. The monthly archive is
  the primary navigation and preserves chronological context.

## Current archive

- [`2026-08/`](2026-08/) contains the first Corbis MCP source-handoff closeout
  and its forward queue, plus the source-release-readiness closeout and forward
  queue, README hero-image blocker, and research-focused README closeout and
  forward queue, plus the public release-materials closeout and forward queue,
  the MCP server-identifier closeout and forward queue, plus the v0.1.1
  release-record correction closeout and forward queue.

---
name: poppify-schema-introspect
description: Inspect the deployed Poppify MCP tool schemas to verify what parameters are actually accepted. Use when: a parameter you passed seems to have been silently dropped, an edit_session {patch} field didn't take effect, the render came out using defaults instead of your overrides, OR before recommending a parameter you're not 100% sure is in the current deployed build. Diffs schema-vs-docs and helps file precise feedback when drift is found.
---

# Inspecting the deployed Poppify MCP schemas

MCP clients strip undeclared fields before forwarding to the server. If a parameter you pass to a tool seems to have been ignored, the most likely cause is **schema/code drift** — the server's handler accepts the field, but the MCP tool registration's Zod schema doesn't declare it, so the field was dropped at the protocol boundary.

This skill teaches Claude how to verify the deployed schema directly.

> **Oct 2026: twelve tools, one meaning each.** `tools/list` now shows `get_capabilities`, `start_session`, `get_session`, `search`, `suggest`, `generate`, `edit_session`, `render`, `publish`, `account`, `add_media`, `submit_feedback`. Most take exactly ONE branch key (`generate({image:{…}})`), and the branch object is the old tool's schema minus the top-level params (`apiKey`, `sessionId`, `expectedVersion`, `spendApproved`). Every change to a reel is `edit_session({sessionId, expectedVersion, commands:[…]})` with `{slide}`, `{patch}`, `{asset}`, `{concept}`, `{strategy}` or `{provider}` commands. The old names (`apply_session_patch`, `update_slides`, `add_slide_image`, `confirm`, …) are NOT in the list but stay callable, so a client with a cached list keeps working — if a diff shows them missing, that is the consolidation, not drift. Removed on purpose, not drift: `refine_concept.overrides` (use `{slide}` set_text / `{patch}` caption), `update_slides rewrite` (use `suggest {copy}`, then set_text), `apply_session_patch.visualEdits` (use `{slide}` add / set_image), and per-slide text/image/duration inside `patch.slides` (they are `{slide}` commands; patch.slides keeps language + heroLine).

## Where to look

The MCP server publishes its tool catalog via the standard MCP `tools/list` request. Claude Code already calls this on connect — the tool definitions are available in the client's MCP state.

To inspect what was returned:

1. List the tools Claude Code currently sees:
   ```
   /mcp poppify
   ```
   That shows the names, but not the param shapes.

2. For the param shapes, ask the deployed server directly via JSON-RPC `tools/list` at the canonical MCP endpoint (`https://poppify.ai/api/mcp`, POST — the Poppify server is stateless, no initialize handshake needed):
   ```bash
   curl -s https://poppify.ai/api/mcp \
     -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
     | sed -n 's/^data: //p' | jq '.result.tools[] | select(.name=="edit_session") | .inputSchema.properties.commands.items.properties.patch'
   ```

   This returns the live JSONSchema of `edit_session`'s `{patch}` command (substitute another tool in `select(.name==...)`, and a branch key — `generate` → `.inputSchema.properties.image`). Cross-reference the field list against the tool docs.

   > Note: `https://poppify.ai/.well-known/mcp.json` is a *discovery manifest* (name, endpoint, a few tool stubs) — it does NOT carry per-tool `inputSchema`, so it cannot be used for drift checks. Only `tools/list` reflects the deployed schemas.
   >
   > `server/discover` (the 2026-07-28 method, POSTed like any other) IS answered now, and is the cheap way to get the supported protocol versions, the server identity and a cache hint (`ttlMs` / `cacheScope`) — but it returns `capabilities: {tools:{}}` with no `inputSchema` either, so the same rule applies. The server card is also served at `/.well-known/mcp/server-card.json` and `/mcp/server-card`.

## Drift checklist

For each tool the user asked you to verify, confirm:

- The parameter name you intended to pass is in `inputSchema.properties`
- The expected type matches (string vs enum vs boolean)
- The parameter is at the top level, not nested inside another object you forgot

## Known previously-dropped fields (now fixed)

These were silent-drop bugs that have been resolved — if you see one of them missing from the deployed schema, the deploy hasn't propagated yet:

- `edit_session {patch}.textColor` — hex color for caption text (originally dropped on the old `customize` tool)
- `edit_session {patch}.textPosition` — `top` / `center` / `bottom`
- `edit_session {patch}.continuousEffect` — boolean, opt-out of continuous motion

If any of these are STILL missing from the live schema: the production build may be stale. File via `submit_feedback({ apiKey, frictionPoints: ["schema drift: edit_session {patch}.textColor missing from deployed schema as of <date>"] })` (there is no `kind`/`description` field — drift reports go in `frictionPoints`) so the Poppify team can investigate.

## What to do if you find drift

1. **Don't keep guessing field names** — the dropped field will never land no matter how you spell it. Once you've confirmed the schema is missing the field, the only path is server-side.
2. **File feedback** with the exact field name + the tool name + the version/build of the MCP you're hitting (quote the date and the `serverInfo` returned by `initialize` or `server/discover` — the server does not emit a Cloud Run revision id anywhere in its MCP responses).
3. **Work around if urgent**: pick the closest sibling field that IS in the schema (e.g. for missing `textColor`, override the whole `textAnimation` style which may shift the color implicitly via recipe palette; not a true substitute but unblocks the user).

## Why this matters

Schema drift bugs are the most expensive bug class in MCP: the user pays seeds for a render, the render uses defaults instead of the requested override, and nobody knows the field was dropped until they verify the output frame-by-frame. This skill catches it BEFORE the render, not after.

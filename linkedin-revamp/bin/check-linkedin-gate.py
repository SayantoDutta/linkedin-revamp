#!/usr/bin/env python3
"""linkedin-revamp PreToolUse safety hook.

Hard safety net that sits UNDER the skill's own prompt-level gates. When the
skill (or a confused / prompt-injected model) tries to run a high-risk Chrome
action — deleting profile content, uploading a file, or changing a LinkedIn
setting — this hook returns a permission decision of "ask", so the user is
prompted by the harness before it happens. It NEVER silently allows a
destructive Chrome action through.

Read from stdin: the PreToolUse payload (JSON) with `tool_name` + `tool_input`.
Write to stdout: a PreToolUse hook decision (JSON), or nothing to allow.

Design notes:
- Only Chrome MCP tools (`mcp__Claude_in_Chrome__*`) are ever gated. Every
  other tool is allowed untouched.
- Read-only Chrome actions (navigate, screenshot, read, list) are allowed so
  the flow stays smooth — the skill reads the profile constantly.
- High-risk actions (upload, delete, settings/privacy/visibility changes,
  connection requests, messages, follows, likes) return "ask".
- Fail-open on a parse error: the skill's prompt-level gates remain the primary
  guarantee, and a hiccup in the hook must not brick the skill. A stderr note
  is emitted so the failure is visible.

This is the Claude Code enforcement layer. In environments that do not run
PreToolUse hooks, the skill's in-prompt gates (execute/safety-gates.md) still
apply — they are the universal layer.
"""
from __future__ import annotations

import json
import sys

CHROME_PREFIX = "mcp__Claude_in_Chrome__"

# Tool-name fragments that are always high-risk regardless of input.
HIGH_RISK_TOOL_FRAGMENTS = ("upload", "file_chooser", "filechooser")

# Substrings that, when found in the stringified tool input, signal a
# destructive or settings-changing action that must be confirmed.
DESTRUCTIVE_MARKERS = (
    "delete",
    "remove skill",
    "remove this",
    "/settings",
    "mypreferences",
    "visibility",
    "privacy",
    "share profile updates",
    "connect",          # connection request
    "send message",
    "send invitation",
    "follow",
    "unfollow",
)

# Markers that are read-only and should NOT trip the destructive check even if
# a destructive substring appears incidentally in a URL being read.
READONLY_TOOL_FRAGMENTS = ("screenshot", "list_connected", "read", "snapshot", "get_")


def decision(permission: str, reason: str) -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": permission,
            "permissionDecisionReason": reason,
        }
    }


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except (ValueError, TypeError):
        # Fail open — prompt gates remain the primary guard.
        print("linkedin-revamp hook: could not parse PreToolUse payload; "
              "deferring to in-prompt safety gates.", file=sys.stderr)
        return 0

    tool_name = str(payload.get("tool_name", ""))

    # Only ever gate Chrome MCP tools. Everything else passes untouched.
    if not tool_name.startswith(CHROME_PREFIX):
        return 0

    short = tool_name[len(CHROME_PREFIX):].lower()
    tool_input = payload.get("tool_input", {})
    blob = json.dumps(tool_input, ensure_ascii=False).lower()

    # Always-ask on uploads (tool-name based — unambiguous).
    if any(frag in short for frag in HIGH_RISK_TOOL_FRAGMENTS):
        out = decision(
            "ask",
            "linkedin-revamp: about to UPLOAD a file to LinkedIn via Chrome. "
            "Confirm this is the banner/image you intend to upload.",
        )
        print(json.dumps(out))
        return 0

    # Read-only tools never trip the destructive check.
    is_readonly = any(frag in short for frag in READONLY_TOOL_FRAGMENTS)

    if not is_readonly and any(marker in blob for marker in DESTRUCTIVE_MARKERS):
        out = decision(
            "ask",
            "linkedin-revamp: this Chrome action looks like a delete, a "
            "connection/message/follow action, or a LinkedIn settings change. "
            "Confirm before it goes live on your profile.",
        )
        print(json.dumps(out))
        return 0

    # Allow read-only / benign Chrome actions (navigate, click, type, etc.)
    # so the flow stays smooth. The skill's own per-section gates still apply.
    return 0


if __name__ == "__main__":
    sys.exit(main())

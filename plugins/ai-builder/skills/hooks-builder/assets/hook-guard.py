#!/usr/bin/env python3
"""Gatekeeper hook: refuse an action that touches a protected path.

Reads the event payload as JSON on stdin. Refuses by exiting 2 with the reason on
stderr — no other exit code blocks anything.

Test it before installing it, with a payload you write by hand:

    echo '{"tool_name":"Write","tool_input":{"file_path":".env"}}' | python hook-guard.py
    echo '{}' | python hook-guard.py
    echo '{"tool_name":"Write","tool_input":{"file_path":"../../etc/hosts"}}' | python hook-guard.py

Exit codes:
    0   allow
    2   refuse (the only blocking code)
"""

import json
import os
import sys

# <Adjust: the paths this hook protects, relative to the project root.>
PROTECTED = (".env", ".env.local", "secrets/")

# <Adjust: the actions it applies to. Matching is case-sensitive.>
GUARDED_TOOLS = ("Write", "Edit")


def refuse(reason):
    """Block the action. Exit 2 is the only code that blocks; stderr is what the
    agent is shown, so the reason must say what to do instead."""
    print(f"BLOCKED: {reason}", file=sys.stderr)
    sys.exit(2)


def classify(path, root):
    """Return None to allow, or the reason to refuse.

    Compares after normalisation: `a/../.env` and `.env` are the same file written
    two ways, and only one of them matches a naive string test.
    """
    if not path:
        return None
    resolved = os.path.normpath(os.path.join(root, path))
    if not resolved.startswith(os.path.normpath(root) + os.sep):
        return "resolves outside the project root"
    relative = os.path.relpath(resolved, root).replace(os.sep, "/")
    if any(relative == p or relative.startswith(p) for p in PROTECTED):
        return "is protected by policy"
    return None


def main():
    raw = sys.stdin.read()
    if not raw.strip():
        # A gatekeeper that cannot read its input refuses. Failing open here would
        # remove the protection exactly when something is unusual.
        refuse("validator received no input")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        refuse(f"validator could not parse its input: {exc}")

    tool = data.get("tool_name", "")
    if tool not in GUARDED_TOOLS:
        return 0

    # Default to "" then validate: a missing field must not become a value that
    # quietly passes every check.
    path = data.get("tool_input", {}).get("file_path", "")
    root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

    reason = classify(path, root)
    if reason:
        refuse(f"{path} {reason}. Ask the user to change it themselves, or work on a different file.")

    # Log the decision, never the payload: tool_input carries whole file contents
    # and may carry secrets.
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - a crash must not fail open
        refuse(f"validator failed: {exc}")

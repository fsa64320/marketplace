#!/bin/bash
# Observer hook: record that an action happened, and never interfere.
#
# An observer must get out of the way when it fails — the opposite of the
# gatekeeper in hook-guard.py. It therefore always exits 0.
#
# Test it before installing it:
#   echo '{"tool_name":"Write","tool_input":{"file_path":"a.txt"}}' | ./hook-observer.sh
#   echo '{}' | ./hook-observer.sh
#   echo '' | ./hook-observer.sh
#
set -uo pipefail
# Deliberately no `-e`: a logging failure must not stop the user working.

# <Adjust: where the record goes. Never inside the project, or the hook logs itself.>
LOG="${CLAUDE_PROJECT_DIR:-$PWD}/../hook-audit.log"

input=$(cat) || exit 0

if ! command -v jq >/dev/null 2>&1; then
    # Say what is missing, once, and get out of the way.
    echo "hook-observer: jq not found, nothing recorded" >&2
    exit 0
fi

# Parse as JSON, not with text matching: file contents travel in this payload and
# will defeat any pattern.
tool=$(jq -r '.tool_name // "unknown"' <<< "$input" 2>/dev/null) || exit 0
path=$(jq -r '.tool_input.file_path // ""' <<< "$input" 2>/dev/null) || exit 0

# Record the decision, never the payload. `.tool_input` holds the whole content of a
# written file, so logging it would copy everything the agent touched into a file with
# no access control.
printf '%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$tool" "$path" >> "$LOG" 2>/dev/null

# Always succeed. An observer cannot block, and must not try.
exit 0

# Events, and the contract

Adapted from the `hooks-builder` skill of claude-vibes (MIT).

**This file is the platform-specific one.** Everything below is Claude Code's, taken from
its documentation. Treat it as a map of what to look for, and confirm on the build you
target before relying on a detail.

## The events

Grouped by the role they can play, which is the property that decides your design.

### Gatekeepers — can refuse the action

| Event | Fires |
| --- | --- |
| `PreToolUse` | before a tool runs |
| `PermissionRequest` | when a permission dialog would be shown |
| `UserPromptSubmit` | when the user submits a prompt |

These are the only ones that can stop something. If the requirement is "prevent", it
has to be one of these.

### Observers — cannot refuse

| Event | Fires |
| --- | --- |
| `PostToolUse` | after a tool succeeds |
| `Notification` | when a notification is sent |
| `SessionStart` | at session start |
| `SessionEnd` | at session end |
| `PreCompact` | before context compaction |

Asking an observer to block is the most common design error. `PostToolUse` in
particular cannot undo what already happened — a formatter belongs here, a validator
does not.

### Controllers — can force continuation

| Event | Fires |
| --- | --- |
| `Stop` | when the agent finishes responding |
| `SubagentStop` | when a delegated agent finishes |

## The exit-code contract

| Exit | Meaning |
| --- | --- |
| `0` | success; stdout may carry a structured decision |
| `2` | **blocking** — stderr is shown to the agent |
| anything else | non-blocking error, visible only in debug output |

**The trap, and it is the one that matters most**: `exit 1` does *not* block. A
validator that reports a problem and exits 1 has done nothing except write to a log
nobody reads. If the hook must refuse, it exits **2**, and the reason goes to stderr
because that is what the agent is shown.

This is also why step 4 of `SKILL.md` insists on deciding the failure path first: a
script that crashes exits with something that is neither 0 nor 2, which means it
**fails open**. For a gatekeeper that is the wrong default, so it must catch its own
errors and exit 2 deliberately.

## Filtering

Hooks are matched against the action, typically by tool name, with pattern support —
an exact name, alternatives, a prefix, everything. Two properties worth checking on
your build before relying on them:

- **Matching is case-sensitive.** A lowercased tool name matches nothing, silently.
- **A filter that is too broad is a cost as well as a risk**: it fires on every
  action, and a slow hook is felt on all of them.

Name, in the hand-back, both what the filter misses and what it catches unintentionally.
The second is what makes people work around a hook.

## The payload

The hook receives structured data on standard input, carrying at least the event name,
the tool name and the tool's input. Read it as structured data — the whole of
`security.md` follows from the fact that these values are machine-generated and may be
hostile.

Do not assume a field is present. A script that reads a missing field and proceeds with
an empty value is the mechanism behind "the hook allowed something it should have
blocked".

## Where the configuration lives

Hooks are declared in the harness's settings, at three scopes: personal, project
(shared and committed), and a local override that is not committed. The project scope
is the one that reaches a team, and therefore the one that needs review — installing a
project hook means running someone else's shell on your machine.

**Deliberately not reproduced here**: the exact file paths and JSON shape. They are the
harness's, they change, and `SKILL.md` must not name them. Read them from the harness's
own documentation at the moment you write the hook, and confirm with its own hook
listing that what you wrote was registered.

## Useful context the harness provides

The environment typically exposes the project root and a plugin root to the hook
process. Prefer them to a hardcoded path: a hook with an absolute path in it works on
exactly one machine.

## Not verified

Everything in this file. Specifically worth testing before you depend on it: whether
`exit 1` is really non-blocking on your build, whether the filter is case-sensitive,
and which fields the payload actually carries for the event you chose. The method is
step 6 of `SKILL.md` — mock input costs a minute and settles all three.

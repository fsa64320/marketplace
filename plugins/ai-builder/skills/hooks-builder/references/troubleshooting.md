# When a hook misbehaves

Symptom, then the check that discriminates, then the fix.

Work in this order, because it separates the two halves cleanly: **test the script with
mock input first.** If it behaves correctly on a hand-written payload, the problem is
configuration; if it does not, the problem is logic, and no amount of settings fiddling
will help. Step 6 of `SKILL.md` is that test.

## It never fires

Configuration, almost always.

| Check | How | If it fails |
| --- | --- | --- |
| Is it registered? | The harness's own hook listing | Not loaded — settings not read, or JSON invalid |
| Is the settings JSON valid? | Parse it | One trailing comma drops the whole file, silently |
| Is the event right? | See `events.md` | An observer where a gatekeeper was meant, or an event that does not fire for that action |
| Does the filter match? | Compare literally, character by character | **Matching is case-sensitive** — a lowercased tool name matches nothing |
| Is the script reachable? | Run its path from a shell | A relative path resolved from an unexpected directory |
| Is the script executable? | — | Missing execute permission, or missing shebang |
| Is the session new? | — | Settings are read at session start |

The case-sensitivity row is the single most common cause. It fails silently, which is
what makes it expensive.

## It fires, but blocks nothing

This is the failure that matters, because the hook looks installed and protects nothing.

| Cause | Fix |
| --- | --- |
| The event cannot block | An observer has no veto. Move to a gatekeeper event — `events.md` |
| The script exits `1` | **`exit 1` does not block.** Refusing requires `exit 2` |
| The script crashes | A crash exits non-2, so it fails **open**. Catch and exit 2 deliberately |
| The reason goes to stdout | The blocking message must go to stderr, which is what the agent is shown |
| The field being checked is absent | A missing field read as empty passes every check. Default and validate |

Verify by breaking it on purpose — step 7 of `SKILL.md`. A gatekeeper that has never
been observed to refuse has not been tested.

## It blocks too much

Not merely an annoyance: an over-broad hook gets disabled, and a disabled hook protects
nothing.

- Narrow the filter to the actions the rule is really about.
- Make the refusal message say *why* and *what to do instead*. A block with no reason
  gets routed around rather than fixed.
- Consider whether the rule belongs at a later event. A formatter that blocks a write
  should have been an observer running after it.

## It fires twice, or fires on itself

- Two entries match the same action — check for an overlapping filter as well as a
  duplicate.
- The hook's own actions trigger it again. A hook that writes a file, on an event that
  fires for writes, is a loop. Exclude its own output path, or move to an event that
  cannot see it.

## It works for me, not for a colleague

- The hook is personal rather than project scope, so it was never shared.
- The script path is absolute and exists on one machine. Use the project root the
  harness provides.
- A dependency is missing — the JSON parser, the interpreter, the formatter it calls.
  Check for it and exit with a clear message rather than failing obscurely.
- The colleague is on another platform. **A hook does not travel**: event names, the
  settings shape and the exit contract are one harness's. There is no portable version
  to fall back to.

## It slows everything down

A hook on a broad filter runs on every matching action, and the user feels the sum.

- Narrow the filter first; it is usually enough.
- Set a timeout, so a hanging hook degrades instead of blocking the session.
- Move expensive work off the hot path: record on the event, process later.

## What no command will tell you

Nothing validates a hook. The settings file parses or it does not; beyond that, an
event that never fires, a filter that matches nothing and a validator that fails open
all look identical from outside — like a hook that is installed and quiet.

Which is why the two verifications in `SKILL.md` are not optional: mock input for the
logic, and deliberately breaking it for the failure path.

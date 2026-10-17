---
name: hooks-builder
description: >
  Builds an event-driven hook — automation that fires on a harness event to observe,
  block or modify an action — and diagnoses one that never fires or blocks the wrong
  thing. Covers choosing the event, fail-safe defaults, the injection risks of running
  shell with the user's rights, and testing with mock input. Least portable of the
  four builders, and says so.
  Use when the user asks "create a hook", "block dangerous commands", "run a formatter
  automatically", "audit every tool call", "validate before writing a file", "why is my
  hook not firing", "why does my hook not block anything", "should this be a hook or a
  skill". Also triggers on « crée-moi un hook », « pourquoi mon hook ne bloque pas »,
  « automatiser une vérification avant écriture ».
license: proprietary
---

# Hooks builder

## What this skill does

Turns a rule the user wants enforced automatically into a hook that fires on the
right event, fails safe, and cannot be turned against them.

## Read this before anything else

**A hook is the least portable artifact of the four, and the only one that runs code
with the user's own rights.** Two consequences that shape every step below:

- **The mechanism does not travel.** Event names, the configuration file, the exit-code
  contract and the JSON payload all belong to one harness. A skill or a command can be
  written once for several platforms; a hook cannot. What travels is the *reasoning* —
  which event, observe versus block, fail safe, quote everything — and that is what
  this body holds. The mechanism is confined to `references/events.md`.
- **A hook executes shell with the user's permissions, on input the agent produced.**
  That makes it the one artifact where a mistake is a security incident rather than a
  wrong answer. `references/security.md` is not optional reading.

If the user wants something portable, say plainly that a hook is not it, and check
step 1 first — most requests that arrive as "add a hook" are better served otherwise.

## Procedure

### 1. Confirm a hook is the right artifact

A hook fires whether or not anyone wants it to. That is its value and its whole risk.

| The task… | Build | Because |
| --- | --- | --- |
| must happen every time, without being asked | **a hook** | no invocation, no discovery |
| must *prevent* something | **a hook** | nothing else can veto an action |
| adds knowledge the agent should apply | **a skill** | discovery, and no side effects |
| is a prompt the user triggers | **a command** | explicit invocation |
| is delegable work in its own context | **an agent** | isolation |

If the rule only matters sometimes, it is not a hook — a hook that fires when it
should not is worse than no hook, because people work around it.

### 2. Choose the event, and check it can do what you need

Ask what must happen and *when*, then match it. The decisive property is whether the
event can **block**: an observation point cannot stop anything, and asking it to is
the most common design error.

Three roles, and they map to different events:

- **Observer** — records, never interferes. Logging, metrics, audit.
- **Gatekeeper** — can refuse the action. Validation, protection, policy.
- **Transformer** — can alter the action's input before it runs.

Which events exist and which role each supports: `references/events.md`.

### 3. Narrow what it fires on

An unfiltered hook runs on everything, which multiplies both its cost and its blast
radius. Restrict it to the actions it is actually about — the narrowest filter that
still catches every case you care about.

State the filter's failure modes out loud: what it will miss, and what it will catch
that you did not intend. Both matter, and the second is what generates workarounds.

### 4. Decide the failure behaviour first, not last

Before writing any logic, answer: **if the hook itself breaks, should the action
proceed?**

- For a **gatekeeper**, no. A validator that crashes must refuse, not wave things
  through — otherwise the protection disappears exactly when something is unusual.
- For an **observer**, yes. A logger that cannot write must not stop the user working.

Write that answer down in the script as the default path. It is the single decision
that most determines whether the hook is trustworthy.

### 5. Write it, defensively

The input is machine-generated and may contain anything, including paths chosen to
break your script. Non-negotiables, with the reasoning in `references/security.md`:

- Parse the input as structured data, never with text pattern matching.
- Quote every variable, and use the argument terminator so a value cannot become a
  flag.
- Validate paths rather than trusting them.
- Never log the payload wholesale — it carries file contents and may carry secrets.
- No privilege escalation, ever. It already runs as the user.

Keep the logic in a script beside the configuration rather than inline once it is more
than one command: inline shell inside a configuration file cannot be tested.

### 6. Test with mock input before installing it

A hook is the one artifact you can fully test **without the harness**, and doing so
first is much cheaper than debugging it live.

Feed the script a hand-written payload and check the exit status and the output. Then
the cases that matter more than the happy path:

- empty input, and input missing the field the script reads
- a path containing a space, a quote, a leading dash, and `..`
- a value that would be dangerous if interpolated unquoted
- an oversized payload

Only then install it, trigger the real action, and confirm it fires. A hook that
passes mock input but never fires is a configuration problem, not a logic one — see
`references/troubleshooting.md`.

### 7. Verify it fails safe

Deliberately break the hook — rename its script, or make it exit unexpectedly — and
confirm the behaviour matches the decision from step 4. This is the step that gets
skipped, and it is the only one that proves the protection is real.

### 8. Hand back

## Expected output format

| Item | Value |
| --- | --- |
| Hook | `<name>` |
| Event | `<event, and the role: observer / gatekeeper / transformer>` |
| Chosen over | `<skill / command / agent, and why>` |
| Fires on | `<the filter, and what it deliberately misses>` |
| On its own failure | `<refuses / allows, and why that is right here>` |
| Mock cases passed | `<the list, including the hostile paths>` |
| Fail-safe verified | `<how it was broken, and what happened>` |
| Platform | `<the harness — a hook does not travel>` |
| Next step | Watch it in real use for a week before widening the filter |

## Additional resources

- `references/events.md` — the events, their roles, the exit-code contract and the
  payload, per platform
- `references/security.md` — why a hook is the risky one, and the patterns that hold
- `references/troubleshooting.md` — never fires, blocks everything, fails open
- `assets/hook-guard.py` and `assets/hook-observer.sh` — copy these

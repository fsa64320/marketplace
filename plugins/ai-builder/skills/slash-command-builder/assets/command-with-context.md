---
description: <What it does, in one line. Shown in the command listing.>
argument-hint: [<input>]
# Single-platform on purpose: the capability names below belong to one harness.
# Scope to the narrowest command family that works, and delete this block for a
# command distributed to several platforms.
allowed-tools: Read, Grep, Glob
---

## Context

<Gather what the prompt needs, rather than assuming the conversation supplies it.
Two mechanisms, both resolved before the model sees the prompt:

  - inline the output of a command — requires the shell capability above, scoped
  - inline a file's contents by referring to its path with an @ prefix

Verify the exact form on the target build with a one-line probe command before
relying on it: the form `[execute: ...]` does NOT work, and it
fails silently by passing through as literal text. See references/syntax.md.>

## Task

<What to do with the context above and $ARGUMENTS.>

If the context section came through as literal placeholder text, nothing was
gathered: say so and stop. Do not reason about the placeholder — that failure looks
like a working command.

## Constraints

- Do not modify any file. Report; the user decides.
- <Other boundaries.>
- State nothing that was not in the gathered context.

## Output format

### Verdict
<One line.>

### Findings
| <Column> | <Column> | <Column> |
| --- | --- | --- |

### Not examined
<Anything in scope that could not be reached, and why.>

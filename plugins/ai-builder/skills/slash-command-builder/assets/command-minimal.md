---
description: <What it does, in one line. Shown in the command listing.>
argument-hint: [<the one free-text input>]
---

## Task

<What to do with $ARGUMENTS. Imperative, one paragraph.>

If $ARGUMENTS is empty, say so and stop rather than proceeding — an empty
placeholder produces a confident answer about nothing.

## Constraints

- <What not to do.>
- <The boundary to respect.>

## Output format

<The actual shape, shown rather than described:>

| <Column> | <Column> |
| --- | --- |

<!--
The filename minus .md is the command name. Lowercase and hyphens.

$ARGUMENTS is used here on purpose: it takes the whole invocation as one block and
cannot be off by one. Positional $1/$2 are offset — $1 is the SECOND word.
See references/syntax.md before using them.

No allowed-tools declared: the key travels between platforms, the capability names
inside it do not. Add it only if this command is deliberately single-platform, and
scope it to the narrowest command family that works.
-->

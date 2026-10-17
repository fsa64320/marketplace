# Command syntax

Adapted from the `slash-command-builder` skill of claude-vibes (MIT).

## Shape

A command is a Markdown file: optional YAML frontmatter, then the prompt. There is
**no `name` field**; the filename minus `.md` is the command name.

```markdown
---
description: What it does, shown in the command listing
argument-hint: [file] [priority]
---

## Context
...

## Task
...
```

`probe-cmd.md` is invoked as `/probe-cmd`. Naming follows
the filename's constraints — lowercase, hyphens, no spaces.

## Arguments — and the off-by-one

Two forms:

| Form | Substituted with |
| --- | --- |
| `$ARGUMENTS` | everything the user typed after the command name, as one block |
| `$1`, `$2`, `$3`… | positional parameters |

In a non-interactive session:

```
/probe-cmd ALPHA BRAVO CHARLIE

  $ARGUMENTS = ALPHA BRAVO CHARLIE
  $1         = BRAVO
  $2         = CHARLIE
  $3         = (empty)
```

Confirmed by a second run with different values (`hello world` gave `$1 = world`).

**`$1` is the second word, not the first.** The positional numbering is offset by
one: the first token after the command name is not reachable through `$1`, and the
last positional resolves to empty. Every guide documents `$1` as the first argument —
including the source this file is adapted from, whose example `Review PR #$1 with
priority $2` would silently read the priority as the PR number.

Consequences, and they are the practical value of this file:

- **Prefer `$ARGUMENTS` whenever the command takes one free-text input.** It is
  correct, and it cannot be off by one.
- **If you use positionals, verify the mapping with distinguishable values.** Testing
  with `a b c` cannot reveal an offset; `ALPHA BRAVO CHARLIE` can.
- **Never document a positional contract you have not run.** Write the mapping you
  observed, not the one you expect.

**Not verified**: whether the offset also applies to an interactive invocation. In a
non-interactive session the whole line is parsed as a prompt, which is a plausible
cause. Confirm interactively before relying on the
numbering — and prefer `$ARGUMENTS`, which sidesteps the question entirely.

## Gathering context

Two mechanisms, both resolved before the prompt reaches the model:

- **Command output** — run something and inline its result. Requires the shell
  capability to be declared in the frontmatter, scoped to the command family used.
- **File reference** — inline a file's contents by referring to its path with an `@`
  prefix. A directory yields a listing, not contents.

**A correction to the source**: the form `[execute: echo X]`
that the source documents **does not execute**. It came through as literal text in
the rendered prompt. The source's own wording contradicts itself on this point,
telling the reader "backticks required" while showing a form with no backticks — the
sign of a syntax mangled in transcription. Do not copy it.

The reliable test is the one in step 7 of `SKILL.md`: if the placeholder appears
verbatim in the output, nothing was gathered. That failure is silent, and it looks
like a working command, because the model will happily reason about the literal text.

**Not verified here**: the exact working form of the command-output syntax on the
current build. Establish it by running a one-line probe command before writing any
command that depends on it, rather than trusting a guide — including this one.

## Frontmatter fields

| Field | Purpose |
| --- | --- |
| `description` | shown in the command listing; write it even though it is optional |
| `argument-hint` | the expected argument shape, shown at invocation |
| `allowed-tools` | capability restriction, scoped per command family |
| `model` | model override for this command |
| `disable-model-invocation` | prevents the agent calling the command on its own |

`description` and `argument-hint` are the two that pay for themselves immediately:
the first makes the command findable, the second makes its contract visible at the
moment the user types it.

**Platform note**: `allowed-tools` is the same key skills use, and the same caveat
applies — the key travels between harnesses, the capability names inside it do not.
Omit it for a command distributed to several platforms.

**Not verified**: whether `model` and `disable-model-invocation` behave as documented.

## Capability scoping

Narrow to the command family the prompt actually runs:

```yaml
allowed-tools: Bash(git:*)                       # git, nothing else
allowed-tools: Bash(git diff:*), Bash(git log:*) # two specific subcommands
allowed-tools: Read, Grep, Glob                  # read-only
```

A command that only reads files should not be able to write them. The restriction
costs one line and removes a whole class of accident.

---
name: slash-command-builder
description: >
  Builds a user-invoked command — a saved prompt the user calls by name, with
  arguments, gathered context and file references — and diagnoses one that does not
  appear or substitutes the wrong argument. Covers choosing a command over a skill,
  the argument forms and their off-by-one, and testing before hand-back.
  Use when the user asks "create a slash command", "make me a /command", "turn this
  prompt into a command", "how do I pass arguments to a command", "why does my
  command get the wrong argument", "why is my command not listed", "should this be
  a command or a skill", "review my command file". Also triggers on « crée-moi une
  commande », « pourquoi ma commande ne s'affiche pas », « commande ou skill ».
license: proprietary
---

# Slash command builder

## What this skill does

Turns a prompt the user retypes into a command they invoke by name, with the
arguments and context it needs, and diagnoses one that misbehaves.

**It produces a platform-independent artifact where it can.** A command is a
Markdown file: frontmatter, then the prompt. That shape travels. The dynamic
features — argument placeholders, gathered context, file references — are the
harness's, and they are isolated in `references/syntax.md`. Placing the file is the
transport's job; no step below names an install path.

## The distinction that decides everything

**A command is invoked by the user. A skill is chosen by the agent.**

| The task… | Build | Because |
| --- | --- | --- |
| is a prompt the user retypes, and *they* decide when | **a command** | invocation is explicit, no discovery needed |
| the agent should recognise and apply on its own | **a skill** | the description drives automatic activation |
| is multi-step and wants its own clean context | **an agent** | isolation, and its own capabilities |
| should run automatically on an event | **a hook** | no invocation at all |
| is one sentence used once | **nothing** | just ask |

A command therefore needs **no trigger phrases** — that whole discipline is
irrelevant here, and it is the most common confusion when coming from skills. What a
command needs instead is a `description` for the listing, and an accurate argument
contract.

## The thing to establish first: the filename is the command name

There is no `name` field. The filename minus `.md` is the command name, so the naming
rule is the filename's: lowercase, hyphens, no spaces.

Unlike a skill (directory wins) or an agent (`name:` field wins), here there is only
one candidate — which makes this the one identity rule of the four that cannot be got
wrong.

## Procedure

### 1. Confirm a command is the right artifact

Use the table above. If the user cannot say *when they would type it*, it is not a
command — it is a skill, and the discovery work belongs there.

### 2. Get the prompt itself

Ask for the prompt they retype today, verbatim. Do not improve it yet: the point of
a command is to preserve something that already works.

Then ask what varies between uses. That, and only that, becomes an argument.

### 3. Choose the argument form deliberately

Two forms, and they are not interchangeable. **The positional form is off by one,
contrary to what almost every guide states — read `references/syntax.md` before using
it, and do not trust your recollection of the numbering.**

- **All-in-one** — the whole invocation as a single block. Right for free text: a
  message, a description, a question.
- **Positional** — separate parameters used in different places. Right for a
  structured contract, and the form that needs the offset check.

If the command takes exactly one free-text input, use the all-in-one form. It is
correct, and it cannot be off by one.

Declare an argument hint so the user sees the expected shape when they invoke it.

### 4. Gather the context the prompt assumes

A command runs in the user's current session, so it *does* see the conversation —
the opposite of an agent. But the prompt should still not depend on it, because the
whole value is reproducibility.

Where the prompt needs facts, have the command fetch them: command output for state,
file references for content. Exact syntax and the capability each one requires:
`references/syntax.md`.

### 5. Restrict capabilities to what the prompt uses

If the command gathers context by running something, it needs that capability
declared, scoped to the narrowest command family that works. A command that only
reads should be able to do nothing else.

The field name and its scoping syntax are the harness's — `references/syntax.md`.
For a command distributed to several platforms, declare nothing and say in the prompt
what it expects.

### 6. Structure the prompt

Three sections carry almost every useful command:

```
## Context      what was gathered, or referenced
## Task         what to do with it, imperatively
## Constraints  what not to do, and the output shape
```

State the output shape rather than describing it. A command whose output varies each
run is a command the user stops trusting.

### 7. Test, in this order

1. **It is listed.** Open a fresh session and check the command appears under its
   filename.
2. **It runs bare.** Invoke it with no arguments. It should either work or say
   plainly what it needs — never silently produce a result built from an empty
   placeholder.
3. **Each argument lands where you meant.** Invoke it with distinctive values, one
   per position — `ALPHA BRAVO CHARLIE`, not `a b c` — and confirm each appears in
   the right slot. **This is the step that catches the positional offset**, and
   indistinguishable test values are exactly why it gets missed.
4. **Gathering works.** If the command fetches context, confirm it appears in the
   prompt rather than as literal placeholder text — that failure mode looks like a
   working command.

Diagnosis for every other symptom: `references/troubleshooting.md`.

### 8. Hand back

## Expected output format

| Item | Value |
| --- | --- |
| Command | `/<name>` |
| Chosen over | `<skill / agent / hook, and why>` |
| Arguments | `<none, all-in-one, or the positional contract>` |
| Offset verified | `<the distinctive values used, and where each landed>` |
| Context gathered | `<what, and the capability it needs>` |
| Platform coupling | `<none, or the platform and why>` |
| Listed as | `<the name it appeared under>` |
| Next step | Use it in real conditions for a week |

## Additional resources

- `references/syntax.md` — the argument forms, the off-by-one, frontmatter,
  context gathering and file references
- `references/platforms.md` — who places the file, and how to verify per harness
- `references/troubleshooting.md` — not listed, wrong argument, placeholder leaking
- `assets/command-minimal.md` and `assets/command-with-context.md` — copy these

---
name: skill-builder
description: >
  Builds an agent skill from a described procedure and diagnoses one that does not
  load or does not trigger: the frontmatter a runtime reads, a body written as a
  procedure, the split into references/, and a lint plus a load test before
  hand-back. Platform-independent — the transport places the files.
  Use when the user asks "create a skill", "write a skill", "make me a skill for
  this", "turn this repetitive task into a skill", "what goes in SKILL.md",
  "why is my skill not triggering", "why does my skill not load", "review my
  SKILL.md", "how do I restrict which tools a skill can use", "will this skill
  work on another platform". Also triggers on « crée-moi un skill », « pourquoi
  mon skill ne se déclenche pas », « relis mon SKILL.md ».
license: proprietary
---

# Skill builder

## What this skill does

Turns a described procedure into a skill folder that loads, triggers reliably and
stays lean — and diagnoses one that does neither. It is self-contained: nothing
here hands the work to another skill.

**It produces a platform-independent artifact.** The skill directory is the
deliverable; placing it in a harness is the transport's job, not the skill's. So no
step below names an install path, and neither should anything you write.

## When not to use it

- For a task carried out once. A skill only pays off on repetition.
- To change a skill you do not own: raise it with its owner instead.

## The thing to establish first

**The directory name is the skill's identity.** The `name:` field does not override
it: a skill whose directory and `name:` disagree loads, and answers to the directory.

Capitals and spaces in a directory name load too, so nothing warns you. The failure
is not a crash — it is a skill addressed by one string and self-described by
another. Make the two agree, in kebab-case.

Note the direction, because an **agent** is the reverse: there the `name:` field wins
and the filename is a container. The evidence for both is in
`references/frontmatter.md`.

## Procedure

### 1. Qualify the need

Interview the user; do not infer the answers. Ask, and wait:

1. How many times a month do you do this task?
2. How do you do it today, step by step?
3. What varies from one time to the next, and what never varies?

Under once a month, or a procedure that changes entirely each time: say plainly
that a skill will bring nothing, and propose a note or a document template.

### 2. Get the scope into one sentence

Have the user complete: "this skill <verb> <object> to <result>".

If it needs "and" between two verbs, there are two skills. Say so and propose the
split — a catch-all triggers badly and is the hardest fault to correct later.

### 3. Collect the trigger phrases

Ask what they will actually type when they want this. Take at least four, in their
words, and keep their phrasing rather than tidying it.

This is the only text read to decide whether the skill activates, so it decides
whether anything else in the folder is ever seen. Ask for the phrases a *colleague*
would use too: the author's own vocabulary is systematically too narrow.

Craft the field from them following `references/descriptions.md` — the formula, the
before/after pairs, and what to cut first when it runs over 1,024 characters.

### 4. Fix the name

Normalise it mechanically: lowercase, spaces to hyphens, drop anything outside
`a-z0-9-`, collapse repeated hyphens, 64 characters maximum. `"My PDF Tool"` becomes
`my-pdf-tool`. The directory takes the same string.

Do **not** ask where the skill will be installed. Ask instead whether it must run on
more than one platform — the answer changes one thing only, whether `allowed-tools`
is declared at all. See `references/platforms.md`.

### 5. Write the frontmatter

Two keys are read by every runtime: `name` and `description`. A third,
`allowed-tools`, is part of the format but carries platform-specific tool names —
omit it unless the skill is deliberately single-platform.

Semantics, limits and traps in `references/frontmatter.md`. Read it before writing:
the key is spelled `allowed-tools`, and a skill using `tools:` restricts nothing
while believing it does.

### 6. Write the body as a procedure

Numbered steps, each one concrete action: read a file, ask a question, run a
command, produce a table. A step that states an intention is not a step.

Address the agent, not a reader. Prerequisites like "a text editor", difficulty
ratings and estimated times are documentation furniture: they are loaded every time
the skill fires and change no behaviour.

Refer to companion files by a path **relative to the skill directory** —
`references/<subject>.md`, `scripts/<tool>.py`. That is the portability seam:
relative paths survive every deploy directory, absolute ones pick a platform.

Finish with the output format **shown, not described** — the actual table with its
columns. That is what makes results reproducible across runs.

### 7. Split it

Keep the body short enough to be worth loading in full every time; move the rest
into `references/`, one file per subject, linked from the body.

Templates and long examples go in `assets/` as **real files**, never pasted into a
fenced block: a fenced block inside a fenced block closes the outer one early and
silently swallows everything after it. Start from `assets/template-minimal/` or
`assets/template-with-script/`, copy the directory, then rename
`SKILL.md.template` to `SKILL.md` (the suffix stops the template from loading as a
skill of its own).

A skill that ships a script keeps it to the deterministic part — parse, count,
validate, render — and keeps every function small: follow `references/scripts.md`.

### 8. Lint it

```bash
python scripts/lint_skill.py <skill-directory>
```

Fourteen mechanical checks, exit code 2 on error, no third-party dependency. Reach
zero errors before going further, and read the warnings out loud to the user rather
than silently accepting them.

Add `--platform <name>` when the skill is deliberately single-platform; the default
is the portable profile, which flags anything that couples the skill to one harness.

The interpreter is `python` on a Windows workstation, where `python3` is not on
`PATH`, and `python3` on macOS and Linux. Try the other one on `command not found`
rather than concluding the script is missing.

### 9. Prove it loads, then that it triggers

The portable check needs no CLI: open a fresh session on the target harness and make
three of the phrases from step 3, unchanged.

Then make two requests that must **not** fire it — a neighbouring domain, and a
vague request. A skill that fires on those is miscalibrated, and the fix is the
scope sentence from step 2, not the trigger phrases.

If it does not fire on its own phrases, the fix is in the `description`, never in the
body: the body is not read until after the decision to activate.

Per-platform shortcuts where one exists, and what no command will tell you:
`references/platforms.md`. Diagnosis for every other symptom:
`references/troubleshooting.md`.

### 10. Hand back

## Expected output format

| Item | Value |
| --- | --- |
| Skill | `<name>` |
| Trigger phrases | `<count>` |
| Description length | `<count>` / 1,024 characters |
| Body length | `<count>` words |
| `references/` | `<files, or none>` |
| Platform coupling | `<none, or the platform and why>` |
| Lint | `<n>` errors, `<n>` warnings |
| Fired on | `<the phrases that triggered it>` |
| Did not fire on | `<the two negative controls>` |
| Next step | Use it in real conditions for a week |

## Additional resources

- `references/descriptions.md` — the description formula, before/after, how to cut
- `references/frontmatter.md` — the portable core, and what is platform-dependent
- `references/platforms.md` — who places the files, targets, per-platform checks
- `references/troubleshooting.md` — does not load, does not trigger, fires wrongly
- `references/scripts.md` — what goes in a script, and how to keep it small
- `scripts/lint_skill.py` — the fourteen checks
- `assets/template-minimal/` and `assets/template-with-script/` — copy these (rename `SKILL.md.template` to `SKILL.md`)

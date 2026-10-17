# When a command misbehaves

Symptom, then the check that discriminates, then the fix.

The governing distinction: **a command is invoked, not discovered.** So there is no
"it was never picked" failure here, and no description tuning to do — if the user
typed the name and nothing happened, the file is not where the harness looks or is
not parsing. That makes command failures faster to diagnose than skill or agent ones.

## It is not listed

| Check | How | If it fails |
| --- | --- | --- |
| Is the extension `.md`? | List the directory | A command without it is not seen |
| Is the filename usable as a name? | lowercase, hyphens, no spaces | The filename *is* the command name |
| Does the frontmatter parse? | Line 1 `---`, a closing `---`, values with `:` quoted, spaces not tabs | A YAML error drops the file silently |
| Is it in the directory the harness reads? | See `platforms.md` | Or the transport put it elsewhere — `apm install --dry-run` |
| Is the session new? | — | Commands are read at session start |

## It runs, but an argument is wrong

**Check this before anything else, because it is counter-intuitive.**

`$1` resolves to the **second** word of the invocation, not the first.
`/cmd ALPHA BRAVO` gives `$1 = BRAVO`.

| Symptom | Cause | Fix |
| --- | --- | --- |
| Everything is shifted by one slot | The positional offset | Renumber, or switch to `$ARGUMENTS` |
| The last positional is empty | Same cause, seen from the other end | As above |
| One argument holds the whole invocation | `$ARGUMENTS` used where positionals were meant | Choose one form deliberately |
| It looks right in testing, wrong in use | Test values were indistinguishable | Retest with `ALPHA BRAVO CHARLIE` |

The last row is the trap worth naming: testing with `a b c`, or with values that read
plausibly in any slot, cannot reveal an offset. Distinguishable values can.

## The placeholder appears verbatim in the output

Nothing was substituted or gathered, and **the command still produced an answer** —
the model reasoned about the literal placeholder text. This is the most dangerous
failure mode here, because the output looks like a result.

| Cause | Fix |
| --- | --- |
| Placeholder misspelled | Check the exact sigil, case included |
| No arguments passed at invocation | Have the command say what it needs rather than proceeding |
| Context-gathering syntax wrong | See `references/syntax.md` — the form `[execute: …]` does **not** work |
| Missing capability for the gathering | Declare the shell capability, scoped to the command family used |
| Referenced file does not exist | Verify the path; a reference that resolves to nothing is silent |

Guard against it in the prompt: "if the argument is empty, say so and stop" costs one
line and converts a silent wrong answer into a clear question.

## It runs, but the output varies every time

The prompt describes the output instead of showing it. Paste the actual shape — the
table with its columns, the sections in order. A command exists to be reproducible;
an unspecified output format removes the only reason to save it.

## It runs, but does more than expected

| Symptom | Cause | Fix |
| --- | --- | --- |
| Modifies files when it should report | No constraint, and the capability allows it | Add the constraint to the prompt **and** narrow the capability |
| Runs commands nobody asked for | Shell capability unscoped | Scope to the command family the prompt names |
| Behaves differently across sessions | The prompt leans on conversation context | A command sees the conversation, but should not depend on it — gather what it needs |

That last row is the difference from an agent: a command *does* see the session. It is
a convenience that quietly makes commands unreproducible, so treat context as
something to gather, not to inherit.

## It works here, not for a colleague

- The command is personal rather than shared, so it was never distributed. See
  `platforms.md`.
- It uses a dynamic feature the colleague's harness does not have. A command with no
  arguments and no gathering is portable; each feature added is a platform commitment.
- It references a file that exists only locally. Reference paths inside the repository,
  never absolute ones.

# When a skill misbehaves

Symptom, then the check that discriminates, then the fix. The checks are ordered so
the cheapest decisive one comes first.

Run `scripts/lint_skill.py` before working down any of these: it catches ten of the
causes below mechanically, on every platform.

## It does not appear at all

Platform-neutral causes first — these are the ones that account for most of it:

| Check | How | If it fails |
| --- | --- | --- |
| Is the file named exactly `SKILL.md`? | List the directory | Rename. `Skill.md` is not it on a case-sensitive filesystem. |
| Is it exactly one level down? | The skill directory holds `SKILL.md` directly | A skill nested one level deeper is not found. Flatten it. |
| Does the frontmatter parse? | Line 1 holds `---`, there is a closing `---`, values containing `:` are quoted, indents are spaces not tabs | A YAML error drops the whole skill silently. The linter catches this. |
| Is the session new? | — | Skills are read at session start. Start a fresh one. |
| Did the transport actually place it? | `apm install --dry-run …` shows placement decisions | Wrong or missing target. See `platforms.md` — with nothing to detect, `install` exits 2 rather than guessing. |

Then the platform-specific ones, which only apply on the harness in question:

- **Claude Code plugins** — a component path resolving outside the plugin root is
  rejected as `path escapes plugin directory`, and the plugin loads **without that
  component**, silently. Check the plugin is installed and enabled.
- **Other targets** — no equivalent failure is known. Confirm placement
  first, then fall back to the behavioural check in `platforms.md`.

A malformed `name` is deliberately **not** on this list: it does not prevent loading.
See `frontmatter.md`.

## It loads but never fires

Almost always the `description`, almost never the body — the body is not read until
after the decision to activate. None of this is platform-specific.

1. **Do the user's actual words appear in the field?** Take the exact sentence they
   typed. If none of its distinctive words is there, the agent had nothing to match.
   Add the phrase verbatim.
2. **Is there a "when" clause?** A field that only says what the skill *is* offers no
   trigger.
3. **Is it under 1,024 characters?** Over the limit it is truncated or rejected, and
   the trigger phrases sit at the end — so they are what is lost. Count it.
4. **Does a neighbouring skill cover the same phrases?** Two fields matching the same
   request is a coin toss. Narrow one scope and name the other skill so the request
   has somewhere to go.
5. **Is the wording aimed at a human?** "Use when you need to build custom workflows"
   describes a reader's situation. "Use when the user asks *'build me a skill'*"
   describes a request. Only the second matches anything.

## It fires when it should not

The scope is too wide. Fix the scope sentence, not the trigger phrases — removing
phrases breaks the previous case without fixing this one.

- Two verbs joined by "and" in the scope sentence means two skills. Split.
- Add an explicit exclusion: "Do not use to <adjacent task> — see <skill>." It is read
  at the same moment as the rest and does real work.

## It fires, then behaves inconsistently

Now it *is* the body.

| Symptom | Cause | Fix |
| --- | --- | --- |
| Skips steps, or invents an order | Steps state intentions, not actions | Rewrite each as one concrete action: read, ask, run, produce |
| Output differs every run | The output format is described instead of shown | Paste the actual table with its columns |
| Half the document seems ignored | A fenced block nested in another closed the outer one early; everything after renders as preformatted text and the structure is gone | Move the inner example to `assets/` as a real file, or use quadruple backticks outside |
| Reads files that do not exist | The body links to paths that were never created | The linter checks every relative path in prose; create it or drop the link |
| Works on one platform, not another | An absolute or harness-specific path in the body | Make every companion path relative to the skill directory |
| Cannot reach a tool it is told to use | The tool is missing from a declared `allowed-tools`, the key is written `tools:`, or the names belong to a different harness | See `frontmatter.md`; for a multi-platform skill, omit `allowed-tools` entirely |
| Ignores a declared dependency | Declared only in `metadata.dependencies` | `metadata` is read by nobody at run time. Name it in the body too |
| Wastes context on every run | Prerequisites, difficulty ratings, estimated times, closing exhortations | Delete. They are loaded every time and change no behaviour |

## What no command will tell you

There is no cross-platform skill linter, which is why this skill ships one. And a
manifest validator is not a skill validator: on Claude Code, `claude plugin validate`
passed a skill carrying a malformed `name` and a `tools:` key without comment.

The check that works everywhere is behavioural: start a fresh session on the target
harness and make the real request. Then make two that must **not** fire it, because
over-triggering looks like success.

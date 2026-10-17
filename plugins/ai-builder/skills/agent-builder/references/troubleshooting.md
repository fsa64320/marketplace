# When an agent misbehaves

Symptom, then the check that discriminates, then the fix. Ordered so the cheapest
decisive check comes first.

The governing distinction: **selection failures live in the `description`, behaviour
failures live in the system prompt.** The prompt is not read until after the agent
has been selected, so editing it can never fix a discovery problem — and this is the
single most common wasted effort.

## It is never picked

| Check | How | If it fails |
| --- | --- | --- |
| Does it load at all? | List the available agents in a fresh session | Not loaded — see the next section |
| Do the user's words appear in the `description`? | Take the exact sentence they typed | None of its distinctive words is there. Add the phrase verbatim |
| Does the description name a role and a trigger? | It should carry role, what, when, and the words users type | A description that only states a capability gives nothing to select on |
| Is another agent a closer match? | Compare descriptions side by side | Narrow this one's scope and add an exclusion to the other |
| Is the session new? | — | Definitions are read at session start |

Explicit invocation working while natural requests fail is the signature of this
whole class: the agent is fine, the description is not.

## It does not load

| Check | How | If it fails |
| --- | --- | --- |
| Does the frontmatter parse? | Line 1 is `---`, there is a closing `---`, values containing `:` are quoted, indentation is spaces | A YAML error drops the definition silently |
| Is it in the directory the harness reads? | See `platforms.md` | Wrong location, or the transport deployed elsewhere — `apm install --dry-run` shows placement |
| Is `description` present and non-empty? | — | An agent with no description cannot be selected, and may not be listed |

A malformed `name` is deliberately **not** on this list: measured 2026-09-13, uppercase,
underscores and spaces all load. See `frontmatter.md`.

## The wrong agent is picked

Two descriptions match the same request, and the choice is effectively arbitrary. It
looks like success, because an agent did answer — which is why it goes unnoticed.

- Narrow the scope sentence of whichever agent is broader.
- Add an explicit exclusion to each: "not for <the other one's territory>".
- If the two genuinely overlap, they are one agent. Merge them.

## It is picked, then asks for context

The prompt is not self-contained. This is the defining agent failure and it has one
cause: a step that assumes the conversation.

- The first numbered step under "When invoked" must **acquire** the material, not
  receive it.
- Replace every referent that points outside the prompt. "The file we discussed"
  becomes "the file named in the request"; "the code above" becomes the command that
  produces it.
- Test it the only way that works: invoke it explicitly in a session where nothing
  relevant was discussed.

## It is picked, then acts outside its remit

| Symptom | Cause | Fix |
| --- | --- | --- |
| Modifies files when it should only report | No constraint saying so, or the platform grants the capability | Add the constraint to the prompt **and** narrow the capability field where the platform has one — a prompt constraint is advisory |
| Runs commands nobody asked for | The capability is unrestricted and the prompt does not bound it | Scope to the command families the steps actually name |
| Skips steps, or invents an order | Steps state intentions rather than actions | Rewrite each as one concrete action |
| Output differs every run | The output format is described instead of shown | Paste the actual shape |
| Claims a complete answer from a partial pass | Nothing told it to report gaps | Add a "Not examined" section to the output format |
| Works on one platform, not another | A path or harness field in the definition | Keep the body to the portable core; see `frontmatter.md` |

## It works, but costs too much

- The prompt is paid for on every invocation. Cut restatements of the role, generic
  advice the model already follows, and anything the output format implies.
- An agent doing two jobs pays for both every time. Split it — the scope sentence
  from step 2 of `SKILL.md` is the test.
- Where the platform allows a model choice, match it to the work: a mechanical check
  does not need the most capable model. See `frontmatter.md` for what is measured and
  what is not.

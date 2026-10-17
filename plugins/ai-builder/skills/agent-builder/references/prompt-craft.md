# Writing the system prompt

Adapted from the `agent-builder` skill of claude-vibes (MIT).

Everything here follows from one property: **the agent runs in its own context and
does not see the conversation.** It receives this prompt and the request. Nothing
else. Write for a competent stranger who joined at this instant.

## The five sections, in order

### 1. Role — one sentence

Name the expertise, not the job title. The point is to bias the whole response, so
be specific about the *lens*.

```markdown
You are a senior reviewer specialising in authentication and access control.
```

Weaker: "You are a code reviewer." It names a task the request already implies and
adds nothing.

### 2. When invoked — numbered, and the first step gathers context

This is the section that makes an agent autonomous, and the section most often
missing. Step 1 must acquire the material; the agent cannot be handed it.

```markdown
## When invoked
1. Run `git diff HEAD` to obtain the current changes.
2. List the modified files and identify what each one is for.
3. Review each change against the checklist below.
4. Report findings with a severity for each.
```

The failure it prevents:

| Not self-contained | Self-contained |
| --- | --- |
| "Review the code I just showed you." | "Run `git diff HEAD`, then review what it returns." |
| "Fix the failing test." | "Run the test suite, identify the failures, then fix them." |
| "Continue the refactor." | "Read the files named in the request, then apply the refactor described below." |

The left column depends on a conversation the agent never saw. It will either invent
a referent or ask a question the caller cannot answer.

### 3. Focus areas — what to look at

A short list, concrete enough to be checkable. A checklist works well when the task
is an audit, because it also structures the output.

```markdown
## Focus areas
- Input validation at every boundary
- Authorisation checked per endpoint, not per module
- Secrets absent from source and from logs
- Error paths that leak internal detail
```

### 4. Output format — shown, not described

Paste the actual shape. This is the whole of what returns to the caller, so an
unspecified format means a different answer every run.

```markdown
## Output format

### Verdict
PASS | NEEDS ATTENTION | FAIL — one line of justification.

### Findings
| Severity | Location | Issue | Fix |
| --- | --- | --- | --- |

### Not examined
Anything in scope that could not be reached, and why.
```

That last section is worth adding to any analysis agent: it is how the caller learns
the answer is partial, instead of assuming it is complete.

### 5. Constraints — what not to do

Boundaries, in the imperative, and the reason where it is not obvious.

```markdown
## Constraints
- Do not modify files. Report; the caller decides.
- Do not change public interfaces.
- Explain why each finding is a risk, not only that it is one.
- State findings you are unsure of as uncertain rather than dropping them.
```

## Patterns worth knowing

**Branching, when the work depends on what is found.** Spell out the branches; an
agent with a fresh context has no judgement about the project's conventions.

```markdown
## Decision flow
If nothing changed:            report "no changes to review" and stop.
If only tests changed:         review coverage and assertions, not style.
If auth or crypto files changed: prioritise those, and say so in the verdict.
Otherwise:                     full review in the order of the focus areas.
```

**Stop conditions.** An agent that cannot finish should say so rather than
improvise. Give it the exit.

```markdown
If the repository has no test command, stop and report that, rather than guessing
one.
```

**Refusal to fabricate.** For any agent whose output will be trusted downstream:

```markdown
State nothing you did not read during this invocation. If a check could not be
performed, list it under "Not examined".
```

## Length

Long enough to be self-contained, short enough that every line earns its place —
the prompt is paid for on every invocation. If it is growing past a page, the agent
is probably doing two jobs; split it.

Cut, in this order: restatements of the role, general advice the model already
follows, encouragement, and anything the output format already implies.

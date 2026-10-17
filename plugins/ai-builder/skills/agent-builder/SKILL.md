---
name: agent-builder
description: >
  Builds a delegated agent — a subagent that runs in its own context — and
  diagnoses one that is never picked or acts outside its remit: choosing an agent
  over a skill, the description that drives discovery, a self-contained system
  prompt, least-privilege capabilities, and a discovery test before hand-back.
  Platform-independent — the transport places the file.
  Use when the user asks "create an agent", "make me a subagent", "write a custom
  agent", "delegate this to an agent", "why is my agent never used", "why does
  Claude pick the wrong agent", "how do I restrict what an agent can do", "should
  this be an agent or a skill", "review my agent definition". Also triggers on
  « crée-moi un agent », « pourquoi mon agent n'est jamais appelé », « agent ou
  skill ».
license: proprietary
---

# Agent builder

## What this skill does

Turns a delegable task into an agent definition that gets picked for the right
requests, works without the conversation that produced it, and cannot do more than
its job requires.

**It produces a platform-independent artifact.** The definition is the deliverable;
placing it in a harness is the transport's job. No step below names an install path
or a harness field, and neither should anything you write.

## The property that governs everything

**An agent runs in its own context and does not see the conversation.** It gets its
system prompt and the request, nothing else. Every consequence in this skill follows
from that one fact:

- The prompt must be self-contained. "Review the code I just showed you" has no
  referent; "run `git diff HEAD`, then review what changed" does.
- The agent must gather its own context, as its first numbered step.
- Its output is all that returns. If the format is not specified, the caller gets
  something different every run.

## Second thing to establish: the name is the identity

1. **The `name:` field is the identity; the filename is just a container.** This is
   the *inverse* of a skill, where the directory name wins and the field is ignored.
   Do not carry the skill habit over.
2. A malformed name — uppercase, underscore, space — **loads anyway**. Nothing warns,
   and nothing rejects it; it simply becomes an identifier nobody can type
   comfortably. Use lowercase and hyphens because it is usable, not because it is
   enforced.

Keep the filename equal to the name regardless: it is the only way to find the file
from the identity. Evidence for both points: `references/frontmatter.md`.

## Procedure

### 1. Check that an agent is the right artifact

This is the step people skip, and it is the one that wastes the most effort. Ask
what the task needs, then match:

| The task… | Build | Because |
| --- | --- | --- |
| is multi-step and benefits from a clean slate | **an agent** | its own context, no pollution of the main thread |
| must be barred from certain capabilities | **an agent** | capabilities are declared per agent |
| adds knowledge or a procedure to the main thread | **a skill** | it shares context and loads on demand |
| is a phrasing the user retypes often | **a slash command / prompt file** | user-invoked, no delegation |
| is one step | **nothing** | ask directly; delegation costs more than it saves |

If the task needs the conversation's history to make sense, it is not an agent.
Say so and propose the alternative.

### 2. Get the scope into one sentence

Have the user complete: "this agent <verb> <object> and returns <result>".

Two verbs joined by "and" means two agents. An agent that reviews *and* fixes will
do neither predictably, because the caller cannot tell which it did.

### 3. Write the description for discovery

An agent's description is read to decide **which agent to delegate to**, so it
carries one part more than a skill's: the role.

```
[role and expertise] + [what it does] + [when to invoke] + [the words the user types]
```

Collect at least four trigger phrases in the user's own words. Then check the
description against the *other* agents available: two descriptions matching the same
request means the wrong one gets picked half the time, and that failure is invisible
because an agent did answer.

State the exclusions explicitly — "does not modify files", "not for performance
questions". They discriminate at selection time, which is where it matters.

### 4. Write the system prompt

Structure, in this order, per `references/prompt-craft.md`:

1. **Role** — one sentence, naming the expertise.
2. **When invoked** — numbered steps, the first of which *gathers context*.
3. **Focus areas** — what to look at.
4. **Output format** — shown, not described.
5. **Constraints** — what not to do, and the boundaries to respect.

Write it for a reader with no history. Every referent must be resolvable from the
prompt plus the request.

### 5. Decide the capabilities, in the abstract first

Name what the agent must be able to *do* — read files, search, edit, run one
specific command family, reach the network — and nothing more. Least privilege is
the default: an analysis agent that can only read cannot damage anything, and that
is worth more than the convenience of leaving it open.

Then, and only then, express that in the target harness's fields. The field names,
the capability names and the scoping syntax are all platform-specific — see
`references/frontmatter.md`. If the agent must run on several platforms, declare
nothing and say so in the prompt body instead.

### 6. Verify, in three passes

- **Discovery.** In a fresh session, make three of the phrases from step 3 without
  naming the agent. It should be picked. If it is not, fix the description, never
  the prompt: the prompt is not read until after selection.
- **Negative control.** Make two requests that must *not* reach it — a neighbouring
  domain, and a vague one. Being picked for those is the harder fault, because it
  looks like success.
- **Autonomy.** Invoke it explicitly, in a session where nothing relevant was
  discussed. If it asks for context the conversation was supposed to supply, the
  prompt is not self-contained. Go back to step 4.

Diagnosis for every other symptom: `references/troubleshooting.md`.

### 7. Hand back

## Expected output format

| Item | Value |
| --- | --- |
| Agent | `<name>` |
| Chosen over | `<skill / command / direct request, and why>` |
| Trigger phrases | `<count>` |
| Capabilities | `<the abstract list>` |
| Platform coupling | `<none, or the platform and why>` |
| Picked on | `<the phrases that selected it>` |
| Not picked on | `<the two negative controls>` |
| Autonomy check | `<pass, or what context it asked for>` |
| Next step | Use it in real conditions for a week |

## Additional resources

- `references/prompt-craft.md` — the five sections, with patterns for each
- `references/frontmatter.md` — the fields, per platform, measured versus documented
- `references/platforms.md` — who places the file, and how to verify per harness
- `references/troubleshooting.md` — never picked, wrong one picked, cannot act
- `assets/agent-minimal.md` and `assets/agent-restricted.md` — copy these

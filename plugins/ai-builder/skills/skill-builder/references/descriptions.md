# Writing the description

The description is the only text read to decide whether a skill activates. It is
loaded for every installed skill, all the time. Everything else in the folder is
downstream of it: a perfect body behind a vague description is never reached.

Adapted from the `skill-builder` skill of claude-vibes (MIT).

## The formula

```
[specific operations] + [when to use it] + [the words the user will type]
```

The three parts do different jobs, and dropping any one of them has a distinct
failure mode: no operations and it matches nothing; no context and it matches
everything; no trigger words and it matches only the vocabulary you happened to
choose.

## Part 1 — specific operations

Concrete verbs, not a mission statement.

| Weak | Strong |
| --- | --- |
| "Helps with files" | "Extract text and tables from PDF files, fill forms, merge documents" |
| "Works with data" | "Analyse CSV data, generate statistics, build pivot tables" |
| "Handles code" | "Review code for security issues, performance problems, missing tests" |

Ban list: *helps, manages, handles, works with, deals with, supports*. Each one
describes a relationship to a subject rather than an action on it.

## Part 2 — when to use it

The situation, the file types, the moment in the workflow.

- Weak: "Extract text from PDF files."
- Strong: "Extract text from PDF files. Use when working with PDF documents or
  forms, or before filling a scanned form."

Without this part the field states a capability and leaves the agent to guess the
occasion.

## Part 3 — the words the user will type

The user does not know the skill exists. They ask in their own vocabulary, and the
trigger phrases are the bridge.

Two rules that carry most of the benefit:

- **Include synonyms.** Users say "Excel", not "spreadsheet"; "PR", not "pull
  request review". Put both.
- **Include the file extensions** when they are what the user names: `.xlsx`,
  `.drawio`, `.pdf`.

Write them in quotes, as whole requests rather than keywords — a quoted phrase
matches a phrasing, a bare keyword matches a topic.

## Before and after

**PDF processing**

```
description: Helps with documents
```

Never fires: no operation, no context, no trigger. Against:

```
description: >
  Extract text, tables and images from PDF files, fill forms, merge and split
  documents. Use when the user asks "extract the text from this PDF", "merge
  these PDFs", "fill in this form", "what does this scanned document say".
  Requires pypdf and pdfplumber.
```

**Code review**

```
description: Reviews code
```

Against:

```
description: >
  Review code for security vulnerabilities, performance problems,
  maintainability and test coverage. Use when the user asks "review this PR",
  "check this before I merge", "audit this module", "is this code safe".
```

**Git commits**

```
description: Helps with git
```

"Git" is a subject, not a task, so it competes with every git-adjacent skill.
Against:

```
description: >
  Generate conventional commit messages from the staged diff. Use when the user
  asks "write me a commit message", "commit this", "what should this commit say",
  "summarise these staged changes".
```

## When it runs over 1,024 characters

Count before handing back — over the limit the field is truncated or rejected, and
the trigger phrases are usually at the end, so they are exactly what is lost.

Cut in this order, and never start with the trigger phrases:

1. **Redundancy in the operations.** "Extract text from PDFs, extract tables from
   PDFs, extract images from PDFs" becomes "extract text, tables and images from
   PDFs".
2. **Operations beyond the fifth.** Keep the ones users actually ask for; the rest
   are discoverable from the body once the skill has fired.
3. **The dependency note**, if there is one. Useful, but it never triggers
   anything — move it into the body.
4. **The context clause**, compressed. "Use when working with" becomes "Use for".
5. **Only then**, the weakest trigger phrases — the ones whose wording is already
   covered by another phrase in the list.

## The two failure modes, and why the fix differs

| Symptom | Cause | Fix |
| --- | --- | --- |
| Never fires | The words the user typed are not in the field | Add the phrase verbatim |
| Fires when it should not | Scope too wide, or overlap with a neighbour | Narrow the scope sentence; name the neighbouring skill so the request has somewhere else to go |

Removing trigger phrases to fix the second one causes the first. They are
different levers.

## Check it against real requests

Before finalising, take the user's own sentences and ask, for each: would this
field match it? Then take two requests that must **not** match — an adjacent
domain and a vague one — and confirm they would not. That second test is the one
people skip, and over-triggering is the harder fault to notice, because the skill
appears to work.

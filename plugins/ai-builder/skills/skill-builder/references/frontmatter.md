# SKILL.md frontmatter

Split into what travels between platforms and what does not. Everything is either
**measured** — dated, with the method — or marked as not verified. The distinction is
deliberate: remembered rules stated as specification is how this subject goes wrong.

## The portable core

Two keys, read by every runtime that consumes the format:

| Key | Purpose |
| --- | --- |
| `name` | declared name of the skill |
| `description` | the only text used to decide activation |

Everything else is either platform-dependent (below) or read by nobody at run time.

`license`, `metadata`, `version`, `author`, `tags` change no behaviour anywhere. That
does not make them pointless — this repository requires `license` and the eight
`metadata` fields, and review depends on them — but it does mean a dependency
declared only in `metadata` is never followed. It must appear in the body too.

Evidence that the format is not one vendor's: Playwright ships `SKILL.md` files
inside its npm package, with the same keys, for agent consumption in general.

```yaml
---
name: playwright-cli
description: Automate browser interactions, test web pages and work with Playwright tests.
allowed-tools: Bash(playwright-cli:*) Bash(npx:*) Bash(npm:*)
---
```

## `name`

- Max 64 characters.
- Kebab-case: lowercase letters, digits, single hyphens. No accent, no underscore,
  no leading, trailing or doubled hyphen.
- **Must equal the directory name.**

**Measured 2026-09-13** on Claude Code. Four probe skills, listed from a fresh
non-interactive session:

| Directory | `name:` field | Loads | Listed as |
| --- | --- | --- | --- |
| `probe-flat` | `probe-flat` | yes | `probe-flat` |
| `probe-titlecase` | `"Probe Title Case"` | yes | `probe-titlecase` |
| `Probe Caps Dir` | `"Probe Caps Dir"` | yes | `Probe Caps Dir` |
| `probe-mismatch` | `totally-different-name` | yes | `probe-mismatch` |

Two conclusions, the second being the one that gets missed:

1. A malformed `name` does **not** prevent loading. Nothing warns.
2. **The directory name is the identity.** `probe-mismatch` answered to its
   directory, and the name it declared appeared nowhere.

So the failure mode is not a crash but a divergence: invocation, documentation and
every reference to the skill disagree, and it surfaces in someone else's session.
Measured on one platform; the rule is worth keeping everywhere, because a directory
name is what every transport in `platforms.md` copies.

Normalisation, applied mechanically:

- `"My PDF Tool"` → `my-pdf-tool`
- `"Code Reviewer!!!"` → `code-reviewer`
- `data_analysis` → `data-analysis`

## `description`

Max 1,024 characters for the whole field, carrying both **what** the skill does and
**when** to invoke it. Full treatment in `descriptions.md`; the mechanics only, here.

A YAML trap worth knowing: a value containing `:` or starting with a special
character must be quoted, or the frontmatter fails to parse and the whole skill is
dropped. `name: API:Builder` is a parse error. The block form sidesteps the question
and is what the skills in this repository use:

```yaml
description: >
  Several lines of text, folded into one, with no quoting worries and
  no line-length problem.
```

## `allowed-tools` — the platform-dependent one

The **key** is part of the format and travels. The **tool names inside it do not**:
`Bash`, `Read`, `Grep` are one harness's vocabulary, and another names the same
capabilities differently or not at all.

**For a skill distributed to more than one platform, omit it.** Absent means "no
skill-level restriction", which is valid everywhere, whereas a list of names from one
harness is meaningless on the others. That is why this skill does not declare it.

Declare it only when the skill is deliberately single-platform, and say so in the
body so the next reader knows the coupling is intentional. List form:

```yaml
allowed-tools:
  - Bash
  - Read
```

Inline form, with per-command scoping:

```yaml
allowed-tools: Bash(playwright-cli:*) Bash(npx:*) Bash(npm:*)
```

Three traps:

- **The key is `allowed-tools`.** `tools:` is not read. A skill using `tools:`
  believes it is restricting its tools and is not, and nothing reports it. The linter
  checks this on every profile.
- **A tool the body needs must be listed**, once you list anything at all. A skill
  told to run its own script without a shell tool fails at the point of use, not at
  load.
- **MCP tools go in by suffix**, never with a registration prefix: the prefix is
  assigned by whichever harness registered the server, and it changes when that
  registration changes.

Restricting tools is worth doing for a single-platform read-only skill — a review
skill that can only read cannot modify anything by accident. Weigh that against
losing portability; both are legitimate, but the choice should be explicit.

## Not verified

- Whether any target beyond Claude Code **rejects** rather than ignores unknown
  frontmatter keys. Untested here; the portable core above is what has been checked.
- Whether every target reads a `references/` subdirectory on demand the same way.
  The format allows it and this repository relies on it, but it has been measured on
  one platform only.
- Whether a debug flag on any platform prints a per-skill load line. Some guides
  claim one for Claude Code; unconfirmed. Use the behavioural check in
  `platforms.md` instead, which is deterministic everywhere.

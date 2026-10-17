# Platforms, and who places the file

## The principle

**A command is an artifact; placing it is the transport's job.** This repository
distributes through APM, which deploys the same content into whichever harness the
user runs. A command file that names its own install path has picked a platform.

## What APM deploys, and where

**Measured 2026-09-13**, APM CLI 0.28.0, `apm targets --json --all`:

| Target | Deploy directory | Detected by |
| --- | --- | --- |
| `agent-skills` | `.agents/` | — (meta-target) |
| `claude` | `.claude/` | `CLAUDE.md` |
| `copilot` | `.github/` | `.github/copilot-instructions.md` |
| `opencode` | `.opencode/` | `.opencode/` |
| `cursor` | `.cursor/` | `.cursor/` |
| `codex` | `.codex/` | `.codex/` |
| `gemini` | `.gemini/` | `GEMINI.md` |
| `grok-build` | `.grok/` | `.grok/` |
| `windsurf` | `.windsurf/` | `.windsurf/` |
| `kiro` | `.kiro/` | `.kiro/` |

Within a harness, a command is conventionally a single file under a `commands/`
subdirectory of that deploy directory, with a personal equivalent under the user's
home directory. Measured for Claude Code only.

```bash
apm install --global --target claude,copilot,opencode <org>/<repo>/skills/<name>
```

## How much of a command travels

More than a hook, less than a skill.

| Part | Travels |
| --- | --- |
| Markdown file, frontmatter then prompt | **yes** — the shape is common |
| `description` | **yes** in substance: every harness needs something to list |
| The prompt body | **yes**, as long as it names no harness |
| Argument placeholders | **no** — the sigils and their numbering are the harness's |
| Context gathering and file references | **no** — syntax differs, and may be absent |
| `allowed-tools` capability names | **no** — the key may travel, the names do not |

So a command with **no arguments and no gathering** is essentially portable: it is a
prompt in a file. Every dynamic feature added is a platform commitment. That is the
trade to state explicitly when the user asks for one, rather than discovering it at
deployment.

## Verification, per platform

The portable check needs no CLI: open a fresh session on the target harness, confirm
the command is listed, and invoke it with distinguishable argument values — see step 7
of `SKILL.md`, which is where the offset gets caught.

- **Claude Code** — measured 2026-09-13. A non-interactive invocation runs the command
  and returns its output, which is how the argument mapping in `references/syntax.md`
  was established:
  ```bash
  claude -p "/<command> ALPHA BRAVO CHARLIE"
  ```
  Two cautions from doing it: a command declaring a capability it then uses may stop
  for approval in that mode, and the parsing of a slash command from a `-p` string is
  not necessarily identical to an interactive invocation.
- **Every other target** — not verified here. Confirm placement with
  `apm install --dry-run` before blaming the command.

## Not verified

- Whether any target other than Claude Code supports argument substitution at all,
  and with which sigils.
- Whether the frontmatter keys beyond `description` are read, ignored or rejected
  elsewhere.
- Deploy directories for the targets APM accepts but did not resolve in the probe
  project. APM 0.30.0 exists; re-run `apm targets --json --all` after updating and
  correct the table above — this file is the only place that needs touching.

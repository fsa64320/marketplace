# Platforms, and who places the files

## The principle

**A skill is an artifact; placing it is the transport's job.** This repository
distributes through APM, which deploys the same skill directory into whichever
harness the user runs. So a skill must describe *what it is* and never *where it
goes* — the moment a `SKILL.md` names an install path, it has picked a platform.

That is the whole portability rule. Everything below is context for it, not
instructions to bake into a skill body.

## What APM deploys, and where

APM CLI 0.28.0, `apm targets --json --all`:

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

The full set accepted by `--target` is wider than what resolves in a given project:
`agent-skills, agents, agy, all, antigravity, claude, codex, copilot, copilot-app,
copilot-cowork, cursor, gemini, grok-build, grok-cloud, hermes, intellij, kiro,
openclaw, opencode, vscode, windsurf`. Some are experimental and need a feature
flag; `all` excludes `agent-skills`, `antigravity` and the experimental ones.

`agent-skills` is the **portable meta-target**: it deploys to `.agents/` and is not
part of `all`, so it must be asked for by name.

Target resolution, highest priority first: `--target` / `--runtime`, then `targets:`
in `apm.yml`, then `apm config set target`, then auto-detection. With nothing to
detect, `install` exits 2 rather than guessing.

```bash
apm install --global --target claude,copilot,opencode <org>/<repo>/skills/<name>
apm install --global --target agent-skills <org>/<repo>/skills/<name>
```

## What this means when writing a skill

| Do | Do not |
| --- | --- |
| Refer to files by a path **relative to the skill directory** — `references/x.md`, `scripts/y.py` | Write `~/.claude/skills/…`, `.github/…`, `.agents/…` or any absolute path |
| Say "the skill directory" | Say "your personal skills folder" |
| Let the user's harness decide which tools exist | Hardcode a harness's tool names in the body |
| Name a companion file | Name the harness that will read it |

Relative paths are the portability seam: they survive every deploy directory in the
table above, and the linter checks them.

## Tool authorisation across platforms

`allowed-tools` is part of the skill format and travels. **The tool names inside it
do not.** `Bash`, `Read`, `Grep` are one harness's vocabulary; another names the same
capabilities differently.

Consequence for a skill meant to run anywhere: **omit `allowed-tools`.** Absent means
"no skill-level restriction", which is valid on every platform, whereas a list of
names from one harness is meaningless on the others. Declare it only when the skill
is deliberately single-platform, and say so in the body when you do.

For MCP tools, name them by **suffix only**, never with a registration prefix — the
prefix is assigned by whichever harness registered the server.

## Verification, per platform

The portable check is behavioural and needs no CLI: start a fresh session on the
target harness and make one of the skill's own trigger phrases. If the skill fires,
it loaded and it matched.

Platform-specific shortcuts, where one exists:

- **Claude Code** — lists what actually loaded:
  ```bash
  claude -p "List verbatim the names of the skills available to you matching <term>."
  ```
  `claude plugin validate <path>` checks a plugin manifest **only**: it passed a
  skill carrying a malformed `name` and a `tools:` key without comment. There is no
  `claude skill` command and no built-in SKILL.md linter, which is why this skill
  ships `scripts/lint_skill.py`.
- **Every other target** — no equivalent one-shot listing has been verified here.
  Use the behavioural check, and `apm install --dry-run` to confirm placement before
  blaming the skill.

## Claude Code plugins — one platform's packaging

Relevant only when the destination is a Claude Code plugin rather than an APM
package. Skip it otherwise; nothing in it generalises.

A plugin is `.claude-plugin/plugin.json` plus its own `skills/`. Three traps:

- **The plugin root is a hard boundary.** A component path resolving outside it is
  rejected with `path escapes plugin directory`, and the plugin then loads *without
  that component*, silently.
- **Skills from a plugin are namespaced** as `<plugin>:<skill>`, and the plugin name
  enters the MCP tool prefix. Renaming the plugin changes both.
- **The plugin version is the update signal.** Unchanged version means "nothing new"
  to users, so increment it with every change to any skill it carries.

## Not verified

Per-platform frontmatter quirks — whether any target ignores or rejects keys beyond
`name` and `description`, and how each handles a `references/` subdirectory — are not
covered here. The portable core in `frontmatter.md` is what holds everywhere; treat anything beyond it as untested until you test it on the target.

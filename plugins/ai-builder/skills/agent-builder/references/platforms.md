# Platforms, and who places the file

## The principle

**An agent definition is an artifact; placing it is the transport's job.** This
repository distributes through APM, which deploys the same content into whichever
harness the user runs. The moment a definition names an install path, it has picked a
platform.

So: no path in the system prompt, no harness name in the body, and companion files
referred to relatively.

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

The wider set accepted by `--target` includes `agents`, `copilot-app`,
`copilot-cowork`, `antigravity`, `hermes`, `openclaw`, `grok-cloud`, `intellij` and
`vscode`; some are experimental and need a feature flag, and `all` excludes
`agent-skills` and the experimental ones. Those did not resolve a deploy directory, so
they are not in the table.

```bash
apm install --global --target claude,copilot,opencode <org>/<repo>/skills/<name>
```

Within a harness, an agent is conventionally a single file under an `agents/`
subdirectory of that deploy directory — on Claude Code, `.claude/agents/<file>.md`,
project scope, and the same under the user's home directory for personal scope. That
layout holds for Claude Code; do not assume it elsewhere.

## Verification, per platform

The portable check is behavioural and needs no CLI. Three passes, in a fresh session:

1. **Discovery** — make a trigger phrase without naming the agent. It should be
   picked.
2. **Negative control** — make a request that must not reach it.
3. **Autonomy** — invoke it explicitly in a session where nothing relevant was
   discussed, and see whether it asks for context it should have gathered itself.

Platform-specific shortcuts, where one exists:

- **Claude Code** — lists what actually loaded, and under which
  identity:
  ```bash
  claude -p "List verbatim every agent type available to you whose name contains <term>."
  ```
  That is how the `name`-versus-filename question in `frontmatter.md` was settled. An
  interactive session also has an agents listing.
- **Every other target** — no equivalent listing has been verified here. Use the
  behavioural passes, and `apm install --dry-run` to confirm placement before blaming
  the definition.

## What no command will tell you

No harness validates an agent definition. A malformed `name` loads, an empty
`description` loads, and a prompt that depends on a conversation it will never see
loads too — the first sign of any of them is an agent that is never picked, or one
that asks for context.

There is therefore no lint for the thing that actually breaks agents. The three
behavioural passes above are the check.

## Not verified

- Whether every target reads an `agents/` subdirectory, and under what name.
- Whether the frontmatter keys beyond `name` and `description` are ignored or
  rejected off Claude Code.
- Deploy directories for the targets listed but unresolved above. APM 0.30.0 exists;
  re-run `apm targets --json --all` after updating and correct the table here — this
  file is the only place that needs touching.

# Agent frontmatter, per platform

An agent definition is a Markdown file: YAML frontmatter, then the system prompt as
the body. That much is shared. **Almost everything else is platform-specific**, far
more than for a skill, so this file separates what travels from what does not.

## The portable core

| Key | Purpose |
| --- | --- |
| `name` | the agent's identity, and how it is addressed |
| `description` | the text read to decide **which** agent to delegate to |

Those two exist wherever the format exists. Write them and nothing else if the agent
must run on more than one harness.

## `name` — the identity, unlike a skill

On Claude Code, three test agents, listed from a fresh non-interactive session:

| File | `name:` field | Loads | Listed as |
| --- | --- | --- | --- |
| `probe-agent` | `probe-agent` | yes | `probe-agent` |
| `probe-mismatch` | `totally-different-agent` | yes | `totally-different-agent` |
| `probe-badname` | `Probe_Bad Name` | yes | `Probe_Bad Name` |

1. **The `name:` field is the identity. The filename is a container.** The exact
   inverse of a skill, where the directory name wins and the field is ignored.
2. **A malformed name loads.** Uppercase, underscore and space were all accepted, and
   nothing warned. Lowercase-with-hyphens is a usability convention here, not a
   validation rule — which is why the sources that present it as "invalid" overstate
   the case.

Keep the filename equal to the name anyway: it is the only way to find the file from
the identity, and every transport copies filenames.

## `description` — read at selection time

Same 1,024-character discipline as a skill's, and one part more, because it competes
with the other agents rather than with nothing:

```
[role and expertise] + [what it does] + [when to invoke] + [the words the user types]
```

Two properties specific to agents:

- **Exclusions discriminate.** "Does not modify files", "not for performance
  questions" do real work at selection time, when several agents partly match.
- **Insistent phrasing is widely recommended** — "use PROACTIVELY after…", "MUST be
  invoked when…" — on the grounds that it raises automatic invocation. Plausible and
  commonly repeated; do not present it as a mechanism.

## Platform-specific fields

These names and values belong to one harness. Read them as an illustration of the
*shape* to look for on your target, not as a portable schema.

### Claude Code

| Field | Effect |
| --- | --- |
| `tools` | the capabilities the agent may use; omitted means it inherits the caller's |
| `model` | which model runs the agent |
| `permissionMode` | how permission prompts are handled |
| `skills` | skills loaded when the agent starts |

Capability scoping is per command family, which is the useful part:

```yaml
tools: Read, Grep, Glob                          # analysis only
tools: Read, Write, Edit, Grep, Glob             # may modify files
tools: Read, Grep, Glob, Bash(git diff:*)        # one command family, read-only use
tools: Bash                                       # unrestricted shell
```

Two corrections to what is commonly written about `model`:

- The documented values include **`fable`** alongside `haiku`, `sonnet` and `opus`,
  and `inherit`. Lists that stop at three are out of date.
- **`sonnet` is not the default.** With `model` omitted, the agent inherits the
  caller's model unless a default subagent model is configured. Sources stating
  "default: sonnet" are wrong on this point.

`permissionMode` and `skills` are **documented but not verified here**. Treat
`bypassPermissions` as something to justify in writing before using: it removes the
check that stops an autonomous agent doing damage.

### Other platforms

Expect the same two-part shape — an identity plus a discovery text —
and expect the capability field to be named and scoped differently or to be absent.
Check on the target before relying on anything beyond the portable core.

## Least privilege, expressed portably

Decide capabilities in the abstract, in the system prompt, and let the frontmatter
narrow them where the platform allows:

```markdown
## Constraints
- Do not modify any file. Report findings; the caller decides what to change.
- Do not run commands other than the ones named in "When invoked".
```

A constraint in the prompt is advisory and travels. A capability restriction in the
frontmatter is enforced and does not. Write both when you can, and never rely on the
prompt alone for something that would be damaging if ignored.

## Not verified

- Whether any platform rejects rather than ignores unknown frontmatter keys.
- Whether `permissionMode` and `skills` behave as documented.
- Whether insistent description phrasing changes selection.
- Precedence when the same agent name exists in two locations at once. Commonly
  stated as project-over-personal; untested here.

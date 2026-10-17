---
name: template-with-script
description: >
  <One sentence: what this skill does.>
  Use when the user asks "<phrase>", "<phrase>", "<phrase>", "<phrase>".
license: proprietary
# allowed-tools is omitted on purpose: the key travels between platforms but the
# tool names inside it do not. Declare it only if this skill is single-platform.
---

# <Skill name>

## What this skill does

<Two sentences.> The parsing is done by `scripts/extract.py` rather than by reading
the file into context, because <the reason — size, binary format, determinism>.

## Procedure

### 1. Locate the input

Ask the user for the path if they have not given one. Do not guess it.

### 2. Run the extraction

```bash
python scripts/extract.py <path>
```

The path is relative to the skill directory, which is what makes this work wherever
the transport deployed it. `python3` on macOS and Linux, `python` on Windows.

Exit codes: `0` ok, `1` bad arguments, `2` unreadable input.

On a non-zero exit, report the code and the message, and stop. Do not fall back to
reading the file by hand: a partial read is worse than an error, because it looks
like a result.

### 3. Restate the output

Present what the script returned, in the format below. State nothing the script did
not return.

## Expected output format

| Item | Value |
| --- | --- |
| Source | `<path>` |
| <Extracted field> | `<value>` |
| <Extracted field> | `<value>` |

## Notes on shipping a script

- Keep it under `scripts/`, beside the skill, and call it by a path relative to the
  skill directory — never an absolute one, and never a harness's deploy directory.
- If you do declare `allowed-tools`, the shell tool must be in it, or the skill
  cannot run its own script and nothing says so until it fails.
- Have the script print text a human can read, not a structure the skill must
  re-parse. The skill's job is to decide, not to marshal.
- Let it fail loudly. A script that swallows its exception and prints nothing turns
  a clear error into an invented answer.

# Writing the script a skill ships

A script is read far more often than it is written: by the next contributor, by
the agent that runs it and reads its traceback, and by the agent asked to change it.
Every rule below exists to keep it readable by all three. Start from
`assets/template-with-script/` and keep it that shape as it grows.

## Decide what goes in the script at all

The script does what is **deterministic**: parse a file, count, validate against a
fixed rule, render an output. Judgement stays with the agent, written as a step in
`SKILL.md`.

A script that grows a cascade of heuristics — guessing what a shape probably means,
scoring candidates, special-casing the fifth layout seen in the wild — is doing the
agent's job in the hardest language for it. Return the facts and let the body of the
skill decide.

## Keep each function small

Measure it with ruff (`ruff check --select C901,PLR0912,PLR0913,PLR0915`); the STA
catalog's CI enforces these limits from its root `pyproject.toml`:

| Rule | Limit | What it catches |
| --- | --- | --- |
| `C901` | complexity 12 | too many paths through one function |
| `PLR0912` | 12 branches | an `if`/`elif` ladder |
| `PLR0915` | 50 statements | a function doing several jobs |
| `PLR0913` | 6 arguments | state threaded by hand |

When one trips, split the function; do not raise the limit or add a `noqa`.

- **A processing pipeline is one function per stage**, called in sequence from a
  function of a dozen lines. Numbered comments (`# 1. …`, `# 2. …`) inside one body
  are the stages asking to be functions: give each the name its comment already has.
- **State shared by the stages goes in one dataclass**, passed along, rather than in
  locals that every later stage reads, or in a growing argument list.
- **One command, one function** in the CLI: `cmd_<name>(args)` parses nothing and
  calls the library.
- **No nested function.** Lift it to module level with a leading underscore; it
  becomes testable and its dependencies become visible.
- **An `elif` ladder over kinds is a dict** from kind to value or to handler.

## Keep the design flat

- No abstraction with a single caller, no base class with a single subclass, no
  plugin registry, no configuration for a choice nobody makes.
- Plain functions, dicts and dataclasses before classes with behaviour.
- Standard library first. A third-party package earns its place, and brings the
  script its own `pyproject.toml` + `uv.lock` (`exclude-newer = "1 day"`,
  `truststore` wherever HTTPS is used).
- No `try/except` around the body: a traceback is a better result than a swallowed
  error the agent will paper over with a plausible answer. Catch only an error you
  turn into a specific message and exit code.
- Past ~300 lines, split into modules under `scripts/lib/`, one subject each — or
  ask again whether part of the work belongs to the agent.

## Simplifying an existing script

1. Pin the behaviour first: a `test` command, or a small set of input files with
   their expected output, run before any change.
2. Extract one stage at a time, rerunning the check after each. Same outputs, same
   messages, same exit codes: a simplification changes no behaviour.
3. In the STA catalog, remove the file from the complexity-debt list in the root
   `pyproject.toml` once ruff passes without it. That list only ever shrinks.

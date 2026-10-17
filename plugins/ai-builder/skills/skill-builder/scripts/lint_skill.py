#!/usr/bin/env python3
"""Lint an agent skill directory.

Platform-independent by default: the checks are properties of the skill format, not
of any one harness. No third-party dependency — the frontmatter is parsed by hand so
the script runs anywhere Python 3.8+ does, and so every finding carries a line
number.

Usage:
    python3 lint_skill.py [--platform NAME] <skill-directory> [<skill-directory> ...]

    --platform portable   (default) flags anything that couples the skill to a
                          single harness, such as a declared `allowed-tools`
    --platform <name>     the skill is deliberately single-platform: the coupling
                          checks become informational instead of warnings

Exit codes:
    0   clean
    1   warnings only
    2   at least one error
"""

import os
import re
import sys
from dataclasses import dataclass

# Keys the runtime reads. Everything else is for review and tooling.
RUNTIME_KEYS = ("name", "description", "allowed-tools")

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FENCE_RE = re.compile(r"^\s*(`{3,})(.*)$")
WHEN_MARKERS = ("use when", "use for", "triggers on", "utiliser quand", "déclenche")
ABS_PATH_RE = re.compile(r"(?:(?<![A-Za-z])[A-Za-z]:[\\/]|/Users/|/home/|/c/Users/)")
SECRET_RE = re.compile(
    r"(api[_-]?key|secret|password|passwd|token|bearer)\s*[:=]\s*['\"]?[A-Za-z0-9_\-./+]{16,}",
    re.I,
)
# Paths in the body worth resolving: skip anchors, URLs and placeholders.
PLACEHOLDER_RE = re.compile(r"[<>{}\[\]*?]|\.\.\.")

# Only paths into a skill's own subdirectories are treated as navigation. A prose
# mention of, say, `.claude-plugin/plugin.json` is an illustration, not a link the
# skill will follow, and flagging it is the noise that gets a linter switched off.
SKILL_SUBDIRS = ("references/", "reference/", "scripts/", "assets/", "docs/", "examples/", "templates/")

# Harness-owned deploy directories. A skill body naming one of these has picked a
# platform, which defeats a transport that deploys the same directory to all of them.
HARNESS_DIRS = re.compile(
    r"(?:~/\.claude|\.claude/skills|\.claude-plugin|\.github/copilot|\.opencode/"
    r"|\.cursor/|\.codex/|\.gemini/|\.grok/|\.windsurf/|\.kiro/|\.agents/)"
)


class Report:
    def __init__(self, title):
        self.title = title
        self.rows = []

    def ok(self, msg):
        self.rows.append(("ok", msg))

    def err(self, msg):
        self.rows.append(("ERROR", msg))

    def warn(self, msg):
        self.rows.append(("warn", msg))

    def info(self, msg):
        self.rows.append(("info", msg))

    @property
    def errors(self):
        return sum(1 for lvl, _ in self.rows if lvl == "ERROR")

    @property
    def warnings(self):
        return sum(1 for lvl, _ in self.rows if lvl == "warn")

    def render(self):
        out = [self.title]
        for lvl, msg in self.rows:
            out.append(f"  {lvl:<5} {msg}")
        return "\n".join(out)


def read_text(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def parse_frontmatter(lines):
    """Return (fields, end_index, error).

    fields maps a top-level key to (value, line_number). Block scalars (`>`, `|`)
    are folded; a key introducing a list or a nested map gets the empty string as
    its value, which is enough for the checks below.
    """
    if not lines or lines[0].strip() != "---":
        return {}, None, "no frontmatter: line 1 is not `---`"

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, None, "frontmatter opened at line 1 is never closed by `---`"

    fields = {}
    i = 1
    while i < end:
        line = lines[i]
        m = re.match(r"^([A-Za-z][\w-]*):(.*)$", line)
        if not m:
            i += 1
            continue
        key, rest = m.group(1), m.group(2).strip()
        lineno = i + 1

        if rest in (">", ">-", ">+", "|", "|-", "|+"):
            fold = rest.startswith(">")
            block = []
            i += 1
            while i < end and (lines[i].strip() == "" or lines[i].startswith((" ", "\t"))):
                block.append(lines[i].strip())
                i += 1
            value = (" " if fold else "\n").join(b for b in block if b != "")
            fields[key] = (value, lineno)
            continue

        if rest == "":
            # a list or a nested map follows; the value itself is not needed
            fields[key] = ("", lineno)
            i += 1
            while i < end and (lines[i].strip() == "" or lines[i].startswith((" ", "\t"))):
                i += 1
            continue

        value = rest
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key] = (value, lineno)
        i += 1

    return fields, end, None


def scan_fences(lines):
    """Return (nested, unterminated_line). Length-aware, per CommonMark:
    a closing fence carries no info string and is at least as long as the opener."""
    open_len = 0
    nested = 0
    opened_at = None
    for i, line in enumerate(lines, 1):
        m = FENCE_RE.match(line)
        if not m:
            continue
        n, info = len(m.group(1)), m.group(2).strip()
        if open_len == 0:
            open_len, opened_at = n, i
        elif info == "" and n >= open_len:
            open_len, opened_at = 0, None
        else:
            nested += 1
    return nested, opened_at


def prose_only(lines):
    """The body with fenced blocks removed. A path inside a fenced block is an
    illustration, not a reference the skill will follow — checking those produces
    noise, which is how a linter gets ignored."""
    out = []
    open_len = 0
    for line in lines:
        m = FENCE_RE.match(line)
        if m:
            n, info = len(m.group(1)), m.group(2).strip()
            if open_len == 0:
                open_len = n
            elif info == "" and n >= open_len:
                open_len = 0
            continue
        if open_len == 0:
            out.append(line)
    return "\n".join(out)


def referenced_paths(text):
    """Relative paths into the skill's own subdirectories that the prose points at."""
    found = set()
    for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):  # markdown links
        found.add(m.group(1).strip())
    for m in re.finditer(r"`([^`\n]+)`", text):  # backticked paths
        c = m.group(1).strip()
        if "/" in c and not c.startswith(("-", "$")) and " " not in c:
            found.add(c)
    out = []
    for p in found:
        if p.startswith(("#", "http://", "https://", "mailto:", "/", "~", "..")):
            continue
        if PLACEHOLDER_RE.search(p):
            continue
        if not p.startswith(SKILL_SUBDIRS):
            continue
        if not re.search(r"\.(md|py|sh|ps1|js|json|ya?ml|txt|drawio|png|csv)$", p) and not p.endswith("/"):
            continue
        out.append(p)
    return sorted(out)


@dataclass
class Skill:
    """What every check reads: the parsed SKILL.md and how the lint was invoked."""

    skill_dir: str
    rel: str
    platform: str
    lines: list
    fields: dict
    end: int
    prose: str


def check_name(rep, skill):
    fields, rel = skill.fields, skill.rel
    if "name" not in fields:
        rep.err("no `name` field")
        return
    name, lineno = fields["name"]
    if not name:
        rep.err(f"`name` is empty (line {lineno})")
        return
    if len(name) > 64:
        rep.err(f"`name` is {len(name)} characters, limit is 64")
    if not NAME_RE.match(name):
        rep.err(f"`name` {name!r} (line {lineno}) is not kebab-case: lowercase letters, digits and single hyphens only")
    if name != rel:
        rep.err(
            f"`name` {name!r} does not match the directory {rel!r} — the directory name is what identifies the skill"
        )
    elif NAME_RE.match(name):
        rep.ok(f"name {name!r} matches the directory")


def check_description(rep, skill):
    fields = skill.fields
    if "description" not in fields:
        rep.err("no `description` field")
        return
    desc, lineno = fields["description"]
    n = len(desc)
    if not desc:
        rep.err(f"`description` is empty (line {lineno})")
    elif n > 1024:
        rep.err(f"`description` is {n} / 1024 characters")
    else:
        rep.ok(f"description {n} / 1024 characters")

    if not any(mk in desc.lower() for mk in WHEN_MARKERS):
        rep.err(
            '`description` has no "when" clause — add "Use when the user asks ..."; without it the skill has no trigger'
        )
    triggers = len(re.findall(r'"[^"]{3,}"', desc)) + len(re.findall(r"«[^»]{3,}»", desc))
    if triggers < 4:
        rep.warn(f"{triggers} quoted trigger phrases (want >= 4)")
    else:
        rep.ok(f"{triggers} quoted trigger phrases")


def check_tools(rep, skill):
    fields, platform = skill.fields, skill.platform
    if "tools" in fields:
        rep.err(f"key `tools:` at line {fields['tools'][1]} is not read by the runtime — the key is `allowed-tools`")
    if "allowed-tools" in fields:
        lineno = fields["allowed-tools"][1]
        if platform == "portable":
            rep.warn(
                f"`allowed-tools` declared at line {lineno} — the key travels but the "
                "tool names inside it belong to one harness. Omit it for a skill "
                "distributed to several platforms, or pass --platform <name>"
            )
        else:
            rep.ok(f"`allowed-tools` declared (line {lineno}), platform {platform!r}")


def check_fences(rep, skill):
    nested, unterminated = scan_fences(skill.lines)
    if unterminated:
        rep.err(
            f"fenced block opened at line {unterminated} is never closed — everything "
            "after it renders as preformatted text"
        )
    if nested:
        rep.err(
            f"{nested} fenced block(s) opened inside another fenced block — the inner "
            "one closes the outer one early; use quadruple backticks outside, or move "
            "the example to its own file"
        )
    if not nested and not unterminated:
        rep.ok("fenced blocks balanced")


def check_referenced_paths(rep, skill):
    missing = [p for p in referenced_paths(skill.prose) if not os.path.exists(os.path.join(skill.skill_dir, p))]
    if missing:
        for p in missing:
            rep.err(f"body points at {p} — not found on disk")
    else:
        rep.ok("every referenced path resolves")


def check_platform_coupling(rep, skill):
    coupled = [ln.strip()[:60] for ln in skill.prose.split("\n") if HARNESS_DIRS.search(ln)]
    if coupled:
        msg = (
            f"{len(coupled)} line(s) name a harness-owned directory (e.g. {coupled[0]!r}) "
            "— a skill describes itself, the transport places it"
        )
        if skill.platform == "portable":
            rep.err(msg)
        else:
            rep.info(f"{msg} [expected on --platform {skill.platform}]")
    else:
        rep.ok("no harness-owned path in the body")


def check_hygiene(rep, skill):
    for i, line in enumerate(skill.lines, 1):
        if ABS_PATH_RE.search(line):
            rep.warn(f"absolute path at line {i}: {line.strip()[:60]}")
            break
    for i, line in enumerate(skill.lines, 1):
        if SECRET_RE.search(line):
            rep.err(f"possible secret at line {i}")
            break


def check_size(rep, skill):
    body_lines = skill.lines[skill.end + 1 :]
    body = "\n".join(body_lines)
    words = len(body.split())
    rep.info(f"body {words} words, {len(body_lines)} lines")
    if words > 2000:
        rep.warn("body over 2,000 words — move content into references/")


# Run in this order once SKILL.md is found and its frontmatter parses.
CHECKS = (
    check_name,
    check_description,
    check_tools,
    check_fences,
    check_referenced_paths,
    check_platform_coupling,
    check_hygiene,
    check_size,
)


def find_skill_md(rep, skill_dir):
    """Return the path to SKILL.md, or None after reporting why it is missing."""
    path = os.path.join(skill_dir, "SKILL.md")
    if os.path.isfile(path):
        rep.ok("SKILL.md found")
        return path
    # catch a case-variant, which fails silently on a case-sensitive checkout
    variants = os.listdir(skill_dir) if os.path.isdir(skill_dir) else []
    near = [f for f in variants if f.lower() == "skill.md"]
    if near:
        rep.err(f"file is named {near[0]!r} — it must be exactly SKILL.md")
    else:
        rep.err("no SKILL.md in this directory")
    return None


def lint(skill_dir, platform="portable"):
    skill_dir = os.path.abspath(skill_dir.rstrip("/\\"))
    rep = Report(skill_dir)

    path = find_skill_md(rep, skill_dir)
    if path is None:
        return rep

    lines = read_text(path).split("\n")
    fields, end, error = parse_frontmatter(lines)
    if error:
        rep.err(error)
        return rep
    rep.ok(f"frontmatter parses (lines 1-{end + 1})")

    prose = prose_only(lines[end + 1 :])
    skill = Skill(skill_dir, os.path.basename(skill_dir), platform, lines, fields, end, prose)
    for check in CHECKS:
        check(rep, skill)
    return rep


def parse_args(args):
    """Return (platform, targets)."""
    platform = "portable"
    targets = []
    i = 0
    while i < len(args):
        if args[i] == "--platform":
            if i + 1 >= len(args):
                raise ValueError("--platform needs a value")
            platform = args[i + 1]
            i += 2
        elif args[i].startswith("--platform="):
            platform = args[i].split("=", 1)[1]
            i += 1
        else:
            targets.append(args[i])
            i += 1
    return platform, targets


def main(argv):
    try:
        platform, targets = parse_args(argv[1:])
    except ValueError as exc:
        print(exc)
        return 1

    if not targets:
        print(__doc__.strip())
        return 1

    worst = 0
    for target in targets:
        if not os.path.isdir(target):
            print(f"{target}: not a directory")
            worst = max(worst, 2)
            continue
        rep = lint(target, platform)
        print(rep.render())
        print()
        if rep.errors:
            worst = max(worst, 2)
        elif rep.warnings:
            worst = max(worst, 1)
        errs = f"{rep.errors} error" + ("" if rep.errors == 1 else "s")
        warns = f"{rep.warnings} warning" + ("" if rep.warnings == 1 else "s")
        print(f"{errs}, {warns}")
        print()
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv))

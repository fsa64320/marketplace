#!/usr/bin/env python3
"""<What this script extracts, in one line.>

Keep it this shape as it grows: references/scripts.md of skill-builder.

Usage:
    python3 extract.py <path>

Exit codes:
    0   ok
    1   bad arguments
    2   input unreadable
"""

import os
import sys


def extract(path):
    """Return the fields the skill will restate, as a list of (label, value)."""
    with open(path, encoding="utf-8") as handle:
        text = handle.read()

    # <The real work goes here. Return facts, not prose.>
    return [
        ("Lines", str(text.count("\n") + 1)),
        ("Characters", str(len(text))),
    ]


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 1

    path = argv[1]
    if not os.path.isfile(path):
        print(f"not a file: {path}", file=sys.stderr)
        return 2

    # No try/except around the body: a crash with a traceback is a better result
    # than a swallowed error the skill will paper over with a plausible answer.
    for label, value in extract(path):
        print(f"{label + ':':<20} {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

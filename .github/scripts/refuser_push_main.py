#!/usr/bin/env python3
"""Hook PreToolUse (Bash) de Claude Code pour ce dépôt.

- `git push` vers main : refusé (code 2, le message revient à Claude).
- `gh pr merge` : soumis à confirmation de Frederick (permissionDecision « ask »).

Lit l'événement JSON sur stdin. Tout le reste passe (code 0).
"""

import json
import re
import shlex
import shutil
import subprocess
import sys

SEPARATEURS = re.compile(r"\s*(?:&&|\|\||;|\||\n)\s*")
CIBLES_MAIN = {"main", "HEAD:main", ":main", "refs/heads/main", "HEAD:refs/heads/main"}


def mots(segment: str) -> list[str]:
    try:
        return shlex.split(segment)
    except ValueError:
        return segment.split()


def sous_commande(tokens: list[str], outil: str) -> list[str] | None:
    """Renvoie les arguments qui suivent `outil` (après ses options globales), ou None."""
    if outil not in tokens:
        return None
    reste = tokens[tokens.index(outil) + 1 :]
    while reste and reste[0].startswith("-"):
        reste = reste[2:] if reste[0] in ("-C", "-c", "-R", "--repo") else reste[1:]
    return reste


def branche_courante(dossier: str) -> str:
    git = shutil.which("git")
    if git is None:
        return ""
    resultat = subprocess.run(
        [git, "-C", dossier, "symbolic-ref", "--short", "-q", "HEAD"], capture_output=True, text=True, check=False
    )
    return resultat.stdout.strip()


def pousse_vers_main(args: list[str], dossier: str) -> bool:
    if not args or args[0] != "push":
        return False
    positionnels = [a for a in args[1:] if not a.startswith("-")]
    refspecs = positionnels[1:]
    if not refspecs:
        return branche_courante(dossier) == "main"
    return any(r.lstrip("+") in CIBLES_MAIN or r.endswith(":main") for r in refspecs)


def demander(raison: str) -> None:
    sortie = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": raison,
        }
    }
    print(json.dumps(sortie, ensure_ascii=False))


def main() -> int:
    try:
        evenement = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    commande = (evenement.get("tool_input") or {}).get("command", "")
    dossier = evenement.get("cwd") or "."
    for segment in SEPARATEURS.split(commande):
        tokens = mots(segment)
        git_args = sous_commande(tokens, "git")
        if git_args is not None and pousse_vers_main(git_args, dossier):
            print(
                "Push direct vers main refusé dans ce dépôt : pousse une branche et ouvre une PR "
                "(gh pr create --base main). Voir AGENTS.md.",
                file=sys.stderr,
            )
            return 2
        gh_args = sous_commande(tokens, "gh")
        if gh_args is not None and gh_args[:2] == ["pr", "merge"]:
            demander("Merge d'une PR sur main : Frederick doit le demander explicitement (AGENTS.md).")
            return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())

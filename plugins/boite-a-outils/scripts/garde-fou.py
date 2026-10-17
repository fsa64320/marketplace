#!/usr/bin/env python3
"""Hook PreToolUse : bloque les commandes Bash destructrices.

Lit l'événement JSON sur stdin. Code de sortie 2 = commande bloquée,
le message sur stderr est renvoyé à Claude.
"""
import json
import re
import sys

MOTIFS_INTERDITS = [
    (r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f?\s+(/|~|\$HOME)(\s|$)", "suppression récursive de la racine ou du dossier personnel"),
    (r"\bgit\s+push\b.*(--force|-f)\b.*\b(main|master)\b", "push forcé sur main/master"),
    (r"\bgit\s+push\b.*\b(main|master)\b.*(--force|-f)\b", "push forcé sur main/master"),
    (r"\bmkfs(\.\w+)?\b", "formatage de disque"),
    (r"\bdd\s+.*of=/dev/", "écriture brute sur un périphérique"),
    (r"\baz\s+group\s+delete\b", "suppression d'un resource group Azure"),
    (r"\baws\s+s3\s+rb\b.*--force", "suppression forcée d'un bucket S3"),
]


def main() -> int:
    try:
        evenement = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    commande = (evenement.get("tool_input") or {}).get("command", "")
    for motif, raison in MOTIFS_INTERDITS:
        if re.search(motif, commande):
            print(
                f"Commande bloquée par le garde-fou boite-a-outils ({raison}). "
                "Demande à l'utilisateur de l'exécuter lui-même s'il la confirme.",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

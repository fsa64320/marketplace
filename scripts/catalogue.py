#!/usr/bin/env python3
"""Génère le tableau des plugins du README à partir des manifestes (stdlib uniquement).

  python3 scripts/catalogue.py          réécrit le tableau entre les marqueurs du README
  python3 scripts/catalogue.py --check  code de sortie 1 si le README n'est pas à jour

Sources : .claude-plugin/marketplace.json (liste, description), plugin.json (version)
et l'inventaire disque de chaque plugin (skills, agents, commandes, hooks, MCP).
"""

import argparse
import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
README = RACINE / "README.md"
DEBUT = "<!-- plugins:start -->"
FIN = "<!-- plugins:end -->"


def lire_json(chemin: Path) -> dict:
    return json.loads(chemin.read_text(encoding="utf-8")) if chemin.exists() else {}


def liste(noms: list[str], prefixe: str = "") -> str:
    return ", ".join(f"`{prefixe}{n}`" for n in sorted(noms))


def composants(nom: str, dossier: Path) -> str:
    parties = []
    skills = [p.parent.name for p in dossier.glob("skills/*/SKILL.md")]
    agents = [p.stem for p in dossier.glob("agents/**/*.md")]
    commandes = [p.stem for p in dossier.glob("commands/**/*.md")]
    hooks = lire_json(dossier / "hooks" / "hooks.json").get("hooks", {})
    mcp = lire_json(dossier / ".mcp.json").get("mcpServers", {})
    if skills:
        parties.append(f"Skills : {liste(skills)}")
    if agents:
        parties.append(f"Agents : {liste(agents)}")
    if commandes:
        parties.append(f"Commandes : {liste(commandes, f'/{nom}:')}")
    if hooks:
        parties.append(f"Hooks : {liste(list(hooks))}")
    if mcp:
        parties.append(f"MCP : {liste(list(mcp))}")
    return " · ".join(parties) or "—"


def tableau() -> str:
    marketplace = lire_json(RACINE / ".claude-plugin" / "marketplace.json")
    lignes = ["| Plugin | Version | Description | Composants |", "| --- | --- | --- | --- |"]
    for entree in sorted(marketplace.get("plugins", []), key=lambda e: e["name"]):
        dossier = (RACINE / entree["source"]).resolve()
        version = lire_json(dossier / ".claude-plugin" / "plugin.json").get("version", "—")
        description = entree.get("description", "").replace("|", "\\|")
        lignes.append(f"| `{entree['name']}` | {version} | {description} | {composants(entree['name'], dossier)} |")
    return "\n".join(lignes)


def readme_attendu() -> str:
    texte = README.read_text(encoding="utf-8")
    if DEBUT not in texte or FIN not in texte:
        raise SystemExit(f"✘ README.md : marqueurs {DEBUT} / {FIN} introuvables")
    avant, reste = texte.split(DEBUT, 1)
    apres = reste.split(FIN, 1)[1]
    return f"{avant}{DEBUT}\n{tableau()}\n{FIN}{apres}"


def ecrire() -> None:
    README.write_text(readme_attendu(), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="vérifie sans écrire")
    args = parser.parse_args()
    attendu = readme_attendu()
    if args.check:
        if README.read_text(encoding="utf-8") != attendu:
            print("✘ Tableau des plugins du README périmé : lance python3 scripts/catalogue.py")
            return 1
        print("✔ Tableau des plugins à jour.")
        return 0
    README.write_text(attendu, encoding="utf-8")
    print("✔ Tableau des plugins régénéré dans README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())

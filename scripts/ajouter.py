#!/usr/bin/env python3
"""Ajoute un plugin ou un composant à la marketplace.

Exemples :
  python3 scripts/ajouter.py plugin mon-plugin "Ce que fait le plugin"
  python3 scripts/ajouter.py skill mon-plugin mon-skill
  python3 scripts/ajouter.py agent mon-plugin mon-agent
  python3 scripts/ajouter.py commande mon-plugin ma-commande
  python3 scripts/ajouter.py hooks mon-plugin
  python3 scripts/ajouter.py mcp mon-plugin
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
MARKETPLACE = RACINE / ".claude-plugin" / "marketplace.json"
PLUGINS = RACINE / "plugins"
MODELE = RACINE / "templates" / "plugin"
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def erreur(message: str) -> None:
    print(f"✘ {message}", file=sys.stderr)
    sys.exit(1)


def verifier_nom(nom: str) -> None:
    if not KEBAB.match(nom):
        erreur(f"« {nom} » doit être en kebab-case (minuscules, chiffres, tirets).")


def dossier_plugin(nom: str) -> Path:
    dossier = PLUGINS / nom
    if not dossier.is_dir():
        erreur(f"Le plugin « {nom} » n'existe pas. Crée-le d'abord : ajouter.py plugin {nom} \"description\"")
    return dossier


def creer_plugin(nom: str, description: str) -> None:
    verifier_nom(nom)
    cible = PLUGINS / nom
    if cible.exists():
        erreur(f"{cible.relative_to(RACINE)} existe déjà.")
    cible.mkdir(parents=True)
    (cible / ".claude-plugin").mkdir()
    manifeste = (MODELE / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    manifeste = manifeste.replace("__NOM__", nom).replace("__DESCRIPTION__", description.replace('"', '\\"'))
    (cible / ".claude-plugin" / "plugin.json").write_text(manifeste, encoding="utf-8")
    for sous_dossier in ("skills", "agents", "commands"):
        (cible / sous_dossier).mkdir()
        (cible / sous_dossier / ".gitkeep").touch()

    donnees = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    donnees["plugins"].append({"name": nom, "source": f"./plugins/{nom}", "description": description})
    MARKETPLACE.write_text(json.dumps(donnees, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"✔ Plugin créé dans plugins/{nom} et déclaré dans marketplace.json")


def creer_depuis_modele(plugin: str, source: Path, cible: Path, ancien: str, nouveau: str) -> None:
    if cible.exists():
        erreur(f"{cible.relative_to(RACINE)} existe déjà.")
    cible.parent.mkdir(parents=True, exist_ok=True)
    cible.write_text(source.read_text(encoding="utf-8").replace(ancien, nouveau), encoding="utf-8")
    (cible.parent / ".gitkeep").unlink(missing_ok=True)
    print(f"✔ Créé : {cible.relative_to(RACINE)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sous = parser.add_subparsers(dest="type", required=True)
    p = sous.add_parser("plugin")
    p.add_argument("nom")
    p.add_argument("description")
    for type_ in ("skill", "agent", "commande"):
        s = sous.add_parser(type_)
        s.add_argument("plugin")
        s.add_argument("nom")
    for type_ in ("hooks", "mcp"):
        s = sous.add_parser(type_)
        s.add_argument("plugin")
    args = parser.parse_args()

    if args.type == "plugin":
        creer_plugin(args.nom, args.description)
        return

    dossier = dossier_plugin(args.plugin)
    if args.type == "skill":
        verifier_nom(args.nom)
        creer_depuis_modele(args.plugin, MODELE / "skills" / "exemple-skill" / "SKILL.md",
                            dossier / "skills" / args.nom / "SKILL.md", "exemple-skill", args.nom)
    elif args.type == "agent":
        verifier_nom(args.nom)
        creer_depuis_modele(args.plugin, MODELE / "agents" / "exemple-agent.md",
                            dossier / "agents" / f"{args.nom}.md", "exemple-agent", args.nom)
    elif args.type == "commande":
        verifier_nom(args.nom)
        creer_depuis_modele(args.plugin, MODELE / "commands" / "exemple-commande.md",
                            dossier / "commands" / f"{args.nom}.md", "exemple-commande", args.nom)
    elif args.type == "hooks":
        creer_depuis_modele(args.plugin, MODELE / "hooks" / "hooks.json.exemple",
                            dossier / "hooks" / "hooks.json", "", "")
        (dossier / "scripts").mkdir(exist_ok=True)
    elif args.type == "mcp":
        cible = dossier / ".mcp.json"
        if cible.exists():
            erreur(f"{cible.relative_to(RACINE)} existe déjà.")
        shutil.copy(MODELE / "mcp.json.exemple", cible)
        print(f"✔ Créé : {cible.relative_to(RACINE)}")


if __name__ == "__main__":
    main()

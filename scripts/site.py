#!/usr/bin/env python3
"""Génère la page GitHub Pages du catalogue à partir des manifestes (stdlib uniquement).

  python3 scripts/site.py                     écrit _site/index.html
  python3 scripts/site.py --sortie DOSSIER    écrit DOSSIER/index.html
  python3 scripts/site.py --depot owner/nom   dépôt GitHub cité dans les commandes d'installation

Sources : .claude-plugin/marketplace.json (liste, catégorie, mots-clés), plugin.json
(version, nom affiché) et l'inventaire disque de chaque plugin (skills, agents,
commandes, hooks, MCP). Le gabarit est site/index.html : le script y remplace le
marqueur __CATALOGUE__ par les données en JSON.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
GABARIT = RACINE / "site" / "index.html"
MARQUEUR = "__CATALOGUE__"
DEPOT_PAR_DEFAUT = "fsa64320/marketplace"
BLOC_YAML = re.compile(r"[>|][+-]?")


def lire_json(chemin: Path) -> dict:
    return json.loads(chemin.read_text(encoding="utf-8")) if chemin.exists() else {}


def frontmatter(chemin: Path) -> dict[str, str]:
    """Champs scalaires du frontmatter YAML, blocs repliés (« > ») compris."""
    bloc = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", chemin.read_text(encoding="utf-8"), re.S)
    if not bloc:
        return {}
    champs: dict[str, str] = {}
    cle = None
    for ligne in bloc.group(1).splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", ligne)
        if m:
            cle, valeur = m.group(1), m.group(2).strip()
            champs[cle] = "" if BLOC_YAML.fullmatch(valeur) else valeur.strip("\"'")
        elif cle and ligne.startswith((" ", "\t")):
            champs[cle] = (champs[cle] + " " + ligne.strip()).strip()
        else:
            cle = None
    return champs


def elements(fichiers: list[Path], nom_de) -> list[dict[str, str]]:
    sortie = []
    for fichier in sorted(fichiers):
        champs = frontmatter(fichier)
        sortie.append({"nom": nom_de(fichier, champs), "description": champs.get("description", "")})
    return sortie


def serveurs_mcp(dossier: Path) -> list[dict[str, str]]:
    serveurs = lire_json(dossier / ".mcp.json").get("mcpServers", {})
    return [
        {"nom": nom, "description": conf.get("url") or conf.get("command", "")}
        for nom, conf in sorted(serveurs.items())
    ]


def composants(nom: str, dossier: Path) -> dict[str, list[dict[str, str]]]:
    hooks = lire_json(dossier / "hooks" / "hooks.json").get("hooks", {})
    return {
        "skills": elements(list(dossier.glob("skills/*/SKILL.md")), lambda f, c: c.get("name") or f.parent.name),
        "agents": elements(list(dossier.glob("agents/**/*.md")), lambda f, c: c.get("name") or f.stem),
        "commandes": elements(list(dossier.glob("commands/**/*.md")), lambda f, c: f"/{nom}:{f.stem}"),
        "hooks": [{"nom": evenement, "description": ""} for evenement in sorted(hooks)],
        "mcp": serveurs_mcp(dossier),
    }


def fiche(entree: dict) -> dict:
    dossier = (RACINE / entree["source"]).resolve()
    manifeste = lire_json(dossier / ".claude-plugin" / "plugin.json")
    return {
        "nom": entree["name"],
        "titre": manifeste.get("displayName") or entree["name"],
        "version": manifeste.get("version", ""),
        "description": entree.get("description") or manifeste.get("description", ""),
        "categorie": entree.get("category", ""),
        "motsCles": entree.get("keywords") or manifeste.get("keywords", []),
        "composants": composants(entree["name"], dossier),
    }


def catalogue(depot: str) -> dict:
    marketplace = lire_json(RACINE / ".claude-plugin" / "marketplace.json")
    return {
        "marketplace": marketplace.get("name", ""),
        "description": marketplace.get("description", ""),
        "proprietaire": marketplace.get("owner", {}).get("name", ""),
        "depot": depot,
        "plugins": [fiche(e) for e in sorted(marketplace.get("plugins", []), key=lambda e: e["name"])],
    }


def page(depot: str) -> str:
    gabarit = GABARIT.read_text(encoding="utf-8")
    if MARQUEUR not in gabarit:
        raise SystemExit(f"✘ {GABARIT.relative_to(RACINE)} : marqueur {MARQUEUR} introuvable")
    # « </ » échappé pour qu'une description ne puisse pas fermer la balise <script>
    donnees = json.dumps(catalogue(depot), ensure_ascii=False).replace("</", "<\\/")
    return gabarit.replace(MARQUEUR, donnees)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sortie", default="_site", help="dossier de sortie (défaut : _site)")
    parser.add_argument("--depot", default=os.environ.get("GITHUB_REPOSITORY") or DEPOT_PAR_DEFAUT)
    args = parser.parse_args()
    sortie = Path(args.sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "index.html").write_text(page(args.depot), encoding="utf-8")
    print(f"✔ Page du catalogue écrite dans {sortie / 'index.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

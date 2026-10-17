#!/usr/bin/env python3
"""Vérifie la cohérence de la marketplace (sans dépendance externe).

Complète `claude plugin validate` avec des règles propres à ce dépôt :
- chaque dossier de plugins/ est déclaré dans marketplace.json, et inversement ;
- le nom de l'entrée correspond au nom du plugin.json ;
- chaque SKILL.md, agent et commande a un frontmatter avec les champs attendus ;
- le nom d'un skill correspond au nom de son dossier ;
- hooks.json et .mcp.json sont du JSON valide avec la bonne enveloppe.

Code de sortie 1 s'il y a au moins une erreur.
"""
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
erreurs: list[str] = []
avertissements: list[str] = []


def lire_json(chemin: Path):
    try:
        return json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        erreurs.append(f"{chemin.relative_to(RACINE)} : JSON invalide ({exc})")
        return None


def frontmatter(chemin: Path) -> dict | None:
    texte = chemin.read_text(encoding="utf-8")
    bloc = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", texte, re.S)
    if not bloc:
        erreurs.append(f"{chemin.relative_to(RACINE)} : frontmatter YAML manquant (bloc --- en tête)")
        return None
    champs = {}
    cle = None
    for ligne in bloc.group(1).splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", ligne)
        if m:
            cle = m.group(1)
            valeur = m.group(2).strip()
            # Bloc YAML replié ou littéral (« > », « |- »…) : la valeur suit sur les lignes indentées
            champs[cle] = "" if re.fullmatch(r"[>|][+-]?", valeur) else valeur.strip('"').strip("'")
        elif cle and ligne.startswith((" ", "\t")):
            champs[cle] = (champs[cle] + " " + ligne.strip()).strip()
        else:
            cle = None
    return champs


def exiger(chemin: Path, champs: dict, *cles: str) -> None:
    for cle in cles:
        if not champs.get(cle):
            erreurs.append(f"{chemin.relative_to(RACINE)} : champ « {cle} » manquant dans le frontmatter")


def verifier_plugin(dossier: Path, nom_entree: str) -> None:
    rel = dossier.relative_to(RACINE)
    manifeste = dossier / ".claude-plugin" / "plugin.json"
    if manifeste.exists():
        donnees = lire_json(manifeste)
        if donnees and donnees.get("name") != nom_entree:
            erreurs.append(f"{rel} : plugin.json name « {donnees.get('name')} » ≠ entrée marketplace « {nom_entree} »")
        if donnees and not donnees.get("version"):
            avertissements.append(f"{rel} : pas de « version » dans plugin.json (les utilisateurs suivront chaque commit)")

    for skill in sorted((dossier / "skills").glob("*/SKILL.md")):
        champs = frontmatter(skill)
        if champs is not None:
            exiger(skill, champs, "name", "description")
            if champs.get("name") and champs["name"] != skill.parent.name:
                erreurs.append(f"{skill.relative_to(RACINE)} : name « {champs['name']} » ≠ dossier « {skill.parent.name} »")
            if re.search(r"[<>]", champs.get("description", "")):
                erreurs.append(f"{skill.relative_to(RACINE)} : la description contient des chevrons < > "
                               "(refusés par claude.ai, pris pour des balises XML)")
    for imbrique in sorted((dossier / "skills").glob("*/*/**/SKILL.md")):
        erreurs.append(f"{imbrique.relative_to(RACINE)} : SKILL.md imbriqué, il serait chargé comme un skill à part. "
                       "Renomme un gabarit en SKILL.md.template")
    for dossier_skill in sorted(p for p in (dossier / "skills").glob("*") if p.is_dir()):
        if not (dossier_skill / "SKILL.md").exists():
            erreurs.append(f"{dossier_skill.relative_to(RACINE)} : SKILL.md manquant (attention à la casse)")

    for agent in sorted((dossier / "agents").glob("**/*.md")):
        champs = frontmatter(agent)
        if champs is not None:
            exiger(agent, champs, "name", "description")

    for commande in sorted((dossier / "commands").glob("**/*.md")):
        champs = frontmatter(commande)
        if champs is not None:
            exiger(commande, champs, "description")

    hooks = dossier / "hooks" / "hooks.json"
    if hooks.exists():
        donnees = lire_json(hooks)
        if donnees is not None and not isinstance(donnees.get("hooks"), dict):
            erreurs.append(f"{hooks.relative_to(RACINE)} : l'objet doit être enveloppé dans une clé « hooks »")

    mcp = dossier / ".mcp.json"
    if mcp.exists():
        donnees = lire_json(mcp)
        if donnees is not None and not isinstance(donnees.get("mcpServers"), dict):
            erreurs.append(f"{mcp.relative_to(RACINE)} : l'objet doit contenir une clé « mcpServers »")


def main() -> int:
    marketplace = lire_json(RACINE / ".claude-plugin" / "marketplace.json")
    if marketplace is None:
        return afficher()

    declares = {}
    for entree in marketplace.get("plugins", []):
        nom = entree.get("name", "")
        if not KEBAB.match(nom):
            erreurs.append(f"marketplace.json : nom de plugin « {nom} » pas en kebab-case")
        if nom in declares:
            erreurs.append(f"marketplace.json : plugin « {nom} » déclaré deux fois")
        source = entree.get("source")
        if isinstance(source, str):
            dossier = (RACINE / source).resolve()
            if not dossier.is_dir():
                erreurs.append(f"marketplace.json : source « {source} » introuvable pour « {nom} »")
                continue
            declares[nom] = dossier
            verifier_plugin(dossier, nom)

    for dossier in sorted(p for p in (RACINE / "plugins").glob("*") if p.is_dir()):
        if dossier.resolve() not in declares.values():
            erreurs.append(f"plugins/{dossier.name} n'est pas déclaré dans marketplace.json "
                           f"(utilise : python3 scripts/ajouter.py plugin {dossier.name} \"description\")")
    return afficher()


def afficher() -> int:
    for a in avertissements:
        print(f"⚠ {a}")
    for e in erreurs:
        print(f"✘ {e}")
    if erreurs:
        print(f"\n{len(erreurs)} erreur(s).")
        return 1
    print("✔ Marketplace cohérente.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

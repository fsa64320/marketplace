#!/usr/bin/env python3
"""Vérifie la cohérence de la marketplace (stdlib uniquement).

Complète `claude plugin validate` avec les règles propres à ce dépôt :
- chaque dossier de plugins/ est déclaré dans marketplace.json, et inversement ;
- le nom de l'entrée correspond au nom du plugin.json ;
- chaque SKILL.md, agent et commande a un frontmatter avec les champs attendus ;
- le nom d'un skill correspond au nom de son dossier, sa description n'a pas de chevrons ;
- aucun SKILL.md imbriqué, aucun apm.yml ;
- hooks.json et .mcp.json sont du JSON valide avec la bonne enveloppe ;
- avec --base <ref> : tout plugin modifié depuis <ref> a changé de version.

Code de sortie 1 s'il y a au moins une erreur.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BLOC_YAML = re.compile(r"[>|][+-]?")
erreurs: list[str] = []
avertissements: list[str] = []


def rel(chemin: Path) -> Path:
    return chemin.relative_to(RACINE)


def lire_json(chemin: Path):
    try:
        return json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        erreurs.append(f"{rel(chemin)} : JSON invalide ({exc})")
        return None


def frontmatter(chemin: Path) -> dict | None:
    texte = chemin.read_text(encoding="utf-8")
    bloc = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", texte, re.S)
    if not bloc:
        erreurs.append(f"{rel(chemin)} : frontmatter YAML manquant (bloc --- en tête)")
        return None
    champs: dict[str, str] = {}
    cle = None
    for ligne in bloc.group(1).splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", ligne)
        if m:
            cle, valeur = m.group(1), m.group(2).strip()
            # Bloc YAML replié ou littéral (« > », « |- »…) : la valeur suit sur les lignes indentées
            champs[cle] = "" if BLOC_YAML.fullmatch(valeur) else valeur.strip("\"'")
        elif cle and ligne.startswith((" ", "\t")):
            champs[cle] = (champs[cle] + " " + ligne.strip()).strip()
        else:
            cle = None
    return champs


def exiger(chemin: Path, champs: dict, *cles: str) -> None:
    for cle in cles:
        if not champs.get(cle):
            erreurs.append(f"{rel(chemin)} : champ « {cle} » manquant dans le frontmatter")


def verifier_manifeste(dossier: Path, nom_entree: str) -> None:
    manifeste = dossier / ".claude-plugin" / "plugin.json"
    if not manifeste.exists():
        return
    donnees = lire_json(manifeste)
    if not donnees:
        return
    if donnees.get("name") != nom_entree:
        erreurs.append(f"{rel(dossier)} : name « {donnees.get('name')} » ≠ entrée marketplace « {nom_entree} »")
    if not donnees.get("version"):
        avertissements.append(f"{rel(dossier)} : pas de « version » dans plugin.json")


def verifier_un_skill(skill: Path) -> None:
    champs = frontmatter(skill)
    if champs is None:
        return
    exiger(skill, champs, "name", "description")
    if champs.get("name") and champs["name"] != skill.parent.name:
        erreurs.append(f"{rel(skill)} : name « {champs['name']} » ≠ dossier « {skill.parent.name} »")
    if re.search(r"[<>]", champs.get("description", "")):
        erreurs.append(f"{rel(skill)} : description avec chevrons < > (refusés par claude.ai)")


def verifier_skills(dossier: Path) -> None:
    racine_skills = dossier / "skills"
    for skill in sorted(racine_skills.glob("*/SKILL.md")):
        verifier_un_skill(skill)
    for sous_dossier in sorted(p for p in racine_skills.glob("*") if p.is_dir()):
        if not (sous_dossier / "SKILL.md").exists():
            erreurs.append(f"{rel(sous_dossier)} : SKILL.md manquant (attention à la casse)")
    for imbrique in sorted(racine_skills.glob("*/*/**/SKILL.md")):
        erreurs.append(
            f"{rel(imbrique)} : SKILL.md imbriqué, chargé comme un skill à part. Renomme-le SKILL.md.template"
        )


def verifier_agents_commandes(dossier: Path) -> None:
    for agent in sorted((dossier / "agents").glob("**/*.md")):
        champs = frontmatter(agent)
        if champs is not None:
            exiger(agent, champs, "name", "description")
    for commande in sorted((dossier / "commands").glob("**/*.md")):
        champs = frontmatter(commande)
        if champs is not None:
            exiger(commande, champs, "description")


def verifier_enveloppe(chemin: Path, cle: str) -> None:
    if not chemin.exists():
        return
    donnees = lire_json(chemin)
    if donnees is not None and not isinstance(donnees.get(cle), dict):
        erreurs.append(f"{rel(chemin)} : l'objet doit contenir une clé « {cle} »")


def verifier_plugin(dossier: Path, nom_entree: str) -> None:
    verifier_manifeste(dossier, nom_entree)
    verifier_skills(dossier)
    verifier_agents_commandes(dossier)
    verifier_enveloppe(dossier / "hooks" / "hooks.json", "hooks")
    verifier_enveloppe(dossier / ".mcp.json", "mcpServers")
    for apm in sorted(dossier.glob("**/apm.yml")):
        erreurs.append(
            f"{rel(apm)} : apm.yml inutile ici, supprime-le (la source de vérité est SKILL.md + plugin.json)"
        )


def verifier_catalogue() -> dict[str, Path]:
    marketplace = lire_json(RACINE / ".claude-plugin" / "marketplace.json")
    if marketplace is None:
        return {}
    declares: dict[str, Path] = {}
    for entree in marketplace.get("plugins", []):
        nom, source = entree.get("name", ""), entree.get("source")
        if not KEBAB.match(nom):
            erreurs.append(f"marketplace.json : nom de plugin « {nom} » pas en kebab-case")
        if nom in declares:
            erreurs.append(f"marketplace.json : plugin « {nom} » déclaré deux fois")
        if not isinstance(source, str):
            continue
        dossier = (RACINE / source).resolve()
        if not dossier.is_dir():
            erreurs.append(f"marketplace.json : source « {source} » introuvable pour « {nom} »")
            continue
        declares[nom] = dossier
        verifier_plugin(dossier, nom)
    for dossier in sorted(p for p in (RACINE / "plugins").glob("*") if p.is_dir()):
        if dossier.resolve() not in declares.values():
            erreurs.append(f"plugins/{dossier.name} absent de marketplace.json (utilise scripts/ajouter.py plugin)")
    return declares


def git(*args: str) -> str:
    executable = shutil.which("git")
    if executable is None:
        raise subprocess.CalledProcessError(127, "git", stderr="git introuvable dans le PATH")
    return subprocess.run([executable, *args], cwd=RACINE, capture_output=True, text=True, check=True).stdout


def plugins_modifies(point: str) -> set[str]:
    chemins = git("diff", "--name-only", point).splitlines()
    chemins += git("ls-files", "--others", "--exclude-standard").splitlines()
    return {c.split("/")[1] for c in chemins if c.startswith("plugins/") and c.count("/") >= 2}


def version_a(ref: str, nom: str) -> str | None:
    try:
        texte = git("show", f"{ref}:plugins/{nom}/.claude-plugin/plugin.json")
    except subprocess.CalledProcessError:
        return None  # plugin nouveau depuis la base
    return json.loads(texte).get("version")


def verifier_versions(base: str, declares: dict[str, Path]) -> None:
    try:
        point = git("merge-base", base, "HEAD").strip()
        modifies = plugins_modifies(point)
    except subprocess.CalledProcessError as exc:
        erreurs.append(f"--base {base} : référence git inutilisable ({exc.stderr.strip()})")
        return
    for nom in sorted(modifies & declares.keys()):
        avant = version_a(point, nom)
        manifeste = lire_json(declares[nom] / ".claude-plugin" / "plugin.json") or {}
        if avant is not None and manifeste.get("version") == avant:
            erreurs.append(f"plugins/{nom} modifié depuis {base} sans changement de version (toujours {avant})")


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", help="référence git de comparaison pour exiger un bump de version (ex. origin/main)")
    args = parser.parse_args()
    declares = verifier_catalogue()
    if args.base:
        verifier_versions(args.base, declares)
    return afficher()


if __name__ == "__main__":
    sys.exit(main())

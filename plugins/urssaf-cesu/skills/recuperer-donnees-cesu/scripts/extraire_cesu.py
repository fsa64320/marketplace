#!/usr/bin/env python3
"""Données de salaire du portail CESU de l'Urssaf (bibliothèque standard uniquement).

Trois commandes, dans l'ordre d'usage :

  recuperer   rejoue une requête « Copier en cURL (bash) » enregistrée dans un fichier
              et écrit la réponse JSON dans un fichier.
                python3 extraire_cesu.py recuperer --curl-fichier requete.txt --sortie reponse.json

  inventaire  repère la liste de déclarations dans la réponse et montre ses champs,
              données personnelles masquées, pour choisir les correspondances.
                python3 extraire_cesu.py inventaire --fichier reponse.json

  tableau     produit le tableau Markdown à partir des correspondances choisies.
                python3 extraire_cesu.py tableau --fichier reponse.json \\
                  --champ employe=salarie.prenom,salarie.nom --champ periode=periode \\
                  --champ brut=salaireBrut --champ net=salaireNet \\
                  --champ patronal=cotisationsPatronales --champ salarial=cotisationsSalariales

Le script ne devine aucun champ : il extrait, masque et met en forme. Le choix des
correspondances revient à l'agent, après lecture de l'inventaire.
"""

import argparse
import json
import re
import shlex
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

HOTES_AUTORISES = ("urssaf.fr",)
CLES_SENSIBLES = re.compile(r"nir|secu|insee|iban|bic|adresse|mail|telephone|portable|naissance|password|token", re.I)
VALEUR_SENSIBLE = re.compile(r"\b\d{13,15}\b|\bFR\d{2}[ \d]{20,}\b")
ROLES = ("employe", "periode", "mois", "annee", "brut", "net", "patronal", "salarial")
MONTANTS = ("brut", "net", "patronal", "salarial")
MOIS_FR = (
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre",
)  # fmt: skip


def quitter(message: str, code: int = 1) -> None:
    print(f"✘ {message}", file=sys.stderr)
    sys.exit(code)


# --- recuperer ---------------------------------------------------------------

OPTIONS_A_VALEUR = {
    "-H",
    "--header",
    "-b",
    "--cookie",
    "-X",
    "--request",
    "-d",
    "--data",
    "--data-raw",
    "--data-binary",
}


def lire_curl(texte: str) -> dict:
    """Décompose une commande « Copier en cURL (bash) » : url, méthode, en-têtes, corps."""
    jetons = shlex.split(texte.replace("\\\n", " "))
    requete = {"url": "", "methode": "", "entetes": {}, "corps": None}
    i = 1
    while i < len(jetons):
        jeton = jetons[i]
        if jeton in OPTIONS_A_VALEUR and i + 1 < len(jetons):
            _option(requete, jeton, jetons[i + 1])
            i += 2
            continue
        if jeton.startswith("http"):
            requete["url"] = jeton
        i += 1
    requete["methode"] = requete["methode"] or ("POST" if requete["corps"] is not None else "GET")
    return requete


def _option(requete: dict, option: str, valeur: str) -> None:
    if option in ("-H", "--header") and ":" in valeur:
        nom, contenu = valeur.split(":", 1)
        requete["entetes"][nom.strip()] = contenu.strip()
    elif option in ("-b", "--cookie"):
        requete["entetes"]["Cookie"] = valeur
    elif option in ("-X", "--request"):
        requete["methode"] = valeur.upper()
    else:
        requete["corps"] = valeur


def verifier_url(url: str) -> None:
    morceaux = urllib.parse.urlsplit(url)
    hote = (morceaux.hostname or "").lower()
    if morceaux.scheme != "https":
        quitter("la requête n'est pas en https : refusée.")
    if not any(hote == h or hote.endswith("." + h) for h in HOTES_AUTORISES):
        quitter(f"l'hôte {hote or '(vide)'} n'est pas un domaine urssaf.fr : la session n'y sera pas envoyée.")


def envoyer(requete: dict) -> bytes:
    entetes = {k: v for k, v in requete["entetes"].items() if k.lower() not in ("accept-encoding", "content-length")}
    corps = requete["corps"].encode("utf-8") if requete["corps"] is not None else None
    demande = urllib.request.Request(requete["url"], data=corps, headers=entetes, method=requete["methode"])
    try:
        with urllib.request.build_opener().open(demande, timeout=30) as reponse:
            return reponse.read()
    except urllib.error.HTTPError as erreur:
        if erreur.code in (401, 403):
            quitter(f"HTTP {erreur.code} : session expirée. Reconnectez-vous et copiez une nouvelle requête.", 2)
        quitter(f"HTTP {erreur.code} renvoyé par le portail.")
    except urllib.error.URLError as erreur:
        quitter(f"portail injoignable ({erreur.reason}).")
    return b""


def cmd_recuperer(args: argparse.Namespace) -> None:
    requete = lire_curl(Path(args.curl_fichier).read_text(encoding="utf-8"))
    if not requete["url"]:
        quitter("aucune URL dans le fichier : copiez la requête avec « Copier en cURL (bash) ».")
    verifier_url(requete["url"])
    contenu = envoyer(requete)
    try:
        json.loads(contenu)
    except ValueError:
        quitter("la réponse n'est pas du JSON : copiez une requête qui renvoie les déclarations.")
    Path(args.sortie).write_bytes(contenu)
    print(f"✔ Réponse JSON enregistrée dans {args.sortie} ({len(contenu)} octets).")


# --- lecture et aplatissement ------------------------------------------------


def lire_json(chemin: str):
    try:
        return json.loads(Path(chemin).read_text(encoding="utf-8"))
    except FileNotFoundError:
        quitter(f"fichier introuvable : {chemin}")
    except ValueError as erreur:
        quitter(f"JSON invalide dans {chemin} : {erreur}")
    return None


def aplatir(objet, prefixe: str = "") -> dict:
    """{"a": {"b": 1}} → {"a.b": 1}. Les listes imbriquées sont laissées de côté."""
    plat = {}
    for cle, valeur in objet.items():
        chemin = f"{prefixe}.{cle}" if prefixe else str(cle)
        if isinstance(valeur, dict):
            plat.update(aplatir(valeur, chemin))
        elif not isinstance(valeur, list):
            plat[chemin] = valeur
    return plat


def listes_de_fiches(objet, chemin: str = "$"):
    """Toutes les listes d'objets du document, avec leur chemin."""
    if isinstance(objet, list):
        if objet and all(isinstance(e, dict) for e in objet):
            yield chemin, objet
        for i, element in enumerate(objet[:1]):
            yield from listes_de_fiches(element, f"{chemin}[{i}]")
    elif isinstance(objet, dict):
        for cle, valeur in objet.items():
            yield from listes_de_fiches(valeur, f"{chemin}.{cle}")


def fiches(document, chemin_liste: str | None) -> tuple[str, list[dict]]:
    """La liste désignée par --liste, sinon la plus longue ; un objet seul vaut une fiche."""
    candidates = dict(listes_de_fiches(document))
    if chemin_liste:
        if chemin_liste not in candidates:
            quitter(f"aucune liste d'objets en {chemin_liste}. Listes trouvées : {', '.join(candidates) or 'aucune'}")
        return chemin_liste, [aplatir(f) for f in candidates[chemin_liste]]
    if candidates:
        chemin, liste = max(candidates.items(), key=lambda c: len(c[1]))
        return chemin, [aplatir(f) for f in liste]
    if isinstance(document, dict):
        return "$", [aplatir(document)]
    quitter("le document ne contient aucun objet JSON exploitable.")
    return "", []


# --- inventaire --------------------------------------------------------------


def masquer(cle: str, valeur):
    if CLES_SENSIBLES.search(cle):
        return "*** masqué ***"
    if isinstance(valeur, str):
        return VALEUR_SENSIBLE.sub("***", valeur)[:60]
    return valeur


def cmd_inventaire(args: argparse.Namespace) -> None:
    document = lire_json(args.fichier)
    chemin, liste = fiches(document, args.liste)
    autres = [c for c, _ in listes_de_fiches(document) if c != chemin]
    print(f"Liste retenue : {chemin} ({len(liste)} fiche(s))")
    if autres:
        print(f"Autres listes : {', '.join(autres)} (choisir avec --liste)")
    cles = sorted({c for f in liste for c in f})
    print("\n| Champ | Exemple (fiche 1) | Rempli dans |")
    print("| --- | --- | --- |")
    for cle in cles:
        exemple = masquer(cle, liste[0].get(cle, ""))
        remplies = sum(1 for f in liste if f.get(cle) not in (None, ""))
        print(f"| `{cle}` | {json.dumps(exemple, ensure_ascii=False)} | {remplies}/{len(liste)} |")


# --- tableau -----------------------------------------------------------------


def lire_champs(valeurs: list[str]) -> dict[str, list[str]]:
    champs: dict[str, list[str]] = {}
    for valeur in valeurs:
        role, _, cles = valeur.partition("=")
        if role not in ROLES or not cles:
            quitter(f"--champ {valeur} : attendu role=cle[,cle], rôle parmi {', '.join(ROLES)}.")
        champs[role] = [c.strip() for c in cles.split(",") if c.strip()]
    if not any(r in champs for r in MONTANTS):
        quitter("indiquez au moins un montant : --champ brut=… ou net=… ou patronal=… ou salarial=…")
    return champs


def montant(valeur) -> float:
    if isinstance(valeur, bool) or valeur in (None, ""):
        return 0.0
    if isinstance(valeur, (int, float)):
        return float(valeur)
    texte = re.sub(r"[^\d,.\-]", "", str(valeur))
    if "," in texte and "." in texte:
        texte = texte.replace(",", "") if texte.rfind(".") > texte.rfind(",") else texte.replace(".", "")
    try:
        return float(texte.replace(",", "."))
    except ValueError:
        quitter(f"montant illisible : {valeur!r}")
    return 0.0


def periode(fiche: dict, champs: dict[str, list[str]]) -> tuple[int, int]:
    """(année, mois) depuis le champ periode (« 2025-01 », « 01/2025 », date ISO) ou mois + annee."""
    if "periode" in champs:
        texte = str(fiche.get(champs["periode"][0], ""))
        if m := re.search(r"(\d{4})-(\d{1,2})", texte):
            return int(m[1]), int(m[2])
        if m := re.search(r"(\d{1,2})/(\d{4})", texte):
            return int(m[2]), int(m[1])
    annee = fiche.get(champs.get("annee", [""])[0])
    mois = fiche.get(champs.get("mois", [""])[0])
    return (int(annee) if annee else 0), (int(mois) if mois else 0)


def ligne(fiche: dict, champs: dict[str, list[str]]) -> dict:
    nom = " ".join(str(fiche.get(c, "")).strip() for c in champs.get("employe", [])).strip()
    annee, mois = periode(fiche, champs)
    valeurs = {r: sum(montant(fiche.get(c)) for c in champs.get(r, [])) for r in MONTANTS}
    return {"employe": nom or "—", "annee": annee, "mois": mois, **valeurs}


def euros(v: float) -> str:
    return f"{v:,.2f} €".replace(",", " ").replace(".", ",")


def cellules(r: dict, gras: bool = False) -> str:
    cout = r["brut"] + r["patronal"]
    montants = [r["brut"], r["net"], r["patronal"], r["salarial"], cout]
    return " | ".join(f"**{euros(v)}**" if gras else euros(v) for v in montants)


def cmd_tableau(args: argparse.Namespace) -> None:
    champs = lire_champs(args.champ)
    _, liste = fiches(lire_json(args.fichier), args.liste)
    lignes = sorted((ligne(f, champs) for f in liste), key=lambda r: (r["employe"], r["annee"], r["mois"]))
    lignes = [r for r in lignes if any(r[m] for m in MONTANTS)]
    if not lignes:
        quitter("aucune fiche avec un montant non nul pour ces champs : revoir les correspondances.")
    print("## Données CESU\n")
    print("| Employé | Période | Salaire brut | Salaire net | Cotis. patronales | Cotis. salariales | Coût employeur |")
    print("| --- | --- | ---: | ---: | ---: | ---: | ---: |")
    for r in lignes:
        quand = f"{MOIS_FR[r['mois'] - 1]} {r['annee']}" if 1 <= r["mois"] <= 12 else "—"
        print(f"| {r['employe']} | {quand} | {cellules(r)} |")
    totaux = {m: sum(r[m] for r in lignes) for m in MONTANTS}
    print(f"| **Total** | — | {cellules(totaux, gras=True)} |")
    absents = [m for m in MONTANTS if m not in champs]
    note = f" Colonnes non renseignées (affichées à 0) : {', '.join(absents)}." if absents else ""
    entete = f"{len(lignes)} déclaration(s), extrait le {datetime.now():%d/%m/%Y}."
    print(f"\n_{entete} Coût employeur = brut + cotisations patronales.{note}_")


# --- point d'entrée ----------------------------------------------------------


def analyseur() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sous = parser.add_subparsers(dest="commande", required=True)
    recuperer = sous.add_parser("recuperer", help="rejoue une requête cURL enregistrée et sauve le JSON")
    recuperer.add_argument(
        "--curl-fichier", required=True, help="fichier contenant la commande « Copier en cURL (bash) »"
    )
    recuperer.add_argument("--sortie", required=True, help="fichier JSON à écrire")
    recuperer.set_defaults(action=cmd_recuperer)
    for nom, action in (("inventaire", cmd_inventaire), ("tableau", cmd_tableau)):
        commande = sous.add_parser(nom)
        commande.add_argument("--fichier", required=True, help="réponse JSON du portail")
        commande.add_argument("--liste", help="chemin de la liste de déclarations, tel qu'affiché par inventaire")
        commande.set_defaults(action=action)
        if nom == "tableau":
            commande.add_argument("--champ", action="append", default=[], help="role=cle[,cle] ; répétable")
    return parser


def main() -> None:
    args = analyseur().parse_args()
    args.action(args)


if __name__ == "__main__":
    main()

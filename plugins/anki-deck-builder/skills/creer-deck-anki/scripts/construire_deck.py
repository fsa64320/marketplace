#!/usr/bin/env python3
"""Construit un deck Anki (.apkg) à partir d'une spécification JSON.

Le format de la spécification est décrit dans references/format-spec.md.
Pour le modèle « langue », chaque terme (et chaque exemple) reçoit un fichier
audio généré par une voix neuronale (edge-tts), intégré au paquet.

Usage :
    uv run --project scripts scripts/construire_deck.py SPEC.json --sortie DOSSIER
    uv run --project scripts scripts/construire_deck.py SPEC.json --verifier
    uv run --project scripts scripts/construire_deck.py SPEC.json --sortie DOSSIER --sans-audio

Codes de sortie :
    0  deck écrit (ou spécification valide avec --verifier)
    2  spécification invalide (détail sur stderr)
    3  voix neuronale injoignable : relancer avec --sans-audio pour la voix de l'appareil
"""

import argparse
import asyncio
import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import edge_tts
import genanki
import truststore

CSS = (Path(__file__).resolve().parent / "carte.css").read_text(encoding="utf-8")
SLUG_RE = re.compile(r"[^a-z0-9]+")
CLOZE_RE = re.compile(r"\{\{c\d+::")
CONCURRENCE_TTS = 5
ESSAIS_TTS = 4

# Champs de chaque modèle : (nom du champ, obligatoire)
CHAMPS = {
    "langue": [
        ("terme", True),
        ("lecture", False),
        ("romanisation", False),
        ("traduction", True),
        ("exemple", False),
        ("exemple_traduction", False),
        ("note", False),
    ],
    "basique": [("recto", True), ("verso", True), ("note", False), ("source", False)],
    "inverse": [("recto", True), ("verso", True), ("note", False), ("source", False)],
    "trous": [("texte", True), ("extra", False), ("source", False)],
}
SENS_LANGUE = ("comprehension", "production", "ecoute")


class SpecInvalide(Exception):
    """Erreur de spécification, rapportée telle quelle à l'agent."""


class VoixInjoignable(Exception):
    """Le service de voix neuronale ne répond pas."""


@dataclass
class Spec:
    titre: str
    modele: str
    cartes: list
    langue: dict = field(default_factory=dict)
    sens: list = field(default_factory=lambda: ["comprehension", "production"])
    tags: list = field(default_factory=list)


# ---------------------------------------------------------------- lecture


def identifiant(*parties: str) -> int:
    """Identifiant stable sur 31 bits, pour que réimporter mette à jour au lieu de dupliquer."""
    empreinte = hashlib.sha256("|".join(parties).encode("utf-8")).hexdigest()
    return int(empreinte[:8], 16) & 0x7FFFFFFF


def lire_spec(chemin: Path) -> Spec:
    try:
        brut = json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SpecInvalide(f"JSON illisible : {exc}") from exc
    modele = brut.get("modele", "basique")
    if modele not in CHAMPS:
        raise SpecInvalide(f"modele « {modele} » inconnu ; attendus : {', '.join(CHAMPS)}")
    spec = Spec(
        titre=brut.get("titre", "").strip(),
        modele=modele,
        cartes=brut.get("cartes", []),
        langue=brut.get("langue", {}),
        sens=brut.get("sens", ["comprehension", "production"]),
        tags=brut.get("tags", []),
    )
    verifier_spec(spec)
    return spec


def verifier_spec(spec: Spec) -> None:
    erreurs = []
    if not spec.titre:
        erreurs.append("titre manquant")
    if not spec.cartes:
        erreurs.append("aucune carte")
    if spec.modele == "langue":
        erreurs += verifier_langue(spec)
    for rang, carte in enumerate(spec.cartes, start=1):
        erreurs += verifier_carte(spec.modele, rang, carte)
    erreurs += verifier_doublons(spec)
    if erreurs:
        raise SpecInvalide("\n".join(f"- {e}" for e in erreurs))


def verifier_langue(spec: Spec) -> list:
    erreurs = []
    if not spec.langue.get("voix"):
        erreurs.append("langue.voix manquante (ex. ja-JP-NanamiNeural, voir references/voix.md)")
    if not spec.langue.get("code"):
        erreurs.append("langue.code manquant (ex. ja-JP)")
    inconnus = [s for s in spec.sens if s not in SENS_LANGUE]
    if inconnus or not spec.sens:
        erreurs.append(f"sens invalide {inconnus or spec.sens} ; valeurs possibles : {', '.join(SENS_LANGUE)}")
    return erreurs


def verifier_carte(modele: str, rang: int, carte: dict) -> list:
    if not isinstance(carte, dict):
        return [f"carte {rang} : objet attendu"]
    vides = [nom for nom, requis in CHAMPS[modele] if requis and not carte.get(nom)]
    erreurs = [f"carte {rang} : champ « {nom} » vide" for nom in vides]
    connus = {nom for nom, _ in CHAMPS[modele]} | {"tags", "sous_deck", "prononcer", "prononcer_exemple"}
    erreurs += [f"carte {rang} : champ « {nom} » inconnu pour le modèle {modele}" for nom in carte if nom not in connus]
    if modele == "trous" and carte.get("texte") and not CLOZE_RE.search(carte["texte"]):
        erreurs.append(f"carte {rang} : aucun trou {{{{c1::…}}}} dans le texte")
    return erreurs


def verifier_doublons(spec: Spec) -> list:
    cle = CHAMPS[spec.modele][0][0]
    vus, erreurs = {}, []
    for rang, carte in enumerate(spec.cartes, start=1):
        valeur = str(carte.get(cle, "")).strip() if isinstance(carte, dict) else ""
        if valeur and valeur in vus:
            erreurs.append(f"carte {rang} : « {valeur} » déjà présent en carte {vus[valeur]}")
        vus.setdefault(valeur, rang)
    return erreurs


# ---------------------------------------------------------------- audio


def texte_a_prononcer(carte: dict, champ: str) -> str:
    """Le texte envoyé à la voix : le champ « prononcer… » s'il existe, sinon le champ lui-même sans HTML."""
    surcharge = carte.get("prononcer" if champ == "terme" else "prononcer_exemple")
    texte = surcharge or carte.get(champ, "")
    return re.sub(r"<[^>]+>", "", texte).replace("～", "").replace("~", "").strip()


def nom_audio(voix: str, texte: str) -> str:
    return f"adb_{hashlib.sha256(f'{voix}|{texte}'.encode()).hexdigest()[:16]}.mp3"


def preparer_audio(spec: Spec) -> dict:
    """Retourne {(rang, champ): (texte, nom_fichier)} pour chaque texte à prononcer."""
    voix = spec.langue["voix"]
    plan = {}
    for rang, carte in enumerate(spec.cartes):
        for champ in ("terme", "exemple"):
            texte = texte_a_prononcer(carte, champ)
            if texte:
                plan[(rang, champ)] = (texte, nom_audio(voix, texte))
    return plan


async def _synthetiser(texte: str, chemin: Path, langue: dict, verrou: asyncio.Semaphore) -> None:
    if chemin.exists() and chemin.stat().st_size > 0:
        return
    derniere = None
    async with verrou:
        for _ in range(ESSAIS_TTS):
            try:
                await edge_tts.Communicate(texte, langue["voix"], rate=langue.get("debit", "-10%")).save(str(chemin))
                if chemin.stat().st_size > 0:
                    return
            except Exception as exc:  # erreurs réseau variées d'aiohttp et d'edge-tts
                derniere = exc
            await asyncio.sleep(2)
    raise VoixInjoignable(f"« {texte} » : {derniere}")


async def _tout_synthetiser(plan: dict, dossier_audio: Path, langue: dict) -> None:
    verrou = asyncio.Semaphore(CONCURRENCE_TTS)
    uniques = {nom: texte for texte, nom in plan.values()}
    premier = next(iter(uniques.items()))
    await _synthetiser(premier[1], dossier_audio / premier[0], langue, verrou)
    await asyncio.gather(*(_synthetiser(t, dossier_audio / n, langue, verrou) for n, t in uniques.items()))


def generer_audio(spec: Spec, dossier_audio: Path) -> dict:
    truststore.inject_into_ssl()  # certificats du système : traverse les proxys d'entreprise
    dossier_audio.mkdir(parents=True, exist_ok=True)
    plan = preparer_audio(spec)
    if plan:
        asyncio.run(_tout_synthetiser(plan, dossier_audio, spec.langue))
    return {cle: nom for cle, (_, nom) in plan.items()}


# ---------------------------------------------------------------- modèles


def gabarits_langue(sens: list, avec_audio: bool, code: str) -> list:
    tts = code.replace("-", "_")
    son = "{{Audio}}" if avec_audio else "{{tts " + tts + ":Terme}}"
    son_ex = "{{AudioExemple}}" if avec_audio else "{{tts " + tts + ":Exemple}}"
    cible = (
        '<div class="terme">{{Terme}}</div>{{#Lecture}}<div class="lecture">{{Lecture}}</div>{{/Lecture}}'
        '{{#Romanisation}}<div class="romanisation">{{Romanisation}}</div>{{/Romanisation}}'
    )
    exemple = (
        '{{#Exemple}}<div class="exemple">{{Exemple}} ' + son_ex + "</div>"
        '{{#ExempleTraduction}}<div class="exemple-trad">{{ExempleTraduction}}</div>{{/ExempleTraduction}}'
        '{{/Exemple}}{{#Note}}<div class="note">{{Note}}</div>{{/Note}}'
    )
    trad = '<div class="traduction">{{Traduction}}</div>'
    tous = {
        "comprehension": ("Compréhension", '<div class="consigne">Que signifie…</div>' + cible, trad + son),
        "production": ("Production", '<div class="consigne">Comment dit-on…</div>' + trad, cible + son),
        "ecoute": ("Écoute", '<div class="consigne">Écoute…</div>' + son, cible + trad),
    }
    return [
        {"name": tous[s][0], "qfmt": tous[s][1], "afmt": '{{FrontSide}}<hr id="answer">' + tous[s][2] + exemple}
        for s in sens
    ]


def modele_langue(spec: Spec, avec_audio: bool) -> genanki.Model:
    noms = ["Terme", "Lecture", "Romanisation", "Traduction", "Exemple", "ExempleTraduction", "Note"]
    if avec_audio:
        noms += ["Audio", "AudioExemple"]
    gabarits = gabarits_langue(spec.sens, avec_audio, spec.langue["code"])
    nom = f"Langue {spec.langue['code']} ({'+'.join(spec.sens)}{', audio' if avec_audio else ''})"
    champs = [{"name": n} for n in noms]
    return genanki.Model(identifiant("modele", nom), nom, fields=champs, templates=gabarits, css=CSS)


def modele_question(inverse: bool) -> genanki.Model:
    verso = '<div class="verso">{{Verso}}</div>{{#Note}}<div class="note">{{Note}}</div>{{/Note}}'
    verso += '{{#Source}}<div class="source">{{Source}}</div>{{/Source}}'
    gabarits = [
        {
            "name": "Question → Réponse",
            "qfmt": '<div class="recto">{{Recto}}</div>',
            "afmt": '{{FrontSide}}<hr id="answer">' + verso,
        }
    ]
    if inverse:
        gabarits.append(
            {
                "name": "Réponse → Question",
                "qfmt": '<div class="recto">{{Verso}}</div>',
                "afmt": '{{FrontSide}}<hr id="answer"><div class="verso">{{Recto}}</div>',
            }
        )
    nom = "Question-réponse (deux sens)" if inverse else "Question-réponse"
    champs = [{"name": n} for n in ("Recto", "Verso", "Note", "Source")]
    return genanki.Model(identifiant("modele", nom), nom, fields=champs, templates=gabarits, css=CSS)


def modele_trous() -> genanki.Model:
    nom = "Texte à trous"
    return genanki.Model(
        identifiant("modele", nom),
        nom,
        fields=[{"name": n} for n in ("Texte", "Extra", "Source")],
        templates=[
            {
                "name": "Trou",
                "qfmt": '<div class="recto">{{cloze:Texte}}</div>',
                "afmt": '<div class="recto">{{cloze:Texte}}</div>{{#Extra}}<div class="note">{{Extra}}</div>{{/Extra}}'
                '{{#Source}}<div class="source">{{Source}}</div>{{/Source}}',
            }
        ],
        css=CSS,
        model_type=genanki.Model.CLOZE,
    )


def construire_modele(spec: Spec, avec_audio: bool) -> genanki.Model:
    fabriques = {
        "langue": lambda: modele_langue(spec, avec_audio),
        "basique": lambda: modele_question(inverse=False),
        "inverse": lambda: modele_question(inverse=True),
        "trous": modele_trous,
    }
    return fabriques[spec.modele]()


# ---------------------------------------------------------------- paquet


def valeurs_note(spec: Spec, rang: int, carte: dict, audio: dict) -> list:
    valeurs = [str(carte.get(nom, "")) for nom, _ in CHAMPS[spec.modele]]
    if spec.modele == "langue" and audio is not None:
        valeurs += [f"[sound:{audio[(rang, c)]}]" if (rang, c) in audio else "" for c in ("terme", "exemple")]
    return valeurs


def tags_carte(spec: Spec, carte: dict) -> list:
    return [SLUG_RE.sub("_", t.lower()).strip("_") for t in [*spec.tags, *carte.get("tags", [])] if t]


def construire_paquet(spec: Spec, audio, dossier_audio: Path) -> tuple:
    modele = construire_modele(spec, avec_audio=audio is not None)
    decks = {}
    for rang, carte in enumerate(spec.cartes):
        nom_deck = f"{spec.titre}::{carte['sous_deck']}" if carte.get("sous_deck") else spec.titre
        deck = decks.setdefault(nom_deck, genanki.Deck(identifiant("deck", nom_deck), nom_deck))
        valeurs = valeurs_note(spec, rang, carte, audio)
        guid = genanki.guid_for(spec.titre, spec.modele, valeurs[0], valeurs[1] if spec.modele != "trous" else "")
        deck.add_note(genanki.Note(model=modele, fields=valeurs, tags=tags_carte(spec, carte), guid=guid))
    paquet = genanki.Package(list(decks.values()))
    if audio:
        paquet.media_files = sorted({str(dossier_audio / nom) for nom in audio.values()})
    return paquet, decks


def nombre_cartes(spec: Spec) -> int:
    if spec.modele == "langue":
        return len(spec.cartes) * len(spec.sens)
    if spec.modele == "inverse":
        return len(spec.cartes) * 2
    if spec.modele == "trous":
        return sum(len(set(re.findall(r"\{\{c(\d+)::", c["texte"]))) for c in spec.cartes)
    return len(spec.cartes)


def nom_fichier(titre: str) -> str:
    ascii_ = unicodedata.normalize("NFKD", titre).encode("ascii", "ignore").decode()
    return SLUG_RE.sub("-", ascii_.lower()).strip("-") or "deck"


# ---------------------------------------------------------------- commande


def parser_arguments(argv: list) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("spec", type=Path, help="spécification JSON du deck")
    parser.add_argument("--sortie", type=Path, help="dossier où écrire le .apkg (et le cache audio)")
    parser.add_argument("--verifier", action="store_true", help="valide la spécification sans rien écrire")
    parser.add_argument("--sans-audio", action="store_true", help="pas de voix neuronale : voix de l'appareil d'Anki")
    args = parser.parse_args(argv)
    if not args.verifier and not args.sortie:
        parser.error("--sortie est obligatoire sauf avec --verifier")
    return args


def executer(args: argparse.Namespace) -> dict:
    spec = lire_spec(args.spec)
    resume = {"titre": spec.titre, "modele": spec.modele, "notes": len(spec.cartes), "cartes": nombre_cartes(spec)}
    if args.verifier:
        return resume | {"statut": "spécification valide"}
    args.sortie.mkdir(parents=True, exist_ok=True)
    dossier_audio = args.sortie / f"audio-{nom_fichier(spec.titre)}"
    audio = None
    if spec.modele == "langue" and not args.sans_audio:
        audio = generer_audio(spec, dossier_audio)
    paquet, decks = construire_paquet(spec, audio, dossier_audio)
    chemin = args.sortie / f"{nom_fichier(spec.titre)}.apkg"
    paquet.write_to_file(str(chemin))
    resume |= {"decks": sorted(decks), "fichiers_audio": len(set((audio or {}).values())), "apkg": str(chemin)}
    resume["voix"] = spec.langue.get("voix") if audio else ("voix de l'appareil" if spec.modele == "langue" else None)
    return resume


def main(argv: list) -> int:
    args = parser_arguments(argv)
    try:
        resume = executer(args)
    except SpecInvalide as exc:
        print(f"Spécification invalide :\n{exc}", file=sys.stderr)
        return 2
    except VoixInjoignable as exc:
        print(f"Voix neuronale injoignable ({exc}). Relancer ailleurs ou avec --sans-audio.", file=sys.stderr)
        return 3
    print(json.dumps(resume, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

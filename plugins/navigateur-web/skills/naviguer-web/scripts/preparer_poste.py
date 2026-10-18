"""Prépare le poste pour agent-browser : vérifie, installe, configure.

Usage :
  python3 preparer_poste.py etat        constate sans rien modifier
  python3 preparer_poste.py installer   installe ce qui manque, puis constate

Sortie : un objet JSON sur stdout. Code de retour 0 si le poste est prêt, 1 sinon.
Bibliothèque standard seulement : le script tourne avant que quoi que ce soit soit
installé, sur Windows, macOS et Linux.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

PAQUET_NPM = "agent-browser"
DOSSIER_ETAT = Path.home() / ".agent-browser"
FICHIER_CONFIG = DOSSIER_ETAT / "config.json"
CONFIG_PAR_DEFAUT = {
    # Le texte des pages est délimité : l'agent le distingue de ses instructions.
    "contentBoundaries": True,
    # Une page géante ne noie pas le contexte.
    "maxOutput": 50000,
    # Les requêtes propres à la CLI (install, doctor, read) passent par le magasin
    # de certificats du système, qui contient la CA d'un proxy d'entreprise.
    "useSystemCa": True,
}
VARIABLES_CA = ("NODE_EXTRA_CA_CERTS", "SSL_CERT_FILE", "REQUESTS_CA_BUNDLE")
VARIABLES_PROXY = ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy")
DELAI_INSTALL = 900
DELAI_COURT = 180


def executer(commande: list[str], delai: int = DELAI_COURT) -> tuple[int, str, str]:
    """Lance une commande sans shell et renvoie (code, stdout, stderr)."""
    env = dict(os.environ, AGENT_BROWSER_USE_SYSTEM_CA="1")
    try:
        fini = subprocess.run(commande, capture_output=True, text=True, timeout=delai, env=env, check=False)
    except (OSError, subprocess.TimeoutExpired) as erreur:
        return 1, "", str(erreur)
    return fini.returncode, fini.stdout.strip(), fini.stderr.strip()


def dossier_bin_npm(npm: str) -> Path | None:
    """Dossier où npm pose les exécutables globaux, même s'il manque au PATH."""
    code, prefixe, _ = executer([npm, "prefix", "-g"])
    if code != 0 or not prefixe:
        return None
    racine = Path(prefixe)
    return racine if platform.system() == "Windows" else racine / "bin"


def trouver_binaire() -> tuple[str | None, bool]:
    """Chemin de agent-browser, et s'il est joignable par le PATH."""
    sur_path = shutil.which(PAQUET_NPM)
    if sur_path:
        return sur_path, True
    npm = shutil.which("npm")
    dossier = dossier_bin_npm(npm) if npm else None
    if dossier is None:
        return None, False
    for nom in (f"{PAQUET_NPM}.cmd", f"{PAQUET_NPM}.exe", PAQUET_NPM):
        candidat = dossier / nom
        if candidat.is_file():
            return str(candidat), False
    return None, False


def version(binaire: str) -> str | None:
    code, sortie, _ = executer([binaire, "--version"])
    return sortie.split()[-1] if code == 0 and sortie else None


def diagnostic(binaire: str) -> dict:
    """Lit `agent-browser doctor --json` : Chrome présent, contrôles en échec."""
    _, sortie, erreur = executer([binaire, "doctor", "--json"])
    try:
        rapport = json.loads(sortie)
    except json.JSONDecodeError:
        return {"chrome": False, "echecs": [erreur or sortie or "doctor illisible"]}
    controles = rapport.get("checks", [])
    chrome = any(c.get("id") == "chrome.installed" and c.get("status") == "pass" for c in controles)
    echecs = [f"{c.get('id')} : {c.get('message')}" for c in controles if c.get("status") == "fail"]
    return {"chrome": chrome, "echecs": echecs}


def ca_detectee() -> str | None:
    """Fichier de CA d'entreprise déclaré dans l'environnement, s'il existe."""
    for variable in VARIABLES_CA:
        valeur = os.environ.get(variable)
        if valeur and Path(valeur).is_file():
            return valeur
    return None


def proxy_detecte() -> str | None:
    return next((os.environ[v] for v in VARIABLES_PROXY if os.environ.get(v)), None)


def lire_config() -> dict:
    try:
        return json.loads(FICHIER_CONFIG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def configurer() -> list[str]:
    """Complète ~/.agent-browser/config.json sans écraser une clé déjà posée."""
    config = lire_config()
    attendu = dict(CONFIG_PAR_DEFAUT)
    ca = ca_detectee()
    # Chromium ne lit le caCert que sous Linux ; ailleurs il suit le système.
    if ca and platform.system() == "Linux":
        attendu["caCert"] = ca
    ajoutees = [cle for cle in attendu if cle not in config]
    if ajoutees:
        config.update({cle: attendu[cle] for cle in ajoutees})
        DOSSIER_ETAT.mkdir(parents=True, exist_ok=True)
        FICHIER_CONFIG.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return ajoutees


def constater() -> dict:
    """État du poste, sans rien modifier."""
    binaire, sur_path = trouver_binaire()
    etat = {
        "systeme": platform.system(),
        "node": shutil.which("node"),
        "npm": shutil.which("npm"),
        "binaire": binaire,
        "sur_path": sur_path,
        "version": version(binaire) if binaire else None,
        "proxy": proxy_detecte(),
        "ca": ca_detectee(),
        "config": lire_config(),
        "chrome": False,
        "echecs": [],
    }
    if binaire:
        etat.update(diagnostic(binaire))
    manque_config = [cle for cle in CONFIG_PAR_DEFAUT if cle not in etat["config"]]
    etat["pret"] = bool(binaire and etat["chrome"] and not etat["echecs"] and not manque_config)
    return etat


def installer_paquet(npm: str) -> str | None:
    """npm install -g agent-browser ; renvoie l'erreur, ou None."""
    code, _, erreur = executer([npm, "install", "-g", PAQUET_NPM], DELAI_INSTALL)
    return None if code == 0 else f"npm install -g {PAQUET_NPM} : {erreur[-800:]}"


def installer_chrome(binaire: str) -> str | None:
    """agent-browser install, avec les bibliothèques système sous Linux si possible."""
    if platform.system() == "Linux":
        code, _, _ = executer([binaire, "install", "--with-deps"], DELAI_INSTALL)
        if code == 0:
            return None
    code, _, erreur = executer([binaire, "install"], DELAI_INSTALL)
    return None if code == 0 else f"agent-browser install : {erreur[-800:]}"


def installer() -> dict:
    """Installe ce qui manque, dans l'ordre : paquet, configuration, Chrome."""
    actions, erreurs = [], []
    npm = shutil.which("npm")
    binaire, _ = trouver_binaire()
    if not binaire and not npm:
        erreurs.append("Node.js et npm absents : installer Node.js LTS d'abord.")
    elif not binaire:
        erreur = installer_paquet(npm)
        erreurs += [erreur] if erreur else []
        actions += [] if erreur else [f"npm install -g {PAQUET_NPM}"]
        binaire, _ = trouver_binaire()
    ajoutees = configurer()
    actions += [f"config.json : {', '.join(ajoutees)}"] if ajoutees else []
    if binaire and not diagnostic(binaire)["chrome"]:
        erreur = installer_chrome(binaire)
        erreurs += [erreur] if erreur else []
        actions += [] if erreur else ["agent-browser install"]
    etat = constater()
    etat.update({"actions": actions, "erreurs": erreurs})
    return etat


def main() -> int:
    parseur = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parseur.add_argument("action", choices=["etat", "installer"])
    action = parseur.parse_args().action
    resultat = installer() if action == "installer" else constater()
    print(json.dumps(resultat, indent=2, ensure_ascii=False))
    return 0 if resultat["pret"] else 1


if __name__ == "__main__":
    sys.exit(main())

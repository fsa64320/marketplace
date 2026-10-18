# Plugin `anki-deck-builder`

Construit des decks Anki (`.apkg`) prêts à importer, sur n'importe quel thème. Le contenu vient de recherches web, de fichiers fournis (PDF, Word, notes, CSV, images) ou d'une liste de l'utilisateur. Pour apprendre une langue, chaque mot et chaque phrase d'exemple reçoit un audio en voix neuronale naturelle, intégré au deck.

## Installation

```bash
claude plugin marketplace add fsa64320/marketplace
claude plugin install anki-deck-builder@sales-marketplace
```

Le script du skill s'exécute avec [`uv`](https://docs.astral.sh/uv/), qui installe lui-même ses dépendances (`genanki`, `edge-tts`, `truststore`) au premier lancement.

## Skill

| Skill | Rôle | Se déclenche sur |
|---|---|---|
| `creer-deck-anki` | Cerne le besoin, rassemble le contenu, rédige les cartes et construit le `.apkg` | « crée un deck Anki », « des cartes Anki sur ce PDF », « vocabulaire espagnol avec audio » |

## Types de cartes

| Modèle | Usage | Cartes par note |
|---|---|---|
| `basique` | question → réponse | 1 |
| `inverse` | question ↔ réponse | 2 |
| `trous` | phrase de cours à trous | 1 par trou |
| `langue` | vocabulaire : compréhension, production, écoute ; lecture, romanisation, exemple, audio | 1 par sens choisi |

## Audio

Les voix neuronales Microsoft (Nanami en japonais, Xiaoxiao en chinois, Elvira en espagnol…) sont appelées par `edge-tts`, sans clé ni compte. Les MP3 sont intégrés au deck : même voix sur ordinateur, iPhone et Android, hors ligne.

Le service doit être joignable en HTTPS (`speech.platform.bing.com`). Sur un réseau qui le bloque, le skill construit le deck avec la voix intégrée de l'appareil et le signale ; une nouvelle construction depuis un réseau ouvert remplace l'audio sans perdre la progression.

## Utiliser le script seul

Depuis `skills/creer-deck-anki/` :

```bash
uv run --project scripts scripts/construire_deck.py assets/exemple-langue.json --sortie ~/Downloads
```

Format de la spécification : `skills/creer-deck-anki/references/format-spec.md`.

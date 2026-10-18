# Format de la spécification JSON

`scripts/construire_deck.py` lit un seul fichier JSON et en tire un `.apkg`. Exemples complets : `assets/exemple-langue.json`, `assets/exemple-question.json`, `assets/exemple-trous.json`.

## Clés de premier niveau

| Clé | Obligatoire | Valeur |
|---|---|---|
| `titre` | oui | nom du deck dans Anki ; donne aussi le nom du fichier `.apkg` |
| `modele` | non (`basique`) | `langue`, `basique`, `inverse` ou `trous` |
| `cartes` | oui | liste des notes (une note peut produire plusieurs cartes) |
| `tags` | non | tags ajoutés à toutes les notes |
| `langue` | si `modele` = `langue` | `{ "nom", "code", "voix", "debit" }` — voir `voix.md` |
| `sens` | non (`comprehension`, `production`) | modèle `langue` seulement : sous-ensemble de `comprehension`, `production`, `ecoute` |

## Champs d'une carte, par modèle

Commun à tous les modèles : `tags` (liste) et `sous_deck` (texte, crée `Titre::Sous-deck` dans Anki).

| Modèle | Champs obligatoires | Champs facultatifs | Cartes produites par note |
|---|---|---|---|
| `langue` | `terme`, `traduction` | `lecture`, `romanisation`, `exemple`, `exemple_traduction`, `note`, `prononcer`, `prononcer_exemple` | une par valeur de `sens` |
| `basique` | `recto`, `verso` | `note`, `source` | 1 |
| `inverse` | `recto`, `verso` | `note`, `source` | 2 (recto → verso et verso → recto) |
| `trous` | `texte` (avec au moins un `{{c1::…}}`) | `extra`, `source` | une par numéro de trou distinct |

Le HTML simple est accepté dans tous les champs (`<b>`, `<i>`, `<br>`, `<ul>`). Un champ inconnu fait échouer la vérification : c'est voulu, une faute de frappe ne disparaît pas en silence.

## Modèle `langue` : ce que l'apprenant voit

| Sens | Recto | Verso |
|---|---|---|
| `comprehension` | terme, lecture, romanisation | traduction, audio du terme, exemple avec son audio, note |
| `production` | traduction | terme, lecture, romanisation, audio, exemple, note |
| `ecoute` | audio seul | terme, lecture, romanisation, traduction, exemple |

`ecoute` n'a de sens qu'avec l'audio neuronal : avec `--sans-audio` il reste possible mais repose sur la voix de l'appareil.

## Ce que la voix prononce

Par défaut, `terme` et `exemple`, sans HTML ni `～`. `prononcer` et `prononcer_exemple` remplacent ce texte quand l'écriture affichée se lit mal : kanji japonais à lecture ambiguë, abréviation, gabarit `～をください`. Exemple : `"terme": "お会計"`, `"prononcer": "おかいけい"`.

## Réimport et mises à jour

Les identifiants de deck, de modèle et de note sont dérivés du titre et du contenu. Réimporter un deck corrigé met à jour les notes existantes au lieu de les dupliquer, tant que `titre` et le premier champ d'une note ne changent pas.

## Sortie de la commande

Le script affiche un résumé JSON sur stdout :

```json
{
  "titre": "Japonais — Au restaurant",
  "modele": "langue",
  "notes": 3,
  "cartes": 6,
  "decks": ["Japonais — Au restaurant::Boissons", "Japonais — Au restaurant::Phrases utiles"],
  "fichiers_audio": 5,
  "apkg": "sortie/japonais-au-restaurant.apkg",
  "voix": "ja-JP-NanamiNeural"
}
```

Codes de sortie : `0` deck écrit, `2` spécification invalide (liste des erreurs sur stderr), `3` voix neuronale injoignable.

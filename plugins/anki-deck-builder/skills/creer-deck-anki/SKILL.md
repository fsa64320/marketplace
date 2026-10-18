---
name: creer-deck-anki
description: >
  Construit un deck Anki (.apkg) prêt à importer sur n'importe quel thème, à partir de
  recherches web ou de fichiers fournis (PDF, Word, notes, CSV, images), avec cartes
  question-réponse, dans les deux sens, à trous ou de vocabulaire. Pour une langue, chaque
  mot et chaque exemple reçoit un audio en voix neuronale naturelle intégré au deck.
  Pose les questions utiles quand la demande est floue. Utiliser quand l'utilisateur dit
  "crée un deck Anki", "fais-moi des flashcards", "des cartes Anki sur ce PDF",
  "un deck pour apprendre le japonais", "vocabulaire espagnol avec audio",
  "transforme ce cours en cartes de révision", "ajoute des cartes à mon deck".
---

# Créer un deck Anki

## Ce que ce skill fait

Il cerne le besoin, rassemble le contenu (web, fichiers, liste de l'utilisateur), rédige les cartes dans une spécification JSON, puis `scripts/construire_deck.py` en fait un `.apkg` avec l'audio neuronal pour les langues.

Toutes les commandes se lancent depuis le dossier de ce skill.

## Étapes

1. **Relève ce que la demande dit déjà** : sujet, source du contenu (web, fichier joint, liste fournie), objectif (examen, voyage, culture, travail), niveau, nombre de cartes, type de cartes. Pour une langue : langue et variante régionale, langue de traduction (celle de l'utilisateur par défaut), écriture et romanisation, sens d'étude.

2. **Pose les questions qui manquent**, et seulement celles-là, en une fois (avec l'outil de questions à choix s'il existe, sinon en texte, quatre questions au plus). Une question vaut d'être posée si sa réponse change le contenu des cartes :

   | Manque | Question | Choix proposés |
   |---|---|---|
   | Sujet trop large (« l'histoire », « Azure ») | Sur quelle partie ? | 3 sous-thèmes concrets + « tout le thème, survol » |
   | Niveau | Quel est ton niveau sur ce sujet ? | Débutant, intermédiaire, avancé |
   | Objectif | À quoi va servir ce deck ? | Examen précis, usage pratique, culture générale |
   | Source | D'où doit venir le contenu ? | Recherches web, le fichier que tu vas m'envoyer, une liste que tu me donnes |
   | Taille | Combien de cartes environ ? | Selon `references/conception-cartes.md` |
   | Langue : sens | Quelles cartes veux-tu ? | Comprendre et produire (conseillé), + écoute seule, comprendre seulement |
   | Langue : voix | Quelle voix ? | Féminine, masculine (tableau de `references/voix.md`) |

   Sujet, source et taille clairs : ne pose aucune question et passe à l'étape 3. L'utilisateur absent ou qui ne répond pas : prends les valeurs par défaut de `references/conception-cartes.md` et annonce-les en tête de ta réponse finale.

3. **Rassemble le contenu** selon la source :
   - Fichier fourni : lis-le en entier avec l'outil adapté à son format (PDF, Word, tableur, image). Les cartes ne contiennent que ce que le document dit ; note la page ou la section dans `source`.
   - Web : fais les recherches nécessaires, privilégie les sources de référence (documentation officielle, encyclopédies, dictionnaires, sites institutionnels), recoupe tout chiffre ou date sur deux sources, et mets le titre de la page dans `source`.
   - Liste de l'utilisateur : garde ses termes tels quels ; complète seulement les champs vides (traduction, lecture, exemple) et signale ce que tu as ajouté.
   - Langue sans source imposée : rédige toi-même à partir du vocabulaire le plus fréquent du thème, en vérifiant la lecture et l'orthographe de chaque mot.

4. **Rédige la spécification JSON** dans un fichier de travail, au format de `references/format-spec.md`, en suivant `references/conception-cartes.md`. Pour une langue, choisis `langue.voix` et `langue.debit` dans `references/voix.md` et remplis `prononcer` quand la colonne du tableau le demande. Pars de l'exemple le plus proche dans `assets/`.

5. **Vérifie la spécification** :

   ```bash
   uv run --project scripts scripts/construire_deck.py SPEC.json --verifier
   ```

   Code 2 : corrige chaque erreur listée sur stderr et relance jusqu'au code 0.

6. **Relis le contenu** avant de construire : pas de doublon de sens, une réponse par carte, aucune faute dans la langue étudiée, chaque fait d'un document présent dans ce document. Pour un deck de plus de 40 notes rédigé sans liste fournie, montre d'abord 5 notes représentatives et la répartition par sous-deck, et demande si le ton et le niveau conviennent ; utilisateur absent : continue.

7. **Construis le deck** dans le dossier où l'utilisateur veut le fichier (son dossier de travail ou ses téléchargements à défaut) :

   ```bash
   uv run --project scripts scripts/construire_deck.py SPEC.json --sortie DOSSIER
   ```

   - Code 0 : passe à l'étape 8.
   - Code 3 (voix neuronale injoignable, typiquement un réseau qui bloque `speech.platform.bing.com`) : si tu disposes d'un autre environnement d'exécution avec un accès internet plus large, comme un terminal sur l'ordinateur de l'utilisateur, copie-y le dossier du skill et la spécification et relance la même commande. Sinon relance avec `--sans-audio` et dis à l'utilisateur que les cartes utiliseront la voix de son appareil, moins naturelle, et qu'une nouvelle construction depuis un réseau ouvert remplacera l'audio sans perdre sa progression.

8. **Livre le fichier** : envoie le `.apkg` à l'utilisateur (ou indique son emplacement s'il est déjà sur son ordinateur) et termine par ce bloc, adapté au résumé JSON du script :

   > **Japonais — Au restaurant** : 3 notes, 6 cartes (compréhension et production), audio en voix Nanami intégré.
   > Pour l'importer : double-clic sur le fichier, ou Fichier → Importer dans Anki.
   > Rythme conseillé : 10 à 20 nouvelles cartes par jour.

   Ajoute une seule suite utile s'il y en a une (deck complémentaire, sens `ecoute`, autre chapitre du document).

## Compléter ou corriger un deck existant

Garde **le même `titre`** et le même premier champ pour les notes existantes : à l'import, Anki met à jour ces notes et ajoute les nouvelles sans toucher à la progression. Reprends la spécification précédente si elle est disponible ; sinon demande à l'utilisateur la liste des termes déjà présents.

## Ce que ce skill ne fait pas

- Lire ou modifier directement la collection Anki de l'utilisateur : il produit un fichier à importer.
- Intégrer des images aux cartes : il se limite au texte et à l'audio.
- Générer l'audio pour un modèle autre que `langue`.

# Voix neuronales par langue

Le script utilise les voix neuronales Microsoft via `edge-tts`, sans clé ni compte. Les fichiers MP3 sont intégrés au `.apkg` : l'apprenant entend la même voix sur ordinateur, iPhone et Android, hors ligne.

## Voix recommandées

| Langue | `code` | Voix féminine | Voix masculine |
|---|---|---|---|
| Japonais | `ja-JP` | `ja-JP-NanamiNeural` | `ja-JP-KeitaNeural` |
| Chinois mandarin | `zh-CN` | `zh-CN-XiaoxiaoNeural` | `zh-CN-YunxiNeural` |
| Coréen | `ko-KR` | `ko-KR-SunHiNeural` | `ko-KR-InJoonNeural` |
| Anglais (États-Unis) | `en-US` | `en-US-AriaNeural` | `en-US-GuyNeural` |
| Anglais (Royaume-Uni) | `en-GB` | `en-GB-SoniaNeural` | `en-GB-RyanNeural` |
| Espagnol (Espagne) | `es-ES` | `es-ES-ElviraNeural` | `es-ES-AlvaroNeural` |
| Espagnol (Mexique) | `es-MX` | `es-MX-DaliaNeural` | `es-MX-JorgeNeural` |
| Allemand | `de-DE` | `de-DE-KatjaNeural` | `de-DE-ConradNeural` |
| Italien | `it-IT` | `it-IT-ElsaNeural` | `it-IT-DiegoNeural` |
| Portugais (Brésil) | `pt-BR` | `pt-BR-FranciscaNeural` | `pt-BR-AntonioNeural` |
| Portugais (Portugal) | `pt-PT` | `pt-PT-RaquelNeural` | `pt-PT-DuarteNeural` |
| Russe | `ru-RU` | `ru-RU-SvetlanaNeural` | `ru-RU-DmitryNeural` |
| Arabe (standard) | `ar-SA` | `ar-SA-ZariyahNeural` | `ar-SA-HamedNeural` |
| Néerlandais | `nl-NL` | `nl-NL-ColetteNeural` | `nl-NL-MaartenNeural` |
| Français | `fr-FR` | `fr-FR-DeniseNeural` | `fr-FR-HenriNeural` |

Langue absente du tableau, ou doute sur un nom : lister les voix disponibles depuis le dossier du skill et filtrer sur le code de langue.

```bash
uv run --project scripts edge-tts --list-voices | grep -i "ko-KR"
```

Choisir une voix `…Neural` de la variante régionale que l'utilisateur veut apprendre. Sans préférence exprimée, prendre la voix féminine du tableau.

## Débit

`debit` accepte un pourcentage signé. Valeurs conseillées :

| Niveau de l'apprenant | `debit` |
|---|---|
| Débutant | `-15%` à `-10%` |
| Intermédiaire | `-5%` ou `+0%` |
| Avancé, travail de l'écoute | `+0%` à `+10%` |

## Ce que la voix doit lire, langue par langue

| Langue | `terme` | `lecture` | `romanisation` | `prononcer` |
|---|---|---|---|---|
| Japonais | forme usuelle (kanji si courant, sinon kana) | kana | rōmaji Hepburn | kana, dès que `terme` contient des kanji |
| Chinois | caractères simplifiés (ou traditionnels si demandé) | pinyin avec tons (`nǐ hǎo`) | vide | inutile : la voix lit les caractères |
| Coréen | hangeul | vide | romanisation révisée | inutile |
| Russe, grec, arabe, hébreu | écriture native (accent tonique noté en russe pour débutant) | vide | translittération | inutile |
| Langues en alphabet latin | le mot, avec article pour les noms (`der Tisch`, `la mesa`) | vide | vide | inutile |

Un `terme` construit comme gabarit (`～をください`, `to ___ sth`) se prononce mal : mettre dans `prononcer` une phrase complète qui l'illustre.

## Repli sans voix neuronale

Le service de voix exige un accès HTTPS à `speech.platform.bing.com`. S'il est bloqué, le script sort en code 3. Relancé avec `--sans-audio`, il construit le même deck dont les cartes utilisent la synthèse vocale intégrée d'Anki (`{{tts …}}`), qui dépend des voix installées sur chaque appareil : correcte sur iPhone et Android, souvent pauvre sur ordinateur.

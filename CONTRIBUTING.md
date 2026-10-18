# Contribuer

Le dépôt est public ; Frederick en est le seul mainteneur. Rien de secret ne s'y committe : l'historique est visible de tous. Ces règles valent pour lui comme pour un agent IA, qui suit en plus [`AGENTS.md`](./AGENTS.md).

## Flux

```bash
git config core.hooksPath .githooks          # une fois par clone : refuse un push direct vers main
git fetch origin
git switch -c feat/description-courte origin/main
# … modifications …
git commit -m "feat(mon-plugin): ajoute le skill truc"
git push -u origin HEAD
gh pr create --base main
```

La CI tourne sur la PR ; une fois verte, on merge en **squash** (le titre de la PR devient le commit de `main`). Une PR = un sujet.

`main` est protégée par le ruleset « Protection de main » : PR obligatoire, merge en squash seul, CI verte (les quatre jobs de `valider.yml`), ni force-push ni suppression, sans contournement. Le hook `pre-push` refuse le push plus tôt, en local. Un cas exceptionnel passe par la désactivation temporaire du ruleset dans Settings > Rules, pas par `AUTORISER_PUSH_MAIN`.

## Portes à lancer avant de pousser

La CI relance les mêmes ; tout constat fait échouer le build : on corrige, on n'explique pas.

```bash
python3 scripts/valider.py --base origin/main
python3 scripts/catalogue.py --check
claude plugin validate . --strict
python3 plugins/ai-builder/skills/skill-builder/scripts/lint_skill.py plugins/<plugin>/skills/<skill>
uvx ruff check . && uvx ruff format --check .
uvx --python 3.12 bandit -c pyproject.toml -r scripts plugins .github/scripts
```

## Branches et commits

Branches `type/description-courte`, en minuscules et tirets : `feat/skill-revue-archi`, `fix/ai-builder-gabarits`, `docs/contribuer`.

Commits au format [Conventional Commits](https://www.conventionalcommits.org/fr/v1.0.0/), **en français** : `type(portée): résumé à l'impératif`.

| Type | Pour |
|---|---|
| `feat` | nouveau plugin, skill, agent, commande, hook ou serveur MCP |
| `fix` | un comportement cassé |
| `docs` | documentation seule |
| `test` | tests et scripts de vérification |
| `chore` | bump de version, ménage |
| `ci` | workflows, scripts de `.github/` et `scripts/` |
| `perf` | plus rapide, même comportement |
| `refactor` | même comportement, autre forme |

La portée est le nom du plugin (`ai-builder`), ou `marketplace` pour ce qui touche le dépôt entier.

Les signatures de commits sont diagnostiquées sur chaque PR (workflow *Signatures des commits*) sans bloquer : l'avertissement donne la cause et l'action.

## Ajouter ou modifier un plugin

```bash
python3 scripts/ajouter.py plugin mon-plugin "Ce que fait le plugin"
python3 scripts/ajouter.py skill    mon-plugin mon-skill
python3 scripts/ajouter.py agent    mon-plugin mon-agent
python3 scripts/ajouter.py commande mon-plugin ma-commande
python3 scripts/ajouter.py hooks    mon-plugin
python3 scripts/ajouter.py mcp      mon-plugin
```

Le script applique `templates/plugin/`, déclare le plugin dans `marketplace.json` et régénère le tableau du README. La page du catalogue (GitHub Pages) se republie seule au merge sur `main` ; pour la voir avant : `python3 scripts/site.py` puis ouvrir `_site/index.html`. Une icône pour la tuile du plugin : `site/icones/<plugin>.svg` (sinon, ses initiales).

Les règles qui mordent, détaillées dans [`CLAUDE.md`](./CLAUDE.md) :

- le nom du dossier fait l'identité : `name` du SKILL.md, du plugin.json et entrée de `marketplace.json` identiques, en kebab-case ;
- **bump de `version`** du plugin à tout changement significatif, sinon personne ne reçoit la mise à jour ;
- après un changement de manifeste ou de composant : `python3 scripts/catalogue.py` ;
- pas de `SKILL.md` imbriqué (gabarit = `SKILL.md.template`), pas de chevrons dans une description, pas d'`apm.yml`, pas de secret en clair.

Un skill déjà écrit ailleurs : copier son dossier dans `plugins/<plugin>/skills/`, supprimer un éventuel `apm.yml`, vérifier que `name` égale le nom du dossier.

Le code livré avec un skill va dans `scripts/` du skill ; avec des dépendances tierces, il a son propre `pyproject.toml` + `uv.lock`. Chaque fonction reste sous le gate ruff (complexité 12, 12 branches, 50 instructions, 6 arguments) : on découpe, on n'ajoute pas de `noqa`.

## Écrire un skill

Utilise `ai-builder:skill-builder` : il porte le format, et `lint_skill.py` est la porte mécanique. Ce qu'on attend en relecture :

- des étapes numérotées, chacune une action concrète ;
- l'agent est adressé directement ; pas de prérequis, de difficulté ni de durée ;
- les chemins sont relatifs au dossier du skill ;
- le format de sortie est montré tel quel ;
- une section dit ce que le skill ne fait **pas** et renvoie au skill voisin ;
- les gabarits et exemples longs sont des fichiers sous `assets/`, pas des blocs de code dans le corps ;
- la description, en français, dit ce que fait le skill, quand l'utiliser et les phrases qui le déclenchent.

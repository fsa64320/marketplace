# CLAUDE.md

Guide pour Claude Code quand il travaille dans ce dépôt.

## Ce qu'est ce dépôt

`fsa64320/marketplace` est la marketplace Claude Code **sales-marketplace** de Frederick : un catalogue de plugins (skills, agents, commandes slash, hooks, serveurs MCP). Il n'y a ni application ni runtime : chaque dossier de `plugins/` est un plugin que Claude Code installe depuis ce dépôt (`claude plugin marketplace add fsa64320/marketplace`). Le catalogue est `.claude-plugin/marketplace.json`.

Le dépôt est public (pour servir la page GitHub Pages du catalogue) et **en français** : documentation, commits, PR, descriptions des skills.

`CONTRIBUTING.md` porte les règles du contributeur humain, `AGENTS.md` celles d'un agent (worktree, portes, ce qu'il ne touche pas). Les conventions de ces trois fichiers doivent rester d'accord.

### Flux

`main` ne reçoit **aucun push direct** : branche `type/description-courte` → PR → CI verte → merge en **squash** par Frederick, ou par Claude uniquement sur sa demande explicite. GitHub l'impose par le ruleset « Protection de main » (Settings > Rules > Rulesets) : PR obligatoire, merge en squash seul, les quatre jobs de `valider.yml` verts, ni force-push ni suppression, sans contournement possible, même pour Frederick. Les hooks locaux (`.githooks/pre-push`, hook de `.claude/settings.json`) refusent le push plus tôt, avec le bon message. Les signatures de commits sont diagnostiquées sur chaque PR, sans bloquer.

Sécurité du dépôt public : détection de secrets avec blocage au push, alertes Dependabot, mises à jour mensuelles des actions des workflows (`.github/dependabot.yml`), approbation exigée pour les workflows de toute PR externe, jeton des workflows en lecture seule. Aucun secret ne va dans le dépôt ni dans son historique : il est public.

Renommer un job de `valider.yml` casse le ruleset (la vérification attendue ne se présente plus et le merge reste bloqué) : renomme aussi la vérification requise dans le ruleset.

## Commandes

Derrière le proxy, pas de `pip` : tout passe par `uv` / `uvx`.

Les portes que la CI relance, à zéro constat avant de pousser :

```bash
python3 scripts/valider.py --base origin/main
python3 scripts/catalogue.py --check
claude plugin validate . --strict && claude plugin validate plugins/<plugin> --strict
python3 plugins/ai-builder/skills/skill-builder/scripts/lint_skill.py plugins/<plugin>/skills/<skill>
uvx ruff check . && uvx ruff format --check .
uvx --python 3.12 bandit -c pyproject.toml -r scripts plugins .github/scripts
```

Créer un plugin ou un composant (applique `templates/plugin/` et régénère le tableau du README) :

```bash
python3 scripts/ajouter.py plugin <plugin> "description"
python3 scripts/ajouter.py skill|agent|commande <plugin> <nom>
python3 scripts/ajouter.py hooks|mcp <plugin>
```

Régénérer le tableau des plugins du README après toute modification d'un manifeste ou d'un composant : `python3 scripts/catalogue.py`.

La page GitHub Pages du catalogue (https://fsa64320.github.io/marketplace/) est générée par `python3 scripts/site.py` à partir des mêmes manifestes et du gabarit `site/index.html` (icône d'un plugin : `site/icones/<plugin>.svg`, carré 64×64 ; sans elle, une tuile à ses initiales) ; elle s'écrit dans `_site/` (ignoré par git) et la CI la republie à chaque merge sur `main`. Rien à régénérer à la main.

Tester l'installation sans toucher à sa configuration (`CLAUDE_CONFIG_DIR` isole la configuration, `./` est exigé pour un chemin local) :

```bash
export HOME=$(mktemp -d) CLAUDE_CONFIG_DIR=$HOME/.claude
claude plugin marketplace add ./ && claude plugin install <plugin>@sales-marketplace
```

CI : `.github/workflows/valider.yml` (structure et versions, `claude plugin validate`, `lint_skill.py`, ruff, bandit), `signatures.yml` (consultatif) et `pages.yml` (publie la page du catalogue sur GitHub Pages après chaque merge sur `main`).

## Modèle de plugin

| Composant | Emplacement | Fichier requis | Règles |
|---|---|---|---|
| Plugin | `plugins/<plugin>/` | `.claude-plugin/plugin.json` | `name` = nom du dossier = entrée de `marketplace.json` ; `version` présente |
| Skill | `skills/<skill>/` | `SKILL.md` (frontmatter `name`, `description`) | `name` = nom du dossier ; annexes dans `references/`, `assets/`, `scripts/` |
| Agent | `agents/<agent>.md` | frontmatter `name`, `description` (+ `tools`, `model`) | outils au plus juste |
| Commande | `commands/<commande>.md` | frontmatter `description` (+ `argument-hint`) | appelée en `/<plugin>:<commande>` |
| Hook | `hooks/hooks.json` | objet enveloppé dans une clé `hooks` | scripts dans `scripts/`, appelés via `${CLAUDE_PLUGIN_ROOT}` |
| MCP | `.mcp.json` | objet avec une clé `mcpServers` | serveurs Python lancés par `uvx` ; secrets en `userConfig` |

### Règles qui mordent

- **Le nom du dossier fait l'identité.** Le `name` d'un SKILL.md égale son dossier ; le `name` d'un plugin.json égale son dossier et son entrée dans `marketplace.json`. Tout en kebab-case. Un écart ne fait pas forcément échouer le chargement : le composant est simplement appelé par un nom et se décrit par un autre.
- **Bump de `version`** du plugin à tout changement significatif : sans lui, les postes déjà installés ne reçoivent rien. `valider.py --base origin/main` refuse un plugin modifié dont la version n'a pas bougé.
- **La description déclenche.** Elle dit ce que fait le composant, quand l'utiliser et les phrases que l'utilisateur tape. Jamais de chevrons `< >` : claude.ai les prend pour des balises et refuse la description.
- **Aucun `SKILL.md` imbriqué.** Un `SKILL.md` sous `assets/` est chargé comme un skill à part : un gabarit s'appelle `SKILL.md.template`.
- **Chemins relatifs au dossier du skill** dans un SKILL.md ; `${CLAUDE_PLUGIN_ROOT}` dans les hooks et les MCP. Jamais de chemin absolu.
- **Pas de secret en clair** dans `.mcp.json` ou `plugin.json` : `userConfig` avec `"sensitive": true`.
- **Pas d'`apm.yml`** : la source de vérité est `SKILL.md` + `plugin.json`, la CI refuse le fichier.
- Toute modification d'un manifeste ou d'un composant change le tableau du README : `python3 scripts/catalogue.py`.

## Scripts livrés avec un skill

Le code exécutable va dans `skills/<skill>/scripts/`. Bibliothèque standard de préférence ; s'il faut des paquets tiers, le dossier `scripts/` porte son propre `pyproject.toml` + `uv.lock` et s'exécute par `uv run --project <dossier scripts>`. Le `pyproject.toml` racine ne configure que ruff et bandit.

Ruff borne la taille de chaque fonction : complexité McCabe 12, 12 branches, 50 instructions, 6 arguments (`C901`, `PLR0912`, `PLR0915`, `PLR0913`). Une fonction qui dépasse se découpe : jamais de `noqa`, jamais de relèvement des seuils. Méthode : `plugins/ai-builder/skills/skill-builder/references/scripts.md`. Bandit tourne sur `scripts/`, `plugins/` et `.github/scripts/` ; un exécutable s'appelle par son chemin résolu (`shutil.which`), pas par un nom nu.

## Style des skills

- Des étapes numérotées, chacune une action concrète avec la commande, l'option ou le champ exact. Une étape qui énonce une intention n'est pas une étape.
- S'adresser à l'agent, pas à un lecteur. Pas de prérequis, de difficulté, de durée : c'est chargé à chaque activation et ne change aucun comportement.
- Le format de sortie se **montre** (le vrai tableau), il ne se décrit pas.
- Une section « Ce que ce skill ne fait pas » renvoie au skill voisin qui le fait.
- Les gabarits et exemples longs sont de vrais fichiers sous `assets/`, jamais des blocs de code dans le corps : un bloc imbriqué ferme le bloc extérieur et avale silencieusement la suite.
- Les descriptions sont en français. Les skills importés gardent la description de leur source.

Pour écrire ou diagnostiquer un composant : `ai-builder:skill-builder`, `ai-builder:agent-builder`, `ai-builder:slash-command-builder`, `ai-builder:hooks-builder`.

## Origine d'ai-builder

Les quatre skills d'`ai-builder` viennent de `sta-ai-tools/skills` (dépôt d'équipe, catalogue APM). Ils ont été adaptés ici : gabarits de `skill-builder` renommés en `SKILL.md.template`, `apm.yml` supprimés. Une correction faite ici se reporte dans la source, et inversement, sinon la prochaine synchronisation l'écrase.

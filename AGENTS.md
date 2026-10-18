# Consignes pour un agent — sales-marketplace

Lis d'abord [`CLAUDE.md`](./CLAUDE.md) : modèle de plugin, règles qui mordent, commandes. Ce fichier dit **comment travailler** dans ce dépôt.

## Langue

Tout en **français** : commits, titres et corps de PR, branches, commentaires, documentation, descriptions de skills. Exception : les skills importés d'`ai-builder` gardent le texte de leur source.

## Travailler dans un worktree dédié

Ne travaille pas dans le clone principal : Frederick y travaille peut-être.

```bash
git fetch origin
git worktree add ../marketplace-<tâche> -b <type>/<description-courte> origin/main
cd ../marketplace-<tâche>
git config core.hooksPath .githooks
```

Puis :

1. Fais le changement, avec `scripts/ajouter.py` pour tout nouveau plugin ou composant.
2. Bumpe la `version` de chaque plugin modifié, puis lance `python3 scripts/catalogue.py`.
3. Lance les portes (ci-dessous) jusqu'à zéro constat.
4. Committe au format `type(portée): résumé à l'impératif`, pousse la branche, ouvre la PR : `gh pr create --base main`.
5. **Ne merge pas.** Frederick merge, ou te le demande explicitement ; dans ce cas `gh pr merge <n> --squash`, que le hook de `.claude/settings.json` soumet à sa confirmation.
6. Une fois la PR mergée : `git worktree remove ../marketplace-<tâche>`.

Jamais de push vers `main` : `.githooks/pre-push` et le hook Claude Code le refusent. Ne contourne ni l'un ni l'autre (`AUTORISER_PUSH_MAIN`, `--no-verify`) : ce sont les seules protections de `main`, GitHub Free n'en offrant aucune sur un dépôt privé.

Une décision qui revient à Frederick surgit en route (périmètre d'un nouveau plugin, compromis de sécurité, deux conceptions incompatibles, un accès qui te manque) : arrête-toi et pose-lui la question plutôt que de trancher.

## Avant de pousser

```bash
python3 scripts/valider.py --base origin/main
python3 scripts/catalogue.py --check
claude plugin validate . --strict && claude plugin validate plugins/<plugin> --strict
python3 plugins/ai-builder/skills/skill-builder/scripts/lint_skill.py plugins/<plugin>/skills/<skill>
uvx ruff check . && uvx ruff format --check .
uvx --python 3.12 bandit -c pyproject.toml -r scripts plugins .github/scripts
```

Atteins zéro constat au lieu d'expliquer les constats restants. Une fonction trop complexe se découpe ; pas de `noqa`, pas de `# nosec`, pas de seuil relevé.

## Ce que tu ne touches pas

- **Une copie installée d'un plugin** (`~/.claude/plugins/…`, le cache de plugins) : c'est un artefact d'installation, la source est ici. Une modification là-bas est perdue à la prochaine mise à jour.
- **`templates/plugin/`** sans mettre à jour `scripts/ajouter.py` dans la même PR : le script remplace des marqueurs précis (`__NOM__`, `exemple-skill`…).
- **Le bloc entre `<!-- plugins:start -->` et `<!-- plugins:end -->` du README** à la main : il est généré par `scripts/catalogue.py`.
- **`_site/`** : page générée par `scripts/site.py`. Le rendu se change dans le gabarit `site/index.html`.
- **Les skills d'`ai-builder`** sans signaler qu'il faut reporter la modification dans `sta-ai-tools/skills`, d'où ils viennent.

## Affirmations sur le contenu

Ne décris pas un skill, un fichier ou un comportement que tu n'as pas ouvert dans la session ; dis clairement ce qui n'a pas été vérifié.

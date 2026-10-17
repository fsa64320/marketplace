# sales-marketplace

Marketplace personnelle de plugins pour Claude Code : skills, agents, commandes slash, hooks et serveurs MCP. Chaque dossier de `plugins/` est un plugin installable séparément.

## Installer

Dans un terminal :

```bash
claude plugin marketplace add fsa64320/marketplace
claude plugin install ai-builder@sales-marketplace
```

Ou dans une session Claude Code : `/plugin marketplace add fsa64320/marketplace`, puis `/plugin` pour parcourir et installer.

Récupérer les nouvelles versions : `claude plugin marketplace update sales-marketplace`, puis mettre à jour le plugin dans `/plugin`. Un plugin dont la `version` n'a pas changé n'est pas redistribué.

## Plugins

Tableau généré par `python3 scripts/catalogue.py` à partir des manifestes ; la CI échoue s'il n'est pas à jour.

<!-- plugins:start -->
| Plugin | Version | Description | Composants |
| --- | --- | --- | --- |
| `ai-builder` | 1.0.2 | Skills pour construire et diagnostiquer des skills, agents, commandes slash et hooks | Skills : `agent-builder`, `hooks-builder`, `skill-builder`, `slash-command-builder` |
<!-- plugins:end -->

Les composants d'un plugin sont préfixés par son nom : `ai-builder:skill-builder`.

## Organisation

```text
.claude-plugin/marketplace.json   catalogue : la liste des plugins publiés
plugins/<plugin>/                 un dossier par plugin
  .claude-plugin/plugin.json      manifeste (nom, version, description)
  skills/<skill>/SKILL.md         skills (+ references/, assets/, scripts/)
  agents/<agent>.md               sous-agents
  commands/<commande>.md          commandes slash → /<plugin>:<commande>
  hooks/hooks.json                hooks (scripts dans scripts/)
  .mcp.json                       serveurs MCP
templates/plugin/                 modèle utilisé par scripts/ajouter.py
scripts/ajouter.py                crée un plugin ou un composant
scripts/valider.py                règles du dépôt (--base : bump de version exigé)
scripts/catalogue.py              tableau des plugins de ce README
.githooks/pre-push                refuse un push direct vers main
.claude/settings.json             même garde-fou pour Claude Code dans ce dépôt
```

## Contribuer

Pas de push direct sur `main` : une branche, une PR, une CI verte, puis un merge en squash. Les règles du flux, des commits et des plugins sont dans [`CONTRIBUTING.md`](./CONTRIBUTING.md) ; un agent IA suit en plus [`AGENTS.md`](./AGENTS.md). Le modèle de plugin et les règles qui mordent sont dans [`CLAUDE.md`](./CLAUDE.md).

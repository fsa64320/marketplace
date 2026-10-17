# sales-marketplace

Marketplace personnelle de plugins pour Claude Code : skills, agents, commandes slash, hooks et serveurs MCP.

## Installer

Dans un terminal :

```bash
claude plugin marketplace add fsa64320/marketplace
claude plugin install boite-a-outils@sales-marketplace
```

Ou dans une session Claude Code : `/plugin marketplace add fsa64320/marketplace`, puis `/plugin` pour parcourir et installer.

Mettre à jour après un push : `claude plugin marketplace update sales-marketplace`.

## Organisation

```text
.claude-plugin/marketplace.json   catalogue : la liste des plugins publiés
plugins/<plugin>/                 un dossier par plugin
  .claude-plugin/plugin.json      manifeste (nom, version, description)
  skills/<skill>/SKILL.md         skills (+ fichiers annexes dans le même dossier)
  agents/<agent>.md               sous-agents
  commands/<commande>.md          commandes slash  → /<plugin>:<commande>
  hooks/hooks.json                hooks (scripts dans scripts/)
  .mcp.json                       serveurs MCP
templates/plugin/                 modèle utilisé par scripts/ajouter.py
scripts/ajouter.py                crée un plugin ou un composant
scripts/valider.py                contrôle la cohérence du dépôt
```

Un plugin regroupe des composants qui vont ensemble. Tous ses composants sont préfixés par son nom (`boite-a-outils:revue-architecture`).

## Ajouter du contenu

```bash
python3 scripts/ajouter.py plugin mon-plugin "Ce que fait le plugin"   # crée et déclare le plugin
python3 scripts/ajouter.py skill    mon-plugin mon-skill
python3 scripts/ajouter.py agent    mon-plugin mon-agent
python3 scripts/ajouter.py commande mon-plugin ma-commande
python3 scripts/ajouter.py hooks    mon-plugin
python3 scripts/ajouter.py mcp      mon-plugin
```

Pour un skill déjà écrit ailleurs, copie simplement son dossier dans `plugins/<plugin>/skills/` : le dossier doit contenir `SKILL.md` et le champ `name` du frontmatter doit être identique au nom du dossier.

Avant de pousser :

```bash
python3 scripts/valider.py
claude plugin validate . --strict
```

La même vérification tourne dans GitHub Actions à chaque push et pull request.

## Versions

Chaque `plugin.json` porte une `version`. Tant qu'elle ne change pas, les utilisateurs restent sur la version installée : incrémente-la quand tu publies une modification d'un plugin.

## Plugins

| Plugin | Contenu |
| --- | --- |
| `boite-a-outils` | Skill `revue-architecture`, agent `architecte-cloud`, commande `/boite-a-outils:adr`, hook garde-fou contre les commandes destructrices, MCP Microsoft Learn et AWS Documentation |

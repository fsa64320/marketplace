# Règles du dépôt fsa-marketplace

Ce dépôt est une marketplace de plugins Claude Code. Quand tu y ajoutes ou modifies du contenu :

- Tout composant (skill, agent, commande, hook, MCP) vit dans un plugin sous `plugins/<plugin>/`, jamais à la racine.
- Pour créer un plugin ou un composant, utilise `python3 scripts/ajouter.py` : il applique le modèle de `templates/plugin/` et déclare le plugin dans `.claude-plugin/marketplace.json`.
- Noms en kebab-case. Le `name` d'un SKILL.md est identique au nom de son dossier ; le `name` d'un plugin.json est identique à son entrée dans marketplace.json.
- La `description` d'un skill ou d'un agent dit ce qu'il fait ET quand l'utiliser : c'est elle qui le déclenche.
- Les scripts appelés par les hooks ou les MCP se référencent via `${CLAUDE_PLUGIN_ROOT}`, jamais par chemin absolu.
- Python : installer les paquets avec `uv` (pip fonctionne mal derrière le proxy) ; les serveurs MCP Python se lancent avec `uvx`.
- Pas de secret en clair dans `.mcp.json` ou `plugin.json` : utiliser `userConfig` avec `"sensitive": true`.
- Incrémente la `version` du plugin.json modifié.
- Avant de committer : `python3 scripts/valider.py` puis `claude plugin validate . --strict` et `claude plugin validate plugins/<plugin> --strict`.
- Mets à jour le tableau « Plugins » du README.

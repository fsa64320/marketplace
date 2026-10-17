---
description: Rédige un Architecture Decision Record (ADR) à partir d'une décision décrite en argument
argument-hint: "<décision à documenter>"
allowed-tools: Read, Write, Glob
---

Rédige un ADR pour la décision suivante : $ARGUMENTS

1. Cherche un dossier `docs/adr/` dans le projet. S'il existe, prends le numéro suivant ; sinon crée-le et commence à `0001`.
2. Nomme le fichier `docs/adr/NNNN-titre-en-kebab-case.md`.
3. Utilise ce gabarit :

```markdown
# NNNN. Titre

- Statut : Proposé
- Date : (date du jour)

## Contexte
## Décision
## Options envisagées
## Conséquences
```

4. Si le contexte est trop mince pour remplir une section, écris ce qui manque plutôt que de l'inventer.

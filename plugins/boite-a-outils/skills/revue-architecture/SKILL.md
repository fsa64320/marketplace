---
name: revue-architecture
description: Revue structurée d'une architecture cloud Azure ou AWS selon les piliers du Well-Architected Framework. À utiliser quand l'utilisateur demande de relire, challenger ou valider un schéma, un document ou une proposition d'architecture.
---

# Revue d'architecture cloud

Tu fais la revue d'une architecture proposée par l'utilisateur (schéma, document, IaC ou description).

## Démarche

1. **Comprendre le contexte** : objectif métier, utilisateurs, volumétrie, contraintes réglementaires, cloud cible (Azure, AWS ou hybride). Si un de ces éléments manque et change la conclusion, pose la question avant de juger.
2. **Évaluer chaque pilier** du Well-Architected Framework :
   - Fiabilité (zones de disponibilité, reprise, points de défaillance uniques)
   - Sécurité (identité, réseau, chiffrement, secrets, journalisation)
   - Optimisation des coûts (dimensionnement, réservations, ressources inactives)
   - Excellence opérationnelle (IaC, observabilité, déploiement)
   - Efficacité des performances (mise à l'échelle, cache, latence)
3. **Pour l'IA générative** : ajouter gouvernance des modèles, protection des données envoyées aux LLM, garde-fous et traçabilité.

## Format de sortie

Un tableau par pilier avec : constat, gravité (Bloquant / Majeur / Mineur), recommandation concrète, service cloud concerné.
Termine par les trois actions prioritaires.

Pour les documents officiels, utilise les serveurs MCP de documentation du plugin quand ils sont disponibles plutôt que ta mémoire.

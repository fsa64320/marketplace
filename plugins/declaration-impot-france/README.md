# Plugin `declaration-impot-france`

Assistant fiscal pour les contribuables français : analyse des documents fiscaux, guide de la déclaration de revenus, optimisation et questions fiscales.

## Installation

```bash
claude plugin marketplace add fsa64320/marketplace
claude plugin install declaration-impot-france@sales-marketplace
```

## Skills

| Skill | Rôle | Se déclenche sur |
|---|---|---|
| `analyse-document-fiscal` | Lit un IFU, un relevé SCPI, une attestation ; consolide les montants par case de la 2042 | « analyse mon IFU », « lis mon relevé SCPI », « IFU Boursorama » |
| `guide-declaration` | Accompagne la saisie sur impots.gouv.fr, écran par écran | « faire ma déclaration », « quelles cases remplir », « remplir le formulaire 2044 » |
| `optimisation-fiscale` | Retient et chiffre les leviers d'économie adaptés au foyer | « PFU ou barème progressif », « LMNP réel ou micro », « combien verser sur mon PER » |
| `expert-fiscal-qa` | Explique une règle ou un dispositif, CGI à l'appui | « comment fonctionne le LMNP », « qu'est-ce que l'IFI », « c'est quoi la case 2DC » |

Chaque skill renvoie aux autres pour ce qui n'est pas de son ressort.

## Barèmes

Les taux, plafonds et seuils sont dans `references/baremes.md`, **dupliqué à l'identique** dans `analyse-document-fiscal`, `expert-fiscal-qa` et `optimisation-fiscale` : mettre les trois copies à jour ensemble à chaque loi de finances. Version actuelle : revenus 2025, déclaration 2026.

## Serveur MCP

`.mcp.json` déclare le serveur MCP de data.gouv.fr (`https://mcp.data.gouv.fr/mcp`), qui donne accès aux jeux de données publics. Aucun skill ne l'appelle encore explicitement.

## Avertissement

Outil d'aide informatif : il ne remplace pas un expert-comptable ou un conseiller fiscal. Pour une situation complexe, consultez un professionnel ou le service des impôts au 0809 401 401.

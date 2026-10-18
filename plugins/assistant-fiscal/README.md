# Plugin `assistant-fiscal`

Assistant fiscal pour les contribuables français : analyse des documents fiscaux, guide de la déclaration de revenus, optimisation et questions fiscales.

## Installation

```bash
claude plugin marketplace add fsa64320/marketplace
claude plugin install assistant-fiscal@sales-marketplace
```

Le plugin s'appelait `declaration-impot-france` jusqu'à la version 1.4.1. Un poste qui a l'ancien nom le désinstalle puis installe le nouveau :

```bash
claude plugin uninstall declaration-impot-france@sales-marketplace
claude plugin marketplace update sales-marketplace
claude plugin install assistant-fiscal@sales-marketplace
```

## Skills

| Skill | Rôle | Se déclenche sur |
|---|---|---|
| `analyse-document-fiscal` | Lit un IFU, un relevé SCPI, une attestation ; consolide les montants par case de la 2042 | « analyse mon IFU », « lis mon relevé SCPI », « IFU Boursorama » |
| `guide-declaration` | Accompagne la saisie sur impots.gouv.fr, écran par écran | « faire ma déclaration », « quelles cases remplir », « remplir le formulaire 2044 » |
| `optimisation-fiscale` | Retient et chiffre les leviers d'économie adaptés au foyer | « PFU ou barème progressif », « LMNP réel ou micro », « combien verser sur mon PER » |
| `expert-fiscal-qa` | Explique une règle ou un dispositif, CGI à l'appui | « comment fonctionne le LMNP », « qu'est-ce que l'IFI », « c'est quoi la case 2DC » |
| `verification-legislation` | Fixe l'année des revenus et vérifie taux, barème, plafonds et cases avant tout chiffrage ; appelé en premier par les quatre autres | « vérifie les barèmes de cette année », « ces chiffres sont-ils encore valables » |

Chaque skill renvoie aux autres pour ce qui n'est pas de son ressort.

## Indépendance vis-à-vis de l'année

Le plugin ne code aucune année en dur. Avant tout calcul, chaque skill applique `verification-legislation`, qui :

1. fixe l'année des revenus (document fourni, date du jour, ou question à l'utilisateur) ;
2. vérifie sur les sources officielles (impots.gouv.fr, BOFiP, service-public.fr, Légifrance) les taux, seuils et cases dont la réponse dépend, ainsi que la loi de finances et la LFSS de l'année ;
3. affiche en tête de réponse une fiche qui donne, pour chaque chiffre, sa valeur, son statut (✅ vérifié, ⚠️ à confirmer, ❌ non vérifié) et sa source.

Sans accès web, les chiffres viennent des valeurs de référence du plugin et sont marqués ❌, avec leur année.

## Mise à jour annuelle

Les valeurs de référence sont dans `skills/verification-legislation/references/valeurs-de-reference.md` (actuellement revenus 2025). Quand le skill signale un écart (« Valeurs de référence du plugin à mettre à jour… »), ou après le vote de la loi de finances (janvier) et la parution de la notice 2042 (avril) : mettre le fichier à jour avec sa date de vérification, bumper la version du plugin, ouvrir une PR.

## Serveur MCP

`.mcp.json` déclare le serveur MCP public de BENSAID Avocats (`https://outils.bensaid-avocats.fr/mcp`), gratuit, sans authentification, en lecture seule. `verification-legislation` l'utilise à son étape 7 :

| Outil | Usage |
|---|---|
| `openfisca_parameter` | barèmes et taux datés |
| `legifrance_article` | article du CGI ou du LPF en vigueur |
| `bofip_search`, `bofip_get` | doctrine BOFiP, versions en vigueur seulement |
| `conventions_search`, `conventions_article` | conventions fiscales, pour les revenus étrangers |

C'est un service tiers sans garantie de disponibilité, et son corpus est daté : il complète la recherche web sur impots.gouv.fr, il ne la remplace pas. Les skills ne lui envoient que des termes juridiques, jamais de données personnelles.

## Avertissement

Outil d'aide informatif : il ne remplace pas un expert-comptable ou un conseiller fiscal. Pour une situation complexe, consultez un professionnel ou le service des impôts au 0809 401 401.

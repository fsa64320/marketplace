# Plugin `cse-totalenergies`

Renseigne sur les deux sites sociaux de TotalEnergies : le **CSE de Pau** (csetotalenergiespau.fr : subventions, voyages organisés, vacances individuelles, billetterie, CESU) et le **CSEC UES AGSH** (csecuesagshtotal.fr : séjours patrimoine, escapades, aides scolaires, prêts, secours). Il lit les sites dans le navigateur de l'utilisateur, déjà connecté, et prépare les demandes sans jamais les valider.

## Installation

```bash
claude plugin marketplace add fsa64320/marketplace
claude plugin install cse-totalenergies@sales-marketplace
```

## Skills

| Skill | Rôle | Se déclenche sur |
|---|---|---|
| `naviguer-cse-csec` | Socle : quel site pour quoi, ouverture des pages publiques et de l'espace privé, interdits | « va sur le site du CSE », « ouvre mon espace CSEC » |
| `solde-et-consommations` | Plafond, subvention consommée, solde, dossiers en attente, historique des aides et prêts | « combien de subvention j'ai utilisé », « mon solde CSE » |
| `voyages-et-sejours` | Voyages groupes, vacances individuelles, locations, escapades, séjours jeunesse ; reste à charge | « où partir cet hiver », « compare les locations du CSEC » |
| `aides-et-prets` | Aide scolaire, permis, BAFA, prêts, secours, CESU, frais de garde : conditions, montants, dates | « ai-je droit à une aide scolaire », « prêt travaux au CSEC » |
| `echeances-et-actualites` | Actualités, offres du moment, dates limites triées | « quoi de neuf au CSE », « dates limites » |
| `preparer-une-demande` | Prérequis, pièces, estimation, fiche de préparation, ouverture du formulaire sans validation | « prépare ma demande d'aide scolaire » |

## Fonctionnement

Les deux sites utilisent le même logiciel (ACL) : mêmes menus, même espace privé. Le plugin ne contient aucun script et aucune donnée personnelle : les skills disent à l'agent où lire et comment présenter le résultat, et les chiffres sont relus sur les sites à chaque demande. Le fichier `skills/naviguer-cse-csec/references/plan-des-sites.md` recense les rubriques et leurs adresses.

L'accès à l'espace privé passe par Claude in Chrome (sinon le navigateur intégré, sinon le plugin `navigateur-web`), dans la session que l'utilisateur a lui-même ouverte.

## Sécurité

- Aucun identifiant ni mot de passe n'est demandé ni saisi : si la session est fermée, l'utilisateur se connecte lui-même.
- Aucune demande n'est validée, envoyée ni confirmée par le plugin ; aucun mandat n'est signé, aucun fichier joint.
- Le dépôt est public : aucune donnée de l'espace privé (identité, enfants, montants personnels) n'y est copiée.

## Limites

- Les adresses des pages changent parfois d'une année à l'autre : le plan est un relevé du 18/10/2026, à rafraîchir depuis les menus.
- Le solde prévisionnel et le reste à charge sont des estimations : le CSE et le CSEC valident le montant définitif.
- Le CSE couvert est celui de Pau. Les autres CSE de l'UES (Paris, CRES, TRTG) ont d'autres sites.

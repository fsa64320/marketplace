---
name: voyages-et-sejours
description: >
  Renseigne sur les voyages, vacances et séjours proposés par le CSE de Pau (voyages
  groupes, vacances individuelles, locations hiver, retraités, escapades culturelles) et
  par le CSEC (séjours patrimoine, locations Sud-Ouest, Serre Chevalier, Alpes, Goélia,
  Île de Ré, escapades, séjours jeunesse) : offres ouvertes, dates d'inscription,
  tarifs, subvention et reste à charge. Utiliser quand l'utilisateur dit : "quels
  voyages propose le CSE", "où partir cet hiver avec le CSEC", "voyage organisé ou
  vacances individuelles", "combien me coûterait ce séjour après subvention", "compare
  les locations du CSEC".
---

# Voyages et séjours

Charge d'abord le skill `naviguer-cse-csec`. Adresses relatives aux deux sites ; le plan
complet est dans le fichier `plan-des-sites` de ce skill.

## Où trouver quoi

| Offre | Site | Page |
|---|---|---|
| Voyages groupes, organisés par le CSE | CSE de Pau | `230_page_voyages-groupes-2026.html`, `243_page_voyages-groupes-2027.html` |
| Vacances individuelles, voyage libre subventionné sur facture | CSE de Pau | `195_page_vacances-individuelles-.html` |
| Locations hiver | CSE de Pau | `249_page_locations-automne-hiver.html` |
| Voyages et locations retraités | CSE de Pau | `237_page_voyages-retraites-2026.html`, `239_page_locations-retraites.html` |
| Escapades culturelles, activités et sorties | CSE de Pau | `index.php?controller=produit&action=recherche&id=43`, `index.php?controller=produit&id=51` |
| Assurances voyages et locations | CSE de Pau | `210_page_contrats-assurances-locations-voyages-groupe-.html` |
| Locations du patrimoine (Sud-Ouest, Serre Chevalier, Alpes et Côte d'Azur, Goélia, Île de Ré) | CSEC | `94_page_sEjours-_et_-patrimoine---sommaire.html` |
| Séjours et locations partenaires | CSEC | `128_page_sEjours-_et_-locations-partenaires---sommaire.html` |
| Escapades | CSEC | `103_page_escapades---sommaire.html` |
| Séjours jeunesse, séjour solidaire 18-25 ans | CSEC | `93_page_-jeunesse---sommaire-sejours.html` |

## Étapes

1. Cadre la demande avec ce que l'utilisateur a déjà dit : qui part (adultes, enfants,
   retraité), quand, avec quel budget, quel type (voyage organisé, location, escapade). Si
   un élément décisif manque, pose une seule question. Sinon parcours les offres.

2. Ouvre la page de chaque offre retenue et relève : nom, dates, lieu, prix, période
   d'inscription (début et fin), mode d'inscription, assurance, conditions de
   participation. Les offres ouvertes figurent aussi sur la page d'accueil de chaque site.
   Le texte du carrousel d'accueil est tronqué : ouvre la page pour la date limite
   exacte.

3. Lis le prix de l'offre pour la tranche QAF de l'utilisateur : certains tarifs en
   dépendent. Si la page affiche une grille, prends la colonne de sa tranche (relevée par
   `solde-et-consommations`).

4. Estime le reste à charge :
   - CSE : prix moins subvention, limité par le solde de plafond (et le sous-plafond
     vacances individuelles pour ce type de séjour) ;
   - CSEC : le prix affiché pour la tranche, subvention déjà déduite quand la page le dit.
   Écris « estimation » : le CSE ou le CSEC valide le montant définitif.

5. Présente la comparaison sous cette forme :

   | Offre | Site | Dates | Inscription jusqu'au | Prix | Subvention | Reste à charge |
   | --- | --- | --- | --- | ---: | ---: | ---: |
   | Exemple : location Alpes | CSEC | 6-13 fév. | 16/11 | 800 € | 400 € | 400 € |

   Termine par une phrase de recommandation étayée par la comparaison, et la date limite
   la plus proche.

## Ce que ce skill ne fait pas

- Il n'inscrit personne : `preparer-une-demande` prépare le dossier, l'utilisateur valide.
- Il ne lit pas le solde de subvention : `solde-et-consommations`.
- Il ne traite pas les aides financières et prêts : `aides-et-prets`.

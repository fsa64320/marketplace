---
name: aides-et-prets
description: >
  Renseigne sur les aides financières, subventions et prêts du CSEC (aide scolaire,
  permis de conduire, BAFA, permis bateau, prêts construction ou achat, amélioration de
  l'habitat, études onéreuses, caisse d'entraide, caisse de secours aux actifs) et du CSE
  de Pau (CESU, frais de garde, classes transplantées, stages et ateliers, activités
  extérieures, transport d'enfant en situation de handicap). Donne conditions, montants,
  dates de campagne et pièces à fournir. Utiliser quand l'utilisateur dit : "ai-je droit
  à une aide scolaire", "prêt travaux au CSEC", "subvention permis de conduire",
  "quelles aides pour mes enfants", "caisse de secours", "aide pour le BAFA".
---

# Aides et prêts

Charge d'abord le skill `naviguer-cse-csec`. Adresses relatives aux deux sites.

## Où trouver quoi

| Aide | Site | Page |
|---|---|---|
| Aide scolaire (campagne de l'année) | CSEC | `132_page_aides-scolaires---2026.html` |
| Subventions permis, sommaire | CSEC | `131_page_subventions-permis---sommaire.html` |
| Permis de conduire, BAFA, permis bateau | CSEC | `87_page_-jeunesse---permis-de-conduire.html`, `86_page_-jeunesse---stage-bafa.html`, `108_page_subvention-permis-bateau.html` |
| Prêts : construction ou achat, amélioration de l'habitat, études onéreuses | CSEC | `76_page_-prEts---construction-achat.html`, `75_page_-prEts---amelioration-de-l-habitat.html`, `74_page_-prEts---etudes-onereuses.html` |
| Caisse d'entraide, caisse de secours aux actifs | CSEC | `78_page_caisse-d-entraide.html`, `119_page_caisse-de-secours-aux-actifs.html` |
| CESU service à la personne, CESU frais de garde, frais de garde | CSE de Pau | `index.php?controller=produit&id=48`, `index.php?controller=produit&id=49`, `index.php?controller=produit&action=recherche&id=17` |
| Stages et ateliers, activités extérieures | CSE de Pau | `index.php?controller=produit&id=16`, `index.php?controller=produit&id=50` |
| Classes transplantées, transport d'enfant en situation de handicap | CSE de Pau | `index.php?controller=produit&action=detail&type_code=SUB&code=SOCLDIV2P&libelle_produit=classes-transplantees`, `234_page_transport-d-enfant-en-situation-de-handicap.html` |

## Étapes

1. Identifie l'aide visée à partir de la demande et du tableau. Si plusieurs aides
   peuvent convenir (enfant au collège : aide scolaire, stage, frais de garde), liste-les
   toutes et traite-les ensemble.

2. Ouvre la page de chaque aide et relève : public concerné et conditions, montant ou
   barème (selon le QAF quand la page l'indique), dates d'ouverture et de clôture de la
   campagne, pièces justificatives, mode de dépôt (en ligne ou non), délai de versement.
   Les campagnes changent chaque année : la page de l'année en cours fait foi, pas une
   valeur retenue d'une conversation précédente.

3. Vérifie les prérequis du CSEC : avant toute demande, les coordonnées bancaires doivent
   être enregistrées et un mandat signé (`index.php?controller=membre&action=bank`), et le
   QAF calculé par le CSE de rattachement. Un utilisateur inactif, retraité ou expatrié
   sous contrat TGI n'a pas accès aux prestations du CSEC.

4. Cherche ce qui est déjà demandé : lis les consommations du site concerné (skill
   `solde-et-consommations`) pour repérer une aide déjà versée ou en cours pour la même
   personne et la même année, et éviter un doublon.

5. Pour un prêt, relève taux, durée, plafond de prêt et conditions de remboursement tels
   qu'ils figurent sur la page ; ne simule pas d'échéancier à partir de chiffres
   supposés.

6. Présente chaque aide sous cette forme :

   | Aide | Site | Pour qui | Montant | Ouverture - clôture | Pièces à fournir | Déjà demandée cette année |
   | --- | --- | --- | --- | --- | --- | --- |
   | Exemple : aide scolaire collège ou lycée | CSEC | enfant scolarisé | 100 € par enfant | 15/09 - 16/11 | certificat de scolarité | oui, 2 dossiers |

## Ce que ce skill ne fait pas

- Il ne dépose aucune demande : `preparer-une-demande`.
- Il ne lit pas le plafond de subvention du CSE : `solde-et-consommations`.
- Il ne donne pas de conseil financier sur l'opportunité d'un prêt : il rapporte les
  conditions affichées par le CSEC.

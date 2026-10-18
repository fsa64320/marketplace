---
name: solde-et-consommations
description: >
  Lit dans l'espace privé du CSE de Pau et du CSEC le plafond annuel de subvention, ce
  qui a été consommé, le solde restant (dont le solde vacances individuelles), les
  dossiers en attente et l'historique des aides, séjours et prêts. Utiliser quand
  l'utilisateur dit : "combien de subvention j'ai utilisé", "combien il me reste au CSE",
  "mon solde CSE", "mon plafond", "mon QAF", "mes consommations CSE", "mes dossiers CSEC",
  "qu'est-ce que j'ai déjà demandé au CSEC".
---

# Solde et consommations

Charge d'abord le skill `naviguer-cse-csec` : choix du navigateur, session ouverte,
attente de 2 secondes sur les pages de l'espace privé.

## Étapes

1. Ouvre le profil du CSE : `https://www.csetotalenergiespau.fr/index.php?controller=membre&action=profil`.
   Le bloc « Mon plafond » donne : plafond annuel, consommations, solde, dont solde
   vacances individuelles, QAF de l'année. Relève ces cinq valeurs telles quelles.

2. Ouvre les consommations : `https://www.csetotalenergiespau.fr/index.php?controller=membre&action=consommation`.
   Chaque année est un bloc de dossiers (numéro, date, produit, subvention, prix, état) et
   une ligne « Total » avec la subvention puis le prix payé. Garde les dossiers de l'année
   en cours.

3. Repère les dossiers à l'état « Inscrit » : ils ne sont pas encore contrôlés, la
   subvention affichée n'est pas comptée dans les consommations du profil. Clique sur le
   numéro d'un dossier pour lire son compteur (par exemple CESU) et savoir s'il est hors
   plafond. Un dossier hors plafond, ou sur un compteur distinct, ne diminue pas le solde
   du plafond global.

4. Calcule le solde prévisionnel : solde du profil moins la subvention de chaque dossier
   « Inscrit » imputable au plafond. Donne-le comme une estimation : c'est le CSE qui
   valide l'imputation.

5. Pour le détail du plafond, des taux et des sous-plafonds (vacances individuelles,
   activités sportives, activités culturelles), lis la grille de la page
   `https://www.csetotalenergiespau.fr/222_page_-reglementation-generale---plafonnement---qaf.html`
   et prends la colonne de la tranche QAF relevée à l'étape 1. Les subventions des
   activités d'enfants ne sont pas limitées par le plafond global, seulement par les
   sous-plafonds.

6. Côté CSEC, ouvre `https://www.csecuesagshtotal.fr/index.php?controller=membre&action=consommation`.
   Il n'y a pas de plafond : la page liste par année les aides scolaires, séjours,
   escapades et prêts avec leur état. Compte « Confirmé » ; ignore « Refusé » dans les
   totaux ; signale les dossiers « Inscrit » à part.

7. Présente la réponse sous cette forme, avec les vrais chiffres :

   | CSE de Pau, année 2026 (exemple) | Montant |
   | --- | ---: |
   | Plafond annuel (QAF B) | 3 000,00 € |
   | Subvention consommée | 500,00 € |
   | Solde restant | 2 500,00 € |
   | dont solde vacances individuelles | 1 500,00 € |
   | Dossiers « Inscrit » à venir | 1 000,00 € |
   | Solde prévisionnel (estimation) | 1 500,00 € |

   Puis une ligne pour le CSEC : nombre de dossiers confirmés de l'année et total des
   subventions, les prêts comptés à part.

## Ce que ce skill ne fait pas

- Il ne modifie ni ne conteste aucun dossier : c'est le CSE ou le CSEC qui tranche.
- Il ne cherche pas quelle offre prendre : `voyages-et-sejours` ou `aides-et-prets`.
- Il ne garde aucun chiffre en mémoire d'une session à l'autre : relis le site à chaque
  demande.

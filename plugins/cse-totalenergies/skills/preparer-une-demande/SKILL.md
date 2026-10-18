---
name: preparer-une-demande
description: >
  Prépare une inscription ou une demande au CSE de Pau ou au CSEC (aide scolaire,
  permis, BAFA, prêt, séjour, vacances individuelles, subvention d'activité) : vérifie
  les prérequis, liste les pièces, estime la subvention, rassemble les informations à
  saisir et ouvre le bon formulaire, sans jamais le valider. Utiliser quand l'utilisateur
  dit : "prépare ma demande d'aide scolaire", "aide-moi à m'inscrire à ce séjour",
  "monte mon dossier de prêt", "qu'est-ce qu'il me faut pour la subvention BAFA",
  "prépare mon inscription au CSE".
---

# Préparer une demande

Charge d'abord le skill `naviguer-cse-csec`. Ce skill prépare ; l'utilisateur valide.

## Étapes

1. Fixe la demande : quelle prestation, quel site, pour qui (lui, un enfant, un
   conjoint). Pour une prestation mal identifiée, lance `voyages-et-sejours` ou
   `aides-et-prets` d'abord.

2. Lis la page de la prestation : conditions, dates d'ouverture et de clôture, montant,
   pièces à fournir, mode de dépôt. Si la campagne est fermée ou pas encore ouverte,
   arrête-toi là et donne la date d'ouverture.

3. Contrôle les prérequis :
   - CSEC : coordonnées bancaires enregistrées et mandat signé
     (`index.php?controller=membre&action=bank`) ; QAF calculé.
   - CSE de Pau : inscription au CSE validée, QAF établi, solde suffisant (lance
     `solde-et-consommations`).
   Un prérequis manquant se traite par l'utilisateur ; indique-lui où.

4. Cherche un doublon dans les consommations du site concerné : même prestation, même
   personne, même année.

5. Estime la subvention et le reste à charge avec les chiffres lus sur le site. Écris
   « estimation ».

6. Remets une fiche de préparation sous cette forme :

   | Rubrique | Contenu |
   | --- | --- |
   | Prestation | Exemple : aide scolaire collège ou lycée, CSEC |
   | Bénéficiaire | l'enfant concerné |
   | Clôture de la campagne | date lue sur la page |
   | Prérequis | mandat signé : oui ; QAF : calculé |
   | Pièces à fournir | liste lue sur la page, à joindre par l'utilisateur |
   | Subvention estimée | montant |
   | Reste à charge estimé | montant |
   | Doublon détecté | aucun |

7. Ouvre la page du formulaire dans le navigateur et arrête-toi avant de le remplir. Ne
   remplis les champs que si l'utilisateur le demande explicitement dans cette
   conversation, avec les valeurs qu'il t'a données. Dans tous les cas :
   - ne clique jamais sur le bouton qui valide, envoie ou confirme : l'utilisateur le fait
     lui-même ;
   - ne joins aucun fichier et ne saisis aucun numéro de compte bancaire ;
   - ne signe aucun mandat.

## Ce que ce skill ne fait pas

- Il ne dépose, n'envoie ni ne confirme aucune demande.
- Il ne renseigne pas sur les offres en général : `voyages-et-sejours`, `aides-et-prets`.
- Il ne conserve aucune donnée personnelle (identité, enfants, coordonnées bancaires)
  dans un fichier du dépôt.

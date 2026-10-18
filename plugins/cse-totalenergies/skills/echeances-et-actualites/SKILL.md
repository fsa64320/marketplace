---
name: echeances-et-actualites
description: >
  Relève les actualités, offres du moment et dates limites d'inscription publiées sur le
  CSE de Pau et le CSEC (campagnes d'aides, inscriptions aux séjours, billetterie,
  calendrier des permanences et expositions, newsletter) et les range par ordre
  chronologique. Utiliser quand l'utilisateur dit : "quoi de neuf au CSE", "les
  actualités du CSEC", "quelles inscriptions sont ouvertes", "dates limites CSE",
  "qu'est-ce que je ne dois pas rater", "offres du moment", "résumé de la newsletter".
---

# Échéances et actualités

Charge d'abord le skill `naviguer-cse-csec`. Les pages d'accueil et les actualités sont
publiques : `WebFetch` suffit.

## Étapes

1. Ouvre la page d'accueil du CSE de Pau (`https://www.csetotalenergiespau.fr/`). Relève
   les actualités (« Les news du CSE »), les offres du carrousel, les blocs « Demandes de
   subvention » et « Billetterie ».

2. Ouvre la page d'accueil du CSEC (`https://www.csecuesagshtotal.fr/`). Chaque
   diapositive du carrousel porte un titre, une date d'ouverture et une date limite ; le
   texte est tronqué dans la lecture de la page, donc ouvre le lien de la diapositive pour
   lire la date exacte.

3. Lis le calendrier des permanences et expositions du CSE
   (`calendrier_liste_evenements_agendas.html`) et, si l'utilisateur le demande, la
   newsletter de chaque site (`index.php?controller=newsletter`).

4. Garde ce qui concerne l'utilisateur : une aide scolaire n'intéresse pas quelqu'un sans
   enfant scolarisé, un séjour jeunesse non plus. Si tu ne sais pas, garde la ligne et
   signale-le.

5. Trie par date limite croissante et présente :

   | Date limite | Site | Offre ou démarche | Lien |
   | --- | --- | --- | --- |
   | 16/11 | CSEC | Exemple : inscriptions séjours hiver | page de l'offre |

   Mets en tête les échéances des quinze prochains jours et marque d'un « urgent » celles
   de la semaine. Ne reprends jamais une date vue dans une session précédente : relis les
   pages.

## Ce que ce skill ne fait pas

- Il ne détaille pas une offre ni son coût : `voyages-et-sejours` ou `aides-et-prets`.
- Il ne s'abonne pas à la newsletter et ne remplit aucun formulaire de contact.
- Il ne programme aucun rappel : demande à l'utilisateur s'il veut une tâche planifiée.

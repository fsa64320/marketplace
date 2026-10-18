---
name: guide-declaration
description: >
  Guide pas à pas le remplissage de la déclaration de revenus en ligne sur
  impots.gouv.fr : documents à réunir, pré-rempli à contrôler, cases de la 2042,
  formulaires 2044 et 2047, charges et crédits d'impôt, vérification finale.
  Utiliser quand l'utilisateur veut remplir sa déclaration : "remplir ma
  déclaration d'impôt", "faire ma déclaration", "comment déclarer mes revenus",
  "guide déclaration 2042", "aide pour ma déclaration", "quelles cases remplir",
  "déclaration en ligne impots.gouv.fr", "comment reporter mon IFU",
  "remplir le formulaire 2044", "remplir le formulaire 2047".
---

# Guide de déclaration de revenus

## Ce que ce skill fait

Il accompagne l'utilisateur écran par écran dans sa déclaration en ligne, en lui disant quelle case remplir avec quel document.

## Étapes

1. Applique d'abord le skill `verification-legislation` du plugin : il fixe l'année des revenus et produit la fiche de vérification qui donne chaque taux, seuil et numéro de case à utiliser.
2. Demande à l'utilisateur lesquels de ces éléments le concernent, en une seule question :
   - IFU des banques et courtiers ;
   - relevés fiscaux SCPI ;
   - attestation fiscale assurance-vie ;
   - loyers perçus en direct ;
   - revenus de source étrangère ;
   - versements PER, dons, emploi à domicile, frais de garde ;
   - avis d'imposition de l'an dernier (plafond PER).
3. Si l'utilisateur fournit des documents fiscaux, analyse-les d'abord avec la procédure de `analyse-document-fiscal` et reprends ses montants consolidés ; ne relis pas les montants une seconde fois ici.
4. Fais-lui contrôler le pré-rempli sur impots.gouv.fr > Mon espace particulier > Déclarer mes revenus : salaires (1AJ / 1BJ), pensions et allocations chômage, revenus de capitaux déclarés par les établissements. Dis-lui de comparer chaque montant pré-rempli à l'IFU correspondant.
5. Revenus de capitaux mobiliers (2042, rubrique 2) : donne pour chaque case concernée le montant et sa source, avec ce tableau ; si la fiche de vérification signale un changement de case pour l'année, suis la fiche.

| Case | Libellé | Source |
|------|---------|--------|
| 2DC | Dividendes ouvrant droit à l'abattement de 40 % | IFU |
| 2TS | Autres revenus distribués, sans abattement | IFU |
| 2TR | Intérêts et produits de placement à revenu fixe | IFU |
| 2BH | Revenus déjà soumis aux PS avec CSG déductible | IFU |
| 2CK | Crédit d'impôt égal au prélèvement forfaitaire non libératoire | IFU |
| 2AB | Crédits d'impôt sur valeurs étrangères | IFU |
| 2CA | Frais et charges déductibles | IFU |
| 3VG / 3VH | Plus-values / moins-values de cession de valeurs mobilières | IFU |

6. Revenus fonciers (rubrique 4) :
   - revenus fonciers bruts du foyer sous le seuil du micro-foncier de la fiche et pas d'option pour le réel : micro-foncier, case 4BE, abattement forfaitaire appliqué par l'administration ;
   - sinon : formulaire 2044 (ligne 211 loyers, lignes 221 à 250 charges et intérêts ; lignes 111 à 114 pour les SCPI), résultat reporté en 4BA (bénéfice), 4BB ou 4BC (déficit).
7. Revenus de source étrangère : fais remplir la 2047 avant la 2042, pays par pays, puis reporter 4BL et 8TK (crédit d'impôt égal à l'impôt français) ou 4EA (taux effectif). Rappelle que 8TK et 4EA sont rarement pré-remplies.
8. Charges, réductions et crédits d'impôt (rubriques 6 et 7) : versements PER (6NS, 6NT, 6NU), pension alimentaire (6GI), dons (7UF, 7UD), emploi à domicile (7DB), garde d'enfant de moins de 6 ans (7GA à 7GC).
9. Option barème (case 2OP) : ne tranche pas ici. Si l'utilisateur hésite, applique la procédure de `optimisation-fiscale`, levier 1.
10. Vérification finale : fais-lui comparer le revenu fiscal de référence avec celui de l'an dernier, lire la simulation affichée avant signature, et cocher cette liste.
   - [ ] 2CK renseignée
   - [ ] 8TK et 4EA renseignées si revenus étrangers
   - [ ] option 2OP décidée en connaissance de cause
   - [ ] enfants rattachés au foyer
   - [ ] coordonnées bancaires à jour
11. Termine par : « Guide indicatif, ne remplace pas un expert-comptable ; en cas de doute, appelez le 0809 401 401 (service gratuit + prix d'un appel). »

## Calendrier

La déclaration en ligne ouvre en avril ; les dates limites tombent fin mai à début juin selon trois zones de départements. Donne les dates exactes de l'année de déclaration si un outil de recherche web est disponible, sinon renvoie à impots.gouv.fr.

## Ce que ce skill ne fait pas

- L'extraction des montants d'un document fiscal : c'est `analyse-document-fiscal`.
- Le choix entre régimes et le chiffrage des économies : c'est `optimisation-fiscale`.
- L'explication d'un dispositif fiscal sans déclaration en cours : c'est `expert-fiscal-qa`.

---
name: analyse-document-fiscal
description: >
  Analyse un ou plusieurs documents fiscaux fournis (IFU, relevé fiscal SCPI,
  attestation assurance-vie, relevé PEA), extrait les montants, les consolide par
  case de la 2042 et produit une synthèse avec guide de saisie. Utiliser quand
  l'utilisateur partage ou mentionne un document fiscal reçu : "analyse mon IFU",
  "lis mon relevé fiscal SCPI", "que signifie cette case de mon IFU",
  "j'ai reçu un document de ma banque", "IFU Boursorama", "relevé Linxea",
  "attestation fiscale", "document Amundi", "relevé de situation",
  "synthèse fiscale de mes documents".
---

# Analyse de document fiscal

## Ce que ce skill fait

Il lit les documents fiscaux de l'utilisateur, en extrait chaque montant déclarable et le place dans la bonne case, sans jamais inventer de chiffre.

## Étapes

1. Ouvre chaque document fourni avec l'outil de lecture de fichier. Si l'utilisateur mentionne un document sans le joindre, demande-le avant d'aller plus loin.
2. Pour chaque document, note l'émetteur, le titulaire, l'année des revenus et le type : IFU, relevé fiscal SCPI, attestation assurance-vie ou relevé PEA / PEA-PME.
3. Relève les montants selon le type :
   - IFU : cases 2DC, 2TS, 2TR, 2BH, 2CK, 2AB, 2CA, 3VG, 3VH, telles qu'imprimées sur l'IFU.
   - Relevé SCPI : revenus fonciers français (lignes 111 à 114 de la 2044, puis 4BA), revenus fonciers étrangers ouvrant droit à crédit d'impôt (4BL et 8TK), revenus étrangers exonérés retenus pour le taux effectif (4EA), plus-values immobilières (3VZ), plus-values mobilières (3VG).
   - Une case absente du document vaut `0,00 €` avec le statut `— Non concerné` : ne l'omets pas et n'en déduis aucun montant.
4. Si plusieurs documents concernent le même foyer, additionne les montants case par case et garde le détail par document pour chaque case alimentée par plusieurs sources.
5. Applique d'abord le skill `verification-legislation` du plugin : il fixe l'année des revenus et produit la fiche de vérification qui donne chaque taux, seuil et numéro de case à utiliser. Passe-lui l'année de revenus relevée à l'étape 2.
6. Produis la réponse en suivant `assets/format-reponse.md` : les 12 blocs, dans l'ordre. Un bloc sans objet (2044, 2047, 2074, IFI, PEA) se réduit à sa phrase « non applicable ». Omets le bloc 11 si les données ne permettent pas d'estimer.
7. Formate chaque montant `X XXX,XX €` (espace pour les milliers, virgule décimale).
8. Termine toujours par le bloc 12 (mise en garde).

## Règles

- Distingue les deux mécanismes des revenus étrangers : crédit d'impôt égal à l'impôt français (4BL et 8TK) et exonération avec taux effectif (4EA). Les revenus 4EA ne sont pas imposés en France mais relèvent le taux appliqué aux autres revenus.
- Signale que 8TK et 4EA sont rarement pré-remplies.
- Tout taux, seuil ou numéro de case de ta réponse vient de la fiche de vérification, jamais de ta mémoire ni des exemples du gabarit.

## Ce que ce skill ne fait pas

- Le parcours complet de déclaration sur impots.gouv.fr, revenus salariaux et charges compris : c'est `guide-declaration`.
- Le choix entre régimes ou la recherche d'économies d'impôt : c'est `optimisation-fiscale`.
- Une question fiscale sans document à analyser : c'est `expert-fiscal-qa`.

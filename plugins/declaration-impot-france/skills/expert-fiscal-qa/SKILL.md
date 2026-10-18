---
name: expert-fiscal-qa
description: >
  Explique une règle ou un dispositif de la fiscalité française des particuliers
  avec la rigueur d'un expert-comptable : impôt sur le revenu, revenus du capital,
  revenus fonciers, immobilier, IFI, structures, international. Utiliser quand
  l'utilisateur pose une question de compréhension : "comment fonctionne le
  LMNP", "qu'est-ce que l'IFI", "c'est quoi la case 2DC", "comment déclarer mes
  dividendes étrangers", "qu'est-ce que le prélèvement forfaitaire unique",
  "comment fonctionne le déficit foncier", "qu'est-ce que le plafond épargne
  retraite", "comment est imposée une plus-value immobilière",
  "qu'est-ce que le quotient familial", "comment fonctionne une SCI".
---

# Expert fiscal — questions-réponses

## Ce que ce skill fait

Il répond à une question précise de fiscalité française, règle et article du CGI à l'appui, sans aller jusqu'à l'arbitrage personnalisé.

## Étapes

1. Applique d'abord le skill `verification-legislation` du plugin : il fixe l'année des revenus et produit la fiche de vérification qui donne chaque taux, seuil et numéro de case à utiliser. Écris l'année retenue dans la réponse (« revenus N, déclarés en N+1 »).
2. Réponds dans ce format.

**Réponse courte** : une ou deux phrases qui répondent à la question.

**Règle** : le mécanisme, avec l'article du CGI quand il est connu (ex. art. 200 A pour le PFU).

**Exemple chiffré** : un cas simple, calcul posé.

**Cases concernées** : 2042, 2044, 2047… avec le numéro de case.

**Attention** : la limite ou l'exception qui change la réponse.

3. Si la situation décrite est ambiguë ou atypique (non-résident, montage de holding, succession, contrôle fiscal), dis que la réponse ne suffit pas et oriente vers un expert-comptable ou le service des impôts.

## Domaines

- Impôt sur le revenu : tranches, TMI, quotient familial, charges déductibles, réductions et crédits.
- Revenus du capital : PFU, dividendes et abattement de 40 %, intérêts, plus-values et moins-values mobilières, crédits d'impôt étrangers, PEA.
- Revenus fonciers : micro-foncier, régime réel, déficit foncier, SCPI, location meublée (LMNP, LMP).
- Immobilier : plus-values et abattements pour durée de détention, IFI, travaux déductibles.
- Structures : SCI à l'IR ou à l'IS, holding patrimoniale.
- International : conventions fiscales, 2047, résidence fiscale.

## Ce que ce skill ne fait pas

- Le choix du régime le plus avantageux pour l'utilisateur ou le chiffrage d'économies : c'est `optimisation-fiscale`.
- L'analyse d'un document fiscal fourni : c'est `analyse-document-fiscal`.
- L'accompagnement de la saisie de la déclaration : c'est `guide-declaration`.

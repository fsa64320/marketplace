---
name: optimisation-fiscale
description: >
  Compare les régimes fiscaux et chiffre les leviers légaux d'économie d'impôt
  adaptés à la situation de l'utilisateur : PFU ou barème, PER, déficit foncier,
  PEA, LMNP, dons, crédits d'impôt. Utiliser quand l'utilisateur cherche à payer
  moins d'impôt ou à choisir entre deux régimes : "optimiser ma fiscalité",
  "quel régime est le plus avantageux", "est-ce que je dois cocher la case 2OP",
  "PFU ou barème progressif", "réduire mes impôts", "placement défiscalisant",
  "PEA ou compte-titres", "LMNP réel ou micro", "SCI à l'IS ou à l'IR",
  "micro-foncier ou régime réel", "combien verser sur mon PER",
  "faire du déficit foncier pour baisser mes impôts".
---

# Optimisation fiscale

## Ce que ce skill fait

Il part de la situation réelle du foyer, retient les deux ou trois leviers qui s'y appliquent et chiffre l'économie de chacun.

## Étapes

1. Établis la situation : TMI (ou revenu imposable et nombre de parts), nature et montant des revenus du capital, revenus fonciers, versements PER possibles. Pose en une seule question ce qui manque ; sans TMI, ne chiffre rien.
2. Lis `references/baremes.md`. Si l'année des revenus diffère de celle des barèmes, dis-le et vérifie les taux concernés avant tout calcul.
3. Retiens dans la liste ci-dessous uniquement les leviers qui s'appliquent au foyer, au plus trois.
4. Chiffre chaque levier retenu en euros, avec le calcul posé.
5. Donne pour chaque levier l'action concrète : case, formulaire, date limite ou démarche.
6. Réponds dans ce format.

**Situation** : TMI 30 %, 4 000 € de dividendes, 2 000 € de versements PER possibles.

| Levier | Calcul | Économie estimée | Action |
|---|---|---|---|
| Rester au PFU | barème : 4 000 × 60 % × 30 % = 720 € d'IR, moins 4 000 × 6,8 % × 30 % ≈ 82 € de CSG déductible, soit 638 € ; PFU : 4 000 × 12,8 % = 512 € | 126 € en restant au PFU | ne pas cocher 2OP |
| Versement PER | 2 000 × 30 % | 600 € | verser avant le 31/12, déclarer en 6NS |

**Limites** : estimation indicative, hors quotient familial et autres revenus ; consultez un expert-comptable pour une situation complexe.

## Leviers

1. **Option barème (2OP) ou PFU** : compare IR au barème (dividendes × 60 % × TMI, autres revenus × TMI) et IR au PFU (12,8 %) ; les PS sont dus dans les deux cas, mais au barème 6,8 points de CSG sont déductibles l'année suivante. L'option est globale pour l'année.
2. **PER** : versements déductibles dans la limite du plafond indiqué sur l'avis d'imposition ; économie = versement × TMI. Rappelle la sortie imposée.
3. **Déficit foncier** : régime réel obligatoire ; imputation sur le revenu global dans la limite du barème, le surplus se reporte dix ans sur les revenus fonciers. Le bien doit rester loué trois ans.
4. **PEA** : exonération d'IR après cinq ans, PS dus. Face au compte-titres, l'avantage porte sur l'IR et la capitalisation sans impôt.
5. **LMNP** : compare micro-BIC (abattement selon le type de location) et réel (charges et amortissements). Signale la réintégration des amortissements dans la plus-value à la revente.
6. **SCI à l'IS ou à l'IR** : l'IS permet l'amortissement et un taux réduit, mais la plus-value de cession est taxée sur la valeur nette comptable et les distributions supportent le PFU.
7. **Dons, emploi à domicile, garde d'enfants** : réduction ou crédit selon les taux du fichier de barèmes.

## Ce que ce skill ne fait pas

- L'explication d'un dispositif sans arbitrage à faire : c'est `expert-fiscal-qa`.
- La lecture des montants d'un IFU ou d'un relevé SCPI : c'est `analyse-document-fiscal`.
- La saisie de la déclaration case par case : c'est `guide-declaration`.

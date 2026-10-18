---
name: verification-legislation
description: >
  Détermine l'année fiscale concernée et vérifie la législation et les chiffres
  en vigueur (taux, barème, plafonds, cases de la 2042) avant tout calcul ou
  conseil fiscal, puis produit une fiche de vérification sourcée. Utiliser quand
  un skill de ce plugin commence (analyse-document-fiscal, guide-declaration,
  optimisation-fiscale, expert-fiscal-qa), ou quand l'utilisateur demande :
  "vérifie les barèmes de cette année", "quels sont les taux en vigueur",
  "la loi de finances a-t-elle changé", "ces chiffres sont-ils encore valables",
  "mets à jour les chiffres fiscaux".
---

# Vérification de la législation

## Ce que ce skill fait

Il fixe l'année des revenus, confronte les valeurs de référence du plugin à la législation de cette année et produit une fiche qui dit, pour chaque chiffre utilisé, s'il est vérifié et d'où il vient. Les autres skills du plugin ne chiffrent rien sans cette fiche.

## Étapes

1. Relève la date du jour dans ton contexte.
2. Fixe l'année des revenus :
   - un document fourni porte une année de revenus : prends-la ;
   - sinon, de janvier à la mi-juin : revenus de l'année précédente, déclarés cette année ;
   - sinon, de la mi-juin à décembre : demande à l'utilisateur s'il parle de la déclaration déjà faite (revenus de l'année précédente) ou de ses revenus de l'année en cours (déclarés l'an prochain) ; pour une question d'optimisation sans réponse, prends l'année en cours.
3. Si une fiche de vérification existe déjà dans la conversation pour cette année de revenus, réutilise-la et arrête-toi là.
4. Lis `references/valeurs-de-reference.md`. Note l'année de revenus qu'il couvre et sa date de dernière vérification.
5. Dresse la liste à vérifier : les valeurs dont dépend la demande de l'utilisateur, les numéros de cases que tu vas citer, et la section « À vérifier chaque année » du fichier. Ne vérifie pas tout le fichier si la question n'en touche qu'une ligne.
6. Si un outil de recherche web est disponible, vérifie chaque élément pour l'année fixée à l'étape 2 :
   - mets l'année dans chaque requête (« plafond PER versements 2026 ») ;
   - tiens pour officielles impots.gouv.fr, bofip.impots.gouv.fr, service-public.fr et legifrance.gouv.fr ;
   - une autre source sert seulement à repérer une réforme : cherche-la ensuite sur une source officielle ;
   - cherche aussi la loi de finances et la LFSS de l'année de déclaration, pour repérer un dispositif créé, supprimé ou modifié.
7. Si le connecteur data.gouv.fr est disponible, interroge aussi OpenFisca, le moteur de calcul socio-fiscal référencé au catalogue (recherche de dataservices « openfisca ») : lis `https://api.fr.openfisca.org/latest/parameter/<identifiant>`, par exemple `impot_revenu.bareme_ir_depuis_1945.bareme`. Une valeur OpenFisca datée et portant sa référence légale vaut ✅. Une valeur absente ou plus ancienne que l'année visée ne prouve rien : OpenFisca peut avoir du retard sur une loi récente.
8. Attribue un statut à chaque élément : ✅ confirmé par une source officielle de l'année, ⚠️ trouvé hors source officielle ou sources contradictoires, ❌ non vérifiable (pas d'outil web, ou rien trouvé pour cette année) ; dans ce dernier cas garde la valeur de référence et indique son année.
9. Place la fiche en tête de ta réponse, au format de `assets/fiche-verification.md`.
10. Dans le reste de la réponse, accole « (à confirmer) » à tout chiffre décisif ⚠️ ou ❌, et ne présente pas un résultat qui en dépend comme certain.
11. Si une valeur vérifiée diffère de la valeur de référence, utilise la valeur vérifiée et termine la réponse par : « Valeurs de référence du plugin à mettre à jour dans fsa64320/marketplace : [élément] [ancienne valeur] → [nouvelle valeur] ([source]). » Ne modifie aucun fichier du plugin installé.

## Ce que ce skill ne fait pas

- L'analyse d'un document : c'est `analyse-document-fiscal`.
- L'accompagnement de la saisie : c'est `guide-declaration`.
- L'arbitrage entre régimes : c'est `optimisation-fiscale`.
- L'explication d'une règle : c'est `expert-fiscal-qa`.

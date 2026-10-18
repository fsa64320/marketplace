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
   - interroge les sources officielles dans cet ordre :
     1. impots.gouv.fr : fiches « particulier », brochure pratique de l'année (« Déclaration des revenus N »), notices des formulaires ; c'est la source des taux, seuils et numéros de cases ;
     2. bofip.impots.gouv.fr, pour un cas limite ou une règle d'interprétation. Chaque page BOFiP existe en plusieurs versions : lis la période de validité affichée en tête et ne retiens que la version en vigueur pour l'année visée ; une version périmée ne vaut rien, même officielle ;
     3. legifrance.gouv.fr, pour le texte de loi (loi de finances, LFSS, CGI) ;
     4. service-public.fr ;
   - date chaque source : une page sans date de mise à jour postérieure à la loi concernée ne confirme pas une valeur récente ;
   - une autre source sert seulement à repérer une réforme : cherche-la ensuite sur une source officielle ;
   - cherche aussi la loi de finances et la LFSS de l'année de déclaration, pour repérer un dispositif créé, supprimé ou modifié.
7. Si les outils du serveur MCP `bensaid-avocats` du plugin sont disponibles, complète l'étape 6 avec eux :
   - `openfisca_parameter` : barèmes et taux, avec `date` au 1er janvier de l'année des revenus (ex. `name` = `impot_revenu.bareme_ir_depuis_1945.bareme`, `date` = `2025-01-01`) ;
   - `legifrance_article` : texte en vigueur d'un article du CGI ou du LPF et sa date d'entrée en vigueur (ex. `code` = `cgi`, `article` = `200 A`) ;
   - `bofip_search` puis `bofip_get` : règle d'interprétation ; ce corpus ne contient que les versions en vigueur, il ne vaut donc pas pour une année passée ;
   - `conventions_search` puis `conventions_article` : traitement des revenus de source étrangère par pays (crédit d'impôt ou taux effectif, 2047).
   Règles d'usage :
   - n'envoie dans une requête que des termes juridiques ou des noms de paramètres, jamais un montant, un nom ou une donnée de l'utilisateur ;
   - une valeur datée qui porte sa référence légale et couvre l'année visée vaut ✅ ;
   - une valeur absente, ou plus ancienne que l'année visée, ne prouve rien : le corpus du serveur et OpenFisca peuvent avoir du retard sur une loi récente ; garde alors le résultat de l'étape 6 ;
   - ce serveur est un service tiers gratuit : s'il ne répond pas, continue sans lui et ne le signale que si l'étape 6 n'a rien donné.
8. Attribue un statut à chaque élément : ✅ confirmé par une source officielle de l'année, ⚠️ trouvé hors source officielle ou sources contradictoires, ❌ non vérifiable (pas d'outil web, ou rien trouvé pour cette année) ; dans ce dernier cas garde la valeur de référence et indique son année.
9. Place la fiche en tête de ta réponse, au format de `assets/fiche-verification.md`.
10. Dans le reste de la réponse, accole « (à confirmer) » à tout chiffre décisif ⚠️ ou ❌, et ne présente pas un résultat qui en dépend comme certain.
11. Si une valeur vérifiée diffère de la valeur de référence, utilise la valeur vérifiée et termine la réponse par : « Valeurs de référence du plugin à mettre à jour dans fsa64320/marketplace : [élément] [ancienne valeur] → [nouvelle valeur] ([source]). » Ne modifie aucun fichier du plugin installé.

## Ce que ce skill ne fait pas

- L'analyse d'un document : c'est `analyse-document-fiscal`.
- L'accompagnement de la saisie : c'est `guide-declaration`.
- L'arbitrage entre régimes : c'est `optimisation-fiscale`.
- L'explication d'une règle : c'est `expert-fiscal-qa`.

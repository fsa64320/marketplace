---
name: naviguer-cse-csec
description: >
  Socle de navigation sur les deux sites sociaux de TotalEnergies : le CSE de Pau
  (csetotalenergiespau.fr) et le CSEC UES AGSH (csecuesagshtotal.fr). Dit quel site
  gère quoi, comment ouvrir les pages publiques et l'espace privé dans le navigateur
  déjà connecté de l'utilisateur, et ce qu'il ne faut jamais faire sur ces sites.
  Utiliser quand l'utilisateur dit : "va sur le site du CSE", "regarde sur le site du
  CSEC", "ouvre mon espace CSE", "où trouver telle information au CSE", et avant tout
  autre skill de ce plugin.
---

# Naviguer sur le CSE et le CSEC

Les deux sites tournent sur le même logiciel (ACL, « Logiciel Comité d'Entreprise ») : mêmes
menus déroulants, même espace privé, mêmes pages `index.php?controller=…`. Les skills voisins
s'appuient sur ce socle.

## Quel site pour quoi

| Besoin | Site | Adresse |
|---|---|---|
| Subventions et plafond annuel, QAF, vacances individuelles, voyages groupes, locations hiver, billetterie, CESU, activités et sections, retraités | CSE de Pau | https://www.csetotalenergiespau.fr/ |
| Séjours patrimoine et locations, escapades, séjours jeunesse, aides scolaires, permis, BAFA, prêts, secours | CSEC UES AGSH | https://www.csecuesagshtotal.fr/ |

Le CSEC ne calcule pas le QAF : il se fait calculer auprès du CSE de rattachement. Les
inactifs, retraités et expatriés sous contrat TGI ne bénéficient pas des prestations du
CSEC.

## Étapes

1. Choisis le site avec le tableau ci-dessus. Une question qui touche les deux (par
   exemple « quel séjour d'hiver choisir ») se traite site par site, puis se compare.

2. Choisis l'outil de lecture :
   - page publique (actualités, règlement, plafonds, catalogue) : `WebFetch` suffit ;
   - espace privé et tout ce qui dépend du compte : navigateur de l'utilisateur, déjà
     connecté. Prends Claude in Chrome (outils `mcp__claude-in-chrome__*`), sinon le
     navigateur intégré, sinon le plugin `navigateur-web`.

3. Ouvre un onglet neuf, charge la page, puis lis-la avec le lecteur de texte du
   navigateur (`get_page_text`). Pour trouver l'adresse d'une rubrique, lis l'arbre de la
   page en mode « tous les éléments » : les sous-menus y figurent avec leur `href`, même
   repliés.

4. Vérifie que la session est ouverte : dans l'en-tête, le lien « Espace privé » porte le
   nom de l'utilisateur, au lieu de « Connexion ».
   - Session fermée : demande à l'utilisateur de se connecter lui-même dans l'onglet, puis
     de te prévenir. Ne tape jamais d'identifiant ni de mot de passe, même pré-remplis
     par le navigateur, et ne valide pas le formulaire de connexion.

5. Bandeau de cookies : choisis « Tout refuser ».

6. Pages de l'espace privé (`index.php?controller=membre&action=profil`,
   `index.php?controller=membre&action=consommation`) : le premier chargement renvoie
   parfois la page d'accueil de l'espace. Attends 2 secondes, relis la page, vérifie son
   titre (« Mes consommations… », « Mon profil ») avant d'en extraire quoi que ce soit.

7. Plan complet des rubriques et adresses des deux sites : lis `references/plan-des-sites.md`.
   Les adresses peuvent changer d'une année à l'autre : si une page ne répond pas, repasse
   par le menu.

## Ce qu'on ne fait jamais

- Cliquer sur un bouton qui valide, envoie, s'inscrit, confirme ou commande.
- Télécharger un fichier sans l'accord de l'utilisateur. Les catalogues et notes en PDF se
  lisent directement depuis leur adresse.
- Recopier dans une réponse, un fichier du dépôt ou un commit des données personnelles
  lues dans l'espace privé : le dépôt de ce plugin est public.

## Ce que ce skill ne fait pas

- Il ne lit pas le solde : `solde-et-consommations`.
- Il ne compare pas les séjours : `voyages-et-sejours`.
- Il ne renseigne pas sur les aides et prêts : `aides-et-prets`.
- Il ne prépare pas de demande : `preparer-une-demande`.

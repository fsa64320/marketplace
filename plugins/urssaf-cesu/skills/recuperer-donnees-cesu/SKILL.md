---
name: recuperer-donnees-cesu
description: >
  Récupère les salaires et cotisations déclarés sur le portail CESU de l'Urssaf
  (cesu.urssaf.fr) pour un particulier employeur et les présente en tableau par
  salarié et par mois : brut, net, cotisations patronales et salariales, coût
  employeur, avec les totaux. Part de la réponse du portail enregistrée par
  l'utilisateur depuis son navigateur ; ne demande jamais d'identifiant. Utiliser
  quand l'utilisateur dit : "récupère mes données CESU", "mes salaires CESU",
  "cotisations CESU de l'année", "combien m'a coûté ma femme de ménage",
  "tableau de mes déclarations URSSAF", "exporte mes bulletins CESU".
---

# Récupérer les données CESU

Le portail CESU n'a pas d'API publique pour l'employeur. Les données viennent de la
réponse JSON que le portail envoie au navigateur de l'utilisateur quand il affiche ses
déclarations. Le script `scripts/extraire_cesu.py` lit cette réponse, masque les données
personnelles et produit le tableau. Lance-le depuis le dossier de ce skill.

## Étapes

1. Demande la période voulue (année ou mois) et si l'utilisateur emploie par CESU ou par
   Pajemploi : le second se traite de la même façon sur pajemploi.urssaf.fr.

2. Fais enregistrer la réponse du portail dans un fichier, en donnant ces consignes telles
   quelles :
   1. Ouvrir cesu.urssaf.fr dans Chrome, Edge ou Firefox et se connecter.
   2. Ouvrir les outils de développement (F12, ou Cmd+Option+I sur Mac), onglet
      **Réseau**, filtre **Fetch/XHR**.
   3. Afficher la page des déclarations ou des bulletins de la période voulue.
   4. Cliquer sur la requête dont l'onglet **Réponse** contient des montants et des
      noms de salariés, puis clic droit sur la requête → **Enregistrer la réponse** (ou
      copier tout le contenu de l'onglet Réponse dans un fichier `reponse.json`).
   5. Donner le chemin du fichier enregistré.

   Ce fichier ne contient aucune donnée de session. Ne demande jamais de coller dans la
   conversation un cookie, un jeton, une commande cURL ou un mot de passe.

3. Si l'utilisateur ne parvient pas à enregistrer la réponse, propose la variante cURL :
   clic droit sur la requête → **Copier** → **Copier en cURL (bash)**, coller dans un
   fichier `requete.txt` sans le montrer, puis lance :

   `python3 scripts/extraire_cesu.py recuperer --curl-fichier requete.txt --sortie reponse.json`

   Le script n'envoie la requête qu'à un domaine urssaf.fr, en https. Code de sortie 2 :
   la session a expiré, l'utilisateur se reconnecte et recopie la requête. N'ouvre pas
   `requete.txt` : il contient le cookie de session.

4. Lance l'inventaire :

   `python3 scripts/extraire_cesu.py inventaire --fichier reponse.json`

   Il affiche la liste de fiches retenue, les autres listes du document et un tableau des
   champs avec un exemple masqué. Si la liste retenue n'est pas celle des déclarations
   (par exemple des liens ou des salariés sans montant), relance avec `--liste` et le
   chemin d'une autre liste. Si aucun champ ne porte de montant, la requête n'est pas la
   bonne : retour à l'étape 2.

5. Choisis les correspondances, une par rôle :

   | Rôle | Champ à prendre | À ne pas prendre |
   | --- | --- | --- |
   | `employe` | prénom puis nom, séparés par une virgule | identifiant, NIR |
   | `periode` | mois de la déclaration (« 2025-01 », « 01/2025 ») | date de déclaration, de paiement, de prélèvement |
   | `mois`, `annee` | seulement si la période est en deux champs | |
   | `brut` | salaire brut déclaré | |
   | `net` | net versé au salarié | net imposable |
   | `patronal`, `salarial` | total des cotisations de chaque part | un taux, une cotisation isolée |

   Un rôle sans champ convaincant reste vide : la colonne sort à 0 et le tableau le
   signale. Si un choix est incertain, montre la correspondance à l'utilisateur avant de
   continuer.

6. Produis le tableau, une option `--champ` par rôle retenu, et `--liste` si tu l'as
   utilisée à l'étape 4 :

   `python3 scripts/extraire_cesu.py tableau --fichier reponse.json --champ employe=salarie.prenom,salarie.nom --champ periode=periode --champ brut=montants.salaireBrut --champ net=montants.salaireNet --champ patronal=montants.cotisationsPatronales --champ salarial=montants.cotisationsSalariales`

   Garde seulement les lignes de la période demandée à l'étape 1, puis présente le
   tableau tel quel :

   | Employé | Période | Salaire brut | Salaire net | Cotis. patronales | Cotis. salariales | Coût employeur |
   | --- | --- | ---: | ---: | ---: | ---: | ---: |
   | Marie Durand | Janvier 2025 | 1 234,56 € | 987,65 € | 432,10 € | 246,91 € | 1 666,66 € |
   | **Total** | — | **1 234,56 €** | **987,65 €** | **432,10 €** | **246,91 €** | **1 666,66 €** |

7. Rappelle de supprimer `requete.txt` s'il a servi, puisqu'il donne accès au compte
   tant que la session est ouverte.

## Ce que ce skill ne fait pas

- Il ne déclare pas un salaire et ne calcule pas de cotisations : c'est le portail CESU
  qui le fait.
- Il ne calcule pas le crédit d'impôt pour l'emploi d'un salarié à domicile :
  `assistant-fiscal:guide-declaration` (case de la 2042) et
  `assistant-fiscal:optimisation-fiscale`. Pour ce montant, l'attestation fiscale annuelle
  téléchargeable sur le portail CESU fait foi, pas ce tableau.
- Il ne se connecte jamais au portail à la place de l'utilisateur et ne conserve aucune
  donnée de session.

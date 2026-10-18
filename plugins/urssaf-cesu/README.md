# Plugin `urssaf-cesu`

Récupère les salaires et cotisations déclarés sur le portail CESU de l'Urssaf (cesu.urssaf.fr) et les présente en tableau par salarié et par mois : brut, net, cotisations patronales et salariales, coût employeur, totaux.

## Installation

```bash
claude plugin marketplace add fsa64320/marketplace
claude plugin install urssaf-cesu@sales-marketplace
```

Le plugin vient de `fsa64320/plugins-claude`, où il s'appelait déjà `urssaf-cesu` (version 1.0.0). Un poste qui l'avait installé depuis là-bas le remplace :

```bash
claude plugin uninstall urssaf-cesu@plugins-claude
claude plugin install urssaf-cesu@sales-marketplace
```

## Skill

| Skill | Rôle | Se déclenche sur |
|---|---|---|
| `recuperer-donnees-cesu` | Lit la réponse du portail enregistrée depuis le navigateur, masque les données personnelles et produit le tableau | « récupère mes données CESU », « cotisations CESU de l'année », « combien m'a coûté ma femme de ménage » |

## Fonctionnement

Le portail CESU n'a pas d'API publique pour l'employeur. L'utilisateur se connecte lui-même dans son navigateur et enregistre la réponse JSON de la page des déclarations (outils de développement, onglet Réseau). Le script `skills/recuperer-donnees-cesu/scripts/extraire_cesu.py` (bibliothèque standard Python, aucune dépendance) a trois commandes :

| Commande | Rôle |
|---|---|
| `inventaire` | repère la liste de déclarations et montre ses champs, NIR, adresse, IBAN, e-mail et téléphone masqués |
| `tableau` | produit le tableau Markdown à partir des correspondances choisies par l'agent (`--champ brut=…`) |
| `recuperer` | variante : rejoue une requête « Copier en cURL (bash) » enregistrée dans un fichier, vers un domaine urssaf.fr en https uniquement |

Le script ne devine aucun champ : il extrait et met en forme, et c'est l'agent qui choisit quel champ est le brut, le net ou les cotisations, après lecture de l'inventaire.

## Sécurité

- Aucun identifiant, cookie ou jeton n'est demandé dans la conversation.
- La variante cURL lit la session dans un fichier local, ne l'affiche jamais et ne l'envoie qu'à urssaf.fr ; supprimer ce fichier après usage.

## Avertissement

Tableau indicatif, reconstitué depuis les données du portail. Pour le crédit d'impôt, l'attestation fiscale annuelle CESU fait foi.

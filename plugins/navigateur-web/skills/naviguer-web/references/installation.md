# Installation d'agent-browser : erreurs et corrections

Chaque section part d'une erreur que renvoie `scripts/preparer_poste.py installer`
(champ `erreurs`, ou `node: null`). Une commande marquée **utilisateur** se donne à
l'utilisateur, qui la lance lui-même : elle demande des droits ou change la
configuration de son poste au-delà d'agent-browser.

## Node.js absent (`"node": null`)

agent-browser s'installe par npm, livré avec Node.js. Version LTS, à faire par
l'**utilisateur** :

| Système | Commande ou source |
| --- | --- |
| Windows, poste d'entreprise | le catalogue logiciel de l'entreprise (Software Center, Portail d'entreprise) |
| Windows, poste personnel | `winget install OpenJS.NodeJS.LTS` |
| macOS | `brew install node`, ou l'installeur de nodejs.org |
| Linux | le paquet `nodejs` de la distribution, ou nvm |

Rouvrir ensuite le terminal (ou la session Claude) pour que `node` et `npm` soient sur
le PATH, puis relancer `installer`.

## `npm install -g agent-browser` échoue

Lis la fin de l'erreur.

- **`EACCES` / `permission denied`** (macOS, Linux) : le préfixe global de npm est un
  dossier système. **Utilisateur** : `npm config set prefix ~/.npm-global`, ajouter
  `~/.npm-global/bin` au PATH (section PATH), relancer `installer`. Jamais `sudo npm`.
- **`SELF_SIGNED_CERT_IN_CHAIN`, `UNABLE_TO_GET_ISSUER_CERT_LOCALLY`** : un proxy
  d'entreprise (Zscaler…) intercepte le TLS et npm ne connaît pas sa CA.
  **Utilisateur** : exporter la CA d'entreprise en fichier PEM, puis
  `npm config set cafile <chemin du .pem>`. Ne jamais proposer `strict-ssl false`.
- **`ETIMEDOUT`, `ECONNREFUSED`, `ENOTFOUND registry.npmjs.org`** : npm ne passe pas
  par le proxy. **Utilisateur** : `npm config set proxy <url du proxy>` et
  `npm config set https-proxy <url du proxy>` — l'adresse est celle que donne le
  support informatique, ou la valeur de `proxy` dans le JSON d'état.
- **`E403` / `E404` sur un registre interne** : npm pointe vers un miroir
  d'entreprise qui ne porte pas le paquet. Le signaler à l'utilisateur, ne pas changer
  `registry` à sa place.

## `agent-browser install` échoue

Cette étape télécharge Chrome for Testing depuis le CDN de Google.

- **Téléchargement bloqué ou erreur de certificat** : le script a déjà posé
  `useSystemCa: true`. Si le blocage persiste, réutilise le Chrome installé sur le
  poste : ajoute `"executablePath": "<chemin de chrome>"` dans
  `~/.agent-browser/config.json`, puis lance `agent-browser doctor`.
  Chemins usuels : `C:\Program Files\Google\Chrome\Application\chrome.exe`,
  `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`, `/usr/bin/google-chrome`.
- **Linux, bibliothèques manquantes** (`libnss3`, `libatk`…) : le script a tenté
  `install --with-deps`, qui demande les droits root. **Utilisateur** :
  `sudo agent-browser install --with-deps`.

## agent-browser installé mais hors du PATH (`"sur_path": false`)

Le binaire est dans le dossier global de npm (`npm prefix -g`, suivi de `/bin` hors
Windows), qui manque au PATH. **Utilisateur**, puis rouvrir le terminal :

| Système | Commande |
| --- | --- |
| Windows (PowerShell) | `[Environment]::SetEnvironmentVariable("Path", $env:Path + ";" + (npm prefix -g), "User")` |
| macOS (zsh) | `echo 'export PATH="$(npm prefix -g)/bin:$PATH"' >> ~/.zshrc` |
| Linux (bash) | `echo 'export PATH="$(npm prefix -g)/bin:$PATH"' >> ~/.bashrc` |

En attendant, appelle agent-browser par le chemin absolu du champ `binaire`.

## `echecs` non vide après l'installation

Ce sont les contrôles en échec de `agent-browser doctor --json`. Lance
`agent-browser doctor` pour le texte complet. `agent-browser doctor --fix` répare les
fichiers de démon périmés et réinstalle Chrome : propose-le à l'utilisateur avant de le
lancer, il supprime des états sauvegardés.

## Ce que le script écrit

`~/.agent-browser/config.json`, sans écraser une clé déjà présente :

| Clé | Valeur | Pourquoi |
| --- | --- | --- |
| `contentBoundaries` | `true` | le texte d'une page est délimité, l'agent le traite comme une donnée |
| `maxOutput` | `50000` | une page géante ne remplit pas le contexte |
| `useSystemCa` | `true` | install, doctor et read font confiance à la CA d'entreprise du système |
| `caCert` | le fichier de `NODE_EXTRA_CA_CERTS` ou `SSL_CERT_FILE` | Linux seulement : c'est le seul système où Chromium lit ce réglage |

Le script ne pose pas de `proxy` : Chromium suit déjà le proxy du système (PAC
compris), et le forcer casserait un poste qui passe par un client Zscaler.

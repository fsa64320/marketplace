#!/usr/bin/env bash
# Traduit le verdict de vérification de GitHub sur chaque commit en diagnostic + action.
#
#   verifier_signatures.sh <chemin d'API gh renvoyant une liste de commits>
#
# Adapté de sta-ai-tools/.github/scripts/verify-signatures.sh. Ici le contrôle est
# CONSULTATIF : GitHub Free ne peut pas exiger de commits vérifiés sur un dépôt privé,
# et les commits poussés depuis une session Claude sont signés par une clé inconnue
# du compte. Le script avertit (::warning) et sort toujours en 0.
set -euo pipefail

chemin="${1:?usage : verifier_signatures.sh <chemin-api-gh>}"

read -r -d '' filtre <<'JQ' || true
def diag:
  { unsigned:               ["SIGNATURE", "commit non signé : git config commit.gpgsign true, ou git commit -S"],
    no_user:                ["E-MAIL",    "l'e-mail du committer n'est rattaché à aucun compte GitHub : mets dans user.email une adresse vérifiée sur ton compte"],
    unverified_email:       ["E-MAIL",    "l'e-mail du committer appartient à un compte mais n'y est pas vérifié : vérifie-le dans les réglages e-mail de GitHub"],
    bad_email:              ["E-MAIL",    "l'e-mail du committer ne fait pas partie des identités de la clé de signature"],
    unknown_key:            ["CLÉ",       "la clé de signature n'est enregistrée sur aucun compte GitHub : ajoute-la comme Signing Key (liste distincte des clés d'authentification). Attendu pour un commit poussé depuis une session Claude"],
    not_signing_key:        ["CLÉ",       "la clé GPG n'a pas l'usage signature"],
    expired_key:            ["CLÉ",       "la clé de signature a expiré"],
    invalid:                ["SIGNATURE", "la signature ne se vérifie pas avec sa clé"],
    malformed_signature:    ["SIGNATURE", "la signature est illisible"],
    unknown_signature_type: ["SIGNATURE", "signature d'un type non reconnu"],
    gpgverify_error:        ["PASSAGER",  "le service de vérification de GitHub a échoué : relance le job"],
    gpgverify_unavailable:  ["PASSAGER",  "le service de vérification de GitHub est indisponible : relance le job"]
  }[.] // ["INCONNU", "raison non reconnue : voir la doc REST sur la vérification des commits"];
.[] | select(.commit.verification.verified == false)
| (.commit.verification.reason | diag) as $d
| [ .sha[0:8], $d[0], .commit.verification.reason, .commit.committer.email, $d[1] ] | @tsv
JQ

non_verifies=$(gh api --paginate "$chemin" --jq "$filtre")

if [ -z "$non_verifies" ]; then
  echo "✔ Tous les commits sont vérifiés."
  exit 0
fi

{
  echo "### Commits non vérifiés (consultatif)"
  echo
  echo "| Commit | Famille | Raison | E-mail | Action |"
  echo "| --- | --- | --- | --- | --- |"
} >> "${GITHUB_STEP_SUMMARY:-/dev/null}"

while IFS=$'\t' read -r sha famille raison email action; do
  printf '\n%s  [%s]  raison=%s\n    e-mail du committer : %s\n    action : %s\n' \
    "$sha" "$famille" "$raison" "$email" "$action"
  echo "::warning title=Commit ${sha} non vérifié (${famille})::${action}"
  echo "| \`${sha}\` | ${famille} | \`${raison}\` | ${email} | ${action} |" >> "${GITHUB_STEP_SUMMARY:-/dev/null}"
done <<< "$non_verifies"

exit 0

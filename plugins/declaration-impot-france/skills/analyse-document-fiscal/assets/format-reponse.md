# Format de réponse — analyse de document fiscal

Produis les 12 blocs ci-dessous, dans cet ordre et avec cette mise en forme, après la fiche de vérification. Les taux, seuils et libellés de cases écrits ici sont des exemples : remplace-les par ceux de la fiche. Remplace chaque `0,00 €` par le montant lu dans le document et `AAAA` par l'année des revenus.

---

### 📄 1. Documents analysés

*(Si un seul document, ligne unique. Si plusieurs documents, tableau complet.)*

| # | Émetteur | Titulaire | Type |
|---|----------|-----------|------|
| 1 | Nom de l'établissement | Prénom Nom | IFU / Relevé SCPI / Attestation AV / Relevé PEA |
| 2 | … | … | … |

| Champ | Valeur |
|-------|--------|
| Année fiscale | AAAA |
| Formulaires concernés | 2042 ☑ / 2044 ☐ / 2047 ☐ / 2074 ☐ / 2042-IFI ☐ |

---

### 📊 2. Formulaire 2042 — Revenus consolidés du foyer

*(Montants consolidés tous documents confondus, y compris enfants mineurs rattachés)*

| Case | Libellé | Montant | Statut |
|------|---------|---------|--------|
| 2DC | Dividendes d'actions (avec droit à abattement 40 %) | 0,00 € | — Non concerné |
| 2TS | Autres revenus distribués, sans droit à l'abattement de 40 % | 0,00 € | — Non concerné |
| 2TR | Intérêts et produits de placement à revenu fixe | 0,00 € | — Non concerné |
| 2BH | Revenus déjà soumis aux PS avec CSG déductible *(sert au calcul de la CSG déductible si option 2OP)* | 0,00 € | — Non concerné |
| 2CK | Crédit d'impôt prélèvement forfaitaire non libératoire | 0,00 € | — Non concerné |
| 2AB | Crédits d'impôt sur valeurs étrangères | 0,00 € | — Non concerné |
| 2CA | Frais et charges déductibles des revenus de capitaux mobiliers | 0,00 € | — Non concerné |
| 3VG | Plus-values nettes sur cessions de valeurs mobilières | 0,00 € | — Non concerné |
| 3VH | Moins-values nettes de l'année | 0,00 € | — Non concerné |
| 3VZ | Plus-values immobilières SCPI (nettes, soumises aux PS) | 0,00 € | — Non concerné |
| 4BA | Revenus fonciers nets (report depuis 2044) | 0,00 € | — Non concerné |
| 4BL | Revenus fonciers étrangers avec crédit d'impôt (report depuis 2047) | 0,00 € | — Non concerné |
| 4EA | Revenus étrangers exonérés pour taux effectif | 0,00 € | — Non concerné |
| 8TK | Crédit d'impôt sur revenus étrangers (= 4BL) | 0,00 € | — Non concerné |

> Statut : `✅ À reporter` ou `— Non concerné`. Ne jamais omettre une case — la laisser à `0,00 €` si non applicable.

*(Si plusieurs documents, ajouter un sous-tableau de détail par case clé, par exemple :)*

**Détail par document — case 2DC**

| Document | Titulaire | 2DC |
|----------|-----------|-----|
| Émetteur 1 | Prénom | 0,00 € |
| … | … | … |
| **Total** | | **0,00 €** |

*(Répéter pour 2CK et toute autre case consolidée depuis plusieurs sources)*

---

### 🏠 3. Formulaire 2044 — Revenus fonciers SCPI (régime réel)

> *(Bloc présent uniquement si le document contient des revenus fonciers en régime réel. Sinon : « Formulaire 2044 non applicable à ce document. »)*
>
> Chaque SCPI constitue un immeuble distinct. Arrondir chaque montant à l'euro le plus proche. Les pays dont les revenus sont exonérés pour taux effectif (ex : Belgique, Pays-Bas, Irlande, Portugal, Finlande selon conventions) **ne figurent pas dans la 2044** — ils passent directement en case **4EA**.

**SCPI [Nom] — [Titulaire(s)] ([N] parts)**
Adresse SCPI : [adresse] — Société de gestion : [nom]

| Immeuble | Pays | 111 Revenus bruts | 112 Frais & charges | 113 Intérêts emprunt | 114 Bénéfice (+) / Déficit (–) |
|----------|------|:-----------------:|:-------------------:|:--------------------:|:------------------------------:|
| 1 | France | 0 € | 0 € | 0 € | **0 €** |
| 2 | Allemagne | 0 € | 0 € | 0 € | **0 €** |
| … | … | … | … | … | … |
| **Ligne 420 — Total** | | **0 €** | **0 €** | **0 €** | **0 €** |

> Report 2042 : **4BA = 0 €** · **4BL = 0 €** · **8TK = 0 €**

*(Répéter un bloc par SCPI distincte)*

**Récapitulatif 2044 — Total foyer**

| SCPI | 111 Bruts | 112 Charges | 113 Intérêts | 114 Net (→ 4BA) | dont 4BL |
|------|:---------:|:-----------:|:------------:|:---------------:|:--------:|
| SCPI 1 | 0 € | 0 € | 0 € | 0 € | 0 € |
| … | … | … | … | … | … |
| **TOTAL** | **0 €** | **0 €** | **0 €** | **0 €** | **0 €** |

> Report final 2042 : **4BA = 0 €** → **4BL = 0 €** → **8TK = 0 €**

> Si micro-foncier (revenus fonciers bruts du foyer ≤ 15 000 € et pas d'option pour le réel) : déclarer directement case **4BE** en 2042, sans remplir 2044.

---

### 🌍 4. Formulaire 2047 — Revenus de source étrangère

> *(Bloc présent uniquement si le document contient des revenus de source étrangère. Sinon : « Formulaire 2047 non applicable à ce document. »)*
>
> Vérifier la convention fiscale applicable entre la France et le pays source — le traitement varie selon les conventions.

**A. Revenus imposés en France avec crédit d'impôt (→ cases 4BL + 8TK) → cadre 4**

| Document | Pays | 4BL / 8TK | Nature |
|----------|------|:---------:|--------|
| SCPI 1 | Allemagne, Espagne… | 0,00 € | Loyers étrangers (crédit d'impôt = impôt FR) |
| … | … | … | … |
| **Total 8TK** | | **0,00 €** | |

> Case **8TK = 0,00 €** — Ce crédit d'impôt annule l'impôt français sur ces revenus étrangers.

**B. Revenus exonérés servant au calcul du taux effectif (→ case 4EA) → cadre 6**

| Document | Pays (exonérés taux effectif) | 4EA |
|----------|:-----------------------------:|:---:|
| SCPI 1 | Belgique, Pays-Bas, Irlande… | 0,00 € |
| … | … | … |
| **Total 4EA** | | **0,00 €** |

> Case **4EA = 0,00 €** — Ces revenus ne sont pas imposés en France mais augmentent le taux d'imposition appliqué aux revenus français (taux effectif).

---

### 📈 5. Formulaire 2074 — Plus-values mobilières (régime dérogatoire)

> *(Bloc présent uniquement si le document mentionne des cessions hors PFU : reports de moins-values antérieures à 2018, abattements pour durée de détention, BSPCE, stock-options. Sinon : « Formulaire 2074 non applicable à ce document. »)*

| Ligne | Libellé | Montant |
|-------|---------|---------|
| 001 | Prix de cession total | 0,00 € |
| 020 | Prix d'acquisition | 0,00 € |
| 021 | Frais d'acquisition | 0,00 € |
| 040 | Plus-value / Moins-value brute | 0,00 € |
| 060 | Abattement pour durée de détention | 0,00 € |
| 070 | Plus-value / Moins-value nette imposable | 0,00 € |

Reports en 2042 C :
| Case 2042 C | Libellé | Montant |
|-------------|---------|---------|
| 3VG | Plus-value nette imposable | 0,00 € |
| 3VH | Moins-value nette reportable | 0,00 € |
| 3UA | Plus-value avec abattement renforcé | 0,00 € |

> Le formulaire 2074 est obligatoire dès lors qu'une compensation entre plus et moins-values ou un abattement s'applique, même si le résultat net est nul. Si la société de gestion indique que le 2074 n'est pas requis, reporter directement en case 3VG.

---

### 🏛️ 6. IFI — Impôt sur la Fortune Immobilière

> *(Bloc présent uniquement si le foyer détient de l'immobilier ou des SCPI. Si patrimoine immobilier net < 1 300 000 €, écrire : « IFI non applicable — seuil de 1 300 000 € non atteint. »)*

Valeur des parts SCPI à déclarer au 01/01/AAAA+1 (= 31/12/AAAA) :

| SCPI | Titulaire | Nb parts | Valeur IFI / part | Valeur IFI totale |
|------|-----------|:--------:|:-----------------:|:-----------------:|
| SCPI 1 | Prénom | N | 0,00 € | **0,00 €** |
| … | … | … | … | … |
| **Total foyer** | | | | **0,00 €** |

> Si le patrimoine immobilier net total dépasse **1 300 000 €**, remplir le formulaire **2042-IFI**. Ajouter la valeur de l'immobilier direct et déduire les dettes immobilières en cours.

---

### 💳 7. PEA — Plan d'Épargne en Actions

> *(Bloc présent uniquement si le foyer détient un PEA. Sinon : « PEA non applicable à ce document. »)*

| Titulaire | Établissement | Référence | Date ouverture | Événement fiscal AAAA |
|-----------|--------------|-----------|----------------|----------------------|
| Prénom | Établissement | N° compte | JJ/MM/AAAA | Aucun / Retrait partiel / Clôture |

> Aucun montant à reporter si aucun retrait en AAAA. Les dividendes et plus-values restent dans l'enveloppe PEA et ne sont imposables qu'en cas de retrait (exonération IR après 5 ans d'ouverture).

---

### 📋 8. Récapitulatif consolidé — Cases à reporter

**Formulaire 2042**

| Case | Montant à reporter | Note |
|------|--------------------|------|
| 2DC | **0,00 €** | |
| 2TS | **0,00 €** | |
| 2TR | **0,00 €** | |
| 2CK | **0,00 €** | Crédit d'impôt direct |
| 2BH | **0,00 €** | CSG déductible, utile si option 2OP |
| 3VG | **0,00 €** | |
| 3VZ | **0,00 €** | |
| 4BA | **0,00 €** | Report depuis 2044 |
| 4BL | **0,00 €** | Revenus étrangers avec crédit d'impôt |
| 4EA | **0,00 €** | Revenus exonérés taux effectif |
| 8TK | **0,00 €** | Crédit d'impôt revenus étrangers (= 4BL) |

---

### 🪜 9. Notice explicative — Comment saisir votre déclaration

*(Produire un guide pas à pas adapté aux documents analysés. Structure type :)*

**Étape 1 — Connexion à impots.gouv.fr**
1. Accédez à [impots.gouv.fr](https://www.impots.gouv.fr) > **Mon espace particulier** > **Déclarer mes revenus**
2. Vérifiez les informations pré-remplies (état civil, adresse, situation familiale, rattachement des enfants mineurs)

**Étape 2 — Revenus de capitaux mobiliers (formulaire 2042, section 2)**
Pour chaque case avec un montant > 0, expliquer en une phrase ce qu'elle contient et comment la saisir.

*Exemple :*
**Case 2DC — Dividendes (X XXX,XX €)**
[Expliquer les sources, l'option PFU vs barème et l'impact de l'abattement 40 %]

**Case 2CK — Crédit d'impôt prélèvement forfaitaire (X XXX,XX €)**
[Rappeler que ce montant vient en déduction de l'impôt final — ne pas l'oublier]

**Étape 3 — Revenus fonciers SCPI (formulaire 2044 puis 2042)**
*(Si applicable)* Expliquer s'il faut remplir d'abord la 2044 ou reporter directement en 4BA.

**Étape 4 — Revenus de source étrangère (formulaire 2047)**
*(Si applicable)* Expliquer les deux mécanismes : crédit d'impôt (4BL + 8TK) et taux effectif (4EA).

**Étape 5 — Plus-values immobilières SCPI (case 3VZ)**
*(Si applicable)* Préciser si les prélèvements sociaux ont déjà été prélevés à la source.

**Étape 6 — Option barème progressif (case 2OP)**
Analyser si l'option est avantageuse en fonction du TMI estimé du foyer.
- TMI de 0 % ou 11 % → barème progressif potentiellement plus favorable
- TMI ≥ 30 % → PFU généralement plus avantageux
- L'option est globale et irrévocable pour l'année

**Étape 7 — Vérifications finales avant validation**
- [ ] Montants pré-remplis cohérents avec les IFU
- [ ] Case 2CK renseignée (crédit d'impôt direct)
- [ ] Case 8TK renseignée si revenus étrangers SCPI (rarement pré-remplie)
- [ ] Case 4EA renseignée si revenus exonérés taux effectif
- [ ] Enfants mineurs correctement rattachés au foyer
- [ ] Coordonnées bancaires à jour pour remboursement éventuel

---

### ⚠️ 10. Points d'attention spécifiques

*(Lister uniquement les points réellement applicables aux documents analysés)*

- [ ] Case **8TK** rarement pré-remplie automatiquement → saisie manuelle via formulaire 2047
- [ ] Case **4EA** non pré-remplie → à saisir manuellement
- [ ] Revenus de source étrangère → vérifier que tous les pays figurent dans le formulaire 2047
- [ ] Prélèvements sociaux déjà prélevés à la source sur 3VZ → ne pas les redéclarer
- [ ] Formulaire **2074** non requis si la société de gestion confirme le report direct en 3VG
- [ ] Option **2OP** : simuler les deux options sur impots.gouv.fr avant de valider
- [ ] **IFI** : ajouter les valeurs PEA et immobilier direct si seuil de 1 300 000 € potentiellement atteint
- [ ] PEA : confirmer l'absence de retrait pour éviter une imposition non anticipée

---

### 🧮 11. Estimation fiscale indicative

*(Omettre si les données sont insuffisantes pour estimer)*

| Composante | Base | Régime PFU (défaut) | Régime barème (option 2OP) |
|------------|------|---------------------|---------------------------|
| Dividendes 2DC | 0,00 € | 12,8 % + PS → 0,00 € | Abattement 40 % → base 0,00 € → TMI |
| Distributions 2TS | 0,00 € | 12,8 % + PS → 0,00 € | TMI sans abattement |
| Intérêts 2TR | 0,00 € | 12,8 % + PS → 0,00 € | TMI sans abattement |
| Plus-values 3VG | 0,00 € | 12,8 % + PS → 0,00 € | TMI |
| Revenus fonciers 4BA | 0,00 € | Barème progressif | Barème progressif |
| Revenus étrangers 4BL | 0,00 € | Crédit d'impôt 8TK → annulation | Crédit d'impôt 8TK → annulation |
| **Crédit d'impôt 2CK** | | **– 0,00 €** | **– 0,00 €** |
| **Crédit d'impôt 8TK** | | **– 0,00 €** | **– 0,00 €** |

> Taux des prélèvements sociaux (PS) : celui de la fiche de vérification pour ce type de revenu et cette année.
>
> Estimation indicative. Le calcul exact dépend de l'ensemble des revenus du foyer (salaires, pensions, autres revenus), du quotient familial et des charges déductibles éventuelles.

---

### ⚖️ 12. Mise en garde

*Cette analyse est produite à titre informatif et pédagogique à partir des éléments fournis. Elle ne constitue pas un conseil fiscal et ne remplace pas l'intervention d'un expert-comptable ou d'un conseiller fiscal agréé. En cas de doute, consultez un professionnel ou le service des impôts (numéro : 0809 401 401).*

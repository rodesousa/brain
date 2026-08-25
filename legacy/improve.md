# Improve — questions ouvertes sur l'évolution du vault

Réflexions architecturales en suspens. Pas urgentes, mais à trancher avant que le vault grossisse.

---

## ✓ Décisions prises

### 2026-05-09 — issues du cobaye HALO

- **Zone clusters** = `raw/clusters/<source-type>/<source-id>/` avec champ `status: pending|kept|discarded`. **Pas** de zone `staging/` séparée. (Question 3, option C confirmée par usage.)
- **Snapshot repo** = option A — un seul fichier markdown `raw/repos/<owner>-<repo>.md` avec frontmatter minimal (`repo`, `url`, `fetched_at`) + README verbatim. Pas de commit SHA, pas de tree, pas de stats. Re-snapshot = overwrite ou nouveau fichier daté à décider plus tard. (Question 2.a)
- ~~**Page wiki pour un repo** = `wiki/repos/<owner>-<repo>.md` avec `type: entity`.~~ **Révisé 2026-05-13** : une entité = une seule page wiki dans son dossier de domaine (`wiki/agents/`, `wiki/tools/`…), pas dans `wiki/repos/`. Le snapshot `raw/repos/<owner>-<repo>.md` reste une source parmi d'autres. Voir règle "Localisation des entités" dans `CLAUDE.md`. (Question 2.b — décision révisée.)
- **Numérotation des clusters** préservée quand certains facets sont écartés en amont (ex : `cluster-01, 02, 03, 05` si la 4 a été retirée). Garde la trace de "ce qui a été considéré et rejeté".
- **Granularité wiki** : plusieurs cluster files `kept` peuvent fusionner dans **une seule** page wiki si les facets se recouvrent (ex : `purpose` + `methodology` → `wiki/repos/halo.md`). Une facet ne mérite pas forcément sa propre page wiki.
- **Citation cluster files depuis wiki/** : via wikilinks Obsidian (`[[cluster-NN-facet]]`). Le lint résout désormais les wikilinks contre `raw/` + `wiki/`, pas seulement `wiki/`.
- **Forward-without-reverse** : check limité aux pages **entre `wiki/` et `wiki/`**. Les pages `wiki/` peuvent citer `raw/` sans réciprocité (`raw/` n'a pas vocation à back-référencer).
- **Triage humain via édition manuelle du frontmatter** (`status: pending` → `kept`/`discarded`). Pas d'outil dédié à ce stade — éditeur ou Obsidian suffit.

---

## Questions encore ouvertes

### 1. Workflow tweets — granularité du digest

**Cas** : ingest cluster-by-cluster validé. Reste : **digest périodique = par mois, par semaine, par batch ?**

### 2.c. Code snippets in-page wiki pour les repos

Quand on ingère un repo, faut-il citer du code source dans la page wiki ?
- **Avec snippets courts (≤20 lignes) pinnés au commit** : self-contained mais maintenance si le repo bouge
- **Sans snippets, juste liens permaliens GitHub** : léger
- **Conditionnel à la facet** : oui pour `key-implementation`, non pour `purpose`/`lessons`

Pas tranché pendant le cobaye HALO parce que le README suffisait. À retrancher au prochain repo où le code lui-même matters.

### 2.d. Re-ingestion d'un repo qui a évolué

Si HALO sort une v2 dans 6 mois, comment on traite la diff ?
- Re-snapshot full (overwrite `raw/repos/halo.md`) ?
- Snapshot daté (`halo-2026-11.md`) avec diff sur les facets affectées ?
- Champ `last_commit_ingested` à tracker dans le frontmatter de la page wiki ?

Peut attendre, pas urgent.

### 4. Fusion ou ségrégation des clusters par type de source

```
raw/clusters/twitter/...
raw/clusters/repos/...
raw/clusters/podcasts/...
raw/clusters/articles/...
```

Cette structure est utilisée actuellement (validée par cobaye HALO). Question résiduelle : les workflows de **création** de clusters diffèrent (grouping pour tweets, décomposition pour repos), donc deux mécaniques distinctes. Mais les workflows de **triage** (status pending/kept/discarded) et **promotion** (kept → wiki) sont identiques.

→ Garder la structure actuelle, accepter que la création soit type-spécifique mais le reste générique.

### 5. Implications pratiques restant à implémenter

- ~~Le lint ignore les `status: discarded` par défaut pour les checks de liens/orphelins.~~ → résolu trivialement parce que `raw/` n'est pas walké pour les checks de liens entre pages wiki.
- **`update_hot.py` flag les clusters `pending` depuis >7 jours** : pas encore implémenté. Utile pour rappel triage.
- **`## My take` dans un cluster `discarded`** explique *pourquoi* discarded : pas systématiquement appliqué pendant le cobaye HALO (les 2 discarded n'avaient pas de raison écrite). À renforcer comme convention dans `CLAUDE.md` ?

---

## Apprentissages du cobaye HALO

1. **Le triage est rapide** — lire 4 cluster files de ~80 lignes chacun = 5-10 min. Workflow utilisable.
2. **Les clusters `discarded` sont peu coûteux** — pas de frustration à voir 50% du travail "jeté", parce que la décision est *informée* (clusters lus avant rejet).
3. **La question dans `## My take`** (cf. cluster-02) est un signal de valeur : indique un point qui mérite d'être clarifié avant promotion. La page wiki finale a intégré la réponse comme section dédiée — utile.
4. **Le bug du lint cross-zones** révèle qu'on n'avait pas pensé à comment `wiki/` cite `raw/`. La règle "tout wikilink doit résoudre" suppose un référentiel unique — il fallait l'élargir.
5. **L'orphelin attendu** sur la 1ère page wiki = warning légitime du lint mais pas actionnable. À mesure que le vault grossit, le warning disparaîtra naturellement. Pas la peine de tweaker le lint.

---

## Décisions à prendre dans cet ordre (mis à jour)

1. ~~Trancher la zone (option A/B/C de la section 3)~~ → **C, fait**
2. ~~Décider si fusion clusters par source~~ → **structure actuelle conservée**
3. Choisir granularité digest tweets (mensuel / hebdo / par batch)
4. ~~Trancher snapshot repos (section 2.a)~~ → **A, fait**
5. ~~Trancher type wiki/repos vs wiki/entities (section 2.b)~~ → ~~**wiki/repos/ + type:entity, fait**~~ → **révisé 2026-05-13** : une entité vit dans son dossier de domaine (`wiki/agents/`, `wiki/tools/`…), pas dans `wiki/repos/`. HALO migré de `wiki/repos/` vers `wiki/tools/`.
6. Snippets in-page repos (section 2.c)
7. Re-ingest evolution repos (section 2.d) — peut attendre
8. Implémenter `pending >7j` dans `update_hot.py` (nouveau)
9. Renforcer convention "raison du discard dans `## My take`" (nouveau)

---

_Dernière mise à jour : 2026-05-09 (après cobaye HALO)_

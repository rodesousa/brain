# Refonte de `brain/`

Document de travail. Mode interview : je pose des questions, tes réponses atterrissent ici.
Le schéma acté (D1-D5) est implémenté dans `AGENTS.md` et testé (premier ingest). Les questions
restantes (veille, lint) se trancheront lors des prochaines sessions.

- Ouvert : 2026-08-12
- Statut : `interview en cours — D1-D5 tranchées`

---

## 1. Le besoin réel (formulé par toi)

> « Je veux stocker des infos que j'ai pas eu encore le temps de lire, je veux stocker la
> source, et avoir un résumé du truc là, et qu'il soit rangé pour que demain si je dis
> "tiens va me chercher ça", tu saches de quoi je parle. »

Trois primitives, dans cet ordre :

1. **Capture** — une source arrive, elle ne doit pas être perdue. Je n'ai pas le temps de la lire *maintenant*.
2. **Résumé** — je veux savoir ce qu'il y a dedans sans l'ouvrir. Le résumé est un *service*, pas un livrable à valider.
3. **Retrieval** — demain, une demande floue et orale (« le truc sur X ») doit retomber sur la bonne page.

Le rangement par **graphe** est jugé pertinent (le lien entre les choses est ce qui rend le retrieval flou possible).

## 2. Ce qui ne va pas dans la version actuelle

| # | Reproche | Cause dans le schéma actuel |
|---|----------|------------------------------|
| C1 | **Trop de fichiers.** Préférence pour un gros fichier par source ou par sujet. | Le workflow ingest crée systématiquement `wiki/sources/<slug>.md` **+** N pages entités **+** clusters dans `raw/clusters/`. Un ingest = 4-8 fichiers. |
| C2 | **La validation ne sert à rien.** « Je m'en fous de valider ou pas ce que tu écris, j'ai la source. » | `lifecycle: draft/reviewed/verified`, marqueurs `^[inferred]` / `^[ambiguous]`, lint « pages draft depuis >14 jours » — tout ça est une machinerie de confiance dont il n'a pas besoin. |
| C3 | **`## My take` est une corvée imposée.** | Section obligatoire sur toute page entité/source/comparison. Mais il ne l'écrit pas lui-même — donc c'est moi qui écris un faux avis, ce qui est pire que rien. |
| C4 | **Le résumé doit être vivant.** Quand il lit la source, ou qu'on en discute, le résumé doit pouvoir être mis à jour — à sa demande ou sur ma proposition quand je le juge pertinent. | Rien dans le schéma actuel ne modélise « update après lecture ». Le workflow est one-shot : ingest → page → figée. |
| C5 | **La veille (LinkedIn / X / RSS) n'est pas modélisée.** Il veut un mode où je vais chercher les données et lui produis une **newsletter perso**. | Le vault n'a que des `raw/tweet/` manuels + `tools/scrape_*.py`. Pas de flux, pas de cadence, pas d'artefact newsletter. |

## 3. Références à exploiter

### gbrain (garrytan)

- **Markdown-first, DB-synced** : la vérité est dans le repo git en markdown ; une DB (Postgres/PGLite) n'est qu'un index de retrieval reconstructible. → séparer *stockage* et *recherche*.
- **Graphe typé auto-câblé, zéro appel LLM** : les arêtes (`works_at`, `founded`, `invested_in`…) sont extraites à l'écriture. Gain mesuré : +31 points de P@5 vs sans graphe.
- **Deux modes de lecture** : `search` (hybride vecteur + BM25, retourne des pages à skimmer) et `think` (réponse synthétisée avec citations **et gap analysis** : ce que le brain ne sait pas encore).
- **Inbox** : fichiers déposés dans `~/.gbrain/inbox/` indexés automatiquement + webhook `/ingest`. → capture sans friction.
- **Schema packs** : la taxonomie de types est configurable, pas gravée. `schema detect` déduit la forme réelle du filesystem.
- **Dream cycles** (cron nocturne) : dédup, réparation de citations, scoring de salience, détection de contradictions.

### aidesk/news (ton propre projet)

Pipeline déjà construit et éprouvé : `scrape → items → dedup → label → newsletter`.

- `sources.json` : liste de comptes suivis, typés (`source_type: twitter`), **taggés**, `is_active`, `last_scraped`, `total_items`.
- `LABELS.md` : labellisation **à deux tiers** — Tier 1 = intérêt éditorial (`video/gros-sujet`, `video/pratique`, `video/reflexion`, `video/deep-dive`, `video/radar`), Tier 2 = labels de traçage thématique. La labellisation est **découplée** du workflow newsletter : elle alimente les tendances et la priorisation.
- `src/dedup/strategies.ts` : la dédup est un problème de première classe, avec plusieurs stratégies.
- `data/export/YYYY-MM-DD_newsletter.md` + `data/analysis/YYYY-MM-DD_analysis.md` : la newsletter est un **artefact daté**, et l'analyse est un artefact séparé.
- Postgres + Docker + Makefile + tests Jest.

**Question de fond que ça pose** : est-ce que la veille de `brain/` doit *réutiliser* cette stack, ou en être une version markdown-only beaucoup plus légère ?

---

## 4. Interview

### D1 — Granularité : inbox → page sujet _(tranché)_

**Le modèle retenu :**

```
inbox/<item>          →  digest  →  wiki/<sujet>.md   (grossit)
   (transitoire)                       (durable, UN fichier)
```

- **Défaut** : un item d'inbox **fusionne** dans **une** page sujet. Un seul fichier durable par sujet, qui grossit à chaque source.
- **Éclatement en plusieurs fichiers** : possible, mais **à la demande uniquement**. Je ne fan-out jamais de moi-même ; au mieux je le propose en une ligne. C'est lui qui déclenche.
- **Sujet inexistant** → je **crée la page sujet** (`wiki/moe.md`) sans demander. Rationale : le besoin est le retrieval de demain ; un article MoE rangé de force sous `quantization` serait introuvable. Créer une page pour ranger juste ≠ créer 6 fichiers par ingest.
- **`raw/` disparaît.** Plus d'archive immuable systématique. Par défaut l'item d'inbox **ne persiste pas** après digestion (l'URL dans le frontmatter suffit — « j'ai la source »). Conserver le texte brut devient une **option** explicite, pas le défaut.

**Conséquence directe sur le schéma actuel** : le workflow ingest passe de 4-8 fichiers créés à **0 ou 1**. `wiki/sources/` et `raw/clusters/` n'ont plus de raison d'exister comme étapes obligatoires.

### Round 2 — en cours

2. **Graphe / retrieval** — que doit-il se passer quand tu dis « va me chercher le truc sur X » ?
3. **Veille** — réutiliser la stack `aidesk/news`, ou markdown-only dans `brain/` ?
4. **Capture** — par quel geste concret une source entre dans l'inbox ?
5. **Difficultés vécues** — qu'est-ce qui t'a fait décrocher du vault actuel, concrètement ?

### D2 — UI de lecture : Obsidian-compatible _(tranché 2026-08-25)_

Obsidian a servi (et sert encore) à la lecture, mais nvim passe aussi bien. Pas d'UI maison à
construire. La contrainte retenue : le vault doit rester **Obsidian-compatible** — en particulier
les wikilinks `[[...]]` et le markdown simple. Tout doit rester lisible et éditable depuis un
éditeur texte (nvim). → on conserve wikilinks + markdown, pas de dépendance à un plugin Obsidian
spécifique, rien qui ne se lise dans un terminal.

### D3 — Granularité : un dossier par sujet, un fichier par défaut _(tranché 2026-08-25)_

```
wiki/<sujet>/<sujet>.md      ← défaut : UN fichier par sujet
```

- **Défaut** : 1 dossier = 1 sujet = 1 fichier, qui grossit à chaque source digérée.
- **Fichiers additionnels** dans le même dossier : à la demande uniquement — je ne crée jamais
  un 2e fichier moi-même ; au mieux je le propose en une ligne, c'est lui qui déclenche.
- **Nouvelle itération = nouveau sujet** : une seconde refonte → son propre dossier, son propre
  fichier. On ne touche jamais à l'existant (rien ne casse).
- **Dépréciation sans suppression** : quand un sujet est remplacé/obsolète, le fichier reste
  (le passé reste consultable), l'index le marque `(deprecated)`.

### D4 — Sort des 54 pages existantes : feuille blanche _(tranché 2026-08-25)_

On repart d'une feuille blanche. L'ancien schéma (dossiers de domaine `wiki/agents/`,
`wiki/tools/`, `wiki/llm_101/`…, `raw/` immuable, clusters/facets, lifecycle, `## My take`) n'est
pas migré. L'ancien contenu part en `legacy/` (rien n'est détruit : git garde l'historique de toute
façon). La nouvelle structure suit D1/D2/D3 :

```
legacy/          ← ancien wiki/ + raw/ (+ ancien index.md), conservé, non maintenu
wiki/<sujet>/<sujet>.md   ← nouveau schéma, au fil des ingests
```

Corollaire : si un sujet des 54 pages redevient pertinent, on le **re-capture** comme une source
fraîche plutôt que de migrer sa page.

### D5 — Capture : une source entre par un geste de chat _(tranché 2026-08-25)_

**Le geste (demain) :** ouvrir `hermes` dans le dossier brain, puis donner la source de 3 façons :
`ingest <url>` | `ingest <chemin>` | texte collé + `ingest`. Pas d'inbox, pas de clipper, pas de
dossier de staging. Un seul geste de chat.

**Ce que l'agent fait (sans poser 10 questions) :**
1. Lit la source.
2. Regarde l'index → sujet existant ? on ajoute dans `wiki/<sujet>/<sujet>.md` ; sinon on crée
   `wiki/<sujet>/<sujet>.md`.
3. Écrit le digest : résumé court en haut, points clés, source (URL + date).
4. Met à jour la ligne de l'index (avec mots-clés pour le fuzzy match).
5. Append dans `log.md`.
6. Si la source est à cheval sur deux sujets : UNE question max, puis on file.

**Le texte brut vit dans le dossier du sujet :**

```
wiki/<sujet>/<sujet>.md          ← digest (une ligne dans l'index)
wiki/<sujet>/sources/<slug>.md   ← texte brut, UN fichier par source
```

- Source substantielle (≈ >150 mots, article/PDF/transcript/URL) → son fichier dans `sources/`.
- Court extrait (< ~150 mots) → le texte va dans le digest directement, pas de fichier source.
- `sources/*.md` ne sont **jamais** dans l'index — l'index ne liste que les **sujets**.

**Exécuté le 2026-08-25** : `wiki/`, `raw/`, `index.md`, `hot.md`, `improve.md`, `2026-05-09.md`,
`Clippings/` déplacés dans `legacy/` (via `git mv`, non destructif). Nouveau `index.md` créé.
`AGENTS.md` marqué `EN REFONTE` (état transitoire, pas le schéma final). `tools/` du vieux schéma
conservés tels quels — à réécrire ou jeter quand la refonte sera validée.

`tools/` a ensuite été déplacé dans `legacy/` aussi (2026-08-25) — le log est désormais maintenu à
la main, plus via `tools/append_log.py`.

### Questions gardées pour les rounds suivants

- Cadence de la newsletter (quotidienne / hebdo / à la demande) et son format (longueur, sections, ton).
- Que devient une source **jamais lue** au bout de N semaines ? (expiration, ou accumulation infinie assumée)
- Le `raw/` immuable : on garde le principe ? (il est sain, mais il double le volume de fichiers)
- Le lint : qu'est-ce qui reste utile dedans si on jette la validation et le `My take` ?
- Distinction **veille** (flux, éphémère, newsletter) vs **wiki** (durable, retrieval) : est-ce qu'un item de veille peut « promouvoir » vers le wiki, et sur quel critère ?

> Reste à passer (2026-08-25, différé à une prochaine session) : veille/newsletter (C5) et lint.
> Les décisions D1-D5 suffisent pour démarrer les ingests et tester le schéma sur le vif.

---

## 5. Recherche : index & mémoire optimisés _(2026-08-25)_

Résultat de la recherche (web + repos munder-difflin / deepseek-harness + doc Hermes + subagent).
Synthèse détaillée dans `research/retrieval-memoire-synthese.md`.

**Verdict** : à 54 pages, l'index plat est déjà le bon système. Les gains à court terme sont des
*outils de recherche + itération* pour l'agent, pas une autre architecture. Vecteur/graphe/DB =
évolutions à ~1000+ pages.

**Ce qui revient partout (sources variées)** :

- **Index = vue dérivée, jamais vérité parallèle.** Le markdown est la vérité ; l'index et la
  recherche (FTS/BM25) sont reconstruisibles à tout moment (gbrain, munder-difflin, qmd).
- **Index = la pièce que le harness lit en entier à chaque fois** → le garder minimal, une ligne
  par sujet, des alias/mots-clés pour le fuzzy match (pattern llms.txt).
- **La capacité d'itération bat les mécanismes de retrieval** : benchmark Letta 2025 — un agent
  avec `grep`/`search_files` sur un fichier bat les outils mémoire spécialisés (74.0 vs 68.5).
  → règle « réécris la requête 2-3 façons avant de dire introuvable ».
- **Les mécanismes mémoire lourds se reproduisent en markdown** : Mem0 = extraction à l'ingest
  (pas de stockage brut) + add-only ; Zep/Graphiti = invalidation des faits contredits →
  `^[superseded]` dans la page ; MemGPT = core mémoire (petit) vs archival (pages) ; git = mémoire
  temporelle ; consolidation périodique = « dream cycle » en markdown.
- **Contre-exemples** : antithesis-skills = testing déterministe, rien sur l'index/mémoire ;
  deepseek-harness = pas de mémoire wiki, mais invariant « model-visible means logged » (tout ce
  que le harness voit doit être reconstruisible depuis les fichiers).

**Actions retenues (markdown-only, maintenant)** :

1. `index.md` : une ligne par sujet, alias/mots-clés, marqueur `(deprecated)` ; sub-grouping >15.
2. Recherche : `grep`/`ripgrep` + règle de réécriture de requête (2-3 formulations).
3. Ingest = extraction distillée dans le fichier sujet (D1) + résumé vivant (C4).
4. Passe de consolidation périodique : maj `summary:`, marquage `^[superseded]`, git commit.
5. **Pas maintenant** : DB vectorielle, graphe DB, Mem0/Zep/Letta. Évolution si ça coince :
   SQLite FTS5 / `qmd search` → hybride `qmd query` → PGLite comme index reconstruisible.

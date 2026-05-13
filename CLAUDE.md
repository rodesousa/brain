# Schema — brain/

Ce vault est un LLM Wiki suivant le pattern de Karpathy (voir `LLM-WIKI-CONCEPT.md`), enrichi de quick wins venant de 5 implémentations communautaires (ar9av/obsidian-wiki, momhq/mom, kdsz001/OpenWiki, sametbrr/llm-wiki-manager, skyllwt/OmegaWiki).

## Structure

- `raw/` — sources brutes (articles, PDF, notes, transcripts). **Immuable** : je lis, je ne modifie pas.
- `wiki/` — pages générées et maintenues par moi. Je suis le seul propriétaire.
- `index.md` — catalogue de toutes les pages du wiki (par catégorie, avec one-liner).
- `log.md` — journal chronologique append-only des opérations.
- `LLM-WIKI-CONCEPT.md` — référence du pattern, ne pas modifier.

## Conventions de pages

### Langue

Français par défaut (langue de l'utilisateur).

### Liens

Wikilinks Obsidian natifs : `[[nom-de-page]]`. Pas de liens markdown relatifs.

### Frontmatter YAML obligatoire sur chaque page wiki

```yaml
---
type: entity | concept | source-summary | comparison | overview
summary: Une phrase de 15-25 mots décrivant ce que la page contient.
lifecycle: draft | reviewed | verified
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [chemin/vers/source1.md, ...]
tags: [3 à 5 tags max]
---
```

**Champs** :
- `summary` — Une ligne. Permet de répondre à une query en lisant juste les frontmatters au lieu d'ouvrir 10 pages. **Doit toujours être à jour.**
- `lifecycle` — État de qualité :
  - `draft` : je viens de l'écrire après ingest, pas encore relu par toi.
  - `reviewed` : relu par toi, contenu validé.
  - `verified` : croisé avec ≥2 sources fiables, considéré stable.
- `tags` — 3 à 5 max. Préférer "nom concret + angle" (`transformers-training` > `transformers`). **Tags interdits** : `ai`, `llm`, `agent`, `tech`, `notes`, `startup`, `interesting`, `cool`.

### Marqueurs inline d'incertitude

Au milieu du texte, marquer ce qui n'est pas tiré directement d'une source :

- `^[inferred]` — déduction de ma part à partir des sources, pas écrit explicitement.
- `^[ambiguous]` — la source dit quelque chose mais l'interprétation est incertaine.

Exemple :
```
Karpathy a quitté Tesla en 2022. Il s'intéresse particulièrement à
l'éducation autour des LLMs ^[inferred] (déduit de ses vidéos YouTube,
pas écrit dans le gist).
```

Pas de marqueur = tiré directement d'une source dans `sources:`.

### Liens bidirectionnels obligatoires

Si page A référence page B avec `[[B]]`, alors page B doit référencer A (typiquement dans une section `## Related` en bas). Le lint vérifie cette propriété.

### Section `## My take`

Toute page d'entité, source-summary ou comparison doit se terminer par une section `## My take` — *mon* avis, pas un résumé. Force la prise de notes critique au lieu de la recopie passive.

```markdown
## My take

Le pattern est élégant mais sa vraie valeur tient au fait de *forcer*
la prise de position. Sans ça, on retombe sur du résumé passif.
```

Si je n'ai pas de take pertinent, l'écrire explicitement (`Pas d'avis tranché — pages purement descriptive`) plutôt que d'omettre la section.

## Workflows

### Ingest — formes selon la nature de la source

Trois cas selon la source. Le triage humain a toujours lieu, mais à un grain différent.

**Source = unité atomique** (article, PDF, transcript, gist) — workflow direct ci-dessous.

**Source = firehose** (tweets, posts, RSS) — préalable : grouper en clusters thématiques (~150 unités), un cluster file par groupe avec `status: pending`, triage cluster-par-cluster (`kept`/`discarded`), seuls les `kept` déclenchent l'ingest dans `wiki/`.

**Source = artefact multi-facettes** (repo GitHub, livre) — préalable : décomposer en *facets* (3 à 6 angles : `purpose`, `architecture`, `key-implementation`, `comparison`, `lessons`, `concerns`…), un cluster file par facet avec `status: pending`, triage par facet, seuls les `kept` déclenchent l'ingest dans `wiki/`.

Dans les deux cas avec préalable : les cluster files vivent dans `raw/clusters/<source-type>/<source-id>/cluster-NN-<theme-ou-facet>.md`. Frontmatter type :

```yaml
---
type: tweet-cluster | repo-cluster
status: pending | kept | discarded
created: YYYY-MM-DD
---
```

Mutation autorisée dans `raw/clusters/` : uniquement le champ `status:` (et `## My take` ajouté au moment du `kept`). Le contenu du cluster reste sinon immuable.

### Ingest (workflow direct, pour toutes les sources arrivées dans `raw/`)

1. **Lire** la source dans `raw/`.
2. **Triage `should_compile`** : avant tout, te dire `yes` / `no` / `maybe` + raison en 1 ligne. Si `no`, la source reste dans `raw/` et on s'arrête. Si `maybe`, tu décides.
3. **Discuter** les takeaways avec toi avant d'écrire.
4. **Discover puis execute** :
   - D'abord lister les pages wiki existantes touchées + raison courte.
   - Puis écrire les changements (préférer `update` sur `create`).
5. Créer `wiki/sources/<slug>.md` avec frontmatter complet (`lifecycle: draft`).
6. Mettre à jour les pages d'entités/concepts touchées (toujours mettre à jour `updated:` et `summary:` si le contenu change).
7. Créer les nouvelles pages d'entités/concepts si nécessaire.
8. Maintenir les liens bidirectionnels.
9. Régénérer l'index : `python3 tools/update_index.py`.
10. Append dans `log.md` : `python3 tools/append_log.py ingest "<titre source>"`.
11. (Optionnel) `python3 tools/lint.py` pour vérifier la cohérence.

### Query

1. Lire `index.md` pour repérer les pages candidates.
2. Lire les `summary:` (frontmatter) des pages candidates pour décider lesquelles ouvrir.
3. Synthétiser, **citer les sources** et les pages wiki utilisées.
4. Si la réponse a de la valeur durable, te proposer `--crystallize` :
   > "Cette réponse pourrait devenir `wiki/comparisons/<slug>.md`. Je file ?"
   Si tu acceptes, créer la page (`lifecycle: draft`), update `index.md`, append `log.md`.
5. Append dans `log.md` : `## [YYYY-MM-DD] query | <question>`.

### Lint

1. **Liens cassés** : tout `[[X]]` doit pointer vers une page existante.
2. **Liens orphelins** : pages sans aucun lien entrant.
3. **Index drift** : entrées dans `index.md` sans page, ou pages sans entrée.
4. **Tags interdits ou hors limites** (>5, ou dans la blacklist).
5. **Forward sans reverse** : si A→B existe, vérifier B→A.
6. **Frontmatter manquant ou incomplet** (champs obligatoires).
7. **Pages `draft` depuis >14 jours** : te demander si tu veux les relire.
8. **Concepts mentionnés sans page dédiée** (heuristique : terme apparaît ≥3 fois sans `[[...]]`).

Append : `## [YYYY-MM-DD] lint | <résumé>` dans `log.md`.

## Format du log

Chaque entrée commence par `## [YYYY-MM-DD] <action> | <details>` pour rester parsable :

```
## [2026-05-07] init | Vault initialisé
## [2026-05-07] ingest | Karpathy LLM Wiki gist
## [2026-05-08] query | Comment intégrer le triage avec Obsidian Web Clipper ?
## [2026-05-08] lint | 3 liens cassés, 2 orphelins, 1 page draft à relire
```

Actions valides : `init | ingest | query | lint | crystallize | update | note`.

## Notes

- Ce schéma est vivant. Toute évolution de convention se fait par discussion avec toi, puis modification de ce fichier (et entrée dans `log.md` avec action `update`).
- Pas de génération autonome silencieuse : confirmer avant de toucher beaucoup de pages.
- Si une règle de ce schéma rentre en conflit avec une situation concrète, **demander** plutôt que d'improviser.
- **Index sub-grouping** : la structure de `wiki/` reste plate par catégorie (`wiki/agents/`, `wiki/concepts/`, `wiki/comparisons/`…) quoi qu'il arrive — un concept multi-domaines n'a pas à choisir un sous-dossier. Le groupement vit dans la vue dérivée `index.md`, pas dans le filesystem. Tant qu'une section de l'index (`## Concepts` notamment) compte ≤15 entrées, on la laisse à plat. Au-delà, patcher `tools/update_index.py` pour sub-grouper par tag dominant (ex. `### Agent reliability`, `### LLM fundamentals`). Pas de migration de fichiers nécessaire.
- **Localisation des entités dans `wiki/`** : une entité a **une seule** page wiki, dans son **dossier de domaine** (`wiki/agents/`, `wiki/tools/`, `wiki/models/`…), quel que soit le type de la source qui l'a fait naître. Les sources s'accumulent dans le champ `sources:` du frontmatter. Le snapshot d'un repo dans `raw/repos/` est une source comme une autre — il **n'impose pas** que la page wiki vive dans `wiki/repos/`. Corollaire : `wiki/repos/` n'existe plus comme dossier wiki ; il n'y a que des dossiers de domaine. (Décision révisée : remplace l'ancienne règle "page wiki pour un repo = `wiki/repos/<owner>-<repo>.md`" actée le 2026-05-09 dans `improve.md`.)

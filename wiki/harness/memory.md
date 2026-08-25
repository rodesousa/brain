---
summary: Volet mémoire du sujet harness — optimiser l'index & la mémoire d'un brain markdown-only : l'index plat suffit à petite échelle, les gains sont dans les outils de recherche + l'itération de l'agent, pas dans une DB vectorielle.
created: 2026-08-25
updated: 2026-08-25
sources:
  - sources/retrieval-memoire-synthese.md
keywords: [memoire, index, retrieval, bm25, vector, rag, progressive-summarization, dream-cycle]
---

# Memory — retrieval & mémoire d'un brain markdown-only

**TL;DR** — À petite échelle (~<300-500 pages), l'index plat est déjà le bon système. Les gains à
court terme sont des outils de recherche + l'itération de l'agent, pas une autre architecture.
Vecteur/graphe/DB = évolutions à ~1000+ pages, pas avant.

## Points clés

- **Index plat = optimal jusqu'à ~300-500 entrées.** L'index tient dans le contexte (~1-2k tokens),
  le LLM fait le fuzzy match « le truc sur X » → page. C'est le pattern `llms.txt` : petit, une
  ligne par sujet, chargé en entier.
- **Index = vue dérivée, jamais vérité parallèle.** Le markdown est la vérité ; index + recherche
  (FTS/BM25) sont reconstruisibles à tout moment (gbrain, munder-difflin, qmd).
- **La capacité d'itération bat les mécanismes de retrieval** (benchmark Letta 2025) : un agent avec
  `grep`/`search_files` sur un fichier bat les outils mémoire spécialisés (74.0 vs 68.5 sur
  LoCoMo). → règle « réécris la requête 2-3 façons avant de dire introuvable ».
- **Les mécanismes des systèmes mémoire lourds se reproduisent en markdown :**
  - Mem0 = extraction à l'ingest (pas de stockage brut) + ADD-only (rien n'est écrasé) → git history.
  - Zep/Graphiti = invalidation des faits contredits (provenance par source) → marquage `^[superseded]`.
  - MemGPT = « core memory » court en contexte (index.md/MEMORY.md) vs « archival » (les pages wiki).
  - git = mémoire temporelle : rien n'est perdu, tout est daté.
- **Progressive summarization** (Tiago Forte) : résumé en couches successives (brut → gras →
  highlight → résumé exécutif). Le `summary:` frontmatter n'est que la couche 1 ; le « résumé
  vivant » (re-compressé à chaque relecture) est la couche 2+.
- **Échelle de retrieval** : index plat → full-text (ripgrep/FTS5/`qmd search`) → hybride
  BM25+vecteur+rerank (`qmd query`) → graphe (gbrain). qmd = évolution naturelle markdown-only
  quand l'index coince (~1000+ pages).

## Application au brain (décisions D1-D5)

- Ingest = extraction distillée (Mem0-style), pas de blob brut.
- Obsidian-compatible = wikilinks + markdown (lisible dans un terminal).
- Index = vue dérivée, une ligne par sujet, mots-clés pour le fuzzy match ; `(deprecated)` sans
  suppression.
- Consolidation périodique (« dream cycle » markdown) : maj `updated:`/`summary:`, marquage
  `^[superseded]`, git commit.
- **Pas maintenant** : DB vectorielle, graphe DB, Mem0/Zep/Letta en service.

## Voir aussi

- [[munder_difflin]] — le sujet principal du dossier : munder-difflin, dont la mémoire multi-agents (hive)
  applique la même philosophie markdown-first
- [[munder-difflin-hive]] — source brute : design du hive (mémoire par agent, mailbox, blackboard)
- [[retrieval-memoire-synthese]] — source brute : la recherche complète (sources, benchmarks, chiffres)

_Source : [[retrieval-memoire-synthese]] (recherche web 2026-08-25)._

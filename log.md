# Log

Journal chronologique du wiki. Append-only.

## [2026-05-07] init | Vault initialisé selon le pattern LLM Wiki de Karpathy. Schéma dans `CLAUDE.md`, concept dans `LLM-WIKI-CONCEPT.md`. Dossiers `raw/` et `wiki/` créés.
## [2026-05-07] update | Schéma enrichi avec 8 quick wins issus de l'analyse de 5 implems communautaires (ar9av/obsidian-wiki, momhq/mom, kdsz001/OpenWiki, sametbrr/llm-wiki-manager, skyllwt/OmegaWiki) : frontmatter `summary`+`lifecycle`, marqueurs `^[inferred]`/`^[ambiguous]`, règle tags (3-5 max + blacklist), liens bidirectionnels obligatoires, triage `should_compile` à l'ingest, `## My take` dans templates, opération `--crystallize` à la query, format de log strict.
## [2026-05-07] init | Bootstrap : 2 éléments créés
## [2026-05-07] update | index.md régénéré (0 pages)
## [2026-05-07] lint | 0 erreurs, 0 warnings sur 0 pages
## [2026-05-07] note | test des scripts tools/
## [2026-05-09] note | improve.md créé — questions ouvertes en suspens : zone staging vs raw/clusters, workflow repos GitHub, fusion clusters par source
## [2026-05-09] note | Cobaye HALO — étape 2/3 : 4 cluster files créés (purpose/methodology/rlm-design/lessons), facet benchmarks-evidence écartée. Status: pending. À triager.
## [2026-05-09] update | index.md régénéré (1 pages)
## [2026-05-09] ingest | context-labs/halo — wiki/repos/context-labs-halo.md créé depuis 2 cluster files kept (purpose + methodology), 2 discardés (rlm-design + lessons)
## [2026-05-09] lint | 2 erreurs, 1 warnings sur 1 pages
## [2026-05-09] lint | 0 erreurs, 1 warnings sur 1 pages
## [2026-05-09] update | improve.md mis à jour après cobaye HALO — 5 décisions actées (zone C, snapshot A, wiki/repos+entity, fusion facets, lint cross-zones), 4 questions encore ouvertes (digest tweets, snippets repos, re-ingest, hot pending), 5 apprentissages capturés
## [2026-05-09] lint | 0 erreurs, 1 warnings sur 1 pages
## [2026-05-09] update | index.md régénéré (1 pages)
## [2026-05-13] update | Règle index sub-grouping ajoutée à CLAUDE.md — filesystem plat par catégorie, sub-grouping par tag dominant dans index.md quand une section dépasse 15 entrées (patch update_index.py, pas de migration)
## [2026-05-13] update | index.md régénéré (1 pages)
## [2026-05-13] update | Convention révisée : entités dans wiki/<domain>/ (agents/tools/...), plus dans wiki/repos/. HALO migré wiki/repos/ → wiki/tools/. CLAUDE.md + improve.md mis à jour.
## [2026-05-13] update | index.md régénéré (2 pages)
## [2026-05-13] ingest | Hermes Agent 0.13 (Tenacity) — vidéo AICodeKing → wiki/agents/hermes-agent.md (lifecycle: draft, single source, à enrichir). Liens bidirectionnels avec context-labs-halo via pattern agent-reliability.
## [2026-05-13] lint | 0 erreurs, 0 warnings sur 2 pages
## [2026-05-13] update | index.md régénéré (2 pages)
## [2026-05-13] lint | 0 erreurs, 0 warnings sur 2 pages
## [2026-05-13] update | Lint reports supprimés. tools/lint.py imprime sur stdout, plus de wiki/reports/. tools/update_index.py et _lib.py nettoyés (REPORTS constant + lint-report type retirés). wiki/reports/lint-*.md supprimés.
## [2026-05-13] update | index.md régénéré (3 pages)
## [2026-05-13] ingest | zero-native landing → wiki/tools/zero-native.md (lifecycle: draft, single source web). Premier élément domaine desktop-apps, pas de liens vers entités existantes.
## [2026-05-13] lint | 0 erreurs, 3 warnings sur 3 pages
## [2026-05-13] lint | 0 erreurs, 1 warnings sur 3 pages
## [2026-05-13] lint | 0 erreurs, 1 warning (zero-native orphelin attendu — premier élément du domaine desktop-apps)
## [2026-05-13] update | index.md régénéré (3 pages)
## [2026-05-13] ingest | vercel-labs/zero-native repo → wiki/tools/zero-native.md mis à jour (3 facets kept : architecture, security-model, mobile-embedding ; 2 discarded : purpose, examples-ecosystem). +1 source primaire (README).
## [2026-05-13] lint | 0 erreurs, 1 warnings sur 3 pages
## [2026-05-13] lint | 0 erreurs, 1 warning (zero-native toujours orphelin, attendu)

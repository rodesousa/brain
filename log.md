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
## [2026-05-13] update | index.md régénéré (4 pages)
## [2026-05-13] ingest | alloy-ex/alloy → wiki/agents/alloy.md (lifecycle: draft, source primaire README, 5 facets kept : purpose-design-boundary, architecture, provider-system, memory-primitive, operational-surface ; 1 discarded : quickstart-and-tables). Liens bidirectionnels avec hermes-agent (philosophies opposées) et context-labs-halo (telemetry compatible).
## [2026-05-13] lint | 0 erreurs, 1 warnings sur 4 pages
## [2026-05-13] lint | 0 erreurs, 1 warning (zero-native toujours orphelin, attendu — alloy correctement linké aux 2 entités existantes)
## [2026-05-13] update | index.md régénéré (5 pages)
## [2026-05-13] ingest | tauri-apps/tauri → wiki/tools/tauri.md (lifecycle: draft, source primaire README, 5 facets kept : purpose-positioning, architecture-stack, bundler-distribution, platforms-coverage, security-webview-protocol ; 1 discarded : governance-licensing). Liens bidirectionnels avec zero-native (challenger direct, tableau comparatif dans My take Tauri).
## [2026-05-13] lint | 0 erreurs, 0 warnings sur 5 pages
## [2026-05-13] lint | 0 erreurs, 0 warnings sur 5 pages — vault entièrement propre, plus d'orphelin (zero-native ↔ tauri résout le warning)
## [2026-05-17] update | index.md régénéré (5 pages)
## [2026-05-17] ingest | Hermes Agent — doc officielle API server
## [2026-05-17] lint | 0 erreurs, 0 warnings sur 5 pages
## [2026-05-18] update | index.md régénéré (5 pages)
## [2026-05-18] ingest | Hermes Agent — docs tips + SOUL.md
## [2026-05-18] lint | 0 erreurs, 0 warnings sur 5 pages
## [2026-05-18] update | index.md régénéré (5 pages)
## [2026-05-18] ingest | Hermes Agent — docs skills + webhook + cron-PR + telegram
## [2026-05-18] lint | 0 erreurs, 0 warnings sur 5 pages
## [2026-05-22] update | index.md régénéré (32 pages)
## [2026-05-22] ingest | LLMs 101: A Practical Guide (2026 Edition) — 22 pages dans wiki/llm_101/
## [2026-05-22] update | ajout dossier projet/ dans Structure de CLAUDE.md (format à préciser lors du premier projet)
## [2026-05-22] update | index.md régénéré (34 pages)
## [2026-05-22] ingest | Karpathy CLAUDE.md viral thread (X @0xDepressionn)
## [2026-05-22] lint | 6 erreurs, 97 warnings sur 34 pages
## [2026-05-22] update | index.md régénéré (36 pages)
## [2026-05-22] ingest | 12 Claude tips (KingWilliamDefi) — extrait 3 prompts utiles dans wiki/prompts/claude-power-prompts.md
## [2026-05-22] update | index.md régénéré (41 pages)
## [2026-05-22] update | lifecycle reviewed pour claude-md-pattern + karpathy-claude-md-viral-thread
## [2026-05-22] update | index.md régénéré (43 pages)
## [2026-05-22] update | 6 pages passées de draft à reviewed (sglang, vllm, memory-bandwidth, 3× ahmad-osman sources)
## [2026-05-22] update | index.md régénéré (43 pages)
## [2026-05-22] lint | 4 erreurs, 120 warnings sur 43 pages
## [2026-05-22] lint | 4 erreurs, 100 warnings sur 43 pages
## [2026-05-22] lint | 4 erreurs, 99 warnings sur 43 pages
## [2026-05-22] ingest | Ahmad Osman trilogie — Part 1 GPU Memory Math (2026)
## [2026-05-22] ingest | Ahmad Osman trilogie — Part 2 Memory Bandwidth (2026)
## [2026-05-22] ingest | Ahmad Osman trilogie — Part 3 Inference Engines (2026)
## [2026-05-22] update | index.md régénéré (43 pages)
## [2026-05-22] update | index.md régénéré (52 pages)
## [2026-05-22] lint | 4 erreurs, 161 warnings sur 52 pages
## [2026-05-22] update | index.md régénéré (52 pages)
## [2026-05-22] lint | 4 erreurs, 109 warnings sur 52 pages
## [2026-05-22] lint | 4 erreurs, 99 warnings sur 52 pages
## [2026-05-22] update | Phase 2 — 6 engines secondaires (mlx, exllamav2/v3, nvidia-dynamo, ollama, mlc-llm) + 3 concepts engine (paged-attention, continuous-batching, inference-bottlenecks)
## [2026-05-22] update | index.md régénéré (52 pages)
## [2026-05-22] lint | 4 erreurs, 99 warnings sur 52 pages
## [2026-06-26] update | index.md régénéré (54 pages)
## [2026-06-26] ingest | ofox.ai — How to Run GLM-5.2 Locally with GGUF (2026)
## [2026-06-26] lint | 4 erreurs, 115 warnings sur 54 pages
## [2026-06-26] lint | 4 erreurs, 111 warnings sur 54 pages
## [2026-08-25] update | refonte.md — D2 (Obsidian-compatible) + D3 (dossier par sujet, 1 fichier par défaut, deprecated dans l'index) tranchées + section 5 (recherche index & mémoire)
## [2026-08-25] update | Feuille blanche exécutée — wiki/, raw/, index/hot/improve/Clippings déplacés dans legacy/ (git mv, non destructif). Nouveau index.md. CLAUDE.md marqué EN REFONTE.

## [2026-08-25] update | tools/ déplacé dans legacy/ — log maintenu à la main (plus de tools/append_log.py), CLAUDE.md + refonte.md mis à jour

## [2026-08-25] update | D5 tranchée — capture par geste de chat (ingest url/chemin/texte collé), digest dans wiki/<sujet>/<sujet>.md, texte brut dans wiki/<sujet>/sources/<slug>.md (source >150 mots seulement), index ne liste que les sujets

## [2026-08-25] ingest | Premier sujet du nouveau schéma — retrieval-memoire (digest + source within), index.md mis à jour

## [2026-08-25] update | index.md réécrit comme carte du harness (préambule agent + mots-clés par ligne), CLAUDE.md mis à jour

## [2026-08-25] update | CLAUDE.md réécrit pour le schéma acté (D1-D5) — démarrage de session, frontmatter digest, ingest, query, lint provisoire. refonte.md statut mis à jour (implémenté + testé)

## [2026-08-25] ingest | Munder Difflin → sujet harness (digest + 2 sources), index.md mis à jour

## [2026-08-25] update | CLAUDE.md renommé AGENTS.md (portable multi-agents). Sujet harness restructuré : 1 dossier wiki/harness/ avec munder_difflin.md (sujet) + memory.md (volet mémoire) + sources/. retrieval-memoire fusionné dans le dossier harness.

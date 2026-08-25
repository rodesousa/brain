---
type: concept
summary: Eval set 30-100 prompts sur le stack réel. Mesurer quality, latency, memory, formatting, retrieval, operations. Ne pas laisser un leaderboard choisir ton stack.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - eval-methodology
  - runbook
---

> *Benchmark the stack you will actually run. A model's BF16 leaderboard score is not your Q4 local reality.*

## Les 6 dimensions à mesurer

### Quality

Correctness sur **tes tâches réelles**, pas seulement des benchmarks génériques (HumanEval, MMLU, etc.). Inclure :
- Tes prompts typiques
- Tes cas limite
- Tes outputs avec vérification

### Latency

- **Time-to-first-token (TTFT)** — sensation de réactivité, dépend du [[prefill-vs-decode|prefill]]
- **Decode TPS** — sensation de fluidité de streaming
- **End-to-end time** — TTFT + decode pour une réponse complète

### Memory

- Weight memory loaded
- [[kv-cache]] growth pendant l'inférence
- Peak VRAM observé
- Headroom sous charge réelle

### Formatting

- [[chat-template]] correctness — sortie cohérente avec le format attendu
- JSON / schema success rate quand applicable
- Tool-call reliability
- Stop-token behavior (le modèle s'arrête au bon moment)

### Retrieval

Si [[rag-pipeline]] :
- Citation faithfulness (le modèle cite ce qu'il a reçu)
- Answer grounding
- Missing-evidence behavior (que fait le modèle quand l'évidence n'est pas dans les chunks)
- Reranker impact (avec vs sans)

### Operations

- Startup time
- Warmup behavior
- Crash recovery
- Logging adequacy
- Privacy
- Version tracking

## Composer l'eval set

**30 à 100 prompts représentatifs**, avec :
- Expected answers ou critères de scoring
- Latency et memory measurements
- Failure categories
- RAG-specific grounding checks (si applicable)
- JSON compliance checks (si applicable)
- Human review pour les tâches ambiguës

## Le piège des leaderboards

> *Do not let a leaderboard choose your local stack for you.*

Les leaderboards publics :
- Sont en BF16 ou FP16, pas ta quantization
- Sont sur des benchmarks génériques, pas ton workload
- Ne capturent pas les bugs format / template / decoding
- Ne mesurent pas ce qui matters chez toi

Utiles pour **discovery** (par où commencer). Pas pour **decision**.

## Quand ré-évaluer

- Nouveau modèle dans la même classe
- Changement de runtime ou version
- Changement de quantization
- Nouveau type de tâche dans le workload réel
- Régulièrement (1× par mois) pour catch les drifts

## Related

- [[local-llm-runbook]] — étape 3, evaluate avant de trust
- [[rag-pipeline]] — évaluation RAG-specific
- [[llm-failure-modes]] — quoi mesurer pour débugger
- [[local-llm-growth-path]] — l'eval set devient critique à intermediate

## My take

La discipline qui sépare les setups locaux qui marchent de ceux qui frustrent. Garder un eval set petit mais représentatif, et passer **chaque nouveau modèle** dessus avant de migrer, transforme la conversation "ce nouveau modèle est-il mieux ?" d'une opinion en une mesure.

---
type: concept
summary: Checklist debug pour LLM local — OOM, gibberish, slow first token, slow streaming, bad documents, bad JSON, repeating loops. Les "boring checks" résolvent plus que de changer de modèle.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - failure-modes
  - runbook
  - llm-troubleshooting
---

La plupart des échecs LLM locaux ne sont pas mystérieux. Ils viennent presque toujours de **memory fit, formatting, runtime support, decoding settings, ou retrieval quality**.

## Checklist par symptôme

### Out of memory

**Cause** : weights, [[kv-cache]], runtime overhead, ou batch ne fit pas.

**Fixes** : modèle plus petit, réduire context, lower batch/concurrency, meilleure [[quantization-llm]], plus de [[vram-math#headroom|headroom]].

### Gibberish ou role confusion

**Cause** : [[chat-template]] / [[tokenizer]] / BOS-EOS / reasoning-mode switch / tool schema wrong.

**Fixes** : vérifier le model card AVANT de blâmer le modèle. Utiliser `apply_chat_template`.

### Slow first token

**Cause** : prefill expensive ([[prefill-vs-decode]]).

**Fixes** : raccourcir le prompt, **prefix caching** (réutiliser le KV cache d'une partie commune), améliorer le [[rag-pipeline]] (moins de chunks inutiles), réduire context, runtime plus rapide.

### Slow streaming

**Cause** : decode bottleneck ([[prefill-vs-decode]]).

**Fixes** : vérifier memory bandwidth, [[quantization-llm]] (weights plus petits = moins de bytes à stream), **CPU spill** (catastrophique — un seul layer offloadé peut tuer la perf), attention backend, [[speculative-decoding]], modèle trop gros pour le hardware.

### Bad document answers

**Cause** : 9 fois sur 10, c'est le **retrieval** qui a failed, pas le LLM.

**Fixes** : inspecter parsed text, chunk boundaries, metadata, top-k retrieval, reranking, citation grounding. Voir [[rag-pipeline]].

### Bad JSON ou tool calls

**Cause** : decoding trop permissif, modèle pas tool-tuned.

**Fixes** : lower temperature, constrained decoding ([[decoding-policies]]), schemas stricts, examples plus parlants, modèle tool-tuned ([[model-types-llm]]).

### Repeating loops

**Cause** : decoding ou template.

**Fixes** : réduire temperature/top-p, ajouter repetition penalties, vérifier stop tokens, vérifier que le template ne fait pas voir au modèle son propre output comme nouveau prompt.

## Le principe transverse

> *Start with the boring checks. They fix more problems than model swapping does.*

L'ordre de debug recommandé :
1. Memory fit
2. Chat template
3. Decoding settings
4. Runtime support / version
5. Retrieval / RAG
6. *Enfin* changement de modèle

## Related

- [[local-llm-runbook]] — checklist générale, prévention
- [[chat-template]] — la cause #1 sous-estimée
- [[kv-cache]] — explique beaucoup d'OOM
- [[rag-pipeline]] — explique 90% des "bad document answers"

## My take

À garder ouvert comme une cheat sheet. La discipline de **toujours vérifier le template avant de blâmer le modèle** sauve des heures. C'est l'inverse du réflexe naturel (qui est de switcher de modèle au moindre problème).

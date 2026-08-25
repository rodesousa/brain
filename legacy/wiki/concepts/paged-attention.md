---
type: concept
summary: Technique de management du KV cache qui partitionne en blocs (pages) — supporte des batches plus grands sans fragmentation mémoire. Signature de vLLM, généralisée depuis.
lifecycle: draft
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - paged-attention
  - kv-cache
  - inference-engines
---

**PagedAttention** est la technique qui résout la **fragmentation du [[kv-cache]]** en le partitionnant en blocs (pages) de taille fixe, à la manière de la mémoire virtuelle d'un OS.

## Le problème : fragmentation du KV cache

Avant PagedAttention, le KV cache était alloué en blocs contigus de taille `max_context_length`. Conséquences :

- **Waste massif** quand une requête utilise 4K tokens d'un budget alloué pour 32K
- **Impossible** de servir efficacement des requêtes de tailles très variables en parallèle
- **OOM** dès que la fragmentation cumulée dépasse le budget total

## La solution : pages

Le KV cache est découpé en **blocs (pages) de taille fixe** — typiquement quelques tokens par bloc. Chaque requête se voit allouer des pages **au fur et à mesure** que son context grandit.

Conséquences :
- **Utilisation mémoire proche du theoretical optimum** — pas de waste sur les contexts courts
- **Batches plus grands** possibles dans le même budget VRAM
- **Sharing des pages** possible — prefix caching réutilise les pages d'un prefix commun entre requêtes

## Origine et adoption

- **Introduite par [[vllm]]** ([Kwon et al., paper original](https://arxiv.org/abs/2309.06180))
- **Généralisée** depuis : [[sglang]] (RadixAttention bâti dessus), [[tensorrt-llm]] (variante NVIDIA), [[exllamav2]] (paged attention dans son design), [[llama-cpp]] (support partiel)

## Quand ça brille

- **Serving multi-user** avec tailles de requêtes variables
- **Long context** où la fragmentation classique devient catastrophique
- **Prefix caching** — pages partagées entre requêtes qui ouvrent le même prompt système

## Quand ça compte moins

- **Single user, context fixe** — la fragmentation classique n'a pas le temps d'apparaître
- **Petits modèles avec petite KV cache** — l'overhead du paging vs le gain est marginal

## Note : "à scale, non optionnel"

> Ahmad : PagedAttention, prefix caching, KV quantization et disaggregation sont **non optionnels à scale**.

## Related

- [[kv-cache]] — le sujet attaqué
- [[vllm]] — l'engine qui a introduit la technique
- [[sglang]] — RadixAttention est une extension prefix-aware
- [[tensorrt-llm]] — variante NVIDIA
- [[exllamav2]] — paged attention dans son design
- [[llama-cpp]] — support partiel
- [[continuous-batching]] — souvent combinée avec PagedAttention
- [[inference-bottlenecks]] — KV cache management est un des 5 bottlenecks
- [[llm-runtimes]] — comparaison engines, technique mentionnée
- [[ahmad-osman-inference-engines-2026]] — source principale

## My take

L'**innovation système** qui a fait passer le serving LLM de "demo" à "production" en 2023-2024. Conceptuellement, c'est la traduction de la **memory virtuelle des OS** au domaine du KV cache LLM — et comme la memory virtuelle, c'est tellement évident une fois nommé qu'on a du mal à croire que ce n'était pas là avant. À internaliser comme "la base" du serving moderne ; si ton engine ne le fait pas, il n'est pas production-grade.

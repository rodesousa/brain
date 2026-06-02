---
type: concept
summary: Budget mémoire pour faire tourner un LLM local — weights + KV cache + runtime overhead + extras. Formule VRAM ≈ B × (bits/8), headroom, et le piège des contexts longs.
lifecycle: verified
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
  - raw/web/gpu-memory-math-for-llms-2026.md
tags:
  - vram-math
  - local-llm-deployment
  - kv-cache
  - quantization
---

Trois consommateurs principaux de VRAM, plus des extras à ne pas oublier.

## Formule de base

```
total_memory = quantized_weights
             + KV_cache_for_context
             + runtime_overhead
             + batch_or_concurrency_overhead
             + safety_margin
```

## 1. Weights

```
weight_memory ≈ parameters × bytes_per_parameter
```

Approximations selon [[quantization-llm]] :
- FP16 / BF16 → 2 B/param
- Q8 → 1 B/param
- Q4 → ~0.5 B/param + format overhead

## 2. KV cache

Voir [[kv-cache]]. Grossit avec le context length actif. Rule of thumb Llama-7B MHA FP16 : ~0.5 MiB/token. Avec GQA ou KV quantization FP8, divise par 2 à 8.

## 3. Runtime overhead

Buffers framework, CUDA workspace, fragmentation mémoire, tenseurs temporaires. Pas négligeable — peut représenter plusieurs GiB pour les gros runtimes serveur (vLLM, TensorRT-LLM).

## 4. Extras à ne pas oublier

- **Batch / concurrency** — chaque requête concurrente a son propre KV cache
- **Vision encoder** — images deviennent des tokens et l'encoder lui-même prend de la VRAM ([[multimodal-token-budget]])
- **Speculative decoding** — drafter models, draft heads, structures de vérification
- **LoRA adapters** — petits mais réels

## MoE wrinkle

Un MoE peut activer seulement une fraction des params par token, mais **les experts inactifs vivent quand même en mémoire**. Le compute scale avec les active params, le loading et la capacity avec le total params.

## Le piège classique

> Un 13B en Q4 peut **fit à 8K context et crasher à 32K** — les weights n'ont pas bougé, le [[kv-cache]] a quadruplé.

Tester avec **le context length que tu utilises réellement**, pas avec un prompt vide.

## Headroom

**Garder 10-20% libre.** Tourner à 99% VRAM = OOM imminent + fragmentation. Le système d'exploitation et le framework ont besoin d'espace de manœuvre.

## Gate pratique pour choisir un modèle

```
weights + KV_cache + runtime_overhead ≤ 80-90% de la VRAM disponible
```

Sinon CPU offload, qui pour rappel = **acceptable pour expérimenter, jamais pour la perf** (le decode collapse).

## Related

- [[quantization-llm]] — premier levier pour réduire les weights
- [[kv-cache]] — détermine la part dynamique
- [[memory-bandwidth]] — la VRAM ne fait pas tout, sa bandwidth non plus
- [[local-llm-runbook]] — étape "estimate the full memory bill"
- [[ahmad-osman-gpu-memory-math-2026]] — la formule + tableaux par-GPU et par-modèle
- [[ahmad-osman-memory-bandwidth-2026]] — la dimension complémentaire (bandwidth)

## My take

La formule à internaliser avant de toute discussion hardware. La conversation "j'ai 24 GB, ça suffit pour quoi ?" n'a aucun sens sans préciser le context length cible et le batch size. Toujours raisonner en budget complet, pas en "ça tient en VRAM idle".

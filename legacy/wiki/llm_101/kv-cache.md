---
type: concept
summary: Working memory de l'inférence LLM — stocke les states key/value des tokens précédents pour éviter de recomputer la séquence à chaque nouveau token généré.
lifecycle: verified
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
tags:
  - kv-cache
  - inference-mechanics
  - vram-math
  - attention-variants
---

Le **KV cache** stocke les states key/value de l'attention pour tous les tokens déjà vus. Sans lui, chaque nouveau token forcerait à recomputer l'attention sur toute la séquence — inutilisable en pratique. Avec lui, la génération est rapide mais paie un prix mémoire qui grandit linéairement avec la longueur du contexte.

## Formule de coût

```
KV_cache ≈ tokens × layers × kv_heads × head_dim × precision × 2
```

Le `× 2` couvre keys et values.

**Rule of thumb** Llama-7B MHA FP16 : ~0.5 MiB par token.
- 4K tokens → ~2 GiB
- 32K tokens → ~16 GiB (le KV cache seul, sans les weights)

C'est pourquoi un modèle 13B Q4 peut fit à 8K context et **crasher à 32K** : les weights n'ont pas bougé, le KV cache a quadruplé.

## Réduire le coût

- **Architecture** : [[attention-variants]] (GQA, MQA) divisent par 4-8 les kv_heads vs MHA classique. C'est la principale leviér.
- **Quantization KV** : FP8 ou INT8 sont des floors pratiques en 2026. Sub-8-bit (KIVI, KVQuant) reste research-heavy — à benchmarker durement avant prod, surtout sur coding, tool calls, JSON, long-context retrieval.
- **Algorithmes serving** : PagedAttention ([[vllm]]) partitionne le KV cache en blocs et limite le waste mémoire. RadixAttention ([[sglang]]) optimise le prefix caching multi-tour. Prefill-decode disaggregation ([[sglang]], [[tensorrt-llm]]) sépare les phases pour scheduling fin.

## À ne pas confondre

KV-cache quantization ≠ weight quantization ([[quantization-llm]]). L'une compresse les weights statiques, l'autre compresse la mémoire de travail dynamique.

KV-cache compression ≠ speculative decoding ([[decoding-policies]]). La spéculative attaque la latency de decode, pas la mémoire KV.

## Related

- [[attention-variants]] — détermine combien de kv_heads, donc le KV cache size
- [[prefill-vs-decode]] — le KV cache se construit pendant prefill, se relit pendant decode
- [[vram-math]] — KV cache est un des 3 consommateurs principaux de VRAM
- [[quantization-llm]] — KV quantization comme axe distinct de weight quantization
- [[long-context-tradeoffs]] — KV cache est le coût principal du long context
- [[memory-bandwidth]] — decode stream weights ET KV cache
- [[llm-runtimes]] — les engines diffèrent dans leur traitement du KV cache
- [[paged-attention]] — la technique fondamentale de management
- [[continuous-batching]] — chaque requête active a son KV
- [[inference-bottlenecks]] — KV cache growth est bottleneck #2
- [[vllm]] — PagedAttention native
- [[sglang]] — RadixAttention + disaggregation
- [[tensorrt-llm]] — KV cache management NVIDIA-optimisé
- [[exllamav2]] — paged attention + KV dedup
- [[nvidia-dynamo]] — multi-tier KV caching au niveau fleet
- [[ahmad-osman-gpu-memory-math-2026]] — la formule de cost du KV cache
- [[ahmad-osman-memory-bandwidth-2026]] — KV cache stream pendant decode
- [[ahmad-osman-inference-engines-2026]] — le traitement du KV cache au niveau engine

## My take

Le concept-clé qui débloque toute la compréhension du local LLM. Une fois que tu sais que le KV cache grandit linéairement avec les tokens, tout le reste (pourquoi 13B fit à 8K mais pas 32K, pourquoi GQA matters, pourquoi long context n'est pas gratuit) devient déductible. Page à garder concise — c'est une référence à pointer, pas un essai.

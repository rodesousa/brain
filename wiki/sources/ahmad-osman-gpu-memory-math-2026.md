---
type: source-summary
summary: Part 1 trilogie Ahmad Osman — la formule VRAM ≈ B × (bits/8), tableaux par-GPU et par-modèle, MoE trap, et limites runtime-specific de GGUF.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/web/gpu-memory-math-for-llms-2026.md
tags:
  - vram-math
  - quantization
  - local-llm-deployment
---

Premier volet de la trilogie d'Ahmad Osman (avril-mai 2026) sur le self-hosting de LLMs. Couvre la **couche capacité** : combien de VRAM faut-il, et pourquoi la math est plus simple qu'elle en a l'air une fois qu'on accepte une seule formule.

## La formule centrale

```
VRAM (GB) ≈ Parameters (B) × (effective bits per weight ÷ 8)
```

Trois points d'ancrage à mémoriser :
- FP16 / BF16 → **~2 GB par 1B params**
- FP8 / INT8 → **~1 GB par 1B params**
- 4-bit quants → **~0.5 GB par 1B params**

Les variantes GGUF (Q-K) se classent entre les deux :

| Format | GB / 1B params |
|---|---|
| Q6_K | ~0.82 |
| Q5_K | ~0.69 |
| Q4_K | ~0.56 |
| Q3_K | ~0.43 |
| Q2_K | ~0.33 |

Voir [[quantization-llm]] pour le détail des trade-offs qualité.

## Ce qui rentre, en pratique

Tableaux croisés modèle ↔ GPU :

| Model | FP16 | FP8 | 4-bit |
|---|---|---|---|
| 7B | ~14 GB | ~7 GB | ~3.5-4 GB |
| 13B | ~26 GB | ~13 GB | ~6-7 GB |
| 70B | ~140 GB | ~70 GB | ~35-40 GB |
| 405B | ~810 GB | ~405 GB | ~200+ GB |

Et l'inverse, par GPU (côté capacité only, pas debit — voir [[memory-bandwidth]]) :

| VRAM | FP16 | FP8 | 4-bit |
|---|---|---|---|
| 8 GB | ~3B | ~6-7B | ~12-13B |
| 16 GB | ~7B | ~13B | ~25B |
| 24 GB | ~10-12B | ~20B | ~35-40B |
| 48 GB | ~20-24B | ~40B | ~70-80B |
| 80 GB | ~35-40B | ~70B | ~140B-class |

## La VRAM tax

Les weights ne sont qu'une partie. Le reste, intégré dans [[vram-math]] :
- **KV cache** ([[kv-cache]]) — explose en long context
- **Activations** — varient par runtime
- **Batching / concurrency** — multiplie vite
- **Framework overhead** (Transformers, vLLM, TensorRT-LLM, llama.cpp)
- **CUDA graphs** — trade extra reserved memory contre latency stability

> Rule of thumb : +10-30% de headroom au-dessus du budget weights+cache.

## Le MoE trap

> "8x7B" sonne comme 56B mais seul un subset d'experts run par token.

→ **Total params = mémoire**, **active params = vitesse**. Confondre les deux = surestimer ou sous-estimer drastiquement. Selon le loader : tous les experts peuvent vivre en VRAM, ou être shardés sur plusieurs GPUs.

## GGUF n'est pas magique

Le format est optimisé pour [[llama-cpp]] — CPU+GPU hybrid, ultra-efficient memory. Mais **ces chiffres ne tiennent que dans ce runtime**. Sortir vers vLLM, TensorRT-LLM ou autre = weights potentiellement dequantizés à la volée, mémoire qui explose. "It fits in 6 GB" est une vérité **runtime-specific**, pas universelle.

## Le mental model final

Pas de matrice de compatibilité à mémoriser. Une seule équation :

```
VRAM ≈ B × (bits ÷ 8) + runtime overhead + KV cache + concurrency
```

Et le shift de question : pas "*can I run this?*" mais "*how do I want to run this?*"

## Related

- [[vram-math]] — concept du wiki, cette source en affine les tableaux et la formule
- [[quantization-llm]] — détail des Q-K et bits-per-weight effectifs
- [[kv-cache]] — la part dynamique de la formule
- [[memory-bandwidth]] — la suite logique (Part 2), capacity ≠ speed
- [[file-formats-llm]] — GGUF est runtime-specific
- [[llama-cpp]] — le runtime natif GGUF où ces chiffres tiennent
- [[ahmad-osman-memory-bandwidth-2026]] — Part 2 de la même série
- [[ahmad-osman-inference-engines-2026]] — Part 3 de la même série

## My take

Le formalisme `VRAM ≈ B × (bits/8)` est plus utile que les benchmarks GPU-spécifiques parce qu'il **se calcule de tête**. La valeur ajoutée vs `wiki/llm_101/vram-math.md` existant tient surtout aux **tableaux par-GPU** : ils transforment la math en action ("avec mes 24 GB, qu'est-ce qui rentre ?"). Le MoE trap et le caveat GGUF runtime-specific sont les deux pièges les plus souvent négligés dans la communauté local-LLM. À combiner systématiquement avec la Part 2 — sans bandwidth, la capacité ne te dit pas si la machine "respire" ou "décode dans du ciment mouillé".

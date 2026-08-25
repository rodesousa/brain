---
type: concept
summary: Réduction de la précision numérique des weights pour économiser mémoire et bandwidth. FP16 → Q4 = sweet spot consumer 2026. Sub-3-bit dégrade math, code, JSON.
lifecycle: verified
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
  - raw/web/gpu-memory-math-for-llms-2026.md
tags:
  - quantization
  - vram-math
  - inference-mechanics
---

La **quantization** stocke les weights en précision réduite pour réduire la mémoire et parfois améliorer le throughput.

## Rules of thumb 2026

| Format | Bytes/param | GB/1B params | Qualité | Quand |
|---|---|---|---|---|
| **FP16 / BF16** | 2 | ~2 | Baseline | Eval, abondance de VRAM |
| **Q8 / INT8** | 1 | ~1 | Quasi-lossless | VRAM dispo, qualité max |
| **Q6_K** | ~0.82 | ~0.82 | Excellente | Compromis fort |
| **Q5_K** | ~0.69 | ~0.69 | Excellente | Compromis fort |
| **Q4_K** | ~0.56 | ~0.56 | Bonne | **Sweet spot consumer** pour chat et docs |
| **Q3_K** | ~0.43 | ~0.43 | Dégradée | Seulement si tu dois fit un plus gros modèle |
| **Q2_K** | ~0.33 | ~0.33 | Très dégradée | Last resort |

> Formule de référence : **VRAM ≈ B params × (effective bits per weight ÷ 8)**, voir [[vram-math]].

## Ce qui dégrade en premier

Quand la quant devient agressive, les premières capacités à céder :
- Math et arithmetic
- Multi-step reasoning
- Code correctness
- Tool use reliability
- JSON / schema adherence
- Subtle instruction following
- Long-context retrieval

Si ton use case touche un de ces axes → benchmark dur avant de descendre sous Q5.

## Principe sous-estimé

> **Un plus petit modèle à haute précision peut battre un plus gros écrasé en trop peu de bits.**

Exemple typique : 7B Q6 > 13B Q2 sur reasoning, en moins de mémoire et plus vite.

→ Ne pas worship le parameter count.

## Quantization weights ≠ quantization KV cache

- **Weight quantization** — compresse les weights statiques. Sujet de cette page.
- **KV-cache quantization** — compresse la mémoire de travail dynamique. Voir [[kv-cache]]. Floor pratique 2026 = FP8/INT8. Sub-8-bit (KIVI, KVQuant) reste research.

Ne pas confondre les deux. Ce sont des leviers orthogonaux.

## Related

- [[vram-math]] — comment la quantization rentre dans le budget total
- [[kv-cache]] — KV quantization comme axe distinct
- [[file-formats-llm]] — GGUF/EXL2/GPTQ/AWQ implémentent différents schémas
- [[memory-bandwidth]] — weights plus petits = moins de bytes à stream = decode plus rapide
- [[vllm]] — quant FP8/MXFP/NVFP/INT/GPTQ/AWQ/GGUF supportée
- [[tensorrt-llm]] — FP8/FP4 sont les leviers natifs NVIDIA
- [[llama-cpp]] — GGUF Q-K natif
- [[mlx]] — quant native sur Apple Silicon
- [[exllamav2]] — EXL2 quant
- [[exllamav3]] — EXL3 quant (QTIP-based)
- [[ahmad-osman-gpu-memory-math-2026]] — tableau détaillé des bits-per-weight effectifs Q-K
- [[glm]] — cas d'école : 753B impossible sans quant 2-bit/4-bit
- [[ofox-glm-5-2-local-2026]] — tailles de quant concrètes GLM-5.2 (2-bit ~240 GB, 4-bit ~376–475 GB)

## My take

Le levier le plus accessible pour faire fit un modèle. Q4 par défaut, descendre seulement avec mesure. Le piège classique : prendre Q2 d'un 13B pour "avoir le plus gros possible" alors qu'un Q5 d'un 7B fait mieux en pratique. Mesurer sur ses prompts réels, pas sur les benchmarks publics.

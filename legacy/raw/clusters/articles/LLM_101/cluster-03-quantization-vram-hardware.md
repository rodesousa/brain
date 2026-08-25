---
type: article-cluster
status: kept
created: 2026-05-22
source: raw/tweet/llms-101-practical-guide-2026.md
---

# Facet 3 — Quantization, VRAM math & hardware

Le côté **"can I run this?"** : combien de mémoire pour les weights + KV cache + overhead, quelle quantization sans casser la qualité, quel GPU pour quelle classe de modèle, et pourquoi memory bandwidth domine la decode speed.

## Sections couvertes

- *What Local Really Means* — l'équation `Local LLM success = model fit + correct prompt format + good runtime + realistic evals`
- *Quantization* — FP16/BF16 → Q8 → Q6/Q5 → Q4 (sweet spot) → Q3/Q2 (research-only)
- *File Formats And Load Safety* — safetensors (safe) vs .bin pickle (RCE risk), GGUF (llama.cpp), ONNX, TensorRT-LLM, EXL2/GPTQ/AWQ
- *VRAM Math For Local Models* — 3 consommateurs (weights, KV cache, runtime overhead) + extras (batch, vision encoder, speculative drafts, LoRA adapters)
- *Hardware Tiers In Practice* — 16 GB minimum, 24 GB best value, 48 GB+ pour le vrai local
- *Choose A Model That Fits* — "smallest model that wins your real workload on your hardware"
- *What Controls Speed* — memory bandwidth, GPU FLOPs, VRAM capacity, attention kernels, quantization, batch size, prompt length

## Claims-clés

- Weight memory ≈ `parameters × bytes_per_parameter` : FP16 = 2 B/param, Q8 = 1 B/param, Q4 ≈ 0.5 B/param
- Total = `quantized_weights + KV_cache_for_context + runtime_overhead + batch_overhead + safety_margin`
- **Garder 10-20% de headroom** — tourner à 99% VRAM = OOM + fragmentation
- Quantization échoue d'abord sur : math, multi-step reasoning, code correctness, tool use, JSON adherence, long-context retrieval
- 7B Q6 peut battre 13B Q2 sur reasoning, en moins de mémoire et plus vite — *"do not worship parameter count"*
- safetensors > .bin pickle (pickle = arbitrary code exec à load) — *"do not let a stranger's model file become a stranger's code execution"*
- GGUF ↔ llama.cpp ; safetensors ↔ vLLM/SGLang/Transformers ; TensorRT-LLM ↔ ONNX/optimized engines — la runtime contraint le format
- MoE : active params ≠ total params (compute vs loading). Experts inactifs vivent quand même en mémoire.
- 13B Q4 fit à 8K, crash à 32K — c'est le KV cache qui a quadruplé, pas les weights
- Decode = memory-bandwidth-bound (lire les weights à chaque token), prefill = compute-bound (traiter en parallèle)
- CPU offload = OK pour expérimenter, *jamais* pour la perf — token speed collapse

## Concepts qui pourraient devenir des pages wiki

- `wiki/llm_101/quantization-llm.md` (FP16 / Q8 / Q6 / Q5 / Q4 / Q3 / Q2)
- `wiki/llm_101/vram-math.md` (formule complète, MoE wrinkle)
- `wiki/llm_101/safetensors-vs-pickle.md` (sécurité load)
- `wiki/llm_101/file-formats-llm.md` (GGUF / EXL2 / GPTQ / AWQ / ONNX / safetensors)
- `wiki/llm_101/memory-bandwidth-decode.md` (pourquoi decode est bw-bound)

## My take

(à compléter au moment du `kept`)

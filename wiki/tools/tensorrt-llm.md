---
type: entity
summary: Stack NVIDIA-max-performance pour serving LLM — Python+C++ runtimes, kernels custom attention/GEMM/MoE, FP8/FP4, Wide Expert Parallelism, intégré à Triton et Dynamo. Trade portabilité contre perf.
lifecycle: draft
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - inference-engines
  - llm-runtimes
  - production-serving
---

**TensorRT-LLM** est l'engine de serving LLM optimisé NVIDIA. Spécialisé, puissant, **pas portable** — tu trades portabilité contre performance.

## Sweet spot

- Datacenter **NVIDIA-only**
- Fleets H100 / H200 / B200 / GB200 / GB300
- Déploiement FP8 / FP4
- Multi-node serving
- MoE à scale

## Workflow

Tu construis des **TensorRT engines** depuis un checkpoint via une Python API, puis tu sers via runtime Python ou C++. La construction des engines coûte du temps et de la mémoire GPU, mais une fois faite, le throughput est excellent.

## Features clés

- Kernels custom pour attention, GEMMs, MoE
- **Prefill-decode disaggregation**
- **Wide Expert Parallelism** (MoE)
- **Speculative decoding** — voir [[speculative-decoding]]
- High-level Python API intégrée à **NVIDIA Dynamo** et **Triton Inference Server**

## Quantization native

- **H100 et plus** : FP8 quant — peut **doubler les perf et halver la mémoire** vs 16-bit avec une perte de précision minimale (voir [[quantization-llm]])
- **B200 et plus** : **FP4 weights** avec kernels optimisés

## Où c'est awkward

- **AMD, Apple, Intel portability** → impossible
- **Modèles expérimentaux qui changent vite** → la conversion engine prend du temps, retarder le support
- **Petits setups locaux** → trop de complexité
- **Équipes qui ont besoin de "ça marche partout"** → mauvais fit

## Quand préférer une alternative

- **Flexibilité, support large** → [[vllm]]
- **Workloads complexes (structured, MoE routing)** → [[sglang]]
- **Single-user local, GGUF** → [[llama-cpp]]

## Note Ahmad

> Tuned specialization but less features.

C'est-à-dire : moins de support de modèles et features expérimentales que [[vllm]] ou [[sglang]], mais la perf absolue est imbattable sur NVIDIA pur.

## Recettes hardware

- **8×H100/H200** : bench TensorRT-LLM si NVIDIA-only et perf justifie le tuning
- **B200/GB200/GB300** : bench TensorRT-LLM contre [[vllm]] et [[sglang]] (gap potentiellement gros)

## Related

- [[vllm]] — alternative plus flexible, plus portable
- [[sglang]] — alternative pour workloads complexes
- [[exllamav3]] — alternative consumer multi-GPU
- [[nvidia-dynamo]] — orchestration au-dessus, intégration tight
- [[paged-attention]] — variante NVIDIA-optimisée
- [[continuous-batching]] — natif
- [[inference-bottlenecks]] — grille de diagnostic
- [[llm-runtimes]] — comparaison wiki
- [[quantization-llm]] — FP8/FP4 sont les leviers natifs
- [[file-formats-llm]] — utilise des "engines" optimisés post-conversion
- [[kv-cache]] — KV cache management NVIDIA-optimisé
- [[prefill-vs-decode]] — disaggregation native
- [[serving-modes-llm]] — production NVIDIA-only est son terrain
- [[speculative-decoding]] — supporté
- [[ahmad-osman-inference-engines-2026]] — source principale

## My take

Le **plafond de verre des perfs NVIDIA**. Si tu n'es pas sur fleet NVIDIA pure et que la perf absolue ne justifie pas la complexité, n'y va pas — [[vllm]] est presque toujours le bon premier choix. Le sweet spot réel : équipes avec ≥8 GPUs, workload stable (pas d'expérimentation modèle constante), et budget pour absorber le tuning. La règle d'Ahmad *"belongs in the bake-off"* est juste : à scale prod NVIDIA, tu compares vLLM, SGLang, TensorRT-LLM sur ton workload réel — pas sur les benchmarks d'NVIDIA, ils sont toujours flatteurs pour leur stack.

---
type: entity
summary: Engine de serving LLM production-default open-source — PagedAttention, continuous batching, parallélisme tensor/pipeline/data/expert/context, quant FP8/MXFP/NVFP/INT/GPTQ/AWQ/GGUF, APIs OpenAI/Anthropic/gRPC.
lifecycle: reviewed
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

**vLLM** est l'engine de référence en open-source pour le serving LLM en production. C'est le premier à évaluer quand quelqu'un dit *"on veut servir des modèles open en prod"*.

## Sweet spot

**General production serving.** Du serveur d'équipe interne ([[serving-modes-llm|team API]]) jusqu'à la prod multi-node. Bien plus capable que le strict minimum local sans atteindre la spécialisation extrême de [[tensorrt-llm]].

## Features clés

- **PagedAttention** — KV cache management qui partitionne en blocs, supporte des batches plus grands sans waste mémoire ([[kv-cache]])
- **Continuous batching** — requêtes ajoutées/retirées en cours de batch sans recharger
- **Chunked prefill** — empêche un long prompt de bloquer le decode des autres requêtes
- **Prefix caching** — réutilisation du KV cache d'une partie commune entre requêtes
- **CUDA/HIP graphs** — réduit l'overhead kernel launch
- **Quantization extensive** — FP8, MXFP8/MXFP4, NVFP4, INT8, INT4, GPTQ, AWQ, GGUF (voir [[quantization-llm]], [[file-formats-llm]])
- **Kernels optimisés** — attention, GEMM, MoE
- **Speculative decoding** — voir [[speculative-decoding]]
- **torch.compile** — graph compilation
- **Disaggregated prefill/decode/encode** — sépare les phases pour scheduling fin

## Parallélisme

vLLM expose **tensor, pipeline, data, expert, et context parallelism**. Multi-node typiquement via Ray.

> **Sans NVLink, pipeline parallelism peut battre tensor parallelism.** Documenté pour setups type L40S. Voir [[memory-bandwidth]] pour la dimension interconnect.

## APIs et intégrations

- OpenAI-compatible
- Anthropic Messages API
- gRPC
- Streaming
- Structured outputs
- Tool calling
- Multi-LoRA

## Hardware

NVIDIA + AMD + x86/ARM/PowerPC CPUs natif. Plugins pour TPUs, Intel Gaudi, Huawei Ascend, Apple Silicon.

## Le piège du "ça suffira"

> Le piège est de supposer que vLLM enlève le besoin de systems thinking.

Il faut encore tuner **batching, context length, GPU memory utilization, parallelism layout, routing**. vLLM te donne un excellent engine — *system design* reste ton job.

## Quand préférer une alternative

- **Long-context / MoE / routing complexe** → [[sglang]] (cousin systems-brained avec prefill-decode disaggregation native)
- **NVIDIA-only, performance absolue justifie le tuning** → [[tensorrt-llm]]
- **Single-user local, GGUF, hardware bizarre** → [[llama-cpp]]
- **Fleet orchestration multi-engine** → NVIDIA Dynamo au-dessus

## Recettes hardware

- **8×H100/H200** : vLLM ou [[sglang]] en premier choix
- **B200/GB200/GB300** : bench vLLM, [[sglang]], [[tensorrt-llm]]
- **AMD MI300/325/350/355** : vLLM ou [[sglang]] sur ROCm — ne pas supposer que les benchmarks NVIDIA transfèrent
- **Dual/quad consumer RTX** : vLLM si le comportement de serving compte (ExLlamaV3 sinon pour le pur squeeze)

## Related

- [[llm-runtimes]] — comparaison wiki des runtimes
- [[sglang]] — cousin avec disagg prefill/decode native
- [[tensorrt-llm]] — alternative NVIDIA-max-perf
- [[llama-cpp]] — alternative portable single-user
- [[mlx]] — alternative Apple Silicon
- [[exllamav2]], [[exllamav3]] — alternatives consumer CUDA
- [[mlc-llm]] — alternative edge / browser
- [[ollama]] — wrapper llama.cpp (NE PAS UTILISER)
- [[nvidia-dynamo]] — orchestration au-dessus
- [[paged-attention]] — sa signature technique
- [[continuous-batching]] — natif
- [[inference-bottlenecks]] — grille de diagnostic
- [[serving-modes-llm]] — team API et production sont son sweet spot
- [[kv-cache]] — PagedAttention attaque ce problème
- [[speculative-decoding]] — supporté
- [[ahmad-osman-inference-engines-2026]] — source principale

## My take

Le **default raisonnable**. Si tu hésites en 2026 pour servir des modèles open à un groupe humain ≥ 5 ou un workload automatisé, **commence par vLLM**. La largeur de support (quant, parallelism, hardware) en fait l'engine le moins risqué à apprendre — l'investissement ne devient pas obsolète si tu changes de GPU ou de famille de modèle. Le rideau de fumée à éviter : croire que vLLM remplace le tuning. Comme le dit Ahmad, *"system design reste ton job"*. Pour 90% des équipes, vLLM bien tuné battra TensorRT-LLM mal tuné, même sur NVIDIA pur.

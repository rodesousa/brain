---
type: entity
summary: Engine d'inférence consumer CUDA — squeeze max sur 1 RTX 3090/4090/5090 via quant EXL2 + paged attention + dynamic batching. Single-GPU local sweet spot.
lifecycle: draft
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - inference-engines
  - llm-runtimes
  - consumer-gpu
---

**ExLlamaV2** est l'engine CUDA local pour faire **punch above its weight** un consumer NVIDIA. C'est le terrain de l'enthusiast solo.

## Sweet spot

- **Single RTX 3090 / 4090 / 5090**
- Local coding assistant
- Local chat
- Modèles quantizés **EXL2**
- Workstation prosumer

Le mot à mémoriser : **local**. C'est l'engine qui rend les quantizés rapides sur les GPUs consumer modernes.

## Features

- **Paged attention** — KV cache management similaire à [[vllm]] PagedAttention
- **Dynamic batching** — requêtes ajoutées/retirées en cours
- **Prompt caching** — réutilisation prefix
- **KV cache deduplication**
- **Batched generation** — multi-requêtes parallèles
- **Streaming**
- **Speculative decoding** — voir [[speculative-decoding]]

## Format natif : EXL2

EXL2 est le format quant communauté GPU-local, voir [[file-formats-llm]]. Optimisé pour ExLlama avec une précision configurable par tenseur (bpw, bits-per-weight variable).

## TabbyAPI

Server OpenAI-compatible au-dessus d'ExLlama. C'est typically la couche serving que tu poses.

## Recettes hardware

- **Single RTX 3090/4090/5090** : ExLlamaV2 pour EXL2 local. [[llama-cpp]] pour GGUF. [[vllm]] si multi-user.

## Quand passer à autre chose

- **2+ GPUs ou MoE local** → [[exllamav3]] (extension multi-GPU + EP)
- **Serving multi-user serious** → [[vllm]]
- **GGUF / portable / CPU+GPU hybrid** → [[llama-cpp]]
- **Production serving** → [[vllm]] ou [[sglang]]

## Verdict d'Ahmad

> ExLlamaV2 is the enthusiast's local CUDA engine. ExLlamaV3 is the frontier for multi-GPU (2-4) local setups.

## Related

- [[exllamav3]] — extension multi-GPU et MoE local
- [[llm-runtimes]] — comparaison wiki
- [[vllm]] — alternative serving multi-user
- [[sglang]] — alternative production
- [[llama-cpp]] — alternative portable
- [[ollama]] — wrapper llama.cpp (NE PAS UTILISER)
- [[paged-attention]] — paged attention dans son design
- [[continuous-batching]] — dynamic batching natif
- [[quantization-llm]] — EXL2 est un schéma spécifique
- [[file-formats-llm]] — EXL2 dans le tableau format ↔ runtime
- [[kv-cache]] — paged attention + KV dedup
- [[speculative-decoding]] — supporté
- [[serving-modes-llm]] — single-user est son terrain
- [[ahmad-osman-inference-engines-2026]] — source principale

## My take

L'**outil enthusiast par excellence** pour 1 GPU consumer. À privilégier sur [[llama-cpp]] dès que tu veux pure perf CUDA sans wrapper hybrid CPU. Le passage à [[exllamav3]] est justifié dès que tu as ≥2 GPUs ou que tu touches au MoE local. Pour le reste, vLLM reste meilleur dès qu'on parle de servir d'autres humains.

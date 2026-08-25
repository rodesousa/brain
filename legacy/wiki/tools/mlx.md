---
type: entity
summary: Framework array d'Apple pour Apple Silicon — unified memory native, MLX-LM pour les LLMs, HF Hub, quantization, LoRA, distributed (MPI, Thunderbolt RDMA). Server pas pour prod.
lifecycle: draft
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - inference-engines
  - llm-runtimes
  - apple-silicon
---

**MLX** est le framework array d'Apple pour Apple Silicon. **MLX-LM** est le package LLM construit dessus. Une stack ML Mac-first.

## Sweet spot

**Mac-first workflows.** Quand tu veux exploiter l'unified memory d'Apple Silicon sans frictions vs un runtime portable.

## La feature clé : unified memory native

Sur Apple Silicon, CPU et GPU partagent **le même pool mémoire**. Les arrays MLX vivent en unified memory et tu choisis le device au moment de l'opération, **pas en bougeant les arrays entre des memory spaces séparés**.

Conséquence : sur une machine M-series avec grosse unified memory, la question ne devient plus *"est-ce que ça fit en VRAM ?"* mais *"est-ce que ça fit en mémoire, et la memory system peut-elle feed le GPU assez vite ?"* — voir [[memory-bandwidth]].

Un quantized model qui ne tiendrait jamais dans un 24 GB consumer GPU peut **fit** sur un Mac Studio M3 Ultra (jusqu'à 512 GB unified). C'est l'avantage capacity. Mais plus lent en decode que HBM tier — voir [[ahmad-osman-memory-bandwidth-2026]].

## Features MLX-LM

- **HuggingFace Hub integration** — load direct depuis HF
- **Quantization** — divers schémas natifs MLX
- **LoRA / full fine-tuning**
- **Distributed inference** — MPI, Ring over TCP, **JACCL** (RDMA over Thunderbolt entre Macs), NCCL (CUDA)
- **Large MLX Community model ecosystem** sur HF

## MLX n'est plus Mac-only

MLX offre désormais des packages **CUDA et CPU-only pour Linux**. C'est moins central qu'Apple Silicon mais à connaître.

## Caveat critique : pas pour production

> MLX-LM's server warns it is **not recommended for production** because it only implements basic security checks.

→ Single-user et expérimentation, oui. Endpoint API publique servant des users, non.

## Quand préférer une alternative

- **Modèles GGUF portables, même sur Mac** → [[llama-cpp]]
- **Serving multi-user privé** → [[vllm]] (même sur Mac si la quantité d'utilisateurs le justifie)
- **Workload tordu (structured outputs lourds, MoE)** → [[sglang]]

## Recettes hardware

- **MacBook / Mac Studio** : MLX / MLX-LM pour Mac-native. [[llama-cpp]] pour GGUF portability cross-OS.

## Related

- [[llm-runtimes]] — comparaison wiki des engines
- [[llama-cpp]] — alternative cross-platform, GGUF
- [[vllm]] — alternative serving multi-user
- [[memory-bandwidth]] — unified memory : grosse capacity, bandwidth medium
- [[quantization-llm]] — MLX a ses propres schémas
- [[file-formats-llm]] — formats MLX
- [[serving-modes-llm]] — single-user et team-API limited
- [[ahmad-osman-memory-bandwidth-2026]] — paradigme Apple unified
- [[ahmad-osman-inference-engines-2026]] — source principale

## My take

L'**outil natural sur Mac**. Sur Mac Studio Ultra avec 192+ GB unified memory, MLX donne accès à des modèles que tu ne peux **physiquement pas** charger sur un consumer NVIDIA. C'est l'angle capacity-roi : tu n'es pas champion en tok/s mais tu peux faire tourner un 70B FP8 sans sharding. À éviter en production publique — son serveur le dit lui-même. Et garder en tête le fork Linux/CUDA de MLX, intéressant à surveiller pour le portable cross-platform.

---
type: entity
summary: Extension d'ExLlamaV2 vers multi-GPU et MoE-local — format EXL3 (QTIP-based), tensor-parallel et expert-parallel sur consumer hardware, multimodal, OpenAI-compat via TabbyAPI.
lifecycle: draft
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
tags:
  - inference-engines
  - llm-runtimes
  - consumer-gpu
---

**ExLlamaV3** étend la philosophie d'[[exllamav2]] vers **multi-GPU et MoE local** sur hardware consumer.

## Sweet spot

- **2-4+ NVIDIA / CUDA GPUs** consumer
- **MoE local** (mixture of experts)
- Box prosumer / workstation enthusiast

## Nouveautés vs V2

- **Format EXL3** — quant basée sur **QTIP** (post-training tensor quantization avancée)
- **Flexible tensor-parallel** — splitting le modèle sur plusieurs GPUs consumer
- **Expert-parallel** — pour les MoE locaux
- **Server OpenAI-compatible** via **TabbyAPI**
- **Continuous dynamic batching**
- **Multimodal support**

## Caveats

> Some models do not support tensor or expert parallelism in ExLlamaV3.

→ Vérifier que ton modèle cible est supporté avant de bâtir un setup multi-GPU autour de cet engine. Plus rough edges qu'[[exllamav2]] mais plus de capabilities.

## Verdict d'Ahmad

> Expect caveats — but ExLlamaV3 is **the frontier for multi-GPU (2-4) local setups**. Rougher edges for better capability.

## Recettes hardware

- **Dual ou quad consumer RTX** : ExLlamaV3 pour multi-GPU quantized inference ou MoE local. [[vllm]] si le comportement de serving matters. [[sglang]] si routing / long-context patterns à tester.

## Quand préférer une alternative

- **Single GPU** → [[exllamav2]] suffit, moins de friction
- **Serving multi-user / production** → [[vllm]] ou [[sglang]]
- **AMD / Apple Silicon** → MLX, [[llama-cpp]]
- **NVIDIA datacenter** → [[tensorrt-llm]]

## Related

- [[exllamav2]] — la version single-GPU, base philosophique
- [[llm-runtimes]] — comparaison wiki
- [[vllm]] — alternative serving multi-user
- [[sglang]] — alternative pour routing/long-context
- [[tensorrt-llm]] — alternative NVIDIA-max-perf
- [[llama-cpp]] — alternative portable
- [[ollama]] — wrapper llama.cpp (NE PAS UTILISER)
- [[continuous-batching]] — dynamic batching natif
- [[quantization-llm]] — EXL3 est QTIP-based
- [[file-formats-llm]] — EXL3 dans le tableau format ↔ runtime
- [[ahmad-osman-inference-engines-2026]] — source principale

## My take

Le **terrain à défricher** quand tu as 2-4 RTX consumer et que tu veux soit faire tourner un MoE local, soit splitter un gros dense. C'est l'engine où la communauté pousse les limites du local CUDA enthusiast. Accepter le côté **frontier** — quelques modèles cassés en TP/EP, debugging un peu manuel — en échange d'une capability impossible ailleurs en consumer. Si tu cherches du calme : ExLlamaV2 (1 GPU) ou vLLM (multi-user-ready).

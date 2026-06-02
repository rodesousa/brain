---
type: entity
summary: Engine d'inférence LLM portability king — Apple Silicon (Metal/NEON), x86 (AVX/AMX), RISC-V, CUDA, ROCm, Vulkan, SYCL, CPU+GPU hybrid. GGUF natif. Pas pour multi-GPU prod.
lifecycle: draft
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - inference-engines
  - llm-runtimes
  - local-llm-deployment
---

**llama.cpp** est *the* portability king. La réponse quand le hardware est **bizarre, contraint, offline, CPU-heavy, edge-oriented, ou pas un tidy NVIDIA datacenter node**.

## Sweet spot

- Hardware bizarre (RISC-V, ARM, vieux x86…)
- Offline / contraint / edge
- CPU-heavy ou CPU+GPU hybrid
- Apple Silicon (mais voir [[#concurrent-mlx]])
- Format **GGUF** comme format de référence ([[file-formats-llm]])

## Support hardware ahurissant

- **Apple Silicon** via ARM NEON, Accelerate, Metal
- **x86** via AVX / AVX2 / AVX512 / AMX
- **RISC-V**
- **NVIDIA CUDA**
- **AMD** via HIP
- **MUSA** (Moore Threads)
- **Vulkan**
- **SYCL**
- **CPU+GPU hybrid offload** — couches partiellement sur GPU, le reste CPU
- **Low-bit quantization** (Q2 à Q8, voir [[quantization-llm]])

C'est l'unique stack qui couvre cette amplitude.

## llama-server

Le HTTP server est **plus capable qu'un toy local runner** :

- Routes OpenAI-compatible
- Anthropic Messages API compatibility
- Reranking
- Continuous batching
- Multimodal
- JSON schema constraints
- Function calling
- Speculative decoding ([[speculative-decoding]])
- Web UI

Donc OK pour [[serving-modes-llm|single-user et team API de petite échelle]], pas pour production multi-node.

## Limites critiques

### Pas pour multi-node prod

Le RPC backend est **explicitement documenté comme proof-of-concept, fragile, insecure**. À ne pas utiliser pour serving sérieux multi-node.

### DO NOT use sur multi-GPU setups

> **Ahmad : do not use llama.cpp or Ollama on multi-GPUs setups — use vLLM or ExLlamaV2.**

Sur 2+ GPUs, [[vllm]] ou ExLlamaV2 sont strictement meilleurs (tensor parallelism, batching efficient, KV cache management). llama.cpp reste excellent sur 1 GPU ou en CPU+GPU hybrid.

## Concurrent MLX

Sur Mac, MLX/MLX-LM exploite mieux la mémoire unifiée native d'Apple. llama.cpp reste pertinent sur Mac pour :
- Portabilité du checkpoint GGUF entre Mac et Linux/Windows
- Workflows hybrid CPU+GPU
- Quand tu veux le même runtime sur tout ton parc

## Verdict d'Ahmad

> Use llama.cpp when portability, offline operation, GGUF, or hybrid offload matter more than fleet-scale serving.

## Recettes hardware

- **CPU-only server** : llama.cpp en premier
- **Single RTX 3090/4090/5090** : llama.cpp pour GGUF ou portabilité (ExLlamaV2 pour pur EXL2, vLLM si serving multi-user)
- **MacBook / Mac Studio** : MLX pour Mac-native, llama.cpp pour GGUF portability

## Related

- [[llm-runtimes]] — comparaison wiki
- [[file-formats-llm]] — GGUF est le format natif
- [[vllm]] — alternative pour multi-GPU et team serving
- [[tensorrt-llm]] — alternative NVIDIA-only max perf
- [[sglang]] — alternative production serveur
- [[mlx]] — alternative Mac-native (mémoire unifiée)
- [[exllamav2]], [[exllamav3]] — alternatives consumer CUDA quant
- [[mlc-llm]] — alternative edge / browser
- [[ollama]] — wrapper convivial, mais NE PAS UTILISER
- [[paged-attention]] — support partiel
- [[continuous-batching]] — supporté côté server
- [[quantization-llm]] — toute la palette Q-K
- [[speculative-decoding]] — supporté côté server
- [[serving-modes-llm]] — single-user est son terrain, team possible, prod non
- [[ahmad-osman-gpu-memory-math-2026]] — GGUF runtime-specific
- [[ahmad-osman-inference-engines-2026]] — source principale

## My take

L'**outil universel** du local LLM. À ne pas confondre avec un *production server* malgré la qualité de llama-server : c'est un excellent single-user et un team-server raisonnable, mais le RPC backend te dira "non" dès que tu essaies de scale. La règle d'or pratique : **llama.cpp = single GPU ou CPU+GPU hybrid**, sinon passer à [[vllm]] ou ExLlamaV2 (selon que tu veux serving multi-user ou squeeze perf single-process). Et bannir Ollama, qui n'a pas la même rigueur — c'est plus pratique en surface, mais cumulé aux soucis sécurité/observability c'est un mauvais choix par défaut.

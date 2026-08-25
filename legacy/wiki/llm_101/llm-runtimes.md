---
type: comparison
summary: Comparaison runtimes/engines LLM 2026 — 4 familles (portable, Apple unified, CUDA quant, production serving) + decision guide one-page. Verdict d'Ahmad Osman intégré.
lifecycle: draft
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
tags:
  - llm-runtimes
  - inference-engines
  - local-llm-deployment
  - serving-modes
---

Un **runtime** (ou **inference engine**) est le software qui load le modèle et exécute l'inférence. En 2026 l'écosystème local est mature et fragmenté — chaque engine gagne sur un axe différent. Cette page est la **vue d'ensemble** ; voir les pages d'entités pour les détails.

## Principe : l'engine suit, il ne pilote pas

> Tu ne choisis pas l'engine en premier. Tu choisis une **stratégie hardware**, une **forme de workload**, un **modèle de serving**. L'engine suit.

L'engine n'est pas "le modèle". C'est traffic cop, memory manager, kernel dispatcher, scheduler, cache accountant, parallelism planner, API surface. Le meilleur engine est celui qui match **ta memory hierarchy, ton interconnect, ton format de quantization, tes targets latency/throughput, ton architecture de modèle, et ta maturity opérationnelle**.

## Decision guide one-page (Ahmad Osman)

| Contexte | Engine |
|---|---|
| Laptop / edge / odd hardware | [[llama-cpp]] |
| Mac-first workflows | [[mlx]] / MLX-LM |
| Single RTX local inference | [[exllamav2]] |
| 2-4+ NVIDIA / CUDA GPUs | [[exllamav3]] |
| General production serving | [[vllm]] |
| Long-context / MoE / routing | [[sglang]] |
| NVIDIA max performance | [[tensorrt-llm]] |
| Cluster orchestration | [[nvidia-dynamo]] |

## Les 4 familles + orchestration

### 1. Portable local runtimes — *"make it run here"*

| Runtime | Spécialité |
|---|---|
| **[[llama-cpp]]** | Portability king — Apple Silicon, x86, RISC-V, CUDA, AMD HIP, MUSA, Vulkan, SYCL, CPU+GPU hybrid. GGUF natif. |
| **[[mlc-llm]]** | Compiler-first universal deployment — REST, Python, JS, iOS, Android. "Ship LLMs everywhere". |
| **ONNX Runtime GenAI** | Foundry Local, Windows ML, VS Code AI Toolkit. CPU, CUDA, DirectML, TensorRT-RTX, OpenVINO, QNN, WebGPU, AMD GPU. |
| **OpenVINO GenAI** | Intel-optimisé — Xeon CPUs, Arc GPUs, Core Ultra, NPUs. OpenAI-compatible serving. |
| **[[ollama]]** | ⚠️ **DO NOT USE** (Ahmad). Plaisant en surface mais carence sécurité, observability, et discipline opérationnelle. |

### 2. Apple unified-memory runtimes — *"use big shared memory and Apple's stack well"*

| Runtime | Spécialité |
|---|---|
| **[[mlx]] / MLX-LM** | Mac-first ML stack — unified memory native, HF Hub integration, quantization, LoRA, distributed inference (MPI, Ring TCP, JACCL Thunderbolt, NCCL CUDA). MLX-LM server **pas recommandé prod**. (Note : [[mlx]] désigne MLX et MLX-LM ensemble.) |

### 3. Consumer CUDA quant engines — *"make my 3090/4090/5090 scream"*

| Runtime | Spécialité |
|---|---|
| **[[exllamav2]]** | Local CUDA quant engine — paged attention, dynamic batching, prompt caching, KV dedup, streaming, speculative decoding. EXL2 format. **Single RTX**. |
| **[[exllamav3]]** | Extends V2 vers multi-GPU et MoE local — EXL3 quant (QTIP-based), tensor/expert parallelism consumer, OpenAI-compat via TabbyAPI, multimodal. **2-4+ consumer NVIDIA**. Caveat : certains modèles ne supportent pas TP/EP. |

### 4. Production serving engines — *"concurrent users, KV cache, batching, parallelism, observability"*

| Runtime | Sweet spot |
|---|---|
| **[[vllm]]** | Production default. PagedAttention, continuous batching, chunked prefill, prefix caching, parallélisme tensor/pipeline/data/expert/context, quant FP8/MXFP/NVFP/INT/GPTQ/AWQ/GGUF, APIs OpenAI+Anthropic+gRPC. |
| **[[sglang]]** | Cousin systems-brained — RadixAttention, **prefill-decode disaggregation native**, structured outputs lourds, multi-LoRA batching. Workloads ugly. |
| **[[tensorrt-llm]]** | NVIDIA max perf — kernels custom attention/GEMM/MoE, FP8/FP4, Wide Expert Parallelism, intégré Triton + Dynamo. Trade portability contre perf. |
| **TGI** | HF production server — tracing, metrics, tensor parallelism, continuous batching. Quand HF integration prime. |
| **LMDeploy** | CUDA-focused — TurboMind (perf) + PyTorch (accessibility). Alternative à vLLM/SGLang/TensorRT-LLM. |

### Orchestration au-dessus

**[[nvidia-dynamo]]** — distributed orchestration layer au-dessus de [[vllm]], [[sglang]], [[tensorrt-llm]]. Disaggregation, intelligent routing, multi-tier KV caching. Quand single-engine ne suffit plus.

## Workload shape → engine emphasis

| Workload | Bottleneck dominant | Engine emphasis |
|---|---|---|
| Prompt court, réponse longue | Decode → bandwidth + batching | [[vllm]], engines avec good batching |
| Prompt long, réponse courte | Prefill → attention kernels + chunked prefill | [[sglang]], [[vllm]] chunked prefill |
| Many users | Scheduler → continuous batching, fairness | [[vllm]] ou [[sglang]] |
| Long context | KV cache → paged attention, KV quant | [[vllm]] PagedAttention, [[sglang]] disagg |
| MoE | Expert routing → EP, interconnect | [[sglang]], [[tensorrt-llm]] Wide EP |
| Multi-node | Interconnect → NVLink, RDMA, pipeline | [[tensorrt-llm]] + [[nvidia-dynamo]] |

## Recettes hardware

- **CPU-only** : [[llama-cpp]] first. OpenVINO pour Intel Xeon. ONNX Runtime GenAI pour app/ONNX.
- **MacBook / Mac Studio** : [[mlx]] / MLX-LM pour Mac-native. [[llama-cpp]] pour GGUF portability.
- **Single RTX 3090/4090/5090** : [[exllamav2]] pour EXL2. [[llama-cpp]] pour GGUF. [[vllm]] si multi-user.
- **Dual/quad consumer RTX** : [[exllamav3]] pour multi-GPU quantized ou MoE. [[vllm]] si serving compte. [[sglang]] si routing/long-context.
- **8×H100/H200** : [[vllm]] ou [[sglang]] en premier. Bench [[tensorrt-llm]] si NVIDIA-only et perf justifie. [[nvidia-dynamo]] pour multi-node.
- **B200/GB200/GB300** : bench [[tensorrt-llm]], [[sglang]], [[vllm]]. [[nvidia-dynamo]] pour fleet.
- **AMD MI300/325/350/355** : [[vllm]] ou [[sglang]] sur ROCm.
- **Intel Xeon / Core Ultra / Arc** : OpenVINO GenAI ou ONNX Runtime GenAI.
- **Browser / mobile / app-native** : [[mlc-llm]] / WebLLM ou ONNX Runtime GenAI.

## Choix par persona

- **Tu débutes** → LM Studio (front Harbor possible)
- **Tu codes en local** → [[llama-cpp]] (CLI server) ou [[exllamav2]]
- **Tu sers ton équipe** → [[vllm]] derrière endpoint OpenAI-compat ; [[sglang]] si workload tordu
- **Tu pars en prod NVIDIA** → bench [[tensorrt-llm]] vs [[vllm]] vs [[sglang]]
- **Tu vises browser / mobile** → [[mlc-llm]] ou WebLLM

## Opinions tranchées (Ahmad Osman)

> **DO NOT use [[ollama]].** Plaisant mais pas de discipline opérationnelle.

> **DO NOT use [[llama-cpp]] on multi-GPU setups** — passer à [[vllm]] ou [[exllamav2]].

> **Local engine ≠ production server.** llama.cpp server est capable, MLX-LM convenient — *aucun* n'est un prod server. Production = sécurité, observability, backpressure, routing, autoscaling, SLA. MLX-LM lui-même warning "not recommended for production".

## Format ↔ runtime (rappel)

Le runtime locke partiellement l'écosystème [[file-formats-llm]] :

- [[llama-cpp]] ↔ **GGUF**
- [[vllm]] / [[sglang]] ↔ **safetensors** ou HF checkpoints + GGUF / GPTQ / AWQ
- [[tensorrt-llm]] ↔ **ONNX** ou engines optimisés (conversion préalable)
- [[exllamav2]] / [[exllamav3]] / TabbyAPI ↔ **EXL2 / EXL3**
- [[mlx]] ↔ formats MLX

Voir [[serving-modes-llm]] pour le découpage single-user / team / production qui informe le choix.

## Related

- [[vllm]], [[sglang]], [[tensorrt-llm]], [[llama-cpp]] — entités production / portable
- [[mlx]], [[exllamav2]], [[exllamav3]] — entités Apple / consumer CUDA
- [[mlc-llm]], [[ollama]] — entités edge / wrapper (note ollama DO NOT USE)
- [[nvidia-dynamo]] — orchestration au-dessus
- [[paged-attention]], [[continuous-batching]] — techniques de serving fondamentales
- [[inference-bottlenecks]] — grille de diagnostic
- [[file-formats-llm]] — chaque engine ↔ format(s)
- [[serving-modes-llm]] — usage shapes le choix
- [[memory-bandwidth]] — la couche débit que l'engine extrait (ou non)
- [[prefill-vs-decode]] — les phases que l'engine orchestre
- [[kv-cache]] — PagedAttention, prefix caching, disaggregation
- [[local-llm-growth-path]] — progression beginner → expert
- [[local-llm-runbook]] — étape "good runtime" dans l'équation
- [[ahmad-osman-inference-engines-2026]] — source principale Part 3
- [[ahmad-osman-memory-bandwidth-2026]] — source Part 2

## My take

La conversation *"quel est le meilleur runtime"* est mal posée. Trois questions remplacent celle-là : **quel hardware ? quel workload shape ? quel mode de serving ?**

Trois défauts raisonnables à mémoriser :
- **Single-user local** → [[llama-cpp]] (ou [[exllamav2]] si CUDA pur sur 1 GPU)
- **Team API** → [[vllm]]
- **Production NVIDIA-only avec budget tuning** → bench [[tensorrt-llm]]

Le reste sont des cas particuliers (Mac → [[mlx]], multi-GPU consumer → [[exllamav3]], workload tordu → [[sglang]], edge → [[mlc-llm]]). Et : bannir [[ollama]], ne pas confondre [[llama-cpp]] server avec un prod server, ne pas faire de multi-GPU sur llama.cpp.

---
type: source-summary
summary: Part 3 trilogie Ahmad Osman — taxonomie complète des engines d'inférence LLM, decision guide one-page, 5 bottlenecks structurels et opinions tranchées (do not use [[ollama]]).
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
tags:
  - inference-engines
  - llm-runtimes
  - serving-modes
  - local-llm-deployment
---

Troisième volet de la trilogie d'Ahmad Osman. Couvre la **couche software** qui transforme la capacité ([[ahmad-osman-gpu-memory-math-2026]]) et la bandwidth ([[ahmad-osman-memory-bandwidth-2026]]) en inférence utilisable.

## Thèse centrale

> Tu ne choisis pas l'inference engine en premier. Tu choisis une stratégie hardware, une forme de workload, un modèle de serving. **L'engine suit.**

L'engine n'est pas "le modèle" — c'est traffic cop, memory manager, kernel dispatcher, scheduler, cache accountant, parallelism planner, API surface, et parfois framework de déploiement.

## Decision guide one-page

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

1. **Portable local runtimes** — [[llama-cpp]], [[mlc-llm]], ONNX Runtime GenAI, OpenVINO, [[ollama]]. *"Make it run here."*
2. **Apple unified-memory runtimes** — MLX, MLX-LM. *"Use big shared memory and Apple's stack well."*
3. **Consumer CUDA quant engines** — [[exllamav2]], [[exllamav3]]. *"Make my 3090/4090/5090 scream with low-bit weights."*
4. **Production serving engines** — [[vllm]], [[sglang]], [[tensorrt-llm]], TGI, LMDeploy. *"Concurrent users, KV cache, batching, parallelism, observability, cost per token."*

Au-dessus : **orchestration layers** comme [[nvidia-dynamo]] coordonnent fleets, disaggregated prefill/decode, routing, autoscaling.

## Les 5 bottlenecks structurels

1. **Memory bandwidth, pas VRAM size** — VRAM décide ce qui fit, bandwidth décide la vitesse de [[prefill-vs-decode|decode]]. Apple M3 Ultra 819 GB/s vs H100 SXM 3.35 TB/s. *Capacity ≠ bandwidth.*
2. **KV cache growth** — grandit avec batch size × context length. PagedAttention partitionne en blocs, voir [[kv-cache]].
3. **Interconnect** — multi-GPU = communication cost. Tensor parallelism a besoin d'all-reduce frequentes. **Sans NVLink, pipeline parallelism peut battre tensor parallelism** (vLLM docs).
4. **Scheduler quality** — qui entre dans le batch, comment prefill et decode partagent l'accélérateur, comment éviter la starvation. *Supporting batching ≠ being a production scheduler.*
5. **Runtime overhead** — CUDA graphs, kernel fusion, sampling, tokenizer, HTTP, LoRA switching, structured decoding. À scale, les 2% s'additionnent.

## Workload shape → engine emphasis

| Workload | Bottleneck dominant |
|---|---|
| Prompt court, réponse longue | Decode → bandwidth + batching |
| Prompt long, réponse courte | Prefill → attention kernels + chunked prefill |
| Many users | Scheduler → continuous batching, cache paging, fairness |
| Long context | KV cache → paged attention, KV quant, offload |
| MoE | Expert routing → expert parallelism, interconnect, grouped GEMMs |
| Multi-node | Interconnect → NVLink, RDMA, pipeline, disaggregation |

## Recettes hardware

- **CPU-only server** : [[llama-cpp]] first. OpenVINO pour Xeon. ONNX Runtime GenAI pour app/ONNX deployment.
- **MacBook / Mac Studio** : [[mlx]] / MLX-LM. [[llama-cpp]] pour portabilité GGUF.
- **Single RTX 3090/4090/5090** : [[exllamav2]] pour EXL2. [[llama-cpp]] pour GGUF. [[vllm]] pour multi-user.
- **Dual/quad consumer RTX** : [[exllamav3]] pour multi-GPU quantized ou MoE. [[vllm]] pour serving. [[sglang]] pour routing/long-context.
- **8×H100/H200** : [[vllm]] ou [[sglang]] d'abord. Bench [[tensorrt-llm]] si NVIDIA-only justifie le tuning. Dynamo quand multi-node nécessaire.
- **B200 / GB200 / GB300** : bench [[tensorrt-llm]], [[sglang]], [[vllm]]. Dynamo pour fleet.
- **AMD MI300/325/350/355** : [[vllm]] ou [[sglang]] sur ROCm.
- **Intel Xeon / Core Ultra / Arc** : OpenVINO GenAI ou ONNX Runtime GenAI.
- **Browser / mobile / app-native** : [[mlc-llm]] / WebLLM ou ONNX Runtime GenAI.

## Les opinions tranchées d'Ahmad

> **Note: DO NOT USE [[ollama]].**

> **DO NOT use [[llama-cpp]] on multi-GPUs setups — use vLLM or [[exllamav2]].**

Le serveur llama.cpp est capable, MLX-LM est convenient, [[ollama]] est plaisant — *mais aucun n'est un production server*. Production = sécurité, observability, backpressure, routing, autoscaling, SLA. MLX-LM lui-même warning "not recommended for production".

## Erreurs classiques

- **Choix par VRAM capacity seul** — bandwidth + scheduler décident la vitesse
- **Tensor parallelism sans NVLink** — tester pipeline parallelism, vLLM docs le signalent pour L40S
- **Ignorer KV cache** — long context + concurrency, PagedAttention + prefix caching + KV quant + disaggregation **non optionnels à scale**
- **Local engine traité comme prod server** — voir ci-dessus
- **Assumer que tout format de quant est portable** — GGUF, EXL2/3, AWQ, GPTQ, FP8, FP4, MLX, ONNX **pas interchangeables**, voir [[file-formats-llm]]
- **Ignorer l'architecture du modèle** — dense, MoE, hybrid attention, multimodal, long-context stressent différents endroits de l'engine
- **Trust benchmark charts sans workload shape** — Llama 3.1 8B @ 1K/128 ne dit rien d'un agent codant à 80K context sur Qwen 3.6 27B

## Benchmarking : ce qui compte

**Mauvais bench** : "180 tok/s".

**Bon bench** inclut : model exact + architecture + active MoE params, weights (dtype, quant, group size, calibration), engine (version + commit + flags), hardware (SKU + mémoire + bandwidth + interconnect + CPU + RAM), workload (input/output length distribs, concurrency, streaming, shared prefixes, structured), métriques (**TTFT, TPOT, p50/p95/p99, tok/s, req/s, GPU mem, KV hit rate, prefill/decode throughput, $/1M tokens**).

10 règles : jamais comparer en single-user tok/s seul, tester ta vraie distribution, concurrency réaliste, séparer [[prefill-vs-decode|prefill et decode]], track p95/p99 pas seulement les moyennes, mesurer le headroom mémoire au context length cible, tester cache reuse si tes prompts partagent des préfixes, bench structured séparément (grammar adds overhead), bench LoRA/multi-LoRA séparément, re-tester après chaque upgrade driver/CUDA/ROCm/model/engine.

## Final principle

Avant de choisir l'engine, répondre à 10 questions : hardware réel, fit en fast memory vs unified, decode vs prefill bottleneck, context + concurrency cibles, prompts partagés (prefix caching), architecture (dense/MoE/multimodal/hybrid), mode (local/team/production), format de quant à kernels optimisés, interconnect (PCIe/NVLink/NVSwitch/Ethernet/RDMA/Thunderbolt), axe d'optimisation (latency/throughput/cost/privacy/portability/dev speed).

**L'engine suit les réponses.**

## Related

- [[llm-runtimes]] — comparaison wiki, cette source en élargit massivement la portée
- [[vllm]], [[sglang]], [[tensorrt-llm]], [[llama-cpp]] — entités production / portable
- [[mlx]], [[exllamav2]], [[exllamav3]] — entités Apple / consumer CUDA
- [[mlc-llm]], [[ollama]] — entités edge / wrapper
- [[nvidia-dynamo]] — orchestration au-dessus
- [[paged-attention]], [[continuous-batching]], [[inference-bottlenecks]] — concepts engine-side
- [[memory-bandwidth]] — la couche débit, prerequisite
- [[prefill-vs-decode]] — workload phases que les engines orchestrent
- [[kv-cache]] — paged attention, prefix caching, disaggregation, KV quant
- [[speculative-decoding]] — bottleneck decode-latency adressé par certains engines
- [[serving-modes-llm]] — single-user / team / production
- [[file-formats-llm]] — chaque engine ↔ format(s) optimisé(s)
- [[ahmad-osman-gpu-memory-math-2026]] — Part 1
- [[ahmad-osman-memory-bandwidth-2026]] — Part 2

## My take

Cette Part 3 est **la pièce la plus à valeur ajoutée du wiki** parce qu'elle remplace les approximations communes ("vLLM = production") par une **taxonomie en 4 familles + decision guide one-page** qui rend les arbitrages explicites. Le passage "DO NOT use [[ollama]]" et "DO NOT use llama.cpp multi-GPU" sont les opinions tranchées qui justifient de garder la source en référence — elles couperont court à beaucoup de débats récurrents. La grille **workload → bottleneck** est la chose à apprendre par cœur : elle résume tout l'art du serving. Faiblesse : Ahmad est très NVIDIA-cluster-fluent et un peu rapide sur AMD/Intel — pour ces stacks, croiser avec les docs ROCm officielles.

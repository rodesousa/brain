---
type: overview
summary: Les 5 bottlenecks structurels du serving LLM selon Ahmad Osman — memory bandwidth, KV cache growth, interconnect, scheduler quality, runtime overhead. Grille de diagnostic universelle.
lifecycle: draft
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
tags:
  - inference-engines
  - inference-bottlenecks
  - production-serving
---

Les **5 bottlenecks structurels** du serving LLM, taxonomie d'Ahmad Osman ([[ahmad-osman-inference-engines-2026]]). Grille de diagnostic universelle : à scale, le problème de perf appartient toujours à au moins un de ces 5.

## 1. Memory bandwidth, pas VRAM size

> VRAM décide ce qui fit. **Bandwidth décide la vitesse de decode.**

Apple M3 Ultra : 819 GB/s. H100 SXM : 3.35 TB/s. La même quantité de mémoire (96 GB par exemple) peut donner deux ordres de grandeur de tok/sec différents selon la bandwidth.

Voir [[memory-bandwidth]] pour les 5 tiers 2026.

## 2. KV cache growth

> KV cache grandit avec **batch size × context length**. Long-context workloads peuvent OOM **même quand les weights fit**.

Solutions : [[paged-attention]] (vLLM, SGLang), KV quantization FP8/INT8 (vLLM, TensorRT-LLM), prefix caching, prefill-decode disaggregation.

Voir [[kv-cache]] pour la formule de cost.

## 3. Interconnect (multi-GPU)

> Dès qu'un modèle traverse plusieurs GPUs, tu paies en communication.

- **Tensor parallelism** → all-reduce frequents → NVLink obligatoire pour la perf
- **Pipeline parallelism** → communique aux boundaries → tolère PCIe
- **Expert parallelism (MoE)** → all-to-all → besoin de bandwidth interconnect élevée

> Sans NVLink, pipeline parallelism peut battre tensor parallelism. ([[vllm]] docs sur L40S)

## 4. Scheduler quality

> Un bon scheduler décide qui entre dans le batch, comment prefill et decode se partagent l'accélérateur, comment éviter la starvation. **Supporting batching ≠ being a production scheduler.**

Voir [[continuous-batching]] pour le sous-jacent, et [[sglang]] pour la disaggregation prefill/decode native.

## 5. Runtime overhead

> CUDA graphs, kernel fusion, sampling, tokenizer, HTTP, LoRA switching, structured decoding. **À scale, les 2% s'additionnent.**

Solutions : torch.compile, CUDA graphs, FlashAttention, kernels custom pour attention/GEMM/MoE.

## Workload shape → bottleneck dominant

| Workload | Bottleneck dominant |
|---|---|
| Prompt court, réponse longue | **Decode** → bandwidth + batching |
| Prompt long, réponse courte | **Prefill** → attention kernels + chunked prefill |
| Many users | **Scheduler** → continuous batching, cache paging, fairness |
| Long context | **KV cache** → paged attention, KV quant, offload |
| MoE | **Expert routing** → expert parallelism, interconnect, grouped GEMMs |
| Multi-node | **Interconnect** → NVLink, RDMA, pipeline, disaggregation |

Voir [[prefill-vs-decode]] pour les régimes phases.

## Comment l'utiliser

Quand tu débogues une perf insatisfaisante :

1. **Profile** — separate TTFT (prefill), TPOT (decode), wait time (scheduler queueing)
2. **Localise** — lequel des 5 explique le gap vs le théorique ?
3. **Compare** — au théorique : si decode tok/s ≈ memory_bandwidth / (model_size_bytes), tu es bandwidth-bound, plafond atteint
4. **Choisis le levier** — quant agressif (réduit bandwidth load), batching agressif (améliore scheduler), interconnect upgrade, etc.

## Related

- [[memory-bandwidth]] — bottleneck #1
- [[kv-cache]] — bottleneck #2
- [[paged-attention]] — solution KV cache
- [[continuous-batching]] — solution scheduler
- [[prefill-vs-decode]] — les régimes phases
- [[llm-runtimes]] — chaque engine attaque ces bottlenecks différemment
- [[vllm]], [[sglang]], [[tensorrt-llm]] — engines couvrant les bottlenecks production
- [[ahmad-osman-inference-engines-2026]] — source principale, taxonomie originale
- [[ahmad-osman-memory-bandwidth-2026]] — bandwidth tier détails

## My take

La **grille universelle de diagnostic** de perf LLM serving. Le mode d'usage est sec : tu observes un problème de perf, tu te demandes **lequel de ces 5 explique le gap au théorique** — la réponse pointe presque toujours vers UN bottleneck dominant, rarement deux. C'est aussi un excellent garde-fou contre les paniques *"il faut changer d'engine"* — souvent le problème est de l'**autre côté** (interconnect insuffisant, scheduler de prod naïf, KV cache mal géré au niveau workload). À garder en référence et appliquer mécaniquement avant tout achat ou migration.

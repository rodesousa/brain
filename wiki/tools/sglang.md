---
type: entity
summary: Cousin systems-brained de vLLM — engine de serving LLM pour workloads ugly (structured outputs, long context, MoE, disaggregation prefill/decode native, routing).
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

**SGLang** est l'engine de serving LLM à choisir quand le workload devient *ugly* : structured outputs lourds, long context, MoE, disaggregation prefill/decode, routing complexe.

## Sweet spot

Production serving "**workload hostile**" — quand le bottleneck n'est plus *"can we run the model?"* mais *"can we run it under hostile traffic sans torcher latency, mémoire et coût ?"*

## Différenciateur — disaggregation native

> Sépare le compute-intensive **prefill** ([[prefill-vs-decode]]) du memory-intensive **decode** en instances spécialisées, transfère le KV cache entre eux.

Conséquence pratique : un long prefill batch n'**interrompt plus** un decode en cours, donc la token latency ne spike plus.

## Features clés

- **RadixAttention prefix caching** — partage prefixes optimisé pour conversations multi-tour
- **Prefill-decode disaggregation** — voir ci-dessus, le différenciateur clé
- **Speculative decoding** — voir [[speculative-decoding]]
- **Continuous batching, paged attention** (comme [[vllm]])
- **Parallélisme** — tensor, pipeline, expert, data
- **Structured outputs** — grammar/JSON-schema constrained decoding
- **Chunked prefill**
- **Multi-LoRA batching**

## Hardware support

NVIDIA, AMD, Intel Xeon, Google TPUs, Huawei Ascend NPUs, etc.

## Quand préférer SGLang à vLLM

- Workload **agents** avec structured outputs JSON/grammar
- **Long context** où la disaggregation aide à tenir les p95/p99
- **MoE** où l'expert parallelism native compte
- **Routing** complexe entre modèles ou instances
- **Multi-LoRA batching** important

## Quand rester sur vLLM

- Workload simple (chat / completion) où la maturity de [[vllm]] suffit
- Pas de structured outputs lourd
- Pas de besoin de disagg prefill/decode

## Caveat

SGLang est plus jeune que [[vllm]] et la communauté plus restreinte — meilleure techno pour les cas tordus, mais accepter de rentrer plus profondément dans les internals si quelque chose casse.

## Related

- [[vllm]] — alternative plus mature, sweet spot général
- [[tensorrt-llm]] — alternative NVIDIA-max-perf
- [[llama-cpp]] — alternative single-user / portable
- [[mlx]] — alternative Apple Silicon
- [[exllamav2]], [[exllamav3]] — alternatives consumer CUDA
- [[mlc-llm]] — alternative edge / browser
- [[nvidia-dynamo]] — orchestration au-dessus
- [[paged-attention]] — base de RadixAttention
- [[continuous-batching]] — natif
- [[inference-bottlenecks]] — grille de diagnostic
- [[llm-runtimes]] — comparaison wiki des runtimes
- [[prefill-vs-decode]] — la disagg sépare les deux phases
- [[kv-cache]] — RadixAttention attaque le prefix caching
- [[file-formats-llm]] — safetensors / HF par défaut
- [[serving-modes-llm]] — production hostile = son terrain
- [[ahmad-osman-inference-engines-2026]] — source principale

## My take

Le **bon outil quand le serving devient un problème de scheduling**, pas un problème de fit. La prefill-decode disaggregation est l'innovation qui sépare SGLang de vLLM — pas une feature cosmétique mais un changement d'architecture qui rend possible des SLA latency tenables sous trafic mixte. À garder en backpocket pour le jour où *"vLLM marche mais nos p99 tank quand des longs prompts arrivent en pleine session decode"*. Pour le reste, [[vllm]] reste le default raisonnable.

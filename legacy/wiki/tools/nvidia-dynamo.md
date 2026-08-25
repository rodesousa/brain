---
type: entity
summary: Couche d'orchestration distributed au-dessus de vLLM/SGLang/TensorRT-LLM — disaggregation, routing intelligent, multi-tier KV caching, autoscaling. Pour quand single-engine ne suffit plus.
lifecycle: draft
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
tags:
  - inference-engines
  - orchestration
  - production-serving
---

**NVIDIA Dynamo** est une couche d'**orchestration distribuée** qui s'installe **au-dessus** des engines de serving comme [[vllm]], [[sglang]], [[tensorrt-llm]]. Ce n'est pas un engine — c'est le "scheduler de scheduler" qui coordonne une fleet.

## Sweet spot

**Quand single-engine ne suffit plus.** Multi-node, multi-engine, trafic mixte, besoins de routing et d'autoscaling au niveau fleet.

## Features

- **Disaggregated prefill/decode** au niveau fleet — instances spécialisées, transfert KV cache inter-node
- **Intelligent routing** — direction des requêtes vers l'engine et le node les plus appropriés (KV-aware, longueur de prompt, etc.)
- **Multi-tier KV caching** — KV cache à plusieurs niveaux (GPU HBM, RAM, NVMe…) pour amortir long context et conversations
- **Autoscaling** — instances montent/descendent selon le trafic
- **Au-dessus de [[vllm]], [[sglang]], [[tensorrt-llm]]** — pas de lock-in sur un engine spécifique

## Recettes hardware

- **8×H100 / H200 node** : Dynamo quand multi-node orchestration devient nécessaire
- **B200 / GB200 / GB300 infrastructure** : Dynamo pour fleet-level orchestration, KV-aware routing, autoscaling

## Quand préférer rester sur single-engine

- < 8 GPUs → [[vllm]] ou [[sglang]] solo suffit
- Workload homogène, pas de besoin de routing intelligent
- Pas de multi-node, pas de fleet
- Pas d'autoscaling

## Verdict d'Ahmad

> NVIDIA Dynamo is a distributed orchestration layer above engines, supporting disaggregation, intelligent routing, and multi-tier KV caching. **Use it when single-engine serving is no longer enough.**

## Related

- [[vllm]] — engine sous-jacent supporté
- [[sglang]] — engine sous-jacent supporté
- [[tensorrt-llm]] — engine sous-jacent (intégration tight via Python API)
- [[llm-runtimes]] — comparaison wiki
- [[kv-cache]] — multi-tier KV caching est sa différenciation
- [[prefill-vs-decode]] — disagg au niveau fleet
- [[serving-modes-llm]] — production fleet est son terrain
- [[ahmad-osman-inference-engines-2026]] — source principale

## My take

Le **toit de la stack** chez NVIDIA. À considérer uniquement à scale **fleet** — ≥8 GPUs, multi-node, traffic mixte avec longs contextes et autoscaling. Pour les équipes plus petites, c'est une complexité qui ne paie pas — un [[vllm]] bien tuné fait largement le job. C'est aussi le signal que le serving LLM est en train de **se ressembler à du distributed computing classique** : à scale, ton problème n'est plus "quel engine" mais "comment je route, scale, et invalide les caches entre 50 instances". Dynamo addresse ce niveau.

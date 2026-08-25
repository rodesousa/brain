---
type: concept
summary: Scheduling pattern où les requêtes entrent et sortent du batch en cours d'exécution — vs static batching qui attend que tout un batch termine. Foundation du serving multi-user moderne.
lifecycle: draft
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - continuous-batching
  - inference-engines
  - serving-modes
---

**Continuous batching** (parfois *in-flight batching* ou *dynamic batching*) est le scheduling pattern où des requêtes **entrent et sortent du batch en cours d'exécution**, vs le static batching classique qui attend qu'un batch entier termine avant d'en démarrer un nouveau.

## Le problème : static batching gaspille

En static batching, un batch de N requêtes attend que la **plus longue** termine pour libérer les slots. Si 7 requêtes finissent en 10 tokens et 1 en 500 tokens, les 7 slots restent **bloqués** pendant 490 tokens de decode pour un seul utilisateur. Catastrophique en serving multi-user.

## La solution : flux continu

À chaque step de decode :
1. Les requêtes qui ont fini libèrent leur slot immédiatement
2. Les nouvelles requêtes en file d'attente peuvent **rejoindre** le batch en cours
3. Pas d'attente "que tout finisse" — c'est un flux

Conséquences :
- **GPU utilization** drastiquement améliorée (rarement < 80% sous charge)
- **Throughput** doublé ou triplé selon la distribution de tailles
- **Latency** plus prévisible — la queue ne s'engorge plus derrière la requête longue

## Combiné avec d'autres techniques

Continuous batching seul ne suffit pas — il combine typiquement avec :

- **[[paged-attention]]** — sinon le KV cache fragmenté empêche les requêtes courtes de rejoindre le batch
- **Chunked prefill** — sinon un long prefill bloque tout le batch
- **Prefix caching** — partage entre requêtes qui s'ouvrent pareil

## Engines qui le supportent

- **[[vllm]]** — natif depuis le début
- **[[sglang]]** — natif
- **[[tensorrt-llm]]** — natif
- **[[llama-cpp]]** server — supporté
- **[[exllamav2]]** / [[exllamav3]] — dynamic batching natif

## Limites

- **Single-user local** — ne sert à rien, il n'y a pas de batch à animer
- **Modèles MoE** — l'expert routing varie par token, l'efficacité du batching dépend des active experts

## Note : "à scale, c'est la base"

> Supporting batching is not the same as **behaving like a production-ready scheduler**. — Ahmad

Un engine peut "supporter le batching" sans avoir un scheduler de qualité production : fairness, admission control, gestion de la starvation, isolation entre tenants.

## Related

- [[paged-attention]] — l'infrastructure mémoire qui rend le continuous batching efficient
- [[kv-cache]] — chaque requête active a son KV
- [[vllm]] — implémentation référence
- [[sglang]] — implémentation avec disagg native
- [[tensorrt-llm]] — natif
- [[llama-cpp]] — supporté côté server
- [[exllamav2]], [[exllamav3]] — dynamic batching natif
- [[inference-bottlenecks]] — scheduler quality est un des 5 bottlenecks
- [[llm-runtimes]] — comparaison engines, technique mentionnée
- [[serving-modes-llm]] — pertinent dès le mode team-API
- [[ahmad-osman-inference-engines-2026]] — source principale

## My take

L'autre **innovation système** du serving LLM (avec [[paged-attention]]) qui a transformé la perf en production. Conceptuellement c'est un classique : *async scheduling* appliqué au domaine inference. La nuance d'Ahmad est précieuse : "supporter le continuous batching" n'est pas un binaire — c'est une qualité de scheduler qui se voit sous charge mixte, pas dans une demo bien rangée. Tester avec ta vraie distribution de prompts est non-négociable.

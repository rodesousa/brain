---
type: concept
summary: Trois modes de serving LLM — single-user local, team API privée, production. Trois jobs différents avec trois ensembles de préoccupations ops.
lifecycle: verified
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
tags:
  - serving-modes
  - local-llm-deployment
  - llm-runtimes
---

Trois modes de serving, trois jobs distincts avec des préoccupations très différentes.

## 1. Single-user local

Desktop app, CLI stack, ou serveur 1-user.

**Outils** : Harbor, LM Studio, [[llama-cpp]] server, ExLlamaV2 / TabbyAPI, scripts Transformers.

**Goal** : itération rapide. Comparer comportement, vitesse, mémoire, prompt formats. Pas besoin d'ops platform.

**Préoccupations** : ce qui fit en VRAM, le bon [[chat-template]], la qualité sur tes prompts à toi.

## 2. Team / private API

OpenAI-compatible endpoint sur workstation ou serveur partagé.

**Outils** : [[vllm]], [[sglang]], [[tensorrt-llm]], [[llama-cpp]] server selon taille modèle et throughput.

**Goal** : plusieurs personnes ou jobs partagent le modèle. Tu deviens un mini-service.

**Préoccupations qui s'ajoutent** :
- Monitoring (latency, throughput, errors)
- Prompt / version management
- Routing entre modèles
- Mesure de latency réaliste sous charge
- API auth basique

## 3. Production

Un autre métier. La conversation explose.

**Outils** : [[vllm]], [[sglang]], [[tensorrt-llm]] à scale, Triton, NVIDIA Dynamo pour orchestration multi-engine, custom.

**Préoccupations supplémentaires** :
- Continuous batching
- Prefix caching
- [[speculative-decoding]]
- PagedAttention
- Tensor parallelism, pipeline parallelism
- Quantized serving
- Structured outputs
- Load balancing
- GPU utilization
- Latency percentiles (p50, p95, p99)
- Prompt caching
- Admission control
- Logging, failover
- Privacy, cost controls

> À production scale, "*can I load the model?*" est la question facile. La vraie question est "*can I serve it reliably under real traffic?*"

## Implications de choix

| Mode | Question principale | Outils typiques |
|---|---|---|
| Single-user | "Ce modèle fit-il ?" | LM Studio, [[llama-cpp]] |
| Team | "Ça scale jusqu'à 10 users ?" | [[vllm]], [[sglang]] |
| Production | "p99 sous 50 RPS ?" | [[vllm]]+, [[tensorrt-llm]], Dynamo, ops platform |

> Ahmad : **local engine ≠ production server**. llama.cpp server est capable, MLX-LM convenient, Ollama plaisant — *aucun* n'est un prod server. Production = sécurité + observability + backpressure + routing + autoscaling + SLA. NE PAS confondre.

## Related

- [[llm-runtimes]] — chaque mode a ses outils privilégiés
- [[local-llm-growth-path]] — progression entre les modes
- [[local-llm-runbook]] — checklist ops pour passer à team ou prod
- [[llm-eval-methodology]] — comment mesurer avant de prod
- [[vllm]], [[sglang]], [[tensorrt-llm]] — engines des modes team/prod
- [[llama-cpp]] — engine single-user et team API limité
- [[mlx]] — engine Mac single-user (server pas prod)
- [[exllamav2]] — engine single-user enthusiast
- [[mlc-llm]] — engine edge (mode hors des 3 standards)
- [[ollama]] — wrapper NE PAS UTILISER
- [[nvidia-dynamo]] — orchestration fleet au-dessus
- [[continuous-batching]] — pertinent dès le mode team-API
- [[ahmad-osman-inference-engines-2026]] — bottlenecks et opinions sur prod vs local

## My take

Ce découpage en 3 niveaux est utile pour ne pas sur-architecturer. Beaucoup de gens lancent vLLM + monitoring + load balancer pour un usage personnel, ce qui revient à un setup ops trop lourd pour le besoin réel. À l'inverse, passer à 5 users sur un llama.cpp server craque vite.

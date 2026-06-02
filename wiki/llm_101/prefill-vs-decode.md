---
type: concept
summary: Deux régimes de performance distincts pendant l'inférence — prefill traite le prompt en parallèle (compute-bound), decode génère un token à la fois (memory-bandwidth-bound).
lifecycle: verified
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
  - raw/web/memory-bandwidth-for-local-ai-hardware-2026.md
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
tags:
  - inference-mechanics
  - memory-bandwidth
  - prefill-decode
  - kv-cache
---

L'inférence LLM se déroule en **deux phases avec des contraintes hardware opposées**.

## Prefill

Traitement du prompt utilisateur. Si tu colles 20 000 tokens, le modèle doit tous les processer avant de pouvoir produire le premier token de réponse.

- **Parallélisable** : tous les tokens du prompt sont traités ensemble
- **Compute-bound** : c'est le GPU FLOPs qui domine
- Construit le [[kv-cache]] qui sera relu pendant le decode
- C'est la phase qui détermine le **time-to-first-token (TTFT)**

## Decode

Génération des tokens de réponse, un à la fois.

- **Séquentiel** : chaque nouveau token dépend de tous les précédents
- **Memory-bandwidth-bound** : le GPU stream les weights repeatedly à chaque token, donc c'est la bande passante mémoire qui domine, pas les FLOPs
- C'est la phase qui détermine les **tokens/seconde** ressentis pendant que l'utilisateur lit

## Conséquences

| Workload | Bottleneck principal |
|---|---|
| Prompt long, réponse courte | Prefill — TTFT lent |
| Prompt court, réponse longue | Decode — streaming lent |
| Conversation longue | Les deux — le KV cache grossit à chaque tour |

C'est pour ça que **deux GPUs avec la même VRAM peuvent avoir des tokens/sec très différents** si leurs bandes passantes diffèrent. Decode aime la bandwidth, pas les FLOPs. Voir [[memory-bandwidth]] pour les tiers 2026.

## Implications de tuning

- **Prefill lent** ? Raccourcir le prompt, utiliser prefix caching (réutilisation du KV cache d'une partie commune), améliorer le retrieval pour donner moins de context inutile.
- **Decode lent** ? Vérifier memory bandwidth, quantization (weights plus petits = moins de bytes à stream), CPU spill (catastrophique), attention kernels, support speculative decoding.

## Speculative decoding (acceleration decode)

Un drafter cheap propose plusieurs tokens, le target model verify en un forward pass. Méthodes 2026 : EAGLE, MTP, DFlash (block diffusion), DDTree (draft tree).

Ne réduit pas la mémoire KV — attaque uniquement la latency.

## Disaggregation prefill/decode

Engines récents ([[sglang]], [[tensorrt-llm]]) **séparent prefill et decode sur des instances spécialisées** et transfèrent le KV cache entre elles. Évite qu'un long prefill batch bloque le decode des autres requêtes. À scale, c'est ce qui tient les p95/p99 sous trafic mixte.

## Related

- [[kv-cache]] — construit en prefill, relu en decode
- [[attention-variants]] — l'attention est appelée dans les deux phases
- [[decoding-policies]] — c'est la couche au-dessus du decode brut
- [[vram-math]] — comprendre les régimes aide à budgéter
- [[memory-bandwidth]] — bandwidth domine decode, FLOPs dominent prefill
- [[llm-runtimes]] — les engines orchestrent ces deux phases
- [[sglang]] — disaggregation native
- [[tensorrt-llm]] — disagg + Wide EP au niveau prefill
- [[inference-bottlenecks]] — workload shape → bottleneck
- [[nvidia-dynamo]] — disagg au niveau fleet
- [[ahmad-osman-memory-bandwidth-2026]] — Part 2 (la dimension bandwidth)
- [[ahmad-osman-inference-engines-2026]] — Part 3 (le scheduling au niveau engine)

## My take

La distinction prefill/decode est la deuxième vérité après le KV cache pour comprendre la perf locale. Quand quelqu'un dit "ce modèle est lent", il faut toujours demander **lent comment** : lent à démarrer (prefill) ou lent à streamer (decode) ? Les remèdes ne sont pas les mêmes.

---
type: concept
summary: Technique d'accélération du decode — un drafter cheap propose plusieurs tokens à l'avance, le target model verify en un seul forward pass. N'aide pas la mémoire KV.
lifecycle: verified
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
tags:
  - speculative-decoding
  - inference-mechanics
  - decode-latency
---

Le **speculative decoding** attaque la latency de decode (token-par-token séquentiel) en faisant **drafter plusieurs tokens à l'avance par un modèle cheap**, puis en les **vérifiant en un seul forward pass** du target model.

## Pourquoi ça aide

Decode normal = 1 forward pass du gros modèle = 1 token. Avec spéculation, 1 forward pass peut **valider plusieurs tokens** si le drafter a bien deviné. Le speedup dépend du taux de match draft/target.

## Méthodes 2026

- **EAGLE-style** — drafter intégré, prédit plusieurs tokens
- **MTP** (multi-token prediction) — variante d'objectif de training qui aide la spéculation
- **DFlash** — block diffusion comme drafter
- **DDTree** (ou DTree) — construit un arbre de drafts et le vérifie efficacement

## Ce que ça ne fait PAS

- **Ne réduit pas la mémoire KV** ([[kv-cache]]) — c'est un speedup decode pur
- **Ne réduit pas le compute total** — au contraire, ajoute le coût du drafter
- **N'est utile que si le runtime le supporte cleanly** — paper speedups ≠ feature desktop

## Quand l'utiliser

- Quand le decode est le bottleneck visible (streaming lent)
- Quand le runtime supporte la méthode ([[vllm]], [[sglang]], [[tensorrt-llm]])
- Quand le target model a un drafter disponible (modèle small de la même famille, ou drafter intégré comme EAGLE)

À ne pas confondre avec la [[kv-cache]] quantization, qui attaque la mémoire, pas la latency.

## Related

- [[prefill-vs-decode]] — pourquoi le decode est séquentiel et donc accélérable
- [[decoding-policies]] — la couche au-dessus, qui choisit le token final
- [[llm-runtimes]] — le support varie par runtime
- [[kv-cache]] — orthogonal, mémoire ≠ latency
- [[vllm]], [[sglang]], [[tensorrt-llm]], [[llama-cpp]], [[exllamav2]] — les engines qui le supportent
- [[ahmad-osman-inference-engines-2026]] — bottleneck taxonomy

## My take

Plus mature en serving qu'en desktop. Pour un single-user local, le gain est réel mais marginal vs un changement de quantization ou un modèle plus petit. À considérer sérieusement seulement quand tu serves plusieurs users en parallèle et que tu cherches du ratio coût/latency.

---
type: concept
summary: MHA, MQA, GQA — trois designs d'attention qui font varier dramatiquement la taille du KV cache à context égal, indépendamment du nombre de paramètres.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - attention-variants
  - inference-mechanics
  - kv-cache
  - transformer-architecture
---

Trois variantes d'attention dominent en 2026, distinguées par **comment les query heads partagent (ou pas) leurs key/value heads** :

| Variante | Sharing | KV cache | Expressivité |
|---|---|---|---|
| **MHA** (multi-head) | 1 KV head par query head | Gros | Max |
| **MQA** (multi-query) | 1 seul KV head pour tous les queries | Très petit | Plus contraint |
| **GQA** (grouped-query) | Groupes de queries partagent 1 KV head | Moyen | Compromis |

GQA est devenu le **middle ground standard** des modèles locaux récents : il préserve la qualité tout en réduisant dramatiquement le [[kv-cache]].

## Conséquence pratique

Deux modèles 7B peuvent se comporter très différemment à long context :
- 7B **MHA** à 128K → peut épuiser un GPU 24 GB
- 7B **GQA** au même context → fit avec marge

**Comparer des modèles par parameter count seul est trompeur.** Il faut regarder : type d'attention, nombre de kv_heads, context length supporté, et support runtime.

## Kernels modernes

Indépendamment de la variante, des implémentations comme **FlashAttention** et SDPA-style réduisent le memory traffic et keep le GPU busy. Un runtime avec de bons kernels peut être **dramatiquement plus rapide** qu'un autre sur le même modèle et la même carte.

## Related

- [[kv-cache]] — la principale conséquence du choix MHA/MQA/GQA
- [[prefill-vs-decode]] — l'attention est exécutée dans les deux phases, mais coûte différemment
- [[vram-math]] — le KV cache impacte directement la VRAM dispo

## My take

C'est l'exemple parfait que "paramètre count" ne suffit pas pour évaluer un modèle local. Un 7B GQA dans une bonne runtime peut être plus utilisable qu'un 13B MHA dans une moins bonne. À mettre en avant quand quelqu'un demande "quel modèle pour ma carte ?"

---
type: source-summary
summary: Part 2 trilogie Ahmad Osman — bandwidth ≠ capacity, 5 tiers de bande passante (1.8 TB/s → <150 GB/s), pourquoi "fitting ≠ serving" décide entre Apple unified et NVIDIA discrete.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/web/memory-bandwidth-for-local-ai-hardware-2026.md
tags:
  - memory-bandwidth
  - local-llm-deployment
  - hardware-tiers
---

Deuxième volet de la trilogie d'Ahmad Osman. Couvre la **couche débit** — le facteur que beaucoup confondent avec la capacité et qui décide en pratique si la machine "respire" ou "decode dans du ciment mouillé à 3 tok/s".

## Le mental model

> Local AI hardware = **capacity × bandwidth × software stack**

- **Capacity** : ce qui rentre — couvert par [[vram-math]] et [[ahmad-osman-gpu-memory-math-2026]]
- **Bandwidth** : à quel point la machine peut "respirer" — sujet de cette page, voir [[memory-bandwidth]]
- **Software stack** : combien du spec sheet tu peux réellement cash out — Part 3, [[ahmad-osman-inference-engines-2026]]

> "fitting ≠ serving" — un 32GB RTX 5090 peut outrun un Mac unified-memory bien plus gros, et inversement le Mac Studio M3 Ultra peut être *la* bonne réponse quand le modèle n'entre simplement pas dans une VRAM consumer (mais beaucoup plus lent pour multi-agentic).

## Les 5 tiers de bandwidth 2026

| Tier | Hardware | Bandwidth |
|---|---|---|
| **1.8 TB/s** | RTX PRO 6000 Blackwell, RTX 5090 | 1792 GB/s |
| **800 GB/s** | Mac Studio M3 Ultra | 819 GB/s |
| **450-650 GB/s** | Mac Studio M4 Max (546), MacBook Pro M5 Max (460-614), AMD AI PRO R9700 (640), Tenstorrent Blackhole p150 (512) | |
| **250-300 GB/s** unified | DGX Spark (273), Mac mini M4 Pro (273), Ryzen AI Max / Strix Halo (256) | |
| **<150 GB/s** thin-and-light | MacBook Air M5 (153), Snapdragon X Elite (135), Intel Lunar Lake (136), Snapdragon X2 Elite (152-228) | |

## Les paradigmes hardware

**Discrete GPU (NVIDIA-dominant)** — bandwidth king si le modèle fit, ou en pool via NVLink/PCIe Gen 5 avec tensor parallelism. Perd quand le modèle ne fit pas.

**Apple unified memory** — *OK bandwidth + capacity together*. M3 Ultra : 819 GB/s + jusqu'à **512 GB** mémoire unifiée. Gagne quand tu veux **un seul box, silencieux, beaucoup de mémoire, sans sharding multi-GPU**. Perd quand raw tok/sec et concurrency dominent.

**DGX Spark** — 128 GB unified @ 273 GB/s. Bandwidth pas impressionnante. Mais coherent memory + CUDA stack = appliance developer NVIDIA. NVFP4 support à maturer.

**Strix Halo / Ryzen AI Max** — premier vrai contender x86 unified-memory : 256-bit LPDDR5X, 128 GB max, ~256 GB/s, ~96 GB exposable en GPU memory. Framework Desktop pertinent ici.

**Tenstorrent** — Wormhole n300 (24 GB @ 576 GB/s), Blackhole p150 (32 GB @ 512 GB/s + 800G interconnect). Stack 100% OSS — wildcard à surveiller.

## Le piège "AI PC"

La plupart des AI PC sont **bandwidth-starved** : Snapdragon X Elite (135 GB/s), Lunar Lake (136 GB/s), MacBook Air M5 (153 GB/s). OK pour petits modèles, assistants, edge. **Pas pour 9B dense playground, multi-agent serious, long-context stress.**

## Pourquoi un gros boîtier peut sembler lent

Même si ça fit, tu paies encore : bandwidth pendant decode ([[prefill-vs-decode]]), KV cache growth ([[kv-cache]]), dequantization, batching + concurrency, scheduler quality, framework overhead. **"It runs" = demo, "it serves" = system design.**

## Multi-GPU n'est pas linéaire

Plus de GPUs ≠ scaling linéaire. Tu achètes : interconnect (PCIe vs NVLink vs RDMA), topology, sync overhead, software maturity.

## Le mental model final

Trois questions, dans l'ordre :
1. **What must fit?** → capacity
2. **What bandwidth tier do I need?** → débit
3. **What software stack can actually deliver it?** → engines, voir Part 3

Bluntly :
- NVIDIA → fastest raw speed
- Apple Ultra → biggest one-box memory
- Strix Halo → first real x86 unified-memory play
- DGX Spark → coherent NVIDIA appliance
- AMD / Intel Arc → rising alternatives
- Tenstorrent → fully opensource stack

Le shift : pas *"which hardware is best?"* mais ***"which bottleneck am I buying?"***

## Related

- [[memory-bandwidth]] — concept du wiki ouvert par cette source
- [[vram-math]] — la dimension capacity, complémentaire
- [[kv-cache]] — stream pendant decode, partie de la bandwidth load
- [[prefill-vs-decode]] — bandwidth domine en decode, FLOPs en prefill
- [[llm-runtimes]] — le software extrait (ou non) la bandwidth disponible
- [[mlx]] — paradigme Apple unified memory
- [[inference-bottlenecks]] — bandwidth = bottleneck #1
- [[ahmad-osman-gpu-memory-math-2026]] — Part 1 (capacity)
- [[ahmad-osman-inference-engines-2026]] — Part 3 (engines)

## My take

La distinction **capacity ≠ bandwidth** est la deuxième révélation après le KV cache pour comprendre pourquoi le hardware local LLM est devenu un terrain miné. Cette source justifie à elle seule la création de la page [[memory-bandwidth]] — le concept manquait sérieusement au wiki existant (mentionné en tag, jamais en page). Le tableau par-tier est aussi la meilleure réponse rapide à "*je devrais acheter un Mac Studio Ultra ou un RTX 5090 ?*" — la réponse honnête est "ça dépend de qui de capacity ou bandwidth est ton bottleneck", et ce qui débloque la conversation c'est de **savoir nommer ces deux axes**.

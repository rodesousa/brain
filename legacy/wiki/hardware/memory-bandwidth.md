---
type: concept
summary: Bande passante mémoire — débit auquel le GPU peut lire ses propres weights. Détermine la vitesse de decode, distinct de la VRAM capacity qui détermine ce qui fit.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/web/memory-bandwidth-for-local-ai-hardware-2026.md
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - memory-bandwidth
  - hardware-tiers
  - local-llm-deployment
---

La **memory bandwidth** est le débit auquel un accélérateur peut lire ses weights depuis sa mémoire. Exprimée en GB/s ou TB/s. C'est le facteur qui décide si une machine "respire" ou décode dans du ciment mouillé.

## Capacity vs bandwidth — le confusion principal

| Dimension | Décide | Métrique |
|---|---|---|
| **Capacity** | Ce qui fit | GB de VRAM / mémoire unifiée |
| **Bandwidth** | À quelle vitesse | GB/s ou TB/s |

> Un 32 GB RTX 5090 et un 96 GB RTX PRO 6000 Blackwell **ont la même bandwidth** (1792 GB/s). Le second peut loader des modèles bien plus gros, mais une fois qu'un modèle fit dans 32 GB, ils décodent à la même vitesse.

Inversement, le Mac Studio M3 Ultra (819 GB/s, 512 GB unified) peut **fit** un modèle énorme qu'aucun RTX consumer ne pourrait charger, mais ne **sert** pas aussi vite.

## Pourquoi la bandwidth domine le decode

Voir [[prefill-vs-decode]] :
- **Prefill** : compute-bound (parallel sur tous les tokens du prompt) → FLOPs comptent
- **Decode** : memory-bandwidth-bound (séquentiel, stream les weights à chaque token) → **bandwidth domine**

Single-user tokens/sec = à 80% un proxy de la memory bandwidth, à condition que le modèle fit et que le runtime soit bien réglé.

## Les 5 tiers de bandwidth 2026

| Tier | Exemples | Bandwidth |
|---|---|---|
| **1.8 TB/s** | RTX PRO 6000 Blackwell, RTX 5090, H100 SXM (3.35 TB/s HBM3) | 1792 GB/s |
| **800 GB/s** | Mac Studio M3 Ultra | 819 GB/s |
| **450-650 GB/s** | Mac Studio M4 Max (546), MacBook Pro M5 Max (460-614), AMD AI PRO R9700 (640), Tenstorrent Blackhole p150 (512) | |
| **250-300 GB/s** unified | DGX Spark (273), Mac mini M4 Pro (273), Ryzen AI Max / Strix Halo (256) | |
| **<150 GB/s** thin-and-light | MacBook Air M5 (153), Snapdragon X Elite (135), Intel Lunar Lake (136), Snapdragon X2 Elite (152-228) | |

**Pivot points** :
- ≤150 GB/s = thin-and-light, viable pour 1B-4B
- ~250-300 GB/s = unified memory commence à devenir intéressant
- 450-650 GB/s = workstation tier sérieux
- 800+ GB/s = expensive, powerful, fun

## Discrete GPU vs unified memory

**Discrete GPU (NVIDIA dominant)** :
- HBM (High Bandwidth Memory) ou GDDR rapide
- Bandwidth king *si le modèle fit*
- Sinon : pooling via NVLink (server-side surtout) ou PCIe Gen 5 avec tensor parallelism
- Perd violemment quand le modèle ne fit pas

**Apple unified memory** :
- CPU et GPU partagent le même pool
- M3 Ultra : 819 GB/s + **512 GB de mémoire**
- Capacity superpower : peut fit des modèles impossibles sur consumer NVIDIA
- Pas HBM-tier en bandwidth — plus lent que RTX PRO 6000 sur decode
- Gagne quand un seul box / silence / grosses mémoires / pas de sharding multi-GPU prime

## Pourquoi un gros boîtier peut sembler lent

Même si ça fit, tu paies encore :
- Bandwidth pendant decode
- KV cache growth ([[kv-cache]])
- Dequantization si le format ne match pas le runtime
- Batching + concurrency
- Scheduler quality
- Framework overhead

> *"It runs"* = demo. *"It serves"* = system design.

## Cas spécial : DGX Spark

128 GB unified @ 273 GB/s. Bandwidth pas impressionnante — c'est un appliance developer pour CUDA + memory coherence, pas un raw monster. NVFP4 support encore à maturer.

## Cas spécial : Strix Halo / Ryzen AI Max

Premier vrai contender x86 unified-memory : 256-bit LPDDR5X, jusqu'à 128 GB, ~256 GB/s, ~96 GB exposable en GPU memory. Framework Desktop pertinent ici.

## Le piège AI PC

Lunar Lake, Snapdragon X Elite, MacBook Air M5 : 135-153 GB/s. **Pas faute, mais clairement pas en compétition avec workstation GPUs**. OK pour 1B-4B, assistants, edge. **Pas pour 9B dense playground sérieux ni multi-agent ni long-context stress.**

## Multi-GPU n'est pas linéaire

Plus de GPUs ≠ scaling linéaire. Tu achètes en plus : interconnect type (PCIe vs NVLink vs RDMA), topology, sync overhead, software maturity. Voir Part 3 d'Ahmad pour le traitement détaillé.

## Mental model

Trois questions, dans l'ordre :
1. **What must fit ?** → capacity, voir [[vram-math]]
2. **What bandwidth tier do I need ?** → cette page
3. **What software stack can actually deliver it ?** → [[llm-runtimes]]

Et le shift : pas *"which hardware is best ?"* mais ***"which bottleneck am I buying ?"***

## Related

- [[vram-math]] — la dimension complémentaire (capacity)
- [[prefill-vs-decode]] — decode bandwidth-bound, prefill compute-bound
- [[kv-cache]] — bandwidth pendant decode lit weights ET KV cache
- [[quantization-llm]] — weights plus petits = moins de bytes à stream
- [[llm-runtimes]] — le software extrait (ou non) la bandwidth disponible
- [[vllm]] — engine production qui exploite la bandwidth
- [[mlx]] — paradigme Apple unified memory
- [[inference-bottlenecks]] — bandwidth est le bottleneck #1
- [[ahmad-osman-gpu-memory-math-2026]] — la dimension capacity (Part 1)
- [[ahmad-osman-memory-bandwidth-2026]] — la source principale (Part 2 trilogie)
- [[ahmad-osman-inference-engines-2026]] — Part 3, le software layer
- [[glm]] — pourquoi GLM-5.2 local plafonne à 3–9 tok/s
- [[ofox-glm-5-2-local-2026]] — illustration : 3–9 tok/s en 2-bit sur Mac 256 GB

## My take

C'est **la deuxième révélation après le KV cache** pour comprendre la perf locale. La phrase à retenir : *"capacity decides what fits, bandwidth decides how hard the box can breathe, software decides how much of that you actually see"*. Énormément de débats hardware ("Mac Studio ou RTX 5090 ?") deviennent simples une fois qu'on nomme ces deux axes séparément — la réponse honnête c'est presque toujours "lequel est ton bottleneck ?". Si je devais ne garder qu'un seul tier en tête, ce serait **300 GB/s = seuil unified memory qui devient intéressant** et **1.5 TB/s = HBM/GDDR rapide où le decode commence à être bridé par autre chose que la mémoire**.

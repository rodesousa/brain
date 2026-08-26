---
summary: FreeToken (FlashML) — moteur de serving MoE edge-native qui fait tourner des modèles frontière (284B-753B) sur PC de jeu / laptop, via CPU-GPU co-execution bandwidth-adaptive, LRU expert cache et caching sémantique. Apache 2.0, arXiv 2608.16157.
created: 2026-08-26
updated: 2026-08-26
sources:
  - sources/freetoken-repo.md
keywords: [freetoken, flashml, moe, inference, serving, edge, offload, hybrid, deepseek-v4, qwen3.6, glm-5.2, llm-local, gpu, tok/s, ttft]
---

# FreeToken

## TL;DR

Moteur d'inférence MoE « edge-native » de FlashML (~8k stars, Apache 2.0) : il sert des modèles
MoE open-weight frontière (284B sur gaming desktop, 753B GLM-5.2 sur GPU workstation, 35B sur
laptop 8GB) sur du matériel perso. L'idée centrale : plutôt qu'une stratégie d'offload fixe, il
mappe continuellement computation + état du modèle sur GPU/CPU/RAM selon la bande passante réelle
(politique q*). APIs OpenAI + Anthropic, branchable sur les agents de code (dont `hermes`).

## Points clés

### Backends MoE (le cœur)
- **fused** — experts résidents GPU (besoin de VRAM).
- **offload** — experts en RAM host, LRU cache de slots sur GPU ; misses streamées en PCIe.
- **cpu** — misses calculées sur CPU au lieu d'être fetchées.
- **hybrid** — par step : une partie des misses fetchée en PCIe, le reste calculé sur CPU,
  overlappé. Split calibré par `ft bench bw` (profil JSON par GPU, règle : hybrid si bande
  passante kernel CPU > 2x bande PCIe).
- **auto** — dense → fused ; MoE → offload, upgradé hybrid si profil dispo.

### Autres briques techniques
- **Format FTW** (fast weight) : conversion optionnelle de checkpoint pour chargement rapide.
- **Prefill streaming double-buffered** full-layer (cache expert qui se remplit pendant le prefill).
- **Semantic-anchor caching** : checkpoints sur état récurrent (GDN) + KV pour que les edits de
  contexte agentiques (tool calls, thinking) ne recomputent pas.
- **Élasticité mémoire** : re-allocation VRAM runtime entre expert cache et KV, sans restart.
- **Attention** : backends trtllm / fi / fa / triton / dsv4_sparse / dsa ; KV radix + variantes
  hybrid-radix (GDN linear state) et SWA.
- **Serveur** : OpenAI `/v1/chat/completions`, `/v1/responses`, Anthropic `/v1/messages`, daemon
  systemd, CLI `ft serve|shell|ctl|launch|checkpoint|bench bw` (port 1919).
- **`ft launch`** : branche Claude Code / Codex / hermes / OpenClaw / OpenCode sur le serveur.

### Modèles supportés
DeepSeek-V4-Flash, GLM-5.2/4.7 (NVFP4), Qwen3.6-35B-A3B (+FP8/NVFP4), Qwen3.5/3-MoE,
gpt-oss-120b/20b, Gemma-4 (dont GGUF natif), MiniMax-M2.5, Muse-Glimmer-30B. Quantifs MXFP4,
NVFP4, FP8, BF16. Chargement HF safetensors + GGUF.

## Chiffres (paper, auto-évalués)

### Mécanique du trade-off vitesse/offload
- Décode : chaque token ne touche que les experts routés (DSV4-Flash : 6/256 experts/layer, 13B actifs
  sur 284B) → seuls les misses du LRU cache passent par PCIe/CPU. Miss rate sur 5090 : 16% (Qwen3.6),
  39% (DSV4) vs 41–62% (KTransformers), 62–89% (llama.cpp).
- Politique q\* (decode) : q\* = m × B_P/B_H — répartit les m misses entre fill PCIe et exécution CPU,
  overlappés → latence par layer ≈ max(transfert, calcul), pas la somme. B_P/B_H mesurés par `ft bench bw`.
- Prefill : l'union des routes ≈ tous les experts → ~64–140 GB streamés. Double buffering full-layer :
  chunk 8192 tokens en ~1.2s (plafond PCIe 5.0, 52.7 GB/s). Sans lui : −19 à −26% de throughput.

### Débits publiés
- RTX 5090 : Qwen3.6-35B-A3B (BF16) **77–83 tok/s** ; DeepSeek-V4-Flash (MXFP4, 284B) **22–25 tok/s**.
  1.5–2.3x les meilleurs baselines (llama.cpp, Ollama, KTransformers, MoE-Infinity).
- RTX 4060 laptop 8GB (PCIe x8) : Qwen3.6 NVFP4 **39.3 tok/s** — > médian Codex prod (33 tok/s), 92% du 4090.
- RTX PRO 6000 (96GB) : GLM-5.2 (753B, NVFP4) **14.9 tok/s** vs 7.3 llama.cpp (2x), TTFT comparable (7.5 vs 7.8s).
- Gaming desktop 32GB : DSV4-Flash (284B) servi interactivement.
- Stabilité agentic : décode dans 12% du single-turn ; TTFT worst-case < 44s vs baselines > 150s
  (llama.cpp 232s, Ollama 179s, KTransformers 946s — au-delà des timeouts des clients agents).

## Notes d'évaluation

- ~72k LOC Python (329 fichiers), 98 tests, dev rapide (40 commits), workflow CI pypi wheels.
- Contrib : PRs agents purs refusés ; résultats perf doivent être A/B e2e sur matériel réel.
- Filiation : mini-sglang → sglang, vLLM, FlashInfer, flash-linear-attention, LightLLM, llama.cpp.
- Intérêt perso : DeepSeek-V4-Flash supporté nativement (modèle que j'utilise via provider nous) ;
  `ft launch hermes` le rend branchable sur le workflow Munder Difflin.

## Voir aussi

- [[munder_difflin]] — harness multi-agents ; FreeToken peut servir de backend local (`ft launch hermes`).
- Source brute : [[freetoken-repo]]
- Paper : arXiv 2608.16157 — « FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution »

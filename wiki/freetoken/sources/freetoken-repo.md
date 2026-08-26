# Source — repo FreeToken (FlashML-org/FreeToken)

Extrait brut de l'analyse du repo (2026-08-26, commit 9ef3651, v0.1.2) + abstract du papier.

## Repo

- https://github.com/FlashML-org/FreeToken — Apache 2.0, ~8k stars, 690 forks, 40 commits, v0.1.2.
- ~72 000 LOC Python (329 fichiers), 98 fichiers de tests. Desktop app (Windows/Linux) via flashml.ai.
- Inspiré de mini-sglang ; code réutilisé de SGLang, vLLM, FlashInfer, flash-linear-attention,
  LightLLM, llama.cpp.

## README — fonctionnalités

- Fast edge-native runtime : MoE serving avec CPU–GPU co-execution bandwidth-adaptive (politique
  q*), prefill streaming full-layer double-buffered, global LRU expert caching, exécution
  graph-compatible (CUDA graphs), format de poids rapide FTW.
- Semantic-aware caching : checkpoints « semantic anchor » pour état récurrent (GDN) et KV caches,
  pour que les edits de contexte agentiques (tool calls, thinking blocks) évitent de recomputer.
- Elastic memory management : re-allocation VRAM runtime entre expert caches et KV, sans restart ni
  rechargement des poids.
- Modèles MoE open-weight frontière : DeepSeek-V4-Flash, Qwen3.6-35B-A3B, GLM-5.2… quantif
  MXFP4, NVFP4, FP8, BF16. APIs Anthropic/OpenAI-compatibles pour agents réels (Codex, Claude Code,
  OpenCode, OpenClaw, DeepSeek Harness).
- Hardware : laptops, gaming desktops, workstations ; NVIDIA RTX 30/40/50 nativement.

## MoE backends (docs/models.md)

`ft serve --moe-backend {auto,fused,offload,cpu,hybrid}` :
- fused : experts résidents sur GPU (besoin VRAM), jamais auto-sélectionné.
- offload : experts en RAM host, cache LRU de slots experts sur GPU ; les misses streament en PCIe.
- cpu : les misses sont calculées sur CPU au lieu d'être fetchées.
- hybrid : par step, fetch d'une partie des misses en PCIe + calcul CPU du reste, overlappés.
  `ft bench bw` une fois par machine pour calibrer le split.
- auto : dense → fused ; MoE → offload, upgradé hybrid si profil `ft bench bw` en cache le recommande.

## ft bench bw (moe/benchbw.py)

Mesure 2 couches : plafonds hardware (STREAM CPU DRAM + copy pinned→device) puis vrais kernels
(CpuMoeExecutor GEMV + OffloadMoeCache.copy_missing / fast_index_copy) ; mesure aussi le couple
overlappé (contention DRAM) → fixe la fetch-fraction du backend hybrid. Règle : hybrid si bande
passante kernel CPU MoE > 2x la bande passante PCIe gather, sinon offload. Formats sans chemin CPU
(block-fp8) → toujours offload. Profil JSON par GPU (`$XDG_CACHE_HOME/freetoken/benchbw/<gpu-uuid>.json`).

## CLI (docs/cli.md)

`ft serve` (API server), `ft shell` (chat TUI), `ft ctl` (contrôle HTTP), `ft launch`
(claude/codex/dsh/hermes/openclaw/opencode — écrit la config provider de l'agent, installe son CLI,
le lance contre le serveur), `ft checkpoint` (conversion HF→FTW fast-load), `ft bench bw`.
`--model` seul flag requis ; dtype, attention/MoE backends, tailles de cache, parsers tool-call/
reasoning résolus auto depuis le checkpoint + GPU. Port défaut 1919. `--gpu` = UUID nvidia-smi ou
index (GPU 0 par défaut, CUDA_VISIBLE_DEVICES).

## Modèles supportés (docs/models.md)

DeepSeek-V4-Flash-0731 ; GLM-5.2 / GLM-4.7 NVFP4 (NVIDIA) ; Qwen3.6-35B-A3B (+FP8/NVFP4),
Qwen3.5-35B-A3B, Qwen3.6-27B (dense), Qwen3-30B-A3B ; gpt-oss-120b/20b ; Gemma-4-26B-A4B/12B/31B
(+GGUF natif pour Gemma-4) ; MiniMax-M2.5 NVFP4 ; Muse-Glimmer-30B. Chargement HF safetensors
direct + GGUF natif. Conversion `ft checkpoint` optionnelle. DeepSeek-V4 exige le sous-dossier
`inference/config.json`.

## Scheduler / engine

- ChunkedReq pour chunked prefill (--max-prefill-length 8192 par défaut), _maybe_pinned pour async H2D.
- Req : hybrid-radix per-request slots (GDN linear-state), mamba ping-pong slots sous overlap,
  toolcall_anchor_len (limite de réutilisation profonde après rewrite de tool call par le client),
  flag aborted pour overlap scheduling.
- kvcache : radix cache, hybrid_radix_cache, swa_radix_cache, dsv4_paged_pool (page size forcé 128),
  linear_state_pool (GDN), pools mha/dsa/bsa. Attention backends : trtllm/fi/fa/triton/dsv4_sparse/dsa.
- MoE cache : slot_cache LRU device-side (flashlib), bank schemas par quant
  (bf16 : gate_up/down ; fp8_block : + scales 128x128 ; q4_0 GGUF ; nvfp4 ModelOpt), fusion des copies
  multi-banks (FREETOKEN_FUSED_COPY), garde anti-degradation cudaMemcpyBatchAsync < 256KB (sm_bank).

## Engine / serveur

- server/ : api_server.py (OpenAI /v1/chat/completions, /v1/responses, /v1/models ; Anthropic
  /v1/messages, /v1/messages/count_tokens), api_models, reasoning_parser, function_call_parser,
  accounting, stats, request_ring, control_api, supervisor.
- daemon/ : service systemd (ft-daemon.service), proxy, serve_manager, metrics, logring, osproc,
  pidfile, client, accounting.
- distributed/ : pynccl, tensor parallelism (tp).

## Benchmarks (benchmarks/)

- bench_decode_moe.py : bs=1 decode tok/s d'un modèle servi, spawn `ft serve` par backend, timing
  des tokens streamés (chemin de serving complet), prompt AIME-25.
- bench_load_weight_generic.py : temps de chargement des expert banks : serial vs parallel O_DIRECT
  vs pre-repacked FTW (Linux).
- bench_offload_cache_copy.py : synthétique, coût de copy d'experts decode par layer.

## Paper (arXiv 2608.16157, soumis 2026-08-17)

FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution. Yang, Fan, Pan, Xi,
Wang, Sun, Keutzer, Han, Zaharia, Xu, Stoica. Co-designe toute la stack de serving autour de deux
réalités : les workloads agents changent continuellement de pattern d'exécution, et le hardware
edge est hétérogène avec un équilibre différent par machine. Plutôt qu'une stratégie d'offload
fixe, il mappe continuellement computation et état du modèle sur les ressources disponibles.
> 20 modèles MoE. Résultats : 35B sur laptop 8GB, 284B sur gaming desktop, 753B GLM-5.2 sur un seul
GPU workstation.

### Chiffres clés de l'évaluation (§1 et §5, RTX 5090 sauf mention)

- Qwen3.6-35B-A3B (BF16) : 77–83 tok/s decode ; DeepSeek-V4-Flash (MXFP4, 284B, 6/256 experts actifs,
  13B/token) : 22–25 tok/s ; 1.5–2.3x les baselines (llama.cpp, Ollama, KTransformers, MoE-Infinity).
- RTX 4060 laptop 8GB (PCIe x8) : 35B NVFP4 à 39.3 tok/s (> 33 tok/s médian Codex prod).
- RTX PRO 6000 96GB : GLM-5.2 (753B-A40B NVFP4) à 14.9 tok/s = 2x llama.cpp, TTFT comparable.
- Décode stable sous workloads agentic (dans 12% du single-turn) ; TTFT worst-case < 44s vs baselines
  > 150s (llama.cpp 232s, KTransformers 946s) — au-delà des timeouts clients (OpenClaw 120s, Claude Code ~10min).
- Prefill : double buffering full-layer → chunk 8192 tokens en 1.19–1.22s = le temps de streamer les
  64.4 GB d'experts à 52.7 GB/s (plafond PCIe 5.0 x16). Sans overlap : −19/−25/−26% à 4k/8k/16k tokens.
- Miss rate decode à capacité de serving 5090 (LRU global) : 16% Qwen3.6 / 39% DSV4 vs 41–62%
  (KTransformers) et 62–89% (llama.cpp, split statique aveugle au routing).
- q* policy : q* = m·B_P/B_H ; exécution CPU lancée d'abord, GPU (fill + grouped eval) en parallèle,
  fusion exacte des sommes partielles (pas d'approximation).
- Coûts bruts : 140 GB d'experts DSV4-Flash FP4 → ~2s (PCIe 5.0 x16), ~5s (PCIe 4.0), 10+s (x8 laptop).
  DDR4 dual-channel ~50 GB/s, DDR5 ~80–90 GB/s vs 1–1.8 TB/s VRAM (le CPU seul ne peut pas porter le décode).
- Chargement disque → host : 140 GB depuis NVMe 7 GB/s ≈ 20s (adressé par FTW + O_DIRECT parallèle).
- GLM-5.2 : KTransformers ne peut pas le servir (753 GB–1.5 TB d'experts host requis vs 512 GiB dispo,
  kernels CPU incompatibles NVFP4).

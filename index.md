# Index

_Régénéré le 2026-05-22 — 52 pages._

## Vues d'ensemble

- [[inference-bottlenecks]] `draft` — Les 5 bottlenecks structurels du serving LLM selon Ahmad Osman — memory bandwidth, KV cache growth, interconnect, scheduler quality, runtime overhead. Grille de diagnostic universelle.
- [[llm-101]] `reviewed` — Hub de la série LLM 101 — point d'entrée pour comprendre les LLMs locaux, organisé en 6 thèmes (mécanique, package, quant/VRAM, runtimes, applications, ops).
- [[local-llm-2026-scene]] `reviewed` — Snapshot des familles de modèles open-weight à connaître en mai 2026 — Qwen, Gemma, Kimi, GLM, DeepSeek, MiniMax, Mistral, Nemotron. Penser en écosystèmes, pas en "best model".
- [[local-llm-growth-path]] `reviewed` — Progression beginner → intermediate → advanced → expert pour faire tourner du LLM local. Quel runtime, quel stack, quelle compétence à acquérir à chaque palier.

## Entités

- [[alloy]] `reviewed` — Boucle d'agent minimaliste OTP-native pour Elixir — completion/tool-call et rien d'autre. 6 providers, GenServer supervisé, memory comme behaviour, design boundary explicite.
- [[exllamav2]] `draft` — Engine d'inférence consumer CUDA — squeeze max sur 1 RTX 3090/4090/5090 via quant EXL2 + paged attention + dynamic batching. Single-GPU local sweet spot.
- [[exllamav3]] `draft` — Extension d'ExLlamaV2 vers multi-GPU et MoE-local — format EXL3 (QTIP-based), tensor-parallel et expert-parallel sur consumer hardware, multimodal, OpenAI-compat via TabbyAPI.
- [[hermes-agent]] `reviewed` — Framework d'agent autonome — context layering SOUL/AGENTS, profils, messageries, providers, MCP, endpoint OpenAI-compatible, skills progressive disclosure, webhooks.
- [[llama-cpp]] `draft` — Engine d'inférence LLM portability king — Apple Silicon (Metal/NEON), x86 (AVX/AMX), RISC-V, CUDA, ROCm, Vulkan, SYCL, CPU+GPU hybrid. GGUF natif. Pas pour multi-GPU prod.
- [[mlc-llm]] `draft` — Engine compiler-first universal deployment — APIs OpenAI-compatibles cross-platform (REST, Python, JS, iOS, Android). Le bon outil pour shipper des LLMs en browser, mobile, app natives.
- [[mlx]] `draft` — Framework array d'Apple pour Apple Silicon — unified memory native, MLX-LM pour les LLMs, HF Hub, quantization, LoRA, distributed (MPI, Thunderbolt RDMA). Server pas pour prod.
- [[nvidia-dynamo]] `draft` — Couche d'orchestration distributed au-dessus de vLLM/SGLang/TensorRT-LLM — disaggregation, routing intelligent, multi-tier KV caching, autoscaling. Pour quand single-engine ne suffit plus.
- [[ollama]] `draft` — Wrapper convivial autour de llama.cpp — gestion de modèles + serveur HTTP simple. Plaisant en surface mais Ahmad recommande explicitement DO NOT USE.
- [[sglang]] `reviewed` — Cousin systems-brained de vLLM — engine de serving LLM pour workloads ugly (structured outputs, long context, MoE, disaggregation prefill/decode native, routing).
- [[tauri]] `reviewed` — Framework Rust+WebView stable pour binaires desktop/mobile tiny via `tao`/`wry`. Bundler intégré (NSIS/WiX/dmg/AppImage), self-updater, custom protocol sans serveur HTTP local.
- [[tensorrt-llm]] `draft` — Stack NVIDIA-max-performance pour serving LLM — Python+C++ runtimes, kernels custom attention/GEMM/MoE, FP8/FP4, Wide Expert Parallelism, intégré à Triton et Dynamo. Trade portabilité contre perf.
- [[vllm]] `reviewed` — Engine de serving LLM production-default open-source — PagedAttention, continuous batching, parallélisme tensor/pipeline/data/expert/context, quant FP8/MXFP/NVFP/INT/GPTQ/AWQ/GGUF, APIs OpenAI/Anthropic/gRPC.
- [[zero-native]] `reviewed` — Framework Vercel Labs (Zig + WebView) pour desktop natives ET module embarqué dans apps mobiles natives via C ABI. Engine WebView (système ou Chromium) au choix. Challenger direct de Tauri.

## Concepts

- [[agent-guardrails]] `reviewed` — Quatre layers de safety pour LLM avec outils — scope tight, constrain execution, treat inputs as hostile, audit trail. Structured outputs ≠ security boundary.
- [[attention-variants]] `reviewed` — MHA, MQA, GQA — trois designs d'attention qui font varier dramatiquement la taille du KV cache à context égal, indépendamment du nombre de paramètres.
- [[chat-template]] `reviewed` — Format de conversation appris pendant le training d'un modèle chat — markup exact pour system/user/assistant/tool. Source #1 des bugs "ce modèle est nul".
- [[claude-md-pattern]] `reviewed` — Fichier CLAUDE.md placé à la racine d'un projet — prompt système persistant lu automatiquement par Claude Code à chaque session pour fixer scope, stack, contexte et garde-fous.
- [[claude-power-prompts]] `reviewed` — Trois prompts utilisables pour Claude — interview pour générer un CLAUDE.md, audit régulier d'un Project, stress-test d'une décision. Extraits d'un listicle X, sources marketing autour.
- [[continuous-batching]] `draft` — Scheduling pattern où les requêtes entrent et sortent du batch en cours d'exécution — vs static batching qui attend que tout un batch termine. Foundation du serving multi-user moderne.
- [[decoding-policies]] `reviewed` — La politique qui transforme les logits du modèle en un token choisi — temperature, top-p, top-k, stop sequences, constrained decoding. Change la voix sans toucher aux weights.
- [[edge-llm]] `reviewed` — LLM sur phones, robots, IoT, browser apps. Contraintes spécifiques — low RAM, low power, thermique, intermittence, latency real-time. Petit modèle fiable > gros modèle fragile.
- [[file-formats-llm]] — Formats binaires pour stocker les weights — safetensors, GGUF, ONNX, EXL2/GPTQ/AWQ, TensorRT engines. Choix lié au runtime, pas cosmétique.
- [[kv-cache]] — Working memory de l'inférence LLM — stocke les states key/value des tokens précédents pour éviter de recomputer la séquence à chaque nouveau token généré.
- [[llm-eval-methodology]] `reviewed` — Eval set 30-100 prompts sur le stack réel. Mesurer quality, latency, memory, formatting, retrieval, operations. Ne pas laisser un leaderboard choisir ton stack.
- [[llm-failure-modes]] `reviewed` — Checklist debug pour LLM local — OOM, gibberish, slow first token, slow streaming, bad documents, bad JSON, repeating loops. Les "boring checks" résolvent plus que de changer de modèle.
- [[local-coding-setup]] `reviewed` — Coding setup local fort = code-capable instruct + retrieval sur codebase + test execution + patch workflow. Un code model sans outils est un demi-produit.
- [[local-llm-runbook]] `reviewed` — Checklist en 4 étapes avant de faire confiance à un LLM local pour du vrai travail — choose & fit, load & format, evaluate & operate, version everything.
- [[long-context-tradeoffs]] `reviewed` — 128K, 256K, 1M tokens — supportés ≠ utiles ≠ gratuits. KV cache grossit linéairement, prefill ralentit, qualité peut décroître. Long context complète RAG, ne le remplace pas.
- [[lora-qlora]] `reviewed` — Méthodes de fine-tuning efficaces — LoRA freeze le base et entraîne des adapters low-rank, QLoRA fait pareil à travers un base 4-bit quantized. À essayer en dernier.
- [[memory-bandwidth]] `reviewed` — Bande passante mémoire — débit auquel le GPU peut lire ses propres weights. Détermine la vitesse de decode, distinct de la VRAM capacity qui détermine ce qui fit.
- [[model-package]] `reviewed` — Un modèle runnable = weights + tokenizer + config + chat template + generation config + license. Les weights ne sont pas le modèle.
- [[model-types-llm]] `reviewed` — Cinq types de modèles selon le post-training — base, instruct, chat, reasoning, tool-tuned. Ils ne se comportent pas pareil, le bon choix dépend du use case.
- [[multimodal-token-budget]] `reviewed` — Images, audio, vidéo deviennent des tokens aussi. Une image haute-res = milliers de tokens dans le context. Multimodal templates plus fragiles que text-only.
- [[open-weight-vs-opensource]] `reviewed` — Open-weight, source-available, opensource AI, local-compatible — 4 catégories souvent confondues. Lire le model card avant tout usage commercial.
- [[paged-attention]] `draft` — Technique de management du KV cache qui partitionne en blocs (pages) — supporte des batches plus grands sans fragmentation mémoire. Signature de vLLM, généralisée depuis.
- [[prefill-vs-decode]] — Deux régimes de performance distincts pendant l'inférence — prefill traite le prompt en parallèle (compute-bound), decode génère un token à la fois (memory-bandwidth-bound).
- [[quantization-llm]] — Réduction de la précision numérique des weights pour économiser mémoire et bandwidth. FP16 → Q4 = sweet spot consumer 2026. Sub-3-bit dégrade math, code, JSON.
- [[rag-pipeline]] `reviewed` — Retrieval-Augmented Generation — retrouve les chunks pertinents avant de générer. 90% des "mauvais RAG" viennent du chunking/retrieval/reranking, pas du LLM.
- [[serving-modes-llm]] — Trois modes de serving LLM — single-user local, team API privée, production. Trois jobs différents avec trois ensembles de préoccupations ops.
- [[speculative-decoding]] — Technique d'accélération du decode — un drafter cheap propose plusieurs tokens à l'avance, le target model verify en un seul forward pass. N'aide pas la mémoire KV.
- [[tokenizer]] `reviewed` — Composant qui transforme texte ↔ token IDs entiers. Détermine combien de texte fit dans le context, à quel coût, et si les chat markers sont vus correctement.
- [[vram-math]] — Budget mémoire pour faire tourner un LLM local — weights + KV cache + runtime overhead + extras. Formule VRAM ≈ B × (bits/8), headroom, et le piège des contexts longs.

## Comparaisons

- [[llm-runtimes]] `draft` — Comparaison runtimes/engines LLM 2026 — 4 familles (portable, Apple unified, CUDA quant, production serving) + decision guide one-page. Verdict d'Ahmad Osman intégré.

## Sources

- [[ahmad-osman-gpu-memory-math-2026]] `reviewed` — Part 1 trilogie Ahmad Osman — la formule VRAM ≈ B × (bits/8), tableaux par-GPU et par-modèle, MoE trap, et limites runtime-specific de GGUF.
- [[ahmad-osman-inference-engines-2026]] `reviewed` — Part 3 trilogie Ahmad Osman — taxonomie complète des engines d'inférence LLM, decision guide one-page, 5 bottlenecks structurels et opinions tranchées (do not use [[ollama]]).
- [[ahmad-osman-memory-bandwidth-2026]] `reviewed` — Part 2 trilogie Ahmad Osman — bandwidth ≠ capacity, 5 tiers de bande passante (1.8 TB/s → <150 GB/s), pourquoi "fitting ≠ serving" décide entre Apple unified et NVIDIA discrete.
- [[karpathy-claude-md-viral-thread]] `reviewed` — Thread X marketing (mai 2026) qui distille un CLAUDE.md viral en 21 règles classées en 3 sections — defaults, behavior, memory+stack — plus les 4 règles attribuées à Karpathy.

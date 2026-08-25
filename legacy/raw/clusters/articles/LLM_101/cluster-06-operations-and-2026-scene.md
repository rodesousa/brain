---
type: article-cluster
status: kept
created: 2026-05-22
source: raw/tweet/llms-101-practical-guide-2026.md
---

# Facet 6 — Operations & 2026 model scene

Le **côté ops** (faire tourner durablement) + la **photographie de l'écosystème** en mai 2026 (qui sont les familles de modèles à connaître). Plus failure modes, privacy, benchmarks, fine-tuning, licenses.

## Sections couvertes

- *Failure Modes And Fixes* — checklist des erreurs locales typiques
- *Privacy Is Not Automatic* — 4 habitudes de baseline sécurité
- *Benchmarks That Matter* — eval set 30-100 prompts sur ton stack réel
- *A Local LLM Runbook* — choose / load / evaluate / version
- *Fine-Tuning* — LoRA / QLoRA, quand fine-tuner (presque jamais en premier)
- *Open-Weight Does Not Mean Opensource* — open-weight vs source-available vs opensource vs local-compatible
- *The 2026 Local Model Scene* — Qwen, Gemma, Kimi, GLM, DeepSeek, MiniMax, Mistral, Nemotron

## Claims-clés

### Failure modes (causes habituelles)

- **OOM** : weights / KV / overhead / batch don't fit → smaller model, reduce context, lower batch, better quant, more headroom
- **Gibberish ou role confusion** : chat template / tokenizer / BOS-EOS / reasoning-mode / tool schema wrong → verify model card AVANT de blâmer le modèle
- **Slow first token** : prefill expensive → shorten prompt, prefix caching, better retrieval, reduce context
- **Slow streaming** : decode bottleneck → memory bandwidth, quantization, CPU spill, attention backend, speculative decoding, modèle trop gros
- **Bad document answers** : c'est presque toujours retrieval qui a failed (chunks, metadata, top-k, reranking, grounding)
- **Bad JSON / tool calls** : lower temp, constrained decoding, stricter schemas, better examples, modèle tool-tuned
- **Repeating loops** : reduce temp / top-p, repetition penalties, check stop tokens, template
- *"Start with the boring checks. They fix more problems than model swapping does."*

### Privacy / security baseline

1. **Load carefully** — safetensors/GGUF reputable sources, avoid untrusted .bin, don't enable `trust_remote_code` casually
2. **Run with boundaries** — unprivileged user, containers/sandboxes pour agents, disabled network quand offline
3. **Protect secrets** — credentials hors prompts/RAG, review desktop app telemetry, validate tool calls before exec
4. **Version what matters** — model + prompt + adapter + runtime + quantization, logs sans dump secrets
- *"Local AI security is mostly boring operational discipline"*

### Benchmarks

- **Quality** (real tasks, pas benchmarks génériques), **Latency** (TTFT, decode TPS, end-to-end), **Memory** (weight, KV growth, peak VRAM, headroom), **Formatting** (template, JSON, tool calls, stop tokens), **Retrieval** (citation faithfulness, grounding, missing-evidence behavior), **Operations** (startup, warmup, crash recovery, logging, privacy, versioning)
- Eval set 30-100 prompts représentatifs, avec expected answers, latency, memory, failure categories
- *"Do not let a leaderboard choose your local stack for you"*

### Runbook (4 étapes finales avant prod)

1. **Choose and fit** — modèle, license, hardware, quantization, full memory bill
2. **Load and format** — safetensors/GGUF reputable, tokenizer + template, context length, decoding params
3. **Evaluate and operate** — TTFT/decode/peak memory, retrieval avant RAG, sandbox avant agents
4. **Version everything** — model, quantization, runtime, prompt, template, adapter, embedding, reranker, eval set, hardware profile

### Fine-tuning

- Méthodes principales : **LoRA** (freeze base, train low-rank adapters) et **QLoRA** (LoRA à travers un base 4-bit quantized)
- Use cases : writing style consistent, domain-specific output format, repetitive classification/extraction, tool-call reliability, persona, domain adaptation que RAG ne résout pas, small-model perf sur narrow task
- Ordre à essayer **AVANT** fine-tuning : correct chat template → better prompting → better model → better decoding → RAG → reranking → few-shot → THEN fine-tuning
- *"Most problems that look like 'the model does not understand my domain' are actually 'my prompt is vague', 'my template is wrong', or 'my retrieval is broken'."*

### License clarté

- **Open-weight** : download possible, mais commercial use / modification / training on outputs / scale deployment / attribution pas garantis
- **Source-available** : code/weights visibles, license pas forcément opensource
- **Opensource AI** (OSI definition) : architecture + parameters + inference code + enough data info → bar bien plus haut que "weights sur HF"
- *"Read the model card and license before using any model commercially"*

### Familles 2026 à connaître

| Famille | Pourquoi tracker |
|---|---|
| **Qwen 3.5 / 3.6** | Stack complet : laptop → workstation → multi-GPU MoE, FP8, long context, multilingue, coding, agents. Default fort. |
| **Gemma 4** | Edge + dense + MoE, multimodal, long context, large language support, Apache 2.0 |
| **Kimi / Moonshot** | Long-horizon coding, multimodal reasoning, tool use, agents |
| **GLM / Z.ai** | Coding agents, long-horizon tasks, MoE, deployment-oriented |
| **DeepSeek** | Large MoE, Multi-head Latent Attention, FP8 serving, sparse attention, high-throughput |
| **MiniMax** | Agent workloads, inference-efficient MoE |
| **Mistral** | Generalist / coding / reasoning / multimodal / specialist, strong deployment |
| **Nemotron 3 (NVIDIA)** | Nano/Super/Ultra sizes, hybrid Mamba-Transformer MoE, TensorRT-LLM/NIM/Dynamo, Blackwell NVFP4/FP8 — signal de la direction NVIDIA pour serving stacks open-weight |

- Qwen 3.5/3.6 27B Dense est un "strong default" pour 2× RTX 3090 (coding, agents, multilingue), context jusqu'à 262K tokens via YaRN

### Inference research 2026

- **PagedAttention** (vLLM) — KV-cache memory waste
- **FP8 KV cache** — runtime feature pratique
- **DFlash / DDTree** — speculative decoding avec block diffusion drafters
- **NVFP4** — NVIDIA, change la conversation deployment sur stacks supportés

## Concepts qui pourraient devenir des pages wiki

- `wiki/llm_101/llm-failure-modes.md` (checklist debug)
- `wiki/llm_101/local-llm-runbook.md`
- `wiki/llm_101/llm-eval-methodology.md` (eval set 30-100 prompts, quoi mesurer)
- `wiki/llm_101/lora-qlora.md` (et quand NE PAS fine-tuner)
- `wiki/llm_101/open-weight-vs-opensource.md`
- `wiki/llm_101/local-llm-2026-scene.md` (snapshot familles, peut devenir une comparison)
- Pages individuelles potentielles : `wiki/llm_101/qwen.md`, `wiki/llm_101/gemma.md`, `wiki/llm_101/kimi.md`, `wiki/llm_101/deepseek.md`, `wiki/llm_101/nemotron.md`…

## My take

(à compléter au moment du `kept`)

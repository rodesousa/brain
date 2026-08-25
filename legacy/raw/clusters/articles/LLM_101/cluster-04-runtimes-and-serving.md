---
type: article-cluster
status: kept
created: 2026-05-22
source: raw/tweet/llms-101-practical-guide-2026.md
---

# Facet 4 — Runtimes & serving modes

Le **layer software** qui transforme du hardware en inference utilisable. Trois questions : quel runtime, pour quel mode (un user / une équipe / une vraie prod), et quelle progression beginner → expert.

## Sections couvertes

- *Runtimes And Serving Modes* — choix de runtime contraint par le format de modèle ; trois modes de serving (single-user / team API / production)
- *How To Grow The Stack* — progression beginner → intermediate → advanced → expert

## Claims-clés

### Runtimes

- Personnel / desktop : **Harbor**, **LM Studio**, **llama.cpp**
- Équipe / API privée : **vLLM**, **SGLang** (OpenAI-compatible endpoint)
- Production NVIDIA : **TensorRT-LLM**
- Browser / mobile : **MLC**, **WebLLM**
- Edge / hardware spécial : **ONNX**

### Le runtime lock l'écosystème de format

- llama.cpp ↔ GGUF
- vLLM / SGLang ↔ safetensors / Hugging Face checkpoints
- TensorRT-LLM ↔ ONNX / optimized engines

### Trois serving modes

1. **Single-user local** — desktop app, CLI, ou serveur 1-user (Harbor, LM Studio, llama.cpp server, ExLlama/TabbyAPI). Goal : itération rapide
2. **Team / private API** — OpenAI-compatible endpoint sur workstation/serveur (vLLM, SGLang, TensorRT-LLM, llama.cpp server). Goal : monitoring, prompt versioning, routing
3. **Production serving** — un autre job : continuous batching, prefix caching, speculative decoding, paged attention, tensor/pipeline parallelism, structured outputs, load balancing, latency percentiles, prompt caching, admission control, logging, failover

### Growth path 4 paliers

| Niveau | Stack | Goal |
|---|---|---|
| Beginner | Harbor / LM Studio, 4-9B instruct Q4, 8-32K context, chat UI | Apprendre prompting, comparer modèles, comprendre speed/memory |
| Intermediate | llama.cpp ou Transformers, GGUF/safetensors, OpenAI-compat localhost, RAG simple, eval set | Build local apps, mesurer qualité |
| Advanced | vLLM / SGLang, 1+ GPU, OAI API, monitoring, prompt versioning, eval suite, RAG + reranking, tool sandboxing | Serve users réels |
| Expert | TensorRT-LLM, custom kernels, runtimes spécialisés, quantization experiments, speculative decoding, multi-GPU, fine-tuning, distillation | Trade engineering time for inference efficiency at scale |

## Concepts qui pourraient devenir des pages wiki

- `wiki/llm_101/llm-runtimes.md` (comparison Harbor / LM Studio / llama.cpp / vLLM / SGLang / TensorRT-LLM)
- `wiki/llm_101/vllm-vs-sglang.md` (si tu vas dans le détail)
- `wiki/llm_101/serving-modes-llm.md` (single / team / production — quels patterns ops à chaque palier)
- `wiki/llm_101/local-llm-growth-path.md` (les 4 niveaux progressifs)

## My take

(à compléter au moment du `kept`)

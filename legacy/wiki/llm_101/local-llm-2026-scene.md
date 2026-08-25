---
type: overview
summary: Snapshot des familles de modèles open-weight à connaître en mai 2026 — Qwen, Gemma, Kimi, GLM, DeepSeek, MiniMax, Mistral, Nemotron. Penser en écosystèmes, pas en "best model".
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - model-families-2026
  - local-llm-deployment
---

L'écosystème open-weight bouge vite. En mai 2026, les users locaux doivent penser en **familles et écosystèmes**, pas en "un seul best model".

## Les 8 familles à tracker

### Qwen 3.5 / 3.6 (Alibaba) — default fort

Couvre **tout le stack** : small pour laptops, dense mid-size pour workstations, MoE pour multi-GPU serving, variantes FP8, long context, multilingue, coding, tools, agentic workflows. Si tu veux un seul écosystème pour aller du laptop expérimental au serving sérieux, **Qwen est un strong default**.

Mention spéciale : **Qwen 3.5 / 3.6 27B Dense** est un des meilleurs candidats pour un setup 2× RTX 3090 sur coding, agents, multilingue. Context jusqu'à 262K tokens, extension YaRN possible.

### Gemma 4 (Google DeepMind)

Pousse vers le **local utile** :
- Modèles edge efficients
- Dense et MoE plus larges
- Multimodalité
- Long context sur les variantes plus grandes
- Broad language support
- Coding/agent stronger
- **Apache 2.0** licensing (un point fort marketing)

À tester quand commercial use et device-side deployment matter.

### Kimi / Moonshot AI

Fort sur **long-horizon coding, multimodal reasoning, tool use, agent workflows**. Architecture orientée agentic natif.

### GLM / Z.ai

Coding agents, long-horizon tasks, MoE systems, deployment-oriented releases. Voir [[glm]] — release phare **GLM-5.2** (MoE 753B, MIT, 1M context).

### DeepSeek

Influent par ses **gros MoE** et ses contributions architecturales :
- Multi-head Latent Attention
- DeepSeekMoE
- FP8 serving paths
- Sparse attention
- High-throughput self-hosting

### MiniMax

À watcher pour **agent workloads** et **inference-efficient MoE**.

### Mistral

Lineup transverse : generalist, coding, reasoning, multimodal, specialist. Strong deployment support.

### Nemotron 3 (NVIDIA)

Famille production-grade pour **agent systems sur hardware NVIDIA** :
- Sizes Nano / Super / Ultra
- Hybrid **Mamba-Transformer MoE**
- Tied à TensorRT-LLM, NIM, Dynamo
- Blackwell NVFP4 / FP8 paths
- Enterprise agent deployment

À traiter moins comme une famille casual desktop et plus comme un **signal de direction** pour les serving stacks open-weight NVIDIA.

## Penser en écosystème

Open-weight AI **n'est plus juste "Llama vs everything else"**. Quand tu choisis une famille, tu choisis :
- Weights
- License ([[open-weight-vs-opensource]])
- [[tokenizer]]
- [[chat-template]]
- Quantizations dispo
- Support runtime ([[llm-runtimes]])
- Serving path
- Community tools
- Failure modes connus

## Inference research à watcher

- **PagedAttention** (vLLM) — KV cache memory waste
- **FP8 KV cache** — feature pratique dans vLLM et autres
- **DFlash / DDTree** — [[speculative-decoding]] avec block diffusion drafters
- **NVFP4** — sur hardware NVIDIA, change la conversation deployment

> *Some of this is production-ready. Some is still research. Some only matters if your runtime supports it cleanly. Do not treat paper speedups as a checkbox in a desktop app.*

## Related

- [[llm-runtimes]] — chaque famille a un support runtime variable
- [[open-weight-vs-opensource]] — vérifier la license par variante
- [[quantization-llm]] — FP8 et NVFP4 changent les options
- [[local-llm-growth-path]] — choix de famille dépend du niveau
- [[file-formats-llm]] — chaque famille a ses formats préférés
- [[glm]] — première famille de la liste à avoir sa page entité dédiée

## My take

Page snapshot qui va dater. À ré-évaluer **tous les 3-6 mois** — le scene bouge trop vite pour qu'une page reste valide longtemps. Le pattern "penser en écosystème" reste valable même quand les noms changent. Bonne candidate pour devenir une [[comparison]] dédiée par axe (coding, agents, edge…) quand on aura plus de sources spécifiques par famille.

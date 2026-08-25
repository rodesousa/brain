---
type: concept
summary: LLM sur phones, robots, IoT, browser apps. Contraintes spécifiques — low RAM, low power, thermique, intermittence, latency real-time. Petit modèle fiable > gros modèle fragile.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - edge-deployment
  - local-llm-deployment
  - small-models
---

L'edge n'est pas juste "une version plus petite du workstation". Les contraintes changent qualitativement.

## Cibles edge

- Phones
- Laptops (sans GPU dédié)
- Robots
- IoT gateways
- Factory devices, véhicules, dispositifs médicaux
- Field equipment offline
- Browser apps

## Contraintes spécifiques

- **Low memory** — souvent 4-16 GB unified
- **Low power** — batterie, dissipation thermique limitée
- **Thermal limits** — peut throttler
- **Intermittent connectivity** — pas de fallback cloud
- **Privacy hard** — données ne doivent pas sortir
- **Real-time latency** — réponse en ms ou seconds, pas minutes
- **Small context windows** — pas de luxe long context
- **Predictable fallback behavior** — un crash n'est pas acceptable

## Setup typique edge

- **Modèle 0.5B-4B**
- Quantization agressive (Q4, parfois Q3 avec eval)
- Tiny prompts (pas de system prompt verbeux)
- Fixed schemas (JSON pour les sorties)
- Tool-assisted workflows (le modèle appelle des outils déterministes, ne fait pas tout lui-même)
- Local embeddings
- Caching agressif (réponses récurrentes)
- **Pas d'historique inutile** (le chat infini n'a pas sa place)

## Principe central

> *When connectivity drops, a local model that keeps working is more valuable than a larger model that fails.*

Un petit modèle qui répond toujours bat un gros modèle qui plante. La fiabilité prime la capacité brute.

## Runtimes edge

- **MLC / WebLLM** pour browser
- **llama.cpp** pour ARM, Apple Silicon
- **ONNX Runtime** pour Intel NPU, ARM, accelerators custom
- **TensorRT-LLM** pour Jetson NVIDIA

## Related

- [[quantization-llm]] — agressif sur edge
- [[multimodal-token-budget]] — VLMs petits sur edge, attention aux tokens images
- [[file-formats-llm]] — GGUF et ONNX dominent
- [[local-llm-2026-scene]] — Gemma 4 et Qwen 3.5 / 3.6 ont des variantes edge

## My take

Le futur du LLM utile passe par l'edge autant que par les gros modèles cloud. Un assistant qui marche dans le métro, un robot qui parle sans connexion, une appli qui ne fuit pas — c'est là où le local prend tout son sens. Et c'est là où la discipline "modèle réservé + fallback simple" gagne contre "le plus gros qui rentre".

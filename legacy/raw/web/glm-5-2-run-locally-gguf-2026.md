---
title: "How to Run GLM-5.2 Locally with GGUF (2026)"
source: "https://ofox.ai/blog/glm-5-2-run-locally-gguf-2026/"
author:
  - "ofox.ai"
published: 2026
created: 2026-06-26
description: "Guide opérationnel pour faire tourner GLM-5.2 (753B MoE, MIT, 1M context) en local via GGUF quantisés Unsloth. Hardware, quants, runners, sampling, et comparaison avec le hébergé."
tags:
  - "clippings"
  - "glm"
  - "local-llm"
---

> ⚠️ Capture via WebFetch (extrait synthétisé, non verbatim). Source canonique = l'URL ci-dessus. Article publié par ofox.ai, qui vend de l'accès API GLM (biais commercial à garder en tête).

## What is GLM-5.2

- MoE **753B paramètres**, publié par **Zhipu / Z.ai** sous licence **MIT**.
- Fenêtre de contexte **1M tokens**.
- Poids BF16 complets ≈ **1,5 TB** → quantization obligatoire pour hardware grand public.

## Hardware requirements

- **Plancher : 256 GB** de mémoire unifiée (Apple Silicon) ou RAM DDR5.
- 256 GB Mac Studio → quant 2-bit `UD-IQ2_M` (~240 GB) → **3–9 tok/s**.
- 512 GB Mac Studio → quant 4-bit `UD-Q4_K_XL` (~376–475 GB) → meilleure qualité.
- 256 GB desktop + RTX 4090 → 2-bit via offload GPU → quelques tok/s (single digit).
- <256 GB : non viable → utiliser une API hébergée.

## Quantization & running locally

- Récupérer les **GGUF quantisés du repo communautaire Unsloth** (pas les BF16 officiels).
- 3 runners :
  1. **llama.cpp** — CLI, contrôle max.
  2. **LM Studio** — GUI desktop avec browser de modèles.
  3. **Unsloth Studio** — UI web avec offload mémoire auto.
- Sampling (défauts Zhipu) : `--temp 1.0 --top-p 0.95 --min-p 0.01`. Mauvais réglages = qualité dégradée.

## Performance reality check

- Outil **mono-utilisateur, mono-session**. Le multi-user exige des GPU datacenter.
- "local GLM 5.2 is a single-stream, single-developer tool."

## Hosted alternative

- **Z.ai Coding Plan ≈ 30 $/mois**, "runs at full speed" (vs 3–9 tok/s local).
- API à l'usage via ofox : **1,40 $/M input, 4,40 $/M output**.
- "A 2-bit local quant at 3-9 tok/s cannot match that for the price of electricity alone."

## Key takeaway

Le local n'a de sens que pour l'**offline / air-gapped**, la **confidentialité**, ou l'**apprentissage** — pas pour économiser. Setup réaliste : Mac 256 GB en 2-bit ; 512 GB pour du 4-bit de qualité.

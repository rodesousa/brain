---
type: entity
summary: Famille de modèles open-weight de Zhipu / Z.ai — orientée coding agents, long-horizon tasks et MoE deployment. GLM-5.2 = MoE 753B, MIT, 1M context.
lifecycle: draft
created: 2026-06-26
updated: 2026-06-26
sources:
  - raw/web/glm-5-2-run-locally-gguf-2026.md
tags:
  - model-families-2026
  - coding-assistants
  - local-llm-deployment
---

Famille open-weight de **Zhipu / Z.ai**, positionnée sur les **coding agents, les long-horizon tasks et les MoE deployment-oriented**. Une des 8 familles à tracker dans [[local-llm-2026-scene]].

## GLM-5.2 (release phare)

- **MoE 753B paramètres**, licence **MIT**, fenêtre de contexte **1M tokens**.
- Poids BF16 complets ≈ **1,5 TB** → [[quantization-llm]] obligatoire pour tourner localement.

## Faire tourner GLM-5.2 en local

Voir [[ofox-glm-5-2-local-2026]] pour le détail. En bref :

- **Plancher hardware : 256 GB** de mémoire unifiée (Apple Silicon) ou RAM DDR5. En dessous → API hébergée.
- **GGUF quantisés Unsloth** (pas les BF16 officiels), via [[llama-cpp]], LM Studio ou Unsloth Studio.

| Machine | Quant | Taille | Débit |
|---|---|---|---|
| Mac Studio 256 GB | 2-bit `UD-IQ2_M` | ~240 GB | 3–9 tok/s |
| Mac Studio 512 GB | 4-bit `UD-Q4_K_XL` | ~376–475 GB | qualité ++ |
| 256 GB desktop + RTX 4090 | 2-bit (offload GPU) | ~240 GB | quelques tok/s |

Le goulot est la [[memory-bandwidth]], pas le compute : à 3–9 tok/s, c'est du batch/asynchrone, pas de l'interactif. Le 2-bit dégrade aussi la qualité ([[quantization-llm]] : sub-3-bit casse math/code/JSON).

Sampling recommandé (défauts Zhipu) : `--temp 1.0 --top-p 0.95 --min-p 0.01`.

## Accès hébergé (Z.ai Coding Plan)

Alternative au local, souvent plus rapide **et** moins chère :

- **Z.ai Coding Plan ≈ 30 $/mois** (Pro), GLM-5.2 à pleine vitesse — vs 3–9 tok/s en local.
- Quota Pro : **600 prompts / cycle de 5 h** + limite hebdo. Mais **GLM-5.2 consomme ×3 en heure de pointe** (14h–18h UTC+8), ×2 hors pointe → ~200 vrais prompts/5h en pointe. ^[inferred] (chiffres tirés des docs z.ai / reviews tierces, pas de l'article ofox — voir https://docs.z.ai/devpack/overview)
- API à l'usage via ofox : **1,40 $/M input, 4,40 $/M output**.

## Related

- [[local-llm-2026-scene]] — GLM = une des 8 familles open-weight à tracker
- [[local-coding-setup]] — GLM est positionné coding ; setup local fort = modèle + retrieval + tests + patch workflow
- [[quantization-llm]] — indispensable pour les 753B de GLM-5.2 sur consumer hardware
- [[memory-bandwidth]] — le facteur qui plafonne les 3–9 tok/s en local
- [[llama-cpp]] — runner GGUF de référence pour GLM-5.2 local
- [[ofox-glm-5-2-local-2026]] — source-summary du guide ofox

## My take

GLM-5.2 en local est plus un **flex / cas air-gapped** qu'un daily driver : 3–9 tok/s c'est plus lent que la lecture humaine, et le 2-bit nécessaire pour tenir sur 256 GB rogne la qualité au moment précis où on a besoin d'un modèle coding fiable. Le rapport qualité/prix réel de GLM, c'est le **Coding Plan à 30 $/mois** — daily driver crédible pour du code routine, avec Claude en filet pour les tâches dures. Le "run locally" de l'article sert surtout à valoriser, par contraste, l'offre hébergée de l'éditeur (ofox vend l'API). À ré-évaluer dans 3-6 mois comme [[local-llm-2026-scene]] : la famille bouge vite.

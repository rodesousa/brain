---
type: source-summary
summary: Guide opérationnel ofox.ai pour faire tourner GLM-5.2 (753B MoE, MIT, 1M context) en local via GGUF Unsloth — hardware, quants, runners, et plaidoyer pour le hébergé.
lifecycle: draft
created: 2026-06-26
updated: 2026-06-26
sources:
  - raw/web/glm-5-2-run-locally-gguf-2026.md
tags:
  - glm
  - local-llm-deployment
  - quantization-options
---

Guide pratique publié par **ofox.ai** pour faire tourner [[glm]] **GLM-5.2** en local. Source utile pour les chiffres concrets (tailles de quant, débits, plancher hardware), mais **pas neutre** : ofox vend de l'accès API GLM, et la conclusion pousse vers le hébergé.

## Le modèle

GLM-5.2 = **MoE 753B**, licence **MIT**, contexte **1M tokens**, BF16 ≈ **1,5 TB**. Sans quantization, intouchable en consumer.

## Hardware (le plancher : 256 GB)

| Machine | Quant | Taille | Débit |
|---|---|---|---|
| Mac Studio 256 GB | 2-bit `UD-IQ2_M` | ~240 GB | 3–9 tok/s |
| Mac Studio 512 GB | 4-bit `UD-Q4_K_XL` | ~376–475 GB | qualité ++ |
| 256 GB desktop + RTX 4090 | 2-bit (offload GPU) | ~240 GB | quelques tok/s |

<256 GB → non viable, passer au hébergé. La RAM/mémoire unifiée est le facteur limitant, pas le GPU brut (le 4090 ne fait que de l'offload partiel).

## Faire tourner

- **GGUF quantisés du repo Unsloth** (pas les BF16 officiels).
- Runners : [[llama-cpp]] (CLI), LM Studio (GUI), Unsloth Studio (web, offload auto).
- Sampling défauts Zhipu : `--temp 1.0 --top-p 0.95 --min-p 0.01`.

## Le verdict de l'article

Local GLM-5.2 = outil **mono-utilisateur, mono-session**. À 3–9 tok/s, le local n'a de sens que pour **offline / air-gapped / privacy / apprentissage**. Pour le reste, le **Z.ai Coding Plan (~30 $/mois)** tourne à pleine vitesse et revient moins cher que l'électricité d'un Mac 256 GB.

## Related

- [[glm]] — page entité ouverte par cette source
- [[quantization-llm]] — les quants 2-bit/4-bit dont dépend tout le setup
- [[memory-bandwidth]] — pourquoi le débit plafonne à 3–9 tok/s
- [[llama-cpp]] — runner GGUF principal du guide
- [[local-coding-setup]] — GLM comme modèle coding local

## My take

La vraie valeur de la source, ce sont les **chiffres datés** (240 GB en 2-bit, 376–475 GB en 4-bit, 3–9 tok/s) — exactement le genre de fait qu'on oublie et qu'on regoogle. Le raisonnement "local ≠ moins cher" est correct mais sert l'agenda commercial d'ofox ; je ne prendrais pas ses recommandations hébergées pour argent comptant sans recouper. Page courte volontairement : c'est un guide opérationnel à péremption rapide, pas une référence conceptuelle.

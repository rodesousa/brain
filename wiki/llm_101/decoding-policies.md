---
type: concept
summary: La politique qui transforme les logits du modèle en un token choisi — temperature, top-p, top-k, stop sequences, constrained decoding. Change la voix sans toucher aux weights.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - decoding-policies
  - inference-mechanics
  - sampling
---

Après le forward pass, le modèle a produit des **logits** (scores bruts pour chaque token possible) puis des **probabilités** (après softmax). Il n'a encore rien "écrit". Le **decoding** est la politique qui transforme ces probabilités en un seul token choisi.

Les choix de decoding ne changent pas les weights, mais ils changent **voix, déterminisme, créativité, profil de risque, tendance à boucler**.

## Trois questions pratiques

1. **Randomness** — combien de variation tolérée ? (`temperature`)
2. **Tail reach** — jusqu'où descendre dans les tokens improbables ? (`top-p` nucleus, `top-k`)
3. **Boundaries** — qu'est-ce qui empêche loops, rambling, schema breaks ? (`repetition_penalty`, `stop_sequences`, `max_tokens`, `constrained_decoding`)

## Presets selon usage

| Usage | Temperature | Sampling | Boundaries |
|---|---|---|---|
| Précis / extraction / JSON | basse (0-0.3) | greedy ou narrow top-p | stop sequences explicites, constrained decoding |
| Coding | basse au 1er pass | greedy ou narrow | sample alternatives seulement si exploration intentionnelle |
| Créatif | haute (0.7+) | top-p large, multiple candidates | reranker post-génération |
| Evals | déterministe (greedy, seed fixe) | — | reproducible |

## Pièges

- **Greedy n'est PAS toujours plus précis** — il est souvent brittle (loops, réponses génériques car jamais d'exploration alternative)
- **Constrained decoding** (JSON schema, grammars) est l'outil quand le format compte plus que la créativité
- **Stop sequences** mal configurés = sortie qui coupe trop tôt ou jamais

## Speculative decoding

Famille de méthodes qui accélèrent le decode en draftant plusieurs tokens à l'avance puis en les vérifiant. EAGLE, MTP, DFlash (block diffusion), DDTree. C'est de la mécanique sous-jacente, pas un decoding parameter standard — exposé par le runtime, pas par l'utilisateur final.

## Related

- [[prefill-vs-decode]] — decoding s'applique sur la phase decode
- [[chat-template]] — un decoding parfait sur un template cassé reste cassé
- [[llm-failure-modes]] — beaucoup de "model is bad" sont en fait des decoding settings mauvais

## My take

Le knob qu'on néglige le plus alors qu'il coûte rien à tuner. Quand un setup local "ne marche pas" pour une tâche structurée, avant de changer de modèle, baisser la temperature et ajouter du constrained decoding règle 70% des cas.

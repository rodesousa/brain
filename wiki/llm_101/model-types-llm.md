---
type: concept
summary: Cinq types de modèles selon le post-training — base, instruct, chat, reasoning, tool-tuned. Ils ne se comportent pas pareil, le bon choix dépend du use case.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - model-types
  - inference-mechanics
---

Tous les LLMs ne sont pas tunés pour le même comportement. **Cinq archétypes** à distinguer avant de juger un modèle :

| Type | Comportement | Use case |
|------|-------------|---------|
| **Base** | Complète ton prompt au lieu d'y répondre | Recherche pretraining, fine-tuning, custom pipelines |
| **Instruct** | Suivre des instructions one-shot | Tâches directes "fais X" |
| **Chat** | Multi-turn dialogue avec role formatting | Assistants conversationnels |
| **Reasoning** | Extra thinking tokens avec verification | Math, raisonnement multi-étapes |
| **Tool-tuned** | Structured calls, JSON, function use fiable | Agents, intégrations API |

## Le piège base model

Demande à un base model "What is the capital of France?" — il peut continuer avec "and what is the population of Paris?" au lieu de répondre "Paris". Il complète ta phrase, il n'y répond pas.

**Ne commence jamais par un base model**, sauf si tu sais pourquoi (research, fine-tuning, custom pipeline). Pour tout le reste, commencer par un récent **instruct ou chat** dans une taille qui fit en mémoire.

## Reasoning models

Ils dépensent **plus de tokens** (thinking tokens internes, parfois invisibles dans l'output final). À prendre en compte :
- Budget context plus élevé
- Latency plus haute (decode séquentiel sur les thinking tokens)
- Use case justifié (math, code complexe, multi-step planning) — sinon overkill

## Tool-tuned models

Optimisés pour produire des appels JSON/function valides. Critique pour agents et intégrations. Un modèle chat générique peut produire du JSON, mais avec moins de fiabilité — bugs typiques : trailing commas, quotes manquantes, fields ratés.

## Related

- [[chat-template]] — chaque type a son format
- [[decoding-policies]] — reasoning aime des params différents
- [[agent-guardrails]] — tool-tuned ≠ safe par défaut
- [[local-llm-runbook]] — choix du type est l'une des premières décisions

## My take

La confusion base vs instruct est probablement la deuxième cause des "ce modèle est cassé" après le [[chat-template]] mal appliqué. Penser à toujours vérifier le suffixe du nom de modèle (`-base`, `-instruct`, `-chat`, `-reasoning`) avant de juger.

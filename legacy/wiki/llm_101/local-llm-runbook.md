---
type: concept
summary: Checklist en 4 étapes avant de faire confiance à un LLM local pour du vrai travail — choose & fit, load & format, evaluate & operate, version everything.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - runbook
  - local-llm-deployment
  - failure-modes
---

**Final gate** avant de trusker un setup LLM local pour du vrai travail. Quatre étapes, séquentielles.

## 1. Choose and fit

- Choisir une **famille de modèle** adaptée à la tâche (chat, coding, reasoning, tool, multimodal — voir [[model-types-llm]])
- **Lire la license** ([[open-weight-vs-opensource]])
- Confirmer hardware requirements
- Choisir un niveau de [[quantization-llm]]
- **Estimer la full memory bill** : weights + [[kv-cache]] pour le context réel + runtime overhead + batch + safety margin. Voir [[vram-math]].

> Ne pas s'arrêter à la taille des weights.

## 2. Load and format

- Préférer **safetensors ou GGUF** depuis sources réputées
- Éviter les fichiers pickle untrusted
- Vérifier [[tokenizer]] et [[chat-template]] — utiliser `apply_chat_template`
- Set context length **intentionnellement** (pas le max par défaut)
- Choisir les [[decoding-policies]] pour la tâche

> *If the template is wrong, the eval is invalid.*

## 3. Evaluate and operate

- Tester avec des prompts **représentatifs** — voir [[llm-eval-methodology]]
- Mesurer **TTFT** (time-to-first-token) et **decode TPS**
- Track peak memory et headroom sous charge
- Évaluer le retrieval **avant** d'ajouter [[rag-pipeline]] (sinon tu testes deux choses à la fois)
- **Sandbox** les tools **avant** d'ajouter [[agent-guardrails|agents]]
- Fine-tuner **seulement** après que les méthodes plus simples aient échoué ([[lora-qlora]])

## 4. Version everything that matters

Track :
- Model
- Quantization
- Runtime (version exacte)
- Prompt
- Chat template
- Adapter (si LoRA)
- Embedding model
- Reranker
- Eval set
- Hardware profile

> *Local systems are easier to control only when you can reproduce what you ran.*

Sans versioning, debug = archéologie.

## L'équation transverse

```
Local LLM success
   = model fit
   + correct prompt format
   + good runtime
   + realistic evals
```

Tout le reste est des détails — mais les détails matter.

## Related

- [[llm-failure-modes]] — quand quelque chose casse, débugger dans cet ordre
- [[vram-math]] — étape 1
- [[chat-template]] — étape 2 (la plus souvent ratée)
- [[llm-eval-methodology]] — étape 3
- [[agent-guardrails]] — sandbox avant tools

## My take

À traiter comme un pre-flight checklist. Tenter de skipper une étape (genre "je versionne après") coûte plus cher que de la faire bien dès le départ. La discipline ennuyeuse paie.

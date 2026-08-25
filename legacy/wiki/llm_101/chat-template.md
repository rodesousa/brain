---
type: concept
summary: Format de conversation appris pendant le training d'un modèle chat — markup exact pour system/user/assistant/tool. Source #1 des bugs "ce modèle est nul".
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - chat-template
  - inference-mechanics
  - prompt-formatting
---

Un modèle chat a été entraîné avec **un format de conversation spécifique**. Utiliser un format différent au runtime casse le modèle silencieusement.

> **Treat the template like an API contract.** If you get it wrong, you are not really testing the model you think you are testing.

## Exemples de formats

ChatML-style :
```
<|system|> You are a helpful assistant.
<|user|> Explain KV cache.
<|assistant|>
```

Llama2 INST-style :
```
[BOS] [INST] Explain KV cache. [/INST]
```

Autres : reasoning tokens (`<thinking>...</thinking>`), tool-call XML/JSON wrappers, format spécifique aux modèles tool-tuned.

## Symptômes d'un template cassé

| Symptôme | Cause souvent |
|---|---|
| Gibberish à la sortie | Tokens spéciaux non reconnus |
| Role confusion (modèle parle "à la place" de l'utilisateur) | Markers user/assistant mélangés |
| System prompt ignoré | Marker `<\|system\|>` absent ou wrong |
| Refus weirdness | Modèle voit son propre output comme un nouveau prompt |
| Broken tool calls | Schema function-call différent de celui appris |
| Benchmarks décevants | Le modèle ne joue pas le bon jeu |
| Repeating loops | Stop tokens (EOS) wrong → le modèle ne sait jamais s'arrêter |

> Si le template est wrong, l'éval est invalide. Avant de blâmer le modèle, vérifier le model card.

## Best practices

- Utiliser `tokenizer.apply_chat_template()` en Transformers — c'est la source de vérité
- Utiliser les templates model-specific dans Harbor, llama.cpp, LM Studio, vLLM, SGLang
- Vérifier le model card pour savoir si c'est base / instruct / chat / reasoning / tool-tuned ([[model-types-llm]])
- BOS/EOS tokens corrects
- Pour tool use : suivre le schéma exact attendu
- **Si ton app permet de switcher de modèle, switcher aussi le template** — hardcoder un format est un piège classique

## Related

- [[model-types-llm]] — savoir si le modèle est chat ou base change ce qu'on lui envoie
- [[tokenizer]] — les markers de chat sont des tokens spéciaux du tokenizer
- [[model-package]] — le chat template fait partie du package
- [[llm-failure-modes]] — gibberish/role confusion vient de là

## My take

Probablement la cause #1 des "ce modèle local est nul" sur Reddit/X. Le coût de bien faire est de zéro (`apply_chat_template` existe), le coût de mal faire est invisible et catastrophique. À pointer dès qu'un benchmark local donne des résultats étranges.

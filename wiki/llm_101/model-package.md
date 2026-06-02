---
type: concept
summary: Un modèle runnable = weights + tokenizer + config + chat template + generation config + license. Les weights ne sont pas le modèle.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - model-package
  - inference-mechanics
  - file-formats
---

Un LLM local runnable est **plus qu'un gros fichier de weights**. Un package complet contient :

1. **Architecture / config** — layer count, hidden size, attention type ([[attention-variants]]), RoPE settings, vocabulary size, special tokens, context length
2. **Weights** — paramètres appris, stockés au choix en safetensors, GGUF, GPTQ, AWQ, EXL2, ou autre format runtime-spécifique ([[file-formats-llm]])
3. **Tokenizer** — règles texte ↔ token IDs ([[tokenizer]])
4. **Chat template** — markup exact pour system/user/assistant/tool messages ([[chat-template]])
5. **Generation config** — defaults pour temperature, top-p, stop tokens, repetition penalties, max tokens
6. **License + model card** — instructions légales et opérationnelles ([[open-weight-vs-opensource]])

## Pourquoi ça compte

Les weights sont le plus gros fichier, mais ils ne sont pas le modèle. **Si le tokenizer, le config, ou le chat template est wrong, les mêmes weights peuvent paraître cassés.**

Quand tu télécharges un modèle, tu télécharges tout le package. Quand tu re-quantizes, tu manipules les weights mais le reste doit voyager avec.

## Implications pratiques

- Un weight file `.safetensors` seul n'est pas exécutable
- Re-quantizer depuis un repo n'est sûr que si tu copies tokenizer + config + template
- Comparer "le même modèle" entre runtimes peut différer si les templates sont gérés différemment
- Switcher de modèle dans une app = switcher le **package complet**, pas juste les weights

## Related

- [[chat-template]] — composant le plus souvent cassé
- [[tokenizer]] — détermine ce que le modèle voit
- [[file-formats-llm]] — comment les weights sont stockés
- [[open-weight-vs-opensource]] — la license fait partie du package

## My take

Le concept à interner pour éviter le piège du "j'ai téléchargé les weights donc j'ai le modèle". Aide à comprendre pourquoi GGUF est apprécié : c'est un format qui embarque tout (weights + tokenizer + template) dans un seul fichier portable.

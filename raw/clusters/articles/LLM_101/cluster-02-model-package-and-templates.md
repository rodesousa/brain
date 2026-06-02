---
type: article-cluster
status: kept
created: 2026-05-22
source: raw/tweet/llms-101-practical-guide-2026.md
---

# Facet 2 — Model package & chat templates

Le **weight file n'est pas le modèle**. Un modèle runnable = weights + tokenizer + config + chat template + generation config + license. Les bugs les plus fréquents en local viennent du *chat template* mal appliqué, pas de la qualité du modèle.

## Sections couvertes

- *What A Model Package Contains* — 6 composants qui doivent voyager ensemble
- *Chat Templates* — formats par modèle (ChatML, `<|system|>...`, `[INST]...`, tool-call XML/JSON), conséquences si erreur (gibberish, role confusion, refus, faux résultats de benchmark)
- *Model Types* — base vs instruct vs chat vs reasoning vs tool-tuned (et pourquoi un base model n'est pas un assistant)

## Claims-clés

- Composants d'un model package : **architecture/config**, **weights** (safetensors/GGUF/GPTQ/AWQ/EXL2…), **tokenizer**, **chat template**, **generation config**, **license + model card**
- *"Treat the template like an API contract"* — utiliser `apply_chat_template` du tokenizer en Transformers
- Erreurs typiques de template : gibberish, role confusion, ignored system prompts, refus weirdness, broken tool calls, mauvais benchmarks → conclusion erronée "ce modèle est nul"
- Base model = complète ton prompt au lieu d'y répondre. Demande à un base "What is the capital of France?" et il continue avec "and what is the population of Paris?"
- Pour switcher de modèle dans une app, il faut **switcher le template aussi** — hardcoder un seul format est une erreur classique
- 5 model types : base (research/fine-tune), instruct (suivi d'instructions), chat (multi-turn), reasoning (extra thinking tokens), tool-tuned (JSON/function calls)

## Concepts qui pourraient devenir des pages wiki

- `wiki/llm_101/chat-template.md` (avec exemples ChatML, Llama2 INST, Qwen)
- `wiki/llm_101/model-package.md` (anatomie d'un model release)
- `wiki/llm_101/model-types-llm.md` (base / instruct / chat / reasoning / tool-tuned)

## My take

(à compléter au moment du `kept`)

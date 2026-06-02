---
type: entity
summary: Engine compiler-first universal deployment — APIs OpenAI-compatibles cross-platform (REST, Python, JS, iOS, Android). Le bon outil pour shipper des LLMs en browser, mobile, app natives.
lifecycle: draft
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - inference-engines
  - llm-runtimes
  - edge-deployment
---

**MLC LLM** est un engine compiler-first qui vise le **universal deployment** : same model, different targets — REST, Python, JS, iOS, Android, browser via WebLLM.

## Sweet spot

> **Ship LLMs everywhere.** Browser, mobile, native apps.

C'est la stack pour quand le LLM doit s'exécuter dans l'environnement de l'utilisateur final, pas sur un serveur centralisé.

## Features

- **APIs OpenAI-compatibles** cross-platform
- **REST, Python, JavaScript, iOS, Android** comme cibles compilation
- **WebLLM** — variante browser (WebGPU)
- **Compiler-first** — passe par TVM Unity pour compiler les graphes vers chaque target

## Recettes hardware / déploiement

- **Browser** : MLC LLM / WebLLM
- **Mobile (iOS/Android)** : MLC LLM (alternative à ONNX Runtime GenAI selon l'écosystème)
- **App-native** : MLC LLM, ou ONNX Runtime GenAI selon stack

## Limites

- **Pas un production server** au sens [[vllm]] / [[sglang]] — c'est un runtime côté client
- La compilation graph par target a un coût et un cycle de feedback plus long que charger un GGUF dans [[llama-cpp]]
- Modèles nouveaux peuvent demander un travail d'adaptation MLX pour les supporter

## Quand préférer une alternative

- **Serveur classique multi-user** → [[vllm]] / [[sglang]]
- **Desktop single-user, GGUF facile** → [[llama-cpp]]
- **App Windows / VS Code AI Toolkit / Foundry Local** → ONNX Runtime GenAI (couverture Windows plus profonde)
- **Intel-centric (Xeon, Arc, NPU)** → OpenVINO GenAI

## Verdict d'Ahmad

> MLC LLM is the compiler-first universal deployment engine with OpenAI-compatible APIs across REST, Python, JavaScript, iOS, and Android. **Best for "ship LLMs everywhere," especially browser, mobile, and native apps.**

## Related

- [[llm-runtimes]] — comparaison wiki
- [[llama-cpp]] — alternative desktop / server simple
- [[vllm]] — alternative serveur multi-user (pas cross-client)
- [[file-formats-llm]] — formats spécifiques MLC
- [[serving-modes-llm]] — edge / client-side, hors des 3 modes standards
- [[ahmad-osman-inference-engines-2026]] — source principale

## My take

L'outil quand **le LLM doit vivre côté utilisateur**, pas côté serveur. Si tu construis une app mobile qui doit fonctionner offline ou une extension browser avec LLM local, MLC est le candidat évident — au prix d'un cycle build plus lourd que charger un GGUF. Pour 95% des cas où le LLM sert depuis un serveur, c'est le mauvais outil — [[vllm]] ou [[llama-cpp]] sont bien meilleurs. Mais pour le **edge deployment**, il est presque sans concurrent (sauf ONNX Runtime GenAI sur Windows-centric).

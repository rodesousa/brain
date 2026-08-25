---
type: concept
summary: Coding setup local fort = code-capable instruct + retrieval sur codebase + test execution + patch workflow. Un code model sans outils est un demi-produit.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - coding-assistants
  - tool-use
  - rag-pipeline
---

Coding est un des meilleurs cas d'usage pour LLM local — prompts contiennent du code privé, latency matters, l'itération est fréquente, les coûts API API grimpent vite, et le modèle local s'intègre bien avec editors, shells, grep, test runners.

## Le setup fort (pas un chatbot nu)

> *A code model without tools is half a product.*

Components à câbler :

- **Modèle code-capable instruct** ([[model-types-llm]]) — 14B-32B si la VRAM le permet
- **Retrieval sur la codebase** — embeddings + index sur les fichiers
- **File paths** + relevant snippets dans le prompt (pas tout le repo)
- **Test execution** — le modèle peut lancer les tests et lire les outputs
- **Patch workflow** — sortie en `diff`/`patch`, pas en "voici le fichier complet réécrit"

## Decoding pour le code

- **Low temperature** ou greedy au premier pass — [[decoding-policies]]
- Sample alternatives **seulement** quand l'exploration est intentionnelle
- **Patches plutôt que vague advice** — demander explicitement

## Ne pas faire

- Laisser un modèle local **réécrire un gros codebase sans review**
- Compter sur le modèle pour "comprendre l'architecture" sans retrieval
- Mesurer la qualité sur des prompts génériques (HumanEval) — mesurer sur **tes bugs réels**

## Eval set

Garder un petit eval set de bugs réels et de tâches typiques. Quand un nouveau modèle sort, le passer dessus avant de switcher. Sans eval set, on switche au feeling.

## Ce que "local" t'achète vraiment

- **Privacy** — code privé reste local
- **Loop bon marché** — pas de coût API par iteration
- **Intégration contrôlée** — editor, shell, tests dans ton scope

Local ne rend pas un coding agent **wise**. Il rend le context privé, la loop cheaper, et l'intégration plus contrôlable. Le jugement reste à l'humain.

## Related

- [[model-types-llm]] — code-capable instruct vs base
- [[agent-guardrails]] — patch workflow protège, pas full filesystem access
- [[rag-pipeline]] — retrieval sur codebase = RAG spécialisé
- [[decoding-policies]] — low temp + deterministic pour le code
- [[glm]] — famille positionnée coding agents, candidate pour ce setup
- [[ofox-glm-5-2-local-2026]] — faire tourner un modèle coding (GLM-5.2) en local

## My take

La règle "patches plutôt que rewrites" est la plus importante. Un modèle qui sort un diff est review-able en 30 secondes. Un modèle qui réécrit un fichier complet noie les diffs réels dans la reformulation. Le format de sortie est presque aussi important que la qualité du modèle.

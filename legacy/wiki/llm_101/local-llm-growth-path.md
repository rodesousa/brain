---
type: overview
summary: Progression beginner → intermediate → advanced → expert pour faire tourner du LLM local. Quel runtime, quel stack, quelle compétence à acquérir à chaque palier.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - local-llm-deployment
  - serving-modes
  - runbook
---

Quatre paliers progressifs pour monter en compétence sur le LLM local.

## Beginner — easiest useful setup

**Stack** : Harbor ou LM Studio, modèle **4B-9B instruct**, Q4, context 8K-32K, UI chat intégrée.

**Goal** : apprendre le prompting, comparer 2-3 modèles dans la même classe de taille sur les mêmes prompts, comprendre les sensations de vitesse et de mémoire. **Pas de custom code.**

**À mesurer** : qu'est-ce qui rentre, qu'est-ce qui ne rentre pas, ce qui rend les réponses "lentes" ou "rapides", quels modèles "comprennent" mieux ton vocabulaire.

## Intermediate — developer setup

**Stack** : llama.cpp ou Transformers, GGUF ou safetensors, serveur OpenAI-compatible local, pipeline [[rag-pipeline]] simple, petit eval set.

**Goal** : appeler ton serveur local depuis une vraie app ou un script, mesurer la qualité de retrieval, servir depuis localhost.

**Nouveau à maîtriser** : [[chat-template]] dans l'API, parsing/chunking de docs, embedding model, mesure latency basique.

## Advanced — private serving setup

**Stack** : vLLM ou SGLang, 1+ GPU, API OpenAI-compatible, monitoring, prompt/version management, eval suite, RAG avec reranking, tool sandboxing.

**Goal** : servir des utilisateurs réels ou des workflows internes, optimiser throughput et latency, maintenir safety et observability.

**Nouveau** : observability (logs, metrics, traces), [[agent-guardrails]] si l'usage inclut des tools, gestion multi-user (rate limits, auth).

## Expert — custom optimization

**Stack** : TensorRT-LLM, custom kernels, runtimes spécialisés, expérimentations quantization, [[speculative-decoding]], multi-GPU parallelism, fine-tuning, distillation, evals de prod.

**Goal** : trader du temps d'engineering contre de l'inference efficiency, du cost lower, et de la quality higher at scale.

**Mindset** : on n'est plus dans "ça marche", on est dans "ça scale à un coût soutenable".

## Comment progresser

Ne pas sauter de palier. Chaque niveau apporte une compétence qui rend le suivant maîtrisable. Beaucoup d'échecs locaux viennent de gens en niveau "beginner" qui tentent un setup advanced sans avoir d'eval set ni de monitoring.

## Related

- [[serving-modes-llm]] — les 3 modes correspondent grossièrement aux niveaux 1, 3, 4
- [[llm-runtimes]] — chaque niveau a son runtime privilégié
- [[local-llm-runbook]] — checklist transverse aux niveaux
- [[llm-eval-methodology]] — devient critique à partir d'intermediate

## My take

La progression la plus saine pour quelqu'un qui débute en LLM local. Pas besoin de comprendre TensorRT-LLM pour avoir un assistant utile chez soi. Le palier le plus sous-estimé est "intermediate" — la transition de UI vers API change tout.

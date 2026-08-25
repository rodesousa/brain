---
type: concept
summary: Retrieval-Augmented Generation — retrouve les chunks pertinents avant de générer. 90% des "mauvais RAG" viennent du chunking/retrieval/reranking, pas du LLM.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - rag-pipeline
  - retrieval
  - long-context
---

**RAG** = Retrieval-Augmented Generation. Au lieu de stuffer toute l'information dans le prompt, on **retrieve les chunks pertinents** depuis une knowledge base et on donne *seulement* ces chunks au modèle.

## Le pipeline complet

```
ingestion → parsing → chunking → embeddings → vector index
  → retrieval → reranking → prompt construction
  → answer generation → grounding check → eval
```

**Chaque étape est un failure point.**

## Failure modes par étage

| Étage | Symptôme typique |
|---|---|
| Parsing | Tables transformées en garbage, formatage perdu |
| Chunking | La réponse est splittée entre deux chunks (silent killer) |
| Embeddings | Sémantique mal capturée pour ton domaine |
| Vector index | Latency, recall |
| Retrieval | Paragraphes hors-sujet remontent |
| Reranking | Bonne réponse enterrée au rang 20 |
| Prompt construction | Trop de context inutile, formatage cassé |
| Grounding | Le modèle invente parce qu'il n'a pas l'évidence |

> *Most bad RAG systems are not bad because of the LLM. They are bad because of chunking, retrieval, reranking, and evaluation.*

## Chunking — le silent killer

Le piège principal. **Fixed-size chunks sans overlap** splittent les phrases et perdent du context. Alternatives à évaluer :
- **Semantic chunking** — découpe sur frontières sémantiques
- **Hierarchical chunking** avec parent-document retrieval — chunk fin pour matching, parent renvoyé pour context

Il n'y a pas de réponse universelle. **Évaluer chunk size, overlap, rules de split sur tes documents à toi.**

## Rerankers — peuvent rescue ou pas

Un bon reranker peut récupérer un retrieval médiocre. **Aucun reranker ne peut récupérer des chunks qui ont perdu la réponse à l'ingestion.**

Le reranker rattrape le rang, pas la perte d'information amont.

## Grounding

Demander au modèle de **citer les chunks** dans sa réponse. Permet de vérifier la fidélité (citation faithfulness). Évaluer périodiquement avec un sample.

## Related

- [[long-context-tradeoffs]] — RAG est la bonne alternative au "tout dans le context"
- [[llm-eval-methodology]] — évaluer le RAG est obligatoire, pas optionnel
- [[agent-guardrails]] — retrieved docs peuvent contenir prompt injection
- [[llm-failure-modes]] — "bad document answers" = retrieval, presque toujours

## My take

> *A good reranker can rescue mediocre retrieval. No reranker can fix chunks that lost the answer during ingestion.*

La phrase qui change la priorité de tuning. Quand un RAG marche mal, le réflexe est de changer le LLM. Le bon réflexe est de regarder les chunks renvoyés au top-10 du retrieval. 9 fois sur 10, la réponse n'y est pas — donc le LLM ne peut rien faire.

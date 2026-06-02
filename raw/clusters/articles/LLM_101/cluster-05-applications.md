---
type: article-cluster
status: kept
created: 2026-05-22
source: raw/tweet/llms-101-practical-guide-2026.md
---

# Facet 5 — Applications (long context, multimodal, RAG, agents, coding, documents, edge)

**Ce qu'on construit vraiment** avec un LLM local + les pièges spécifiques à chaque cas d'usage. Le pattern récurrent : la qualité du système global ne dépend pas du modèle, mais du pipeline autour (retrieval, parsing, guardrails, evals).

## Sections couvertes

- *Long Context* — coûts réels du long context, comment compenser
- *Multimodality* — VLM, audio, vidéo, token budget caché
- *Coding With Local Models* — code-capable + repo retrieval + patch loop + test execution
- *Local Agents Need Guardrails* — 4 layers de safety (scope / constrain / hostile inputs / audit trail)
- *RAG Beats Giant Prompts* — pipeline RAG : ingestion → parsing → chunking → embeddings → vector index → retrieval → reranking → prompt construction → generation → grounding → eval
- *Documents And Knowledge Work* — meeting transcripts, contracts, technical docs, citations
- *Edge Deployment* — phones, robots, IoT, browser apps ; contraintes différentes (RAM, power, thermique, intermittent)

## Claims-clés

### Long context

- Plus de context = plus de KV memory, prefill plus lent, attention plus chère, qualité qui décroît avec la distance
- Un modèle peut bien gérer la fin d'un long doc et rater les détails au début
- *"Think of long context as expensive attention, not a free notebook"*
- Habitudes : instructions critiques au début ET à la fin, headers/delimiters, citations chunked, summary memory au lieu d'historique infini

### Multimodality

- Image = tokens aussi (vision encoder ajoute mémoire + image patches consomment context)
- Une image haute-res = milliers de tokens
- Petits VLMs hallucinent les détails visuels, OCR varie, charts/tables restent durs
- *"Do not trust a demo of a simple photo to prove invoice extraction quality"*

### Coding

- Setup fort = code-capable instruct + retrieval sur codebase + file paths + relevant snippets + test execution + patch workflow
- Décodage low-temperature / deterministic
- Demander des **patches** plutôt que des "vague advice"
- Garder un petit eval set de bugs réels
- *"A code model without tools is half a product"*

### Agents

- Tool use change le safety model : un chatbot qui hallucine = annoying, un agent avec filesystem access = peut delete things, browser access = leak secrets, shell access = damage la machine
- **4 layers de safety** :
  1. **Scope tight** — only the dirs / APIs / network / credentials needed
  2. **Constrain execution** — sandboxes, containers, least-priv users, confirmations destructives, schema-validated args
  3. **Treat inputs as hostile** — RAG docs, web pages, tickets, emails peuvent contenir prompt injection
  4. **Audit trail** — log tool calls, model versions, prompts, approvals (sans dump secrets)
- Structured outputs ≠ security boundary
- *"For serious tool use, put policy checks outside the model"*

### RAG

- 90% des "bad RAG" viennent de chunking / retrieval / reranking / evaluation, pas du LLM
- Chunking strategy = silent killer — fixed-size sans overlap split les phrases, semantic chunking marche souvent mieux
- *"A good reranker can rescue mediocre retrieval. No reranker can fix chunks that lost the answer during ingestion"*
- Pipeline : parsing → chunking → embeddings → vector index → retrieval → reranking → prompt → answer → grounding check → eval

### Documents

- Préserver page/section metadata, chunker sémantiquement, embeddings + rerankers, ask citations, séparer answer / sources / reasoning, evaluate citation faithfulness
- Meeting transcripts : préserver speaker labels + timestamps
- Contracts : chunker par clause/section, pas par token count arbitraire
- *"Do not assume the model knows what is in your documents"*

### Edge

- Contraintes : low memory, low power, thermal limits, intermittent connectivity, privacy, real-time latency, small context, predictable fallback
- Setup typique : **0.5B-4B model**, aggressive quantization, tiny prompts, fixed schemas, tool-assisted workflows, local embeddings, caching, pas d'historique inutile
- *"When connectivity drops, a local model that keeps working is more valuable than a larger model that fails"*

## Concepts qui pourraient devenir des pages wiki

- `wiki/llm_101/long-context-tradeoffs.md`
- `wiki/llm_101/rag-pipeline.md` (avec failure modes par stage)
- `wiki/llm_101/agent-guardrails.md` (4 layers)
- `wiki/llm_101/local-coding-setup.md` (patch loop)
- `wiki/llm_101/edge-llm.md`
- `wiki/llm_101/multimodal-token-budget.md`

## My take

(à compléter au moment du `kept`)

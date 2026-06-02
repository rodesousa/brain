---
type: concept
summary: 128K, 256K, 1M tokens — supportés ≠ utiles ≠ gratuits. KV cache grossit linéairement, prefill ralentit, qualité peut décroître. Long context complète RAG, ne le remplace pas.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - long-context
  - kv-cache
  - rag-pipeline
---

Le **long context** sonne magique : 128K, 256K, jusqu'à 1M tokens en un prompt. Utile mais coûteux à plusieurs niveaux.

## Coûts cachés

- **Mémoire** — [[kv-cache]] linéaire avec le nombre de tokens. À 100K tokens, c'est généralement le poste mémoire dominant
- **Latency prefill** — traiter 100K tokens prend du temps, même parallélisable
- **Attention work** — quadratique théorique, optimisé en pratique mais reste cher
- **Qualité dégradée avec la distance** — modèle peut bien gérer la fin d'un long doc et rater des détails au début
- **Distraction** — plus de context = plus de texte pertinent ET non pertinent = signal/bruit dégradé

> *Supported context length is not the same as cheap, fast, or equally accurate context.*

Un modèle annoncé 128K peut **ralentir au crawl à 64K et perdre cohérence à 100K**. Toujours tester aux longueurs que tu utiliseras.

## Use cases légitimes

- Whole-document analysis
- Codebase slices (faire lire plusieurs fichiers ensemble)
- Legal / technical review (chercher des contradictions)
- Transcript summarization
- Multi-file reasoning
- RAG fallback quand le retrieval rate du context critique

## Long context ≠ remplacement de RAG

Le pattern correct : **RAG pour les gros corpus, long context pour le evidence final sélectionné**. Pas l'un OU l'autre.

Long context te coûte sur tous les tokens. [[rag-pipeline]] te coûte seulement sur les chunks retournés.

## Habitudes qui aident

- **Instructions critiques au début ET à la fin** (lost-in-the-middle)
- **Headers et delimiters** pour structurer
- **Citations chunked** dans la réponse demandée — force le modèle à pointer
- **Compresser l'historique** plutôt que tout garder
- **Summary memory** plutôt qu'historique infini de chat

## Related

- [[kv-cache]] — le coût principal
- [[rag-pipeline]] — la bonne alternative à "dump tout dans le context"
- [[prefill-vs-decode]] — long prompt = long prefill = TTFT élevé
- [[multimodal-token-budget]] — images = tokens, même budget

## My take

> *Think of long context as expensive attention, not a free notebook.*

Cette phrase mérite d'être imprimée. La tendance "balance tout le doc dans le prompt" est un piège : tu paies pour des tokens que le modèle ne va pas bien attendre. RAG bien fait > 128K naïf, 9 fois sur 10.

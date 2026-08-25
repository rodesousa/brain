---
type: concept
summary: Images, audio, vidéo deviennent des tokens aussi. Une image haute-res = milliers de tokens dans le context. Multimodal templates plus fragiles que text-only.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - multimodal-llm
  - tokenizer-design
  - vram-math
---

Les modèles **multimodal** (VLM, audio, vidéo) acceptent autre chose que du texte. Mais cet "autre chose" devient **des tokens dans le même budget context** que le texte.

## Le coût caché

- **Vision encoder** ajoute de la mémoire (poids dédiés + activations)
- **Image patches** consomment le context window
- **Audio chunks** explosent le budget si la durée monte
- **Vidéo** = audio + frames, multiplicateur fort

> Une image haute-résolution peut consommer **plusieurs milliers de tokens** dans le context window.

Si tu fais du VLM local, **compte les image tokens comme tu comptes les text tokens**. Même budget.

## Templates multimodaux

Plus faciles à casser que les text-only templates :
- Position des markers `<image>` dans la séquence
- Encoding des patches (par patch ou par image)
- Reasoning multimodal-specific tokens
- Tool calls qui retournent des images

Le [[chat-template]] doit gérer tout ça **exactement** comme à l'entraînement.

## Capacités réalistes 2026

- **Petits VLMs** hallucinent les détails visuels — un objet absent peut être "vu"
- **OCR** varie fortement selon le modèle et la qualité d'image
- **Charts et tables** restent durs — souvent mieux servis par des outils dédiés
- **Photos simples** ≠ documents complexes

> *Do not trust a demo of a simple photo to prove invoice extraction quality.*

Toujours évaluer avec **tes** documents, **tes** images, **tes** cas d'usage.

## Implications budget

| Contenu | Tokens approximatifs |
|---|---|
| Image 224×224 basse-res | ~256 tokens |
| Image haute-res (1024px) | 1K-4K tokens |
| Page PDF rendue en image | 2K-8K tokens |
| 1 minute d'audio | 1K-3K tokens |

Pour un VLM avec 32K context, **8 pages PDF rendues en images peuvent saturer** le context. À comparer avec un parsing texte (qui rend 8 pages en ~5-15K tokens, et préserve la structure).

## Related

- [[tokenizer]] — les tokens ne sont pas que du texte
- [[kv-cache]] — image tokens y vivent comme les autres
- [[vram-math]] — vision encoder dans les extras
- [[rag-pipeline]] — pour les docs scannés, OCR + chunk texte est souvent meilleur qu'image directe

## My take

Le marketing "modèle multimodal 1M context" cache que les images bouffent ce context très vite. Pour de l'analyse documentaire sérieuse, OCR + RAG texte reste souvent supérieur à VLM brut sur PDF rendu. À garder en tête face aux démos "regardez il voit tout".

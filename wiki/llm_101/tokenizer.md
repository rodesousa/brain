---
type: concept
summary: Composant qui transforme texte ↔ token IDs entiers. Détermine combien de texte fit dans le context, à quel coût, et si les chat markers sont vus correctement.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - tokenizer-design
  - inference-mechanics
  - context-window
---

Les LLMs ne voient pas du texte mais des **tokens** — petits chunks représentés comme des entiers. Le **tokenizer** fait la traduction dans les deux sens.

Un token peut être : un mot entier, un fragment ("inter", "national", "ization"), un signe de ponctuation, une chaîne précédée d'un espace, un fallback byte-level, ou un marker de contrôle (`<|user|>`, `<|assistant|>`).

## Familles principales

- **BPE-style** (Byte-Pair Encoding) — itératif sur les paires fréquentes
- **SentencePiece-style** — alternative populaire chez Google, supporte mieux les langues sans whitespace

Différents modèles, différents tokenizers. **Un document de 4 000 mots peut donner 5 000 tokens dans un tokenizer et 7 500 dans un autre.**

## Pourquoi le tokenizer matters

| Impact | Pourquoi |
|---|---|
| Combien de texte fit | Le context window est mesuré en tokens |
| Taille du [[kv-cache]] | Cache proportionnel aux tokens |
| Latency de prompt | Prefill traite des tokens, pas des mots |
| Efficacité multilingue / code | Certains tokenizers compriment mieux selon la langue ou la syntaxe |
| Tokens/sec comparables | Pas vraiment — entre familles, c'est apples vs oranges |
| Chat markers vus correctement | Si le tokenizer ne reconnaît pas `<|user|>` comme token spécial, le [[chat-template]] est cassé |

## Vocabulaire

Un vocabulaire plus large peut compresser certains textes en moins de tokens, mais agrandit l'embedding et l'output projection (donc les weights et la mémoire). Pas de free lunch.

## Context window 2026

Modèles locaux courants : 8K, 32K, 128K, 256K. Modèles serveur : jusqu'à 1M tokens. Mais **context supporté ≠ context utile** — voir [[long-context-tradeoffs]].

## Related

- [[chat-template]] — utilise les special tokens du tokenizer
- [[kv-cache]] — taille proportionnelle aux tokens
- [[long-context-tradeoffs]] — le coût des tokens, pas leur prix
- [[multimodal-token-budget]] — images et audio deviennent aussi des tokens

## My take

Le moins glamour des composants, le plus souvent ignoré dans les comparaisons. C'est aussi pour ça que les benchmarks "tokens/seconde" entre familles différentes ne disent pas grand-chose : compter des tokens d'un tokenizer ≠ compter ceux d'un autre.

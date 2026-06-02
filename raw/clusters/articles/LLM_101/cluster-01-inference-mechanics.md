---
type: article-cluster
status: kept
created: 2026-05-22
source: raw/tweet/llms-101-practical-guide-2026.md
---

# Facet 1 — Inference mechanics

Le **modèle mental fondamental** : un LLM ne génère pas une réponse d'un coup, il prédit *un token à la fois* dans une boucle. Tout le reste (hardware, runtime, quantization) se déduit de cette boucle + de la mémoire qu'elle consomme.

## Sections couvertes

- *What An LLM Actually Does* — la boucle d'inférence en 6 étapes
- *Tokens* — texte → IDs entiers, tokenizers (BPE / SentencePiece), context window
- *Transformers* — décodeur-only, RoPE, layers (embeddings, attention, MLP, layernorm, output projection)
- *Attention* — MHA / MQA / GQA, FlashAttention / SDPA
- *KV Cache* — working memory pendant la generation, formule mémoire, FP8/INT8 KV
- *Prefill And Decode* — deux régimes perf différents (parallèle vs séquentiel)
- *Decoding* — politique qui transforme logits → token choisi (temperature, top-p, top-k, stop sequences, constrained decoding)

## Claims-clés

- `f(theta, sequence) → distribution sur next_token` — formulation mathématique
- KV cache ≈ `tokens × layers × kv_heads × head_dim × precision × 2`
- Rule of thumb : ~0.5 MiB/token en FP16 KV cache pour Llama 7B MHA → 16 GiB à 32K tokens
- GQA/MQA réduisent dramatiquement le KV cache vs MHA classique
- Prefill = compute-bound (parallélisable), Decode = memory-bandwidth-bound (séquentiel)
- Sub-8-bit KV cache = research-heavy, à benchmarker avant utilisation
- Greedy decoding n'est pas plus précis, juste plus brittle (loops, génériques)
- Speculative decoding (DFlash, DDTree, EAGLE-style) attaque la decode latency mais ne réduit pas la mémoire KV

## Concepts qui pourraient devenir des pages wiki

- `wiki/llm_101/kv-cache.md`
- `wiki/llm_101/attention-variants.md` (MHA / MQA / GQA / FlashAttention)
- `wiki/llm_101/prefill-vs-decode.md`
- `wiki/llm_101/decoding-policies.md`
- `wiki/llm_101/tokenizer.md`
- `wiki/llm_101/rope-positional-encoding.md`
- `wiki/llm_101/speculative-decoding.md`

## My take

(à compléter au moment du `kept`)

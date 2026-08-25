---
type: entity
summary: Wrapper convivial autour de llama.cpp — gestion de modèles + serveur HTTP simple. Plaisant en surface mais Ahmad recommande explicitement DO NOT USE.
lifecycle: draft
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/web/inference-engines-llms-local-ai-hardware-2026.md
tags:
  - inference-engines
  - llm-runtimes
  - local-llm-deployment
---

**Ollama** est un wrapper convivial autour de [[llama-cpp]] — gestion de modèles via CLI + serveur HTTP simple. Tour de force d'UX : il a démocratisé le local LLM.

## Verdict d'Ahmad : DO NOT USE

> **Note: DO NOT USE Ollama.**

L'auteur d'[[ahmad-osman-inference-engines-2026]] est explicite. Et :

> **DO NOT use llama.cpp or Ollama on multi-GPUs setups — use vLLM or ExLlamaV2.**

## Pourquoi pas ?

Le verdict détaillé n'est pas explicitement développé dans la source mais s'inscrit dans le principe :

> Local engine ≠ production server. llama.cpp server is capable. MLX-LM server is convenient. **Ollama is pleasant yet SHOULD NOT BE USED.**

> Production means security, observability, backpressure, routing, autoscaling, and SLA behavior.

Lecture critique ^[inferred] : Ollama abstrait tellement [[llama-cpp]] qu'on perd le contrôle des paramètres importants (KV cache size, attention kernels, quantization spécifique, chat template) tout en ajoutant ses propres défauts non-documentés. C'est un mauvais default — surfaces marketing-friendly cachant des choix opaques.

## Quand le voir quand même ?

- **Pure prototyping individuel jetable**, et tu n'as jamais utilisé llama.cpp directement
- **Demo** où la simplicité d'install compte plus que tout le reste

Dans ces deux cas, considérer LM Studio (encore plus user-friendly) ou apprendre [[llama-cpp]] directement (à peine plus complexe et beaucoup plus contrôlable).

## Alternatives recommandées

| Cas d'usage | Alternative |
|---|---|
| Desktop débutant | LM Studio |
| Single-user local sérieux | [[llama-cpp]] |
| Single CUDA GPU enthusiast | [[exllamav2]] |
| Team API | [[vllm]] |
| Multi-GPU consumer | [[exllamav3]] |

## Related

- [[llama-cpp]] — l'engine sous-jacent, à utiliser directement
- [[llm-runtimes]] — comparaison wiki
- [[serving-modes-llm]] — pourquoi local engine ≠ production server
- [[ahmad-osman-inference-engines-2026]] — source principale, explicite "DO NOT USE"

## My take

Ollama est l'exemple paradigmatique du **trade UX-contre-rigueur** dans le local LLM. Pour démocratiser, il a flouté beaucoup de choses que tu **dois** comprendre pour ne pas te tirer dans le pied : quel chat template ton modèle attend, comment ton context length scale en KV cache, quelle quantization tu charges, quelles attention kernels sont utilisés. Le verdict d'Ahmad est tranché et je le partage : passe directement à [[llama-cpp]] (1 GPU) ou [[vllm]] (multi-user). La courbe d'apprentissage marginale paye largement dès la première semaine.

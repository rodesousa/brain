---
type: concept
summary: Méthodes de fine-tuning efficaces — LoRA freeze le base et entraîne des adapters low-rank, QLoRA fait pareil à travers un base 4-bit quantized. À essayer en dernier.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - fine-tuning
  - lora-qlora
---

**Fine-tuning** change le comportement d'un modèle en l'entraînant sur des données supplémentaires. Pour les users locaux, les deux méthodes principales sont **LoRA** et **QLoRA**.

## LoRA

- **Freeze** le base model
- Entraîne **uniquement** des adapter weights low-rank (matrices A et B telles que `ΔW = A·B`, avec A et B beaucoup plus petites que W)
- Trainable parameters drastiquement réduits
- Permet de **maintenir plusieurs adapters légers** pour la même base
- Swap d'adapter à chaud possible

## QLoRA

Extension de LoRA :
- Base model **quantized en 4-bit** (gelé)
- Fine-tuning **à travers** le base quantized vers des LoRA adapters
- Permet de fine-tuner des modèles plus gros sur du hardware modeste

## Quand fine-tuner

- Style d'écriture cohérent (voix, ton)
- Format de sortie domain-specific (formulaires, rapports)
- Classification / extraction répétitive
- Tool-call format reliability (au-delà du prompt engineering)
- Persona d'assistant spécialisé
- Domain adaptation que [[rag-pipeline]] ne résout **pas** (vocabulaire spécialisé, conventions internes)
- Performance d'un small model sur une tâche narrow

## Quand NE PAS fine-tuner (d'abord)

> *Most problems that look like "the model does not understand my domain" are actually "my prompt is vague", "my template is wrong", or "my retrieval is broken".*

L'ordre à essayer **avant** fine-tuning :
1. [[chat-template]] correct
2. Better prompting (system prompt, examples)
3. Better model (taille au-dessus, ou famille différente)
4. [[decoding-policies]] tunées
5. [[rag-pipeline]] (retrieval bien fait)
6. Reranking
7. Few-shot examples
8. **THEN** fine-tuning

## Plan de fine-tuning sain

- Data propre, train/validation/test splits
- Baseline evals **avant** ([[llm-eval-methodology]])
- Cible de comportement claire
- Safety review
- Overfitting checks
- Regression evals (pas de dégradation sur ce qui marchait avant)
- Adapter versioning
- License review (le base model autorise-t-il le fine-tuning et la redistribution de l'adapter ?)
- **Rollback plan**

## Related

- [[model-types-llm]] — comprendre l'écart instruct/chat/base avant fine-tuning
- [[rag-pipeline]] — souvent suffit à résoudre "domain adaptation"
- [[open-weight-vs-opensource]] — license du base limite ce que tu peux faire
- [[local-llm-runbook]] — fine-tuning = étape 3 quand simpler methods fail

## My take

LoRA/QLoRA sont accessibles techniquement et tentants. Le vrai piège est de fine-tuner trop tôt — la plupart du temps, un template correct + un RAG bien fait + un prompt clair résout 80% des problèmes qui ressemblent à "le modèle ne connaît pas mon domaine". Garder fine-tuning pour les cas où simpler methods ont vraiment été essayées et ont échoué.

---
type: concept
summary: Open-weight, source-available, opensource AI, local-compatible — 4 catégories souvent confondues. Lire le model card avant tout usage commercial.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/llms-101-practical-guide-2026.md
tags:
  - open-source-licensing
  - model-package
---

En 2026, "open model" est utilisé sloppily. Quatre catégories distinctes :

## 1. Open-weight

Tu peux **télécharger les weights**. Ça ne garantit **pas** :
- Usage commercial
- Modification libre
- Training sur les outputs du modèle
- Deployment à n'importe quelle scale
- Absence d'attribution requirements
- Absence de clauses de patent ou de copyleft

C'est le minimum bar. La majorité des "modèles ouverts" 2026 sont open-weight.

## 2. Source-available

Le code ou les weights sont **visibles**. La license n'est pas forcément opensource pour autant. Visible ≠ libre.

## 3. Opensource AI (OSI definition)

Le bar le plus haut. La définition OSI considère qu'un système AI est opensource s'il inclut :
- **Architecture** publique
- **Parameters / weights** disponibles
- **Inference code** publié
- **Enough data information and code** pour dériver les paramètres (information sur les données + code de training)

Beaucoup plus exigeant que "les weights sont sur Hugging Face".

## 4. Local-compatible

Tu peux le faire tourner localement. **Ne dit rien** sur la license. Un modèle peut être :
- Local-compatible mais commercial-restricted
- Open-weight mais pas vraiment local-compatible (taille rédhibitoire pour consumer hardware)

## Restrictions à chercher dans les licenses

Même quand une license a l'air permissive, lire pour :
- **No competitive use** (interdit aux concurrents directs du créateur)
- **No training on outputs** (les outputs ne peuvent pas servir à entraîner un autre modèle)
- **No deployment au-dessus d'une scale** (au-delà de X users, license commerciale requise)
- **Geographic exclusions** (interdit dans certaines juridictions)
- **Attribution requirements** (mention obligatoire)
- **Patent clauses** (octroi ou rétractation de droits patent)
- **Copyleft-like obligations** sur les derivatives (LoRA adapters tombent-ils dedans ?)

## Règle pratique

> *Read the model card and license before using any model commercially.*

Un modèle peut être excellent, downloadable, et localement runnable tout en étant un mauvais fit légal ou opérationnel.

## Familles courantes 2026 et leur position

- **Llama** (Meta) — open-weight avec restrictions ("Llama community license")
- **Qwen 3.5/3.6** (Alibaba) — Apache 2.0 sur la plupart, vérifier par taille
- **Gemma 4** (Google) — Apache 2.0 (un des points forts marketing)
- **DeepSeek** — license maison, vérifier
- **Mistral** — mixte (Apache 2.0 sur certains, Mistral Research License sur d'autres)
- **Kimi / Moonshot** — license maison

Toujours **vérifier la license du tag spécifique** que tu télécharges. Une famille peut avoir plusieurs licenses selon la variante.

## Related

- [[model-package]] — la license fait partie du package
- [[local-llm-2026-scene]] — chaque famille a sa politique
- [[local-llm-runbook]] — étape "confirm hardware AND license"
- [[lora-qlora]] — vérifier que la license autorise le fine-tuning et la redistribution de l'adapter

## My take

Le piège juridique est sous-estimé dans la communauté local LLM, parce que pour un usage perso, peu importe. Mais dès qu'on monte une startup, qu'on sert des clients, ou qu'on publie des adapters fine-tunés, la license du base devient critique. Vaut mieux le savoir avant d'avoir un problème que pendant un legal review.

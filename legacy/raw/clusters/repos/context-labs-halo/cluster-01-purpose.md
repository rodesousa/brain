---
type: repo-cluster
repo: context-labs/halo
facet: purpose
status: kept
created: 2026-05-09
source: raw/repos/context-labs-halo.md
---

# HALO — purpose

## Le problème adressé

Les agent harnesses (Claude Code, Cursor, etc. ou harnesses custom) déployés en production accumulent des **failure modes systémiques** : refus en boucle, hallucination de tool calls, arguments redondants, incohérences sémantiques. Ces failures sont :
- Fréquentes en environnements à haut trafic (forte variance d'exécution)
- Non visibles trace par trace (chaque incident isolé semble bénin)
- Coûteuses à diagnostiquer manuellement (les traces sont longues et nombreuses)

## La proposition de valeur

HALO automatise la boucle "observation → diagnostic → correction" à l'échelle d'un harness :
- Collecte les traces d'exécution (OpenTelemetry-compatible)
- Identifie les failure modes **systémiques** (pas juste des incidents isolés)
- Produit un rapport
- Le rapport est consommé par un coding agent qui modifie le harness
- Boucle qui se répète

## Pour qui

Équipes qui exploitent des agents en prod, en environnement à fort volume, et qui veulent améliorer le harness sans changer le modèle sous-jacent (= "harness optimization", distinct de "model improvement").

## Pourquoi c'est intéressant pour toi

Tu vis dans Claude Code, donc :
- Le pitch "améliorer le harness sans toucher au modèle" est directement actionnable sur ton propre setup
- L'idée d'observer systématiquement les traces avant de patcher au feeling colle au principe "mesure avant d'optimiser"
- Ça révèle un cycle de vie qu'on néglige souvent : on configure un agent, on l'oublie, on le redécouvre cassé 3 mois plus tard

## My take

Le but est de créér une boucle de retro action pour améliorer les call des tools, les prompts. Il faudrait pour améliorer avoir des indicateurs de performance.

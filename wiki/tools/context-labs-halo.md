---
type: entity
summary: Outil d'analyse automatique de traces d'agents en prod — détecte les failure modes systémiques et fait appliquer les fixes par un coding agent.
lifecycle: reviewed
created: 2026-05-09
updated: 2026-05-13
sources:
  - raw/repos/context-labs-halo.md
tags:
  - harness-optimization
  - trace-analysis
  - observability-tooling
  - prod-agent-tooling
---

# context-labs/halo

HALO (Hierarchical Agent Loop Optimization) est une méthodologie + un outil pour rendre les agent harnesses **récursivement auto-améliorants** à partir de leurs traces d'exécution. Cible : équipes qui exploitent un agent en production à fort volume.

## Le problème adressé

Les agent harnesses déployés en prod accumulent des **failure modes systémiques** — refus en boucle, hallucinations de tool calls, arguments redondants, incohérences sémantiques. Ces failures sont :
- Fréquentes dès qu'il y a du volume et de la variance d'exécution
- Invisibles trace par trace (chaque incident isolé semble bénin)
- Coûteuses à diagnostiquer à la main (les traces sont longues et nombreuses)

L'observation manuelle ne scale pas, et un coding agent généraliste type Claude Code lancé sur une poignée de traces tend à *overfit* aux erreurs visibles dans 1-2 cas plutôt qu'à généraliser au niveau du harness.

## La méthodologie — la boucle HALO en 5 étapes

> 1. Collect execution traces from your agent harness. HALO uses OpenTelemetry-compatible tracing.
> 2. Feed traces into HALO-RLM engine.
> 3. The engine decomposes the traces to understand common failure modes across harness executions and produces a report with its findings.
> 4. This report is fed into a coding agent like Cursor or Claude Code to generate and apply a set of changes to your harness.
> 5. The harness is then re-deployed, more traces are gathered, and the cycle repeats.

Décomposition des rôles :

| Acteur | Rôle |
|---|---|
| Le harness en prod | Émet les traces (OpenTelemetry) pendant son fonctionnement normal |
| HALO-RLM | Analyse — décompose, agrège, identifie les patterns systémiques |
| Le rapport | Document structuré des failure modes |
| Le coding agent (CC, Cursor) | Lit le rapport, modifie le code du harness |
| L'humain | Valide les changements (implicite) |

Boucle fermée mais **assistée** : l'humain peut intervenir à chaque cycle, notamment pour valider les changements de l'étape 4.

## Question pratique — qui collecte les traces ?

Ni HALO ni un agent dédié : **c'est le harness en production qui émet les traces naturellement** pendant qu'il fait son job. HALO **consomme** un fichier JSONL de traces préexistantes, ne les orchestre pas.

Implication directe : HALO suppose un agent déjà déployé à l'échelle. Pas pertinent pour des prototypes ou des usages mono-utilisateur — pas assez de volume pour que l'analyse statistique ait du signal. C'est cohérent avec l'insistance du README sur les "high-traffic environments".

## Caractéristiques techniques

- Distribution : package Python `halo-engine` sur PyPI, CLI + API
- Tracing : OpenTelemetry-compatible
- Format d'entrée : fichier JSONL de traces
- Benchmark validé : AppWorld (gain +10 à +16 points SGC sur Gemini 3 Flash et Sonnet 4.6 selon split)
- License : MIT

## My take

Le but est de créer une boucle de rétroaction pour améliorer les calls de tools et les prompts d'un harness. La pièce manquante du raisonnement, qui mérite réflexion : **il faudrait avoir des indicateurs de performance** pour mesurer si la boucle améliore vraiment les choses, sinon on ne sait pas distinguer un changement qui aide d'un changement qui dérive. HALO mentionne ça implicitement via les benchmarks (dev/test split) mais en prod réelle, les indicateurs sont moins évidents — c'est probablement le vrai problème ouvert.

Pas applicable à mon usage CC perso (pas de prod scale), mais le pattern méta "outil spécialisé pour analyse de traces, distinct du coding agent qui applique les fixes" reste exportable.

## Sources

- [[context-labs-halo]] — README brut snapshoté le 2026-05-09
- [[cluster-01-purpose]] — facet purpose (kept)
- [[cluster-02-methodology]] — facet methodology (kept, contient la question/réponse sur la collecte)

Facets écartées : `rlm-design` (cluster-03, discarded), `lessons` (cluster-05, discarded).

## Related

- [[hermes-agent]] — framework d'agent qui adresse au runtime les mêmes failure modes que Halo détecte post-hoc dans les traces (zombies, hallucination gate, perte de goal, recovery après crash).

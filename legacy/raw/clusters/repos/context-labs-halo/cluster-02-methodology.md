---
type: repo-cluster
repo: context-labs/halo
facet: methodology
status: kept
created: 2026-05-09
source: raw/repos/context-labs-halo.md
---

# HALO — methodology

## La boucle HALO en 5 étapes

> The core HALO loop is surprisingly simple:
>
> 1. Collect execution traces from your agent harness. HALO uses OpenTelemetry-compatible tracing.
> 2. Feed traces into HALO-RLM engine.
> 3. The engine decomposes the traces to understand common failure modes across harness executions and produces a report with its findings.
> 4. This report is fed into a coding agent like Cursor or Claude Code to generate and apply a set of changes to your harness.
> 5. The harness is then re-deployed, more traces are gathered, and the cycle repeats.

## Décomposition des rôles

| Acteur | Rôle |
|---|---|
| Le harness en prod | Génère les traces (OpenTelemetry) |
| HALO-RLM | Analyse — décompose, agrège, identifie les patterns systémiques |
| Le rapport | Document structuré des failure modes |
| Le coding agent (CC, Cursor) | Lit le rapport, modifie le code du harness |
| L'humain | Valide les changements (implicite — pas explicite dans le README mais probable) |

## Condition de bon fonctionnement

> We find high-traffic environments tend to generate more data with higher variance across executions, creating the type of issues that HALO is great at identifying.

→ Ne marche bien qu'à partir d'un certain volume de traces. Sur un harness à faible trafic, l'analyse statistique n'a pas assez de signal.

## Boucle ouverte vs fermée

Le loop est *fermé* (re-deploy → traces → ...) mais l'humain peut intervenir à chaque cycle (notamment à l'étape 4, valider les changements proposés). C'est une auto-amélioration **assistée**, pas autonome.

## Pourquoi c'est intéressant pour toi

- La séparation claire des 5 étapes est exportable comme **template d'auto-amélioration** pour n'importe quel système agentique, pas seulement le tien
- L'idée de séparer "moteur d'analyse" et "moteur de modification" (RLM vs coding agent) plutôt qu'un agent unique fait les deux : choix design qui mérite réflexion
- L'OpenTelemetry comme standard de trace = bon réflexe d'observabilité

## My take

Ma question c'est qui lance l'agent pour collecter autant de data ? Il faut que ce soit HALO lui meme ?

## Réponse

Ni HALO ni un agent dédié — c'est **le harness en production qui émet les traces naturellement** pendant son fonctionnement normal. Le harness (CC, Cursor, custom) est instrumenté avec OpenTelemetry → traces émises en arrière-plan à chaque exécution → collectées dans un trace store (typiquement un fichier JSONL) → consommées par HALO via `halo path_to_traces.jsonl`.

HALO **consomme** les traces, ne les **orchestre** pas. C'est pour ça que le README insiste sur "high-traffic environments" : il faut un volume suffisant généré naturellement par l'usage en prod, sans effort de collecte.

**Implication** : HALO suppose un agent déjà déployé à l'échelle. Pas pertinent pour des prototypes ou des usages mono-utilisateur.

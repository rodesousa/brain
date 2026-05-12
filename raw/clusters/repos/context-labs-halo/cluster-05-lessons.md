---
type: repo-cluster
repo: context-labs/halo
facet: lessons
status: discarded
created: 2026-05-09
source: raw/repos/context-labs-halo.md
---

# HALO — leçons transférables au-delà du repo

## 1. "Outil spécialisé pour tâche spécialisée"

Pattern récurrent : dès qu'une tâche a des contraintes structurelles fortes, un outil généraliste devient plus cher qu'un dédié, même si le modèle sous-jacent est meilleur. Cf. cluster `rlm-design` pour l'argumentation détaillée. **Application directe** : auditer où dans tes workflows tu utilises CC pour des tâches qui mériteraient un sous-outil dédié.

## 2. "Observabilité avant optimisation"

> Collect execution traces from your agent harness.

L'étape 1 de HALO n'est pas du tuning — c'est de la collecte. **Tu ne peux pas améliorer ce que tu n'observes pas.** Avant de patcher un harness au ressenti, instrumenter (OpenTelemetry chez HALO, mais le principe est outil-agnostique).

**Application directe** : as-tu de l'observabilité sur tes workflows agents ? Quelles traces, accessibles, comment ?

## 3. Méta-pattern : un agent qui améliore l'agent

HALO incarne un cycle :
- Niveau 0 : ton agent fait son job
- Niveau 1 : un autre agent (HALO-RLM) regarde le niveau 0 et propose des fixes
- Niveau 2 (implicite) : un humain valide les fixes du niveau 1

C'est une **stratification** : chaque niveau opère sur les outputs du niveau d'en dessous. **Application** : même pattern pour code review (CC fait du code, autre CC le review), pour planning (un agent décompose, un autre exécute), etc.

## 4. Méthodo dev/test split anti-overfitting

> We iterated on the harness using the `dev` split, and then used the `test_normal` split as a proxy to verify that improvements did not come from overfitting.

Idée empruntée au ML classique mais appliquée à l'optimisation de harness. **Application** : si tu améliores un prompt système ou un agent, garde un set d'exemples "test" jamais vus pendant l'itération, vérifie que tes gains tiennent dessus.

## 5. Le critère "high variance"

> high-traffic environments tend to generate more data with higher variance across executions, creating the type of issues that HALO is great at identifying.

L'analyse statistique n'a de sens qu'à partir d'un certain volume + une certaine variance. **Corollaire** : sur un harness mono-tâche peu varié, HALO (et tout équivalent) ne servirait à rien — un humain qui regarde 10 traces fait le même boulot. Critère utile pour décider si l'investissement vaut le coup.

## Pourquoi c'est intéressant pour toi

C'est ici que se trouve la vraie valeur du repo pour toi : pas l'outil HALO en lui-même (que tu n'utiliseras peut-être jamais directement), mais les patterns extractibles. Les 5 leçons ci-dessus sont chacune **utilisable indépendamment de HALO** dans ton propre travail.

## My take

_(à remplir au moment du `kept`)_

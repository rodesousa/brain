---
type: repo-cluster
repo: context-labs/halo
facet: rlm-design
status: discarded
created: 2026-05-09
source: raw/repos/context-labs-halo.md
---

# HALO — pourquoi une RLM spécialisée plutôt que CC généraliste

## L'argument central

> A general-purpose harness like Claude Code is the wrong tool for trace analysis. This isn't because the model isn't smart, but because traces can get extremely long, and you need a specialized toolkit in order to make observations about systemic agentic behavior. We noticed in our testing that harnesses like CC would often overfit to an error present in a single/few traces rather than generalize to harness-level problems. This led us to creating a specialized form of a RLM.

Trois raisons distinctes empilées :
1. **Volume** — les traces sont longues, le contexte CC se sature vite
2. **Toolkit dédié** — il faut des primitives spécifiques (agrégation, clustering de patterns, statistiques d'erreurs) que CC n'a pas par défaut
3. **Failure mode de CC** — il *overfit* aux erreurs visibles dans 1-2 traces au lieu d'identifier les patterns systémiques (= échec de généralisation)

## Qu'est-ce qu'une RLM ?

Le README pointe vers [alexzhang13/rlm](https://github.com/alexzhang13/rlm). RLM = "Recursive Language Model". Pas explicité dans le README de HALO. À investiguer si tu pousses cette facet plus loin.

## Le pattern design transférable

L'argument "outil généraliste vs spécialisé" se rejoue ailleurs :
- IDE généraliste vs éditeur dédié (VS Code vs Vim pour des cas spécifiques)
- ORM vs SQL brut quand la requête est tordue
- LLM généraliste vs modèle fine-tuné sur ton domaine
- Coding agent généraliste vs trace analyzer spécialisé ← le cas de HALO

La règle implicite : **dès qu'une tâche a des contraintes structurelles fortes (volume, primitives requises, failure modes spécifiques), un outil généraliste devient plus coûteux qu'un outil dédié — même si le modèle sous-jacent est puissant.**

## Pourquoi c'est intéressant pour toi

- Tu utilises CC partout — ce papier te dit *où* CC ne sera *pas* le bon outil
- Le critère "overfit aux 1-2 cas visibles" est observable chez tes propres usages : quand tu demandes à CC d'analyser plusieurs incidents, il a tendance à se focaliser sur le dernier
- L'argument se généralise au-delà des traces d'agents : analyse de logs, code review à l'échelle, etc.

## My take

_(à remplir au moment du `kept`)_

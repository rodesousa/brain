---
type: concept
summary: Fichier CLAUDE.md placé à la racine d'un projet — prompt système persistant lu automatiquement par Claude Code à chaque session pour fixer scope, stack, contexte et garde-fous.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources: [raw/web/karpathy-claude-md-viral-thread.md]
tags: [claude-code, prompt-engineering, context-file, coding-assistant]
---

## Le problème

Claude Code démarre chaque session avec zéro contexte projet. Il ne connaît ni le stack, ni les conventions, ni les décisions passées, ni les approches déjà écartées. Conséquences récurrentes :

- Refactors non demandés sur du code adjacent.
- Suggestions de frameworks incompatibles avec l'architecture en place.
- Décisions déjà tranchées qui sont contredites.
- 30 min/jour passées à ré-expliquer le même contexte ^[ambiguous] (chiffre marketing, ordre de grandeur plausible).

## Le pattern

Un fichier `CLAUDE.md` plain text à la racine du projet, lu automatiquement par Claude Code au démarrage de chaque session. Trois catégories de contenu se sont stabilisées dans les versions virales :

### 1. Defaults — calibrer le ton et le profil

- Profil utilisateur (rôle, expertise, gaps de connaissance).
- Contexte projet (goal, audience, contraintes, à-éviter).
- Style de communication (longueur, voice, vocabulaire à proscrire).
- Comportements de réponse (no filler, match length to task, admit uncertainty).

### 2. Behavior — fixer les garde-fous d'action

- Stay in scope — ne toucher que ce qui est demandé.
- Ask before big changes — confirmation explicite avant réécriture.
- Confirm before destructive — list impact avant deletes/overwrites.
- Hard stops production — deploys, migrations, API externes.
- Always show diff — files changed / not touched / follow-up.

### 3. Memory + Stack — donner une mémoire

- `MEMORY.md` — decision log append-only (what / why / what rejected).
- `ERRORS.md` — failure log après >2 tentatives infructueuses.
- Lock du tech stack — langage, framework, PM, db, test, styling.
- Permanent facts — contraintes architecturales toujours vraies.

## Les "4 règles" attribuées à Karpathy

Distillation virale, sans lien vers le gist original ^[ambiguous] :

1. **Ask, don't assume** — clarifier avant de coder.
2. **Simplest solution first** — pas d'abstractions non demandées.
3. **Don't touch unrelated code** — pas de refactor en passant.
4. **Flag uncertainty explicitly** — l'incertitude assumée coûte moins cher que la confiance erronée.

Ces 4 règles sont des truismes d'ingénierie, leur valeur tient à leur **explicitation écrite** plus qu'à leur originalité.

## Limites et angles morts

- **Pas de garantie d'application** — le modèle peut violer ses propres règles, surtout en milieu de session longue ou sur tâches mal cadrées.
- **Risque d'inflation** — un `CLAUDE.md` qui grossit dilue les règles importantes dans le bruit.
- **Conflit avec d'autres signaux** — instructions du user en cours de session peuvent contredire le fichier ; ordre de priorité à clarifier.
- **Pas un substitut à la review** — réduit le bruit mais ne supprime pas le besoin de relire les diffs.

## Convergence avec ce vault

Le pattern `MEMORY.md` décrit ici recoupe la mémoire persistante que ce vault utilise déjà côté `memory/MEMORY.md` (index de mémoires user/feedback/project/reference). Le `CLAUDE.md` du vault lui-même implémente la partie "behavior + stack" appliquée à un cas wiki plutôt que codebase. ^[inferred]

## Related

- [[karpathy-claude-md-viral-thread]] — source de ce résumé.

## My take

Le pattern est réel, utile, et largement adopté — mais son packaging viral noie une vérité simple dans du marketing. Trois choses à retenir :

1. **L'écriture explicite des règles a une valeur, même si les règles sont banales.** Forcer "don't touch unrelated code" sur disque change le comportement plus que de l'attendre comme acquis.
2. **Le bon `CLAUDE.md` est court, situé, et révisé.** Coller 21 règles génériques sans les adapter au projet, c'est du cargo cult. Mieux vaut 5 règles spécifiques que 21 génériques.
3. **Les patterns `MEMORY.md` / `ERRORS.md` sont la partie la plus sous-estimée.** C'est là que se joue le passage d'un assistant amnésique à un collaborateur qui apprend du projet. Le reste est de l'hygiène de prompt.

Pour ce vault : le pattern justifie d'enrichir le `CLAUDE.md` projet avec une section explicite "à ne jamais faire" plutôt que de compter sur l'inférence depuis les conventions. Convergence avec la mémoire user/feedback déjà en place.

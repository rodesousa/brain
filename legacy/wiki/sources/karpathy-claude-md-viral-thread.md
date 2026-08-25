---
type: source-summary
summary: Thread X marketing (mai 2026) qui distille un CLAUDE.md viral en 21 règles classées en 3 sections — defaults, behavior, memory+stack — plus les 4 règles attribuées à Karpathy.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources: [raw/web/karpathy-claude-md-viral-thread.md]
tags: [claude-code, prompt-engineering, context-file, coding-assistant]
---

## Identité

- Auteur : @0xDepressionn sur X (status 2055999112470839383).
- Publié : 2026-05-17. Clippé : 2026-05-22.
- Format : thread listicle, ton hype, structuré ROI ($X/semaine gaspillé sans CLAUDE.md).
- Référence centrale : un `CLAUDE.md` arrivé #1 GitHub Trending (82k stars, 7,8k forks) — origine attribuée à Karpathy qui aurait identifié 4 comportements faisant échouer Claude Code.

## Claim principal (à vérifier)

> "Coding accuracy went from 65% to 94%" après adoption du fichier.

Aucune source, méthodologie, ni lien vers le gist Karpathy original. À traiter comme claim marketing, pas comme résultat reproductible. ^[ambiguous]

## Les 21 règles, par section

### Defaults (7 règles)

1. Kill the filler — pas de "Great question!", démarrer par la réponse.
2. Match length to task — courte pour simple, longue pour complexe, jamais de padding.
3. Show options before acting — 2-3 approches avant tâche significative, attendre choix.
4. Admit uncertainty before it costs me — flagger l'incertitude factuelle explicitement.
5. Who I am and what I know — profil user (rôle, expertise, gaps) pour calibrer la profondeur.
6. Current project context — projet, goal, audience, contraintes, à-éviter.
7. Lock your voice — style d'écriture, longueur phrases, vocabulaire à utiliser/éviter.

### Behavior (7 règles)

1. Stay in scope — modifier seulement ce qui est demandé, signaler le reste sans toucher.
2. Ask before big changes — décrire avant de réécrire, attendre confirmation.
3. Confirm before destructive — lister l'impact, demander confirmation explicite in-session.
4. Hard stops for production — deploys, migrations, API calls externes, side effects irréversibles.
5. Always show what changed — files changed / what modified / not touched / follow-up.
6. Never act without explicit confirmation — send/post/publish/share/schedule.
7. Think before you write code — raisonnement step-by-step pour architecture/debug/non-trivial.

### Memory + Stack (7 règles)

1. `MEMORY.md` decision log — what decided / why / what rejected, lu en début de session.
2. Session end summary — déclencheur "session end" → écrire dans `MEMORY.md`.
3. `ERRORS.md` failure log — >2 tentatives → logger ce qui n'a pas marché.
4. Permanent facts list — contraintes architecturales toujours vraies.
5. Lock your tech stack — langage/framework/PM/db/test/styling, ne pas suggérer d'alternatives.
6. Extended thinking for hard decisions — architecture, perf, db design, décisions long-terme.
7. Les **4 règles "virales" de Karpathy** :
   1. Ask, don't assume.
   2. Simplest solution first.
   3. Don't touch unrelated code.
   4. Flag uncertainty explicitly.

## Argumentaire ROI (à prendre avec recul)

- 30 min/jour à re-expliquer le contexte = $375/sem/dev.
- 1h/sem à revert des changements non autorisés = $225/sem/dev.
- 2h/sem à récupérer de décisions oubliées = $375/sem/dev.
- Total : **$975/sem/dev**, $253k/an pour équipe de 5.

Chiffrage qui assume $150/h dev partout, sans coût alternatif, sans gain marginal décroissant. Marketing, pas étude. ^[inferred]

## Related

- [[claude-md-pattern]] — le concept extrait de cette source.

## My take

Le contenu pratique est solide et largement aligné avec les bonnes pratiques Claude Code que j'utilise déjà (scope discipline, ask-before-destructive, decision log). Mais le packaging est trompeur sur trois axes :

1. **Attribution Karpathy douteuse** — le thread ne link pas le gist original. Les "4 règles virales" sont des truismes d'ingénierie qui n'ont rien de spécifique à Karpathy. Ça sent le name-dropping pour gonfler la viralité.
2. **Le 65% → 94%** est cité sans benchmark, sans méthodo, sans baseline. Inutilisable comme preuve, à citer "selon l'auteur" si on s'y réfère.
3. **Le ROI** mélange coûts horaires théoriques et hypothèses non vérifiables. C'est un outil de conversion, pas de mesure.

Ce qui mérite d'être retenu malgré le ton : le **pattern `MEMORY.md` + `ERRORS.md`** est exactement ce que ce vault implémente côté `memory/` — convergence intéressante qui valide l'intuition. Les 7 règles "Behavior" sont la liste la plus actionnable du thread et recoupent ce qu'on documente déjà dans le [[claude-md-pattern]].

Verdict : source utile comme **inventaire de règles à piocher**, à ne pas citer comme autorité.

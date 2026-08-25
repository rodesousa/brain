---
type: concept
summary: Trois prompts utilisables pour Claude — interview pour générer un CLAUDE.md, audit régulier d'un Project, stress-test d'une décision. Extraits d'un listicle X, sources marketing autour.
lifecycle: reviewed
created: 2026-05-22
updated: 2026-05-22
sources:
  - raw/tweet/12-claude-tips-kingwilliamdefi.md
tags:
  - claude-anthropic
  - prompt-patterns
  - decision-framework
  - project-setup
---

Trois prompts ré-utilisables, extraits d'un post X de @KingWilliamDefi (mai 2026). Le post lui-même est du content marketing listicle, mais ces trois prompts ont une valeur durable indépendante.

## 1. Générer un CLAUDE.md par interview

À lancer dans un nouveau Project / nouvelle conversation. Le modèle pose 10 questions une par une, puis produit le fichier.

```text
Interview me with 10 questions to build my CLAUDE.md.

Cover: who I am, my exact audience, my tone in 3 words, my hard rules, my goals this month, and 3 examples of my best work.

One question at a time. After I answer all 10 - write the final file in under 200 lines.
```

**Quand l'utiliser** : démarrage d'un nouveau Project, ou refonte d'un CLAUDE.md devenu obsolète.

**Variantes utiles** :
- Remplacer "this month" par "this quarter" pour un setup long-terme
- Demander "under 100 lines" pour un Project léger
- Ajouter "ask follow-up if my answer is vague" pour pousser à la précision

## 2. Audit régulier d'un Project

À lancer tous les 14 jours environ sur un Project actif. Force le modèle à pointer les trous, pas à valider.

```text
Review my Project instructions and files.

Tell me: what context is missing that would make you more accurate.

What you're currently guessing that I should just tell you directly.

What files would help most if I uploaded them. I want gaps, not compliments.
```

**Quand l'utiliser** : Project qui tourne depuis 2-4 semaines, qualité des outputs qui plafonne ou dérive.

**Le knob critique** : *"I want gaps, not compliments"* — sans cette phrase, le modèle tend à valider l'existant.

## 3. Stress-test de décision

À lancer **avant** de prendre une décision importante. Force le modèle à jouer l'avocat du diable.

```text
Here is the decision I'm about to make: [describe it]

1. What has to be true for this to work
2. Which assumption is weakest
3. Who is on the other side of this and what do they know that I don't
4. What would make you tell me not to do this

Don't validate me. Stress-test me.
```

**Quand l'utiliser** : avant un investissement, un changement de cap, un commit irréversible, un hire/fire, un launch.

**Le pattern à retenir** : explicitement demander *"don't validate me"* — sinon Claude (comme tout LLM RLHF-tuné vers la politesse) penche vers l'accord.

## Pattern transverse

Les trois prompts partagent une même mécanique : **forcer le modèle à produire du contenu *contre* l'utilisateur** (questions au lieu de réponses ; gaps au lieu de compliments ; stress-test au lieu de validation). C'est la chose à internaliser, plus que les prompts eux-mêmes.

Sans cette discipline, Claude est utilisé comme **yes-man amélioré** — confirmation de ce qu'on pense déjà, formulé plus joliment. La valeur réelle vient de l'inverse.

## Related

- *(à ajouter si une page sur le pattern "anti-sycophancy" / "adversarial prompting" est créée plus tard)*

## My take

Le post source vend "12 trucs", mais 9 d'entre eux sont des rappels de features (CLAUDE.md, Projects, Skills, Scheduled Tasks). Les 3 prompts capturés ici sont la vraie valeur durable. À garder comme cheat sheet — particulièrement le stress-test (#3), qui est probablement le plus sous-utilisé en pratique parce que demander à un LLM de te contredire demande une discipline qu'on n'a pas naturellement.

Source unique pour l'instant. À enrichir quand on croisera d'autres prompts du même genre (livre *Reid Hoffman's Impromptu*, articles sur "anti-sycophancy", etc.).

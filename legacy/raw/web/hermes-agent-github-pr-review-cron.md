---
source-type: web
url: https://hermes-agent.nousresearch.com/docs/guides/github-pr-review-agent
fetched: 2026-05-18
---

# Hermes Agent — GitHub PR Review Agent (cron-driven) (doc guides)

Snapshot de la page de documentation `guides/github-pr-review-agent` du site officiel de Hermes Agent (Nous Research), au 2026-05-18.

## Overview

Construire un agent IA qui review automatiquement les pull requests GitHub sur un schedule, pour résoudre le bottleneck "PRs sit for days waiting for eyeballs".

## Architecture

```
Cron Timer → Hermes Agent + gh CLI + skill + memory → GitHub API → Review delivery (Telegram, Discord, local)
```

Polling approach, pas event-driven (cf. guide webhook séparé).

## Prerequisites

- Hermes Agent installé avec gateway running.
- GitHub CLI (`gh`) authentifié via `gh auth login`.
- Optionnel : Telegram ou Discord configuré pour les notifications.
- Alternative : sauver les reviews localement via `deliver: "local"`.

## Steps

**Step 1** — Vérifier l'accès GitHub :

```
gh pr list --repo NousResearch/hermes-agent --state open --limit 3
```

**Step 2** — Test manuel d'une review :

```
gh pr diff 3888 --repo NousResearch/hermes-agent
```

**Step 3** — Créer une skill à `~/.hermes/skills/code-review/SKILL.md` définissant les guidelines de review (bugs, security, performance, style, tests).

**Step 4** — Enseigner les conventions via memory (type annotations, ORM requirements, testing frameworks).

**Step 5** — Créer le cron job :

```
hermes cron create "0 */2 * * *" "[instructions]" --name "pr-review" --deliver telegram --skill code-review
```

**Step 6** — Lancer manuellement :

```
hermes cron run pr-review
```

## Advanced Options

- Poster les reviews directement sur GitHub via `gh pr review`.
- Générer des weekly dashboards le lundi matin.
- Monitorer plusieurs repos séquentiellement.

## Troubleshooting

- `gh` absent du PATH.
- Reviews génériques → ajouter skill + memory.
- Cron qui ne run pas → vérifier le status de la gateway.
- Rate limits → GitHub autorise 5 000 requêtes/heure pour users authentifiés.

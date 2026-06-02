---
source-type: web
url: https://hermes-agent.nousresearch.com/docs/guides/webhook-github-pr-review
fetched: 2026-05-18
---

# Hermes Agent — Webhook GitHub PR Review (doc guides)

Snapshot de la page de documentation `guides/webhook-github-pr-review` du site officiel de Hermes Agent (Nous Research), au 2026-05-18.

## Overview

Setup de PR reviews automatisés via **webhooks**. Quand une PR est opened/updated, GitHub envoie une requête webhook POST qui déclenche Hermes : fetch du diff, analyse, post de commentaire.

Variante event-driven du pattern présenté dans la version cron (`github-pr-review-agent`).

## Prerequisites

- Hermes Agent installé et running avec gateway capability.
- GitHub CLI installé et authentifié sur le host de la gateway.
- URL **publiquement reachable** pour l'instance Hermes.
- Accès admin sur le repo pour gérer les webhooks.

## Configuration

Activer les webhooks dans `~/.hermes/config.yaml` sous la section `platforms`. Éléments clés :

- **Port** : 8644 par défaut (customizable). À distinguer du port API server (8642).
- **Rate limiting** : 30 requêtes/minute par route.
- **Route-specific settings** : secret, events filter, prompt template, delivery method.
- **Payload field resolution** : syntaxe `{field}` et `{nested.field}` pour substitution dynamique depuis le payload du webhook.

## Détails d'implémentation critiques

- **Le webhook payload ne contient pas les diffs de code**. La config instructe l'agent de récupérer le diff lui-même : `gh pr diff {number} --repo {repository.full_name}`.
- **Le filtrage d'events GitHub se fait au niveau header uniquement**. On peut spécifier `pull_request`, mais **on ne peut pas filtrer par action subtype** (`opened`, `closed`, `labeled`) au niveau routing. Le prompt gère cela en instruisant l'agent à skipper certaines actions.

## Delivery Options

Les réponses peuvent être routées vers :

- Commentaires GitHub (via `gh pr comment`)
- Slack
- Discord
- Telegram, Signal, SMS, ou logging local

## Testing

- **Local dev** : ngrok pour exposer le localhost endpoint.
- Smoke test fourni : curl construisant un webhook payload **proprement signé** pour tester sans repo GitHub réel.

## Sécurité

> "Webhook payloads contain attacker-controlled data — PR titles, commit messages, and descriptions can contain malicious instructions."

Recommandations :

- Run la gateway en environnement sandboxé (Docker, SSH) quand internet-exposed.
- HMAC signature validation.
- Rate limiting.
- Idempotency caching via delivery ID headers.

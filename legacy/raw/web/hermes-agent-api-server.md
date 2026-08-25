---
source-type: web
url: https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server
fetched: 2026-05-17
---

# Hermes Agent — API server (doc user-guide)

Snapshot du contenu utile de la page de documentation `features/api-server` du site officiel de Hermes Agent (Nous Research), au 2026-05-17.

## Vue d'ensemble

Le serveur API expose Hermes Agent comme un **endpoint HTTP compatible OpenAI**, utilisable depuis des frontends comme **Open WebUI**, **LobeChat**, **LibreChat**. L'agent traite les requêtes avec sa toolset complète et renvoie une réponse, le streaming affichant les indicateurs de progression d'outils.

## Quick start

Activer le serveur API en ajoutant dans `~/.hermes/.env` :

```
API_SERVER_ENABLED=true
API_SERVER_KEY=change-me-local-dev
API_SERVER_CORS_ORIGINS=http://localhost:3000
```

Démarrer la gateway : `hermes gateway` (écoute sur `http://127.0.0.1:8642`).

Test curl :

```bash
curl http://localhost:8642/v1/chat/completions \
  -H "Authorization: Bearer change-me-local-dev" \
  -H "Content-Type: application/json" \
  -d '{"model": "hermes-agent", "messages": [{"role": "user", "content": "Hello!"}]}'
```

## Endpoints principaux

### Chat Completions (OpenAI-compatible)

- **POST /v1/chat/completions** — Format standard OpenAI Chat Completions (stateless, conversation complète par requête). Supporte les images inline via `image_url` (HTTP/HTTPS distantes ou `data:image/`). Streaming = Server-Sent Events avec événements `chat.completion.chunk` + événement custom `hermes.tool.progress` pour la visibilité des outils.

### Responses API (state-ful)

- **POST /v1/responses** — Format OpenAI Responses API avec état de conversation côté serveur. Supporte `previous_response_id` pour la préservation du contexte multi-tour et un paramètre `conversation` pour des conversations nommées. Accepte les images inline dans `input[].content` avec parts `input_text` et `input_image`.
- **GET /v1/responses/{id}** — Récupère une réponse stockée par ID.
- **DELETE /v1/responses/{id}** — Supprime une réponse stockée.

### Models / capabilities / health

- **GET /v1/models** — Liste l'agent comme modèle disponible (par défaut = nom du profil).
- **GET /v1/capabilities** — Description machine-readable de la surface API et des features (`chat_completions`, `responses_api`, `run_submission`, `streaming`, etc.).
- **GET /health** — Health check, retourne `{"status": "ok"}`.
- **GET /health/detailed** — Health check étendu (sessions actives, usage ressources).

### Runs API (alternative streaming)

- **POST /v1/runs** — Crée un run d'agent, retourne un `run_id` pour la subscription aux events. Accepte une chaîne `input`, optionnellement `session_id`, `instructions`, `conversation_history`, ou `previous_response_id`.
- **GET /v1/runs/{run_id}** — Poll l'état courant du run (utile pour des dashboards sans SSE).
- **GET /v1/runs/{run_id}/events** — Stream Server-Sent Events (progression d'outils, deltas de tokens, events lifecycle).
- **POST /v1/runs/{run_id}/stop** — Interrompt un tour d'agent en cours.

### Jobs API (travail planifié en arrière-plan)

- **GET /api/jobs** — Liste tous les jobs planifiés.
- **POST /api/jobs** — Crée un job planifié (même format que `hermes cron`).
- **GET /api/jobs/{job_id}** — Récupère la définition du job et son dernier état d'exécution.
- **PATCH /api/jobs/{job_id}** — Update partiel des champs du job.
- **DELETE /api/jobs/{job_id}** — Supprime le job et annule les runs en cours.
- **POST /api/jobs/{job_id}/pause** — Met en pause sans suppression.
- **POST /api/jobs/{job_id}/resume** — Reprend un job mis en pause.
- **POST /api/jobs/{job_id}/run** — Déclenche une exécution immédiate.

## Configuration (variables d'environnement)

- `API_SERVER_ENABLED` (défaut : `false`)
- `API_SERVER_PORT` (défaut : `8642`)
- `API_SERVER_HOST` (défaut : `127.0.0.1`)
- `API_SERVER_KEY` — Bearer token (requis pour les adresses non-loopback)
- `API_SERVER_CORS_ORIGINS` — allowlist séparée par virgules
- `API_SERVER_MODEL_NAME` — défaut = nom du profil ou `hermes-agent`

## Sécurité

L'API donne **un accès complet à la toolset de hermes-agent, y compris les commandes terminal**. Auth Bearer token via header `Authorization` obligatoire sur adresses non-loopback. CORS désactivé par défaut, à activer uniquement pour origins explicitement de confiance.

Security headers ajoutés :

- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: no-referrer`

Features CORS (quand activé) :

- Cache preflight : `Access-Control-Max-Age: 600`
- Streaming SSE avec headers CORS
- Support `Idempotency-Key` (cache de réponse 5 minutes)

## System prompt

Les system prompts fournis par le frontend (via Chat Completions) ou `instructions` (Responses API) **se superposent** au system prompt central de l'agent, qui conserve ses outils, sa mémoire et ses skills.

## Setup multi-utilisateurs

Créer des profils par utilisateur avec configs et mémoires isolés :

```bash
hermes profile create alice
hermes profile create bob
# Configurer le port de chaque profil dans ~/.hermes/profiles/{name}/.env
hermes -p alice gateway &
hermes -p bob gateway &
```

Les serveurs API annoncent les noms de profil comme IDs de modèles dans `/v1/models`.

## Frontends compatibles

Intégrations testées : **Open WebUI** (126k stars), **LobeChat** (73k), **LibreChat** (34k), **AnythingLLM** (56k), **NextChat** (87k), **ChatBox** (39k), **Jan** (26k), et d'autres. SDK Python OpenAI et curl direct également supportés.

## Limitations

- **Stockage des réponses** : persistence SQLite, max 100 réponses stockées (éviction LRU).
- **Pas d'upload de fichiers** : images inline supportées, fichiers uploadés non supportés.
- **Champ `model` cosmétique** : le LLM réel est configuré côté serveur dans `config.yaml`.

## Proxy mode

Le serveur API sert de backend pour le **mode proxy de la gateway**. Une autre instance Hermes configurée avec `GATEWAY_PROXY_URL` forwarde les messages vers ici, ce qui permet des déploiements scindés (par exemple Docker Matrix E2EE forwardant vers un agent côté host).

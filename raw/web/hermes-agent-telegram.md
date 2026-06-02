---
source-type: web
url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram
fetched: 2026-05-18
---

# Hermes Agent — Telegram integration (doc user-guide)

Snapshot de la page de documentation `user-guide/messaging/telegram` du site officiel de Hermes Agent (Nous Research), au 2026-05-18.

## Core Setup (étapes 1-5)

1. Créer un bot via **BotFather**, obtenir API token.
2. Customiser apparence du bot.
3. Gérer la **privacy mode** (pour groupes).
4. Trouver son numeric user ID.
5. Configurer Hermes en interactif ou manuellement via env vars.

## Variables d'environnement

- `TELEGRAM_BOT_TOKEN` — token d'authentification du bot
- `TELEGRAM_ALLOWED_USERS` — comma-separated user IDs avec accès
- `TELEGRAM_HOME_CHANNEL` — channel pour les résultats de tâches planifiées

## Privacy mode

> "Privacy mode is the single most common source of confusion when using bots in groups."

Doit être **désactivée** dans les settings de BotFather, et le bot doit être **retiré puis re-ajouté** au groupe pour que les changements prennent effet.

## Features avancées

### Webhook mode

Pour les déploiements cloud : `TELEGRAM_WEBHOOK_URL` + `TELEGRAM_WEBHOOK_SECRET` au lieu du polling, permet auto-wake cost-effective.

### Voice support

- **Incoming voice messages** : STT providers (local `faster-whisper`, Groq, ou OpenAI).
- **Outgoing audio** : rendu en native voice bubbles. Optional ffmpeg conversion pour Edge TTS.

### Multi-session topics

`/topic` permet des conversations parallèles style ChatGPT au sein d'un seul DM. Bindings persistants stockés en SQLite.

### Group features

- Mention patterns
- Forum topic skill binding
- Allowlists séparées pour users group-only
- Ignored thread configuration

### Streaming transport

Native draft rendering sur DMs avec graceful fallback vers message editing pour groupes/topics.

## Sécurité & access control

- Garder le bot token secret.
- `TELEGRAM_ALLOWED_USERS` recommandé comme safety measure obligatoire.
- Slash command access tiers (admin vs regular).
- Exec approval workflows.

## File handling & media

Envoi de fichiers générés via tags `MEDIA:/path/to/file` avec extensions de file type spécifiées. Mapping volumes Docker à gérer pour assurer des chemins host-accessibles.

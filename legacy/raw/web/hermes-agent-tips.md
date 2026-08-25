---
source-type: web
url: https://hermes-agent.nousresearch.com/docs/guides/tips
fetched: 2026-05-17
---

# Hermes Agent — Tips & Best Practices (doc guides)

Snapshot du contenu utile de la page de documentation `guides/tips` du site officiel de Hermes Agent (Nous Research), au 2026-05-17.

## Getting the Best Results

- **Be Specific About What You Want** — Plutôt que des requêtes vagues, fournir du contexte détaillé. Au lieu de "fix the code", dire "fix the TypeError in `api/handlers.py` on line 47 — the `process_request()` function receives `None` from `parse_body()`".
- **Provide Context Up Front** — Inclure dès le départ : file paths, error messages, expected behavior. Coller les error tracebacks directement.
- **Use Context Files for Recurring Instructions** — Créer un `AGENTS.md` à la racine du projet, lu automatiquement à chaque session.
- **Let the Agent Use Its Tools** — Éviter le pas-à-pas tenant-la-main. Dire "find and fix the failing test" et laisser l'agent explorer (file search, terminal, code execution).
- **Use Skills for Complex Workflows** — Taper `/skills` pour parcourir les skills disponibles avant d'écrire de longues explications. Invocation directe : `/axolotl` ou `/github-pr-workflow`.

## CLI Power User Tips

- **Multi-Line Input** : `Alt+Enter`, `Ctrl+J`, ou `Shift+Enter` pour insérer un retour à la ligne sans envoyer.
- **Paste Detection** : la CLI détecte automatiquement les pastes multi-lignes et les envoie en un seul message.
- **Interrupt and Redirect** : `Ctrl+C` une fois pour interrompre et rediriger. Double-press dans les 2 s pour forcer la sortie.
- **Resume Sessions with `-c`** : `hermes -c` reprend la dernière session avec full conversation history ; `hermes -r "my research project"` reprend par titre.
- **Clipboard Image Paste** : `Ctrl+V` pour coller une image du clipboard vers le vision analysis.
- **Slash Command Autocomplete** : taper `/` puis `Tab` pour voir toutes les commandes et skills installés.
- `/verbose` cycle l'affichage des tool outputs : `off → new → all → verbose`.

## Context Files

### `AGENTS.md` — "Your Project's Brain"

Fichier à la racine du projet avec décisions d'architecture, conventions de code, instructions spécifiques au projet :

```
# Project Context
- This is a FastAPI backend with SQLAlchemy ORM
- Always use async/await for database operations
- Tests go in tests/ and use pytest-asyncio
- Never commit .env files
```

### `SOUL.md` — Customize Personality

Éditer `~/.hermes/SOUL.md` pour fixer une voix par défaut stable :

```
# Soul
You are a senior backend engineer. Be terse and direct.
Skip explanations unless asked. Prefer one-liners over verbose solutions.
Always consider error handling and edge cases.
```

### Compatibilité `cursorrules`

Hermes lit automatiquement `.cursorrules` ou `.cursor/rules/*.mdc` depuis le working directory.

### Discovery

Hermes charge le `AGENTS.md` top-level au démarrage de session. Les fichiers en sous-répertoire sont découverts **paresseusement** pendant les tool calls.

Les context files doivent rester concis — chaque caractère compte dans le token budget.

## Memory & Skills

- **Memory vs. Skills — ce qui va où** : la mémoire stocke des **faits** (environnement, préférences, locations) ; les skills gèrent des **procédures** (workflows multi-étapes, recettes réutilisables).
- **When to Create Skills** : si une tâche prend ≥5 étapes et qu'on va la répéter, dire à l'agent "save what you just did as a skill called `deploy-staging`".
- **Managing Memory Capacity** : mémoire bornée (~2 200 chars pour `MEMORY.md`, ~1 375 pour `USER.md`). L'agent consolide les entrées quand c'est plein.
- **Let the Agent Remember** : après une session productive, dire "remember this for next time" et l'agent sauve les key takeaways.

> **Important** : la mémoire est **frozen mid-session** — les changements n'apparaissent dans le system prompt qu'à la session suivante.

## Performance & Cost

- **Don't Break the Prompt Cache** : garder un system prompt stable (mêmes context files, même mémoire) pour bénéficier des cache hits moins chers sur les messages suivants.
- **Use `/compress` Before Hitting Limits** : `/compress` résume la conversation history pour réduire le token count quand la session devient longue.
- **Delegate for Parallel Work** : demander à l'agent d'utiliser `delegate_task` avec des subtasks parallèles pour de la recherche indépendante sur plusieurs sujets.
- **Use `execute_code` for Batch Operations** : demander des scripts qui font les opérations en batch plutôt que de lancer les commandes une par une.
- **Choose the Right Model** : `/model` pour switcher. Modèles frontier (Claude Sonnet/Opus, GPT-4o) pour le reasoning complexe ; switcher vers plus rapide pour du formatting simple.
- `/usage` et `/insights` pour monitorer la consommation de tokens.

## Messaging Tips

- **Set a Home Channel** : `/sethome` dans le chat Telegram ou Discord préféré pour recevoir les résultats de cron jobs et les outputs planifiés.
- **Use `/title` to Organize Sessions** : nommer les sessions (`/title auth-refactor`) pour les retrouver via `hermes -r "auth-refactor"`.
- **DM Pairing for Team Access** : activer le DM pairing pour que des teammates demandent des codes one-time. Approuver avec `hermes pairing approve telegram XKGH5N7P`.
- **Tool Progress Display Modes** : `/verbose` contrôle la visibilité de l'activité d'outils. Garder les messaging bots sur `new` pour moins de bruit.

Les sessions se reset automatiquement après idle time (défaut : 24 h) ou quotidiennement à 4h du matin, ajustable dans `~/.hermes/config.yaml`.

## Security

### Docker pour code non-trusté

Set `TERMINAL_BACKEND=docker` dans le `.env` :

```
TERMINAL_BACKEND=docker
TERMINAL_DOCKER_IMAGE=hermes-sandbox:latest
```

### Encoding Windows

UTF-8 explicite pour les fichiers :

```python
with open("results.txt", "w", encoding="utf-8") as f:
    f.write("✓ All good\n")
```

En PowerShell :

```
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
```

### Review avant "Always"

Quand on approuve une commande dangereuse, choisir `session` plutôt qu'`always` tant qu'on n'est pas à l'aise.

### Command Approval

Hermes vérifie les commandes contre des patterns dangereux (recursive deletes, SQL drops, etc.). Ne pas désactiver en prod. Dans les container backends, ces checks sont **skippés** — s'assurer que les images sont correctement lockées.

### Allowlists messaging

Ne **jamais** mettre `GATEWAY_ALLOW_ALL_USERS=true`. Utiliser les allowlists par plateforme :

```
TELEGRAM_ALLOWED_USERS=123456789,987654321
DISCORD_ALLOWED_USERS=123456789012345678
GATEWAY_ALLOWED_USERS=123456789,987654321
```

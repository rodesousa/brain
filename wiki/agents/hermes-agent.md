---
type: entity
summary: Framework d'agent autonome — context layering SOUL/AGENTS, profils, messageries, providers, MCP, endpoint OpenAI-compatible, skills progressive disclosure, webhooks.
lifecycle: reviewed
created: 2026-05-13
updated: 2026-05-18
sources:
  - raw/youtube/hermes-agent-3-aicodeking.md
  - raw/web/hermes-agent-api-server.md
  - raw/web/hermes-agent-tips.md
  - raw/web/hermes-agent-soul-md.md
  - raw/web/hermes-agent-skills.md
  - raw/web/hermes-agent-webhook-github-pr-review.md
  - raw/web/hermes-agent-github-pr-review-cron.md
  - raw/web/hermes-agent-telegram.md
tags:
  - coding-agent
  - agent-reliability
  - context-layering
  - mcp-integration
  - openai-compatible-api
---

# Hermes Agent

> ⚠ Page enrichie par la doc officielle `features/api-server` (2026-05-17), qui confirme une partie des claims YouTube : existence d'une gateway, exposition OpenAI-compatible, profils multi-utilisateurs, jobs/cron, MCP. Les claims spécifiques à la release 0.13 (codename "Tenacity", liste des P0 vulns, noms de modèles cités) restent **non vérifiés** — toujours à recouper avec le changelog officiel.

Framework d'agent autonome supportant profils multiples, sessions persistantes, intégrations messageries (Slack, Telegram, Discord, WhatsApp, IRC, Teams, Matrix, DingTalk, Google Chat), providers de modèles pluggables, MCP étendu, et adaptateurs IDE (Zed, VS Code, JetBrains via ACP).

## Release 0.13 — "Tenacity" ^[ambiguous] (mai 2026)

Thème annoncé : faire en sorte que les agents puissent continuer à travailler sans perdre leur état, dériver de leur objectif, crasher silencieusement, ou rester bloqués.

### Kanban durable multi-agents

Cœur du changement. Le Kanban passe de tableau visuel à work queue durable :

- **Heartbeats + reclaim logic** pour détecter workers crashés ou disparus
- **Zombie detection** : un worker qui exit sans terminer sa tâche bloque automatiquement
- **Retry budgets** et per-task max retries
- **Hallucination gate** : détecte quand un agent prétend avoir créé/complété une tâche mais l'état du board ne match pas — avec recovery UX

### Persistance et focus de l'agent

- `/goal` : objectif persistant à travers les tours d'une session — l'agent garde une cible à optimiser même quand la session s'étire
- **Checkpoints V2** : réécriture de la couche de state persistence avec pruning et discard rails. Auto-resume de session interrompue après restart de la gateway

### Sécurité

8 vulns P0 fermées ^[ambiguous]. Secret redaction par défaut. Scoping Discord par guild d'origine. WhatsApp rejette les inconnus par défaut, pas de self-chat. Améliorations sur credential safety, MCP OAuth handling, browser SSRF, cron prompt injection scanning, log redaction pour debug sharing.

### MCP et tooling

- **MCP** : SSE transport, OAuth forwarding pour SSE, stale pipe retries, keep-alive, support image dans tool results
- **Post-write delta linting** après file writes (Python, JSON, YAML, TOML) — surface immédiatement les syntax errors générés par l'agent
- **No-agent cron mode** : cron-jobs en script-only watchdog qui n'invoquent le LLM que si le script produit un output (économie de coût)

### Providers et modèles

Provider profile abstraction + plugin directory pour extensibilité. Nouveaux modèles cités ^[ambiguous] : DeepSeek V4 Pro, XAI Grok 4.3, OpenRouter Owl Alpha (route gratuite), Tencent HY3 Preview. OAuth persistant entre profils. Response caching OpenRouter.

### Multimodal et i18n

Video analyze tool (natif Gemini et compatibles). XAI custom voices comme TTS avec voice cloning. i18n CLI/gateway : ZH, JP, DE, ES, FR, UA, TR. Doc site avec locale chinoise.

### IDE / ACP

Adaptateurs ACP pour Zed, VS Code, JetBrains. `/steer` (guider un agent en cours d'exécution sans l'interrompre complètement), `/q` (queue follow-up work).

### Skills et écosystème

Optional skills ajoutés ^[ambiguous] : Shopify, Here Now (personal shopping), Anthropic financial services, Kanban video orchestrator, SearXNG (self-hosted search). Curator (sous-outil) gagne `archive`, `prune`, `list archive`.

## API server / gateway (endpoint OpenAI-compatible)

`hermes gateway` expose l'agent comme un endpoint HTTP **compatible OpenAI** (`/v1/chat/completions` et `/v1/responses`), avec sa toolset complète — **y compris les commandes terminal**. Écoute par défaut sur `127.0.0.1:8642`. Activé via `API_SERVER_ENABLED=true` dans `~/.hermes/.env`. Bearer token (`API_SERVER_KEY`) obligatoire sur adresses non-loopback ; CORS désactivé par défaut.

Surface API exposée :

- **Chat Completions stateless** (`/v1/chat/completions`) — format OpenAI standard, supporte images inline (`image_url`), streaming SSE avec event custom `hermes.tool.progress` pour la visibilité des outils.
- **Responses API stateful** (`/v1/responses`) — état de conversation côté serveur, `previous_response_id` pour le multi-tour, conversations nommées.
- **Runs API** (`/v1/runs`) — création de run, poll, stream SSE, stop. Alternative aux SSE de Chat Completions pour dashboards.
- **Jobs API** (`/api/jobs`) — CRUD + pause/resume/run sur les jobs planifiés (même format que `hermes cron`). Confirme l'angle "no-agent cron mode" mentionné côté YouTube.
- **Capabilities** (`/v1/capabilities`) — description machine-readable des features supportées.

Le system prompt du frontend (Chat Completions) ou `instructions` (Responses API) **se superpose** au system prompt central — l'agent conserve sa toolset, mémoire et skills. Le champ `model` est cosmétique, le vrai LLM est dans `config.yaml` côté serveur.

Multi-utilisateurs : un profil = des configs/mémoires isolés + un port + un model ID dans `/v1/models` (`hermes -p alice gateway`, `hermes -p bob gateway`). Confirme le claim YouTube sur les profils.

Frontends testés cités par la doc : **Open WebUI**, **LobeChat**, **LibreChat**, **AnythingLLM**, **NextChat**, **ChatBox**, **Jan** — soit l'écosystème complet des UIs OpenAI-compatible (>400k stars cumulés). Hermes vise donc explicitement à se brancher dans la même prise que n'importe quel modèle hébergé.

Limites doc : storage SQLite des réponses plafonné à 100 (LRU), pas d'upload de fichiers (images inline uniquement).

## Context layering : `SOUL.md` / `AGENTS.md` / `/personality`

Hermes formalise une **hiérarchie de contexte à trois niveaux** dans le system prompt, avec un *routing rule* explicite : "if it should apply everywhere, put it in `SOUL.md`".

- **`~/.hermes/SOUL.md`** — identité de l'instance, placée en **première position du system prompt**. Personnalité, tone, style de communication, gestion de l'incertitude. Auto-seedé au premier run, **jamais overwritten**. La doc propose quatre archétypes : *Pragmatic Engineer*, *Research Partner*, *Teacher/Explainer*, *Tough Reviewer*. Structure suggérée : `# Identity / # Style / # Avoid / # Defaults`.
- **`AGENTS.md` à la racine du projet** — contexte projet : conventions de code, file paths, ports, commandes. Chargé au démarrage de session (top-level), les fichiers en sous-répertoires sont découverts paresseusement pendant les tool calls. **Compatibilité native `.cursorrules` et `.cursor/rules/*.mdc`**.
- **`/personality`** — override de session, temporaire, ne modifie pas `SOUL.md`.

La séparation est nette dans la doc : "Be direct" / "Avoid hype language" vont dans SOUL.md ; "Use pytest, not unittest" / "API runs on port 8000" vont dans AGENTS.md. Pattern comparable à Claude Code / `CLAUDE.md` ^[inferred], mais Hermes **dédouble** identité (qui je suis) et contexte projet (où je suis), là où Claude Code les mélange dans un seul fichier.

## Mémoire et skills

### Mémoire

- **Bornée** : `MEMORY.md` ~2 200 chars, `USER.md` ~1 375 chars. L'agent consolide automatiquement les entrées quand c'est plein.
- **Frozen mid-session** : les modifications de mémoire n'apparaissent dans le system prompt qu'à la session suivante. ⚠ implication non triviale pour les workflows long-running.

### Skills (knowledge documents on-demand)

> "Skills are on-demand knowledge documents that teach Hermes how to handle specific tasks."

- Chaque skill installée = automatiquement un slash command (`/ascii-art`, `/github-pr-workflow`, etc.). Invocation possible aussi en langage naturel (déclenche le tool `skill_view`).
- **Progressive disclosure** (3 niveaux pour rester token-efficient) :
  1. `skills_list()` — ~3k tokens pour toutes les skills, au début de session.
  2. `skill_view(name)` — chargement du `SKILL.md` complet à la demande.
  3. `skill_view(name, file_path)` — fichiers de référence (sous-docs, templates, scripts) seulement si nécessaire.
- **Hub officiel** : `hermes skills install official/research/arxiv` (ou URL directe `hermes skills install https://example.com/SKILL.md`). Activation effective à la **prochaine session** sauf `/reset` ou `--now`.
- **Plugin skills** : namespacing `plugin:skill` (`skill_view("superpowers:writing-plans")`). Non listées system-wide, chargement explicite seulement.
- **SKILL.md** = markdown + frontmatter YAML, structure recommandée `# When to Use / # Procedure / # Pitfalls / # Verification`. Peut embarquer `references/`, `templates/`, `scripts/`.
- **Config par skill** : frontmatter `metadata.hermes.config` déclare les clés à prompter au premier usage, stockées dans `config.yaml` sous `skills.config.*`.
- **`skill_manage`** : l'agent peut **créer et update des skills lui-même** — après résolution d'un problème complexe, Hermes peut proposer de sauver l'approche comme skill réutilisable.
- **Per-platform** : TUI `hermes skills` pour activer/désactiver skills par plateforme (CLI, Telegram, Discord, etc.).

### Skills vs Memory — règle de routage

| Aspect | Skills | Memory |
|---|---|---|
| Contenu | Procédural (how) | Factuel (what) |
| Loading | À la demande | Chaque session |
| Taille | Centaines de lignes OK | Doit rester compact |
| Coût tokens | Zéro tant que non chargé | Petit coût constant |
| Auteur | Toi, agent, ou Hub | Agent depuis conversations |

> "If you'd put it in a reference document, it's a skill. If you'd put it on a sticky note, it's memory."

## Webhooks (platform `webhooks`)

Surface **séparée** de l'API server (et de chacune des messageries). Activée dans `~/.hermes/config.yaml` sous la section `platforms`.

- **Port** : 8644 par défaut (vs 8642 pour l'API server). Two ports = deux trust boundaries distinctes.
- **Rate limit** : 30 requêtes/minute par route.
- **Routes configurables** : secret HMAC, filtre d'events, **prompt template**, méthode de delivery.
- **Substitution dynamique** : `{field}` et `{nested.field}` dans le prompt résolvent depuis le payload. Mais : pas de filtrage par sous-action (ex. impossible de filtrer `pull_request.opened` vs `pull_request.closed` au niveau routing — le prompt doit gérer le skip lui-même).
- **Delivery** : commentaires GitHub (`gh pr comment`), Slack, Discord, Telegram, Signal, SMS, ou log local.
- **Sécurité** : HMAC signature, idempotency caching via delivery ID, sandboxing recommandé (Docker, SSH) quand internet-exposed.

> "Webhook payloads contain attacker-controlled data — PR titles, commit messages, and descriptions can contain malicious instructions."

Cas d'usage canonique documenté : **PR review automatique** sur événement GitHub. Variante cron alternative (`hermes cron create "0 */2 * * *" ... --skill code-review`) si la latence event n'est pas nécessaire ou si l'instance n'est pas publiquement reachable.

## Messageries (surfaces multi-plateformes)

Patterns transversaux observés dans la doc Telegram, généralement applicables aux autres adaptateurs (Discord, Slack, etc.) ^[inferred] :

- **Allowlists obligatoires** par plateforme (`TELEGRAM_ALLOWED_USERS`, `DISCORD_ALLOWED_USERS`, `GATEWAY_ALLOWED_USERS`). Jamais `GATEWAY_ALLOW_ALL_USERS=true`.
- **Polling vs webhook** : déploiement local utilise polling, déploiement cloud utilise webhook URL + secret pour auto-wake cost-effective.
- **Voice STT/TTS** : entrée voix via `faster-whisper` local, Groq ou OpenAI ; sortie en native voice bubbles avec optional Edge TTS via ffmpeg.
- **Multi-session par DM** : `/topic` ouvre des conversations parallèles style ChatGPT au sein d'un même chat. Bindings persistants en SQLite.
- **`MEDIA:/path/to/file`** : tag inline pour envoyer des fichiers générés. ⚠ mapping volumes Docker à gérer pour chemins host-accessibles.
- **Streaming transport** : native draft rendering sur DMs, fallback message-editing pour groupes/topics.
- **Telegram-specific gotcha** : "privacy mode" sur BotFather = single most common source of confusion en groupe. Doit être désactivée, et le bot retiré/re-ajouté pour propager le change.

## Runtime, sécurité, ergonomie CLI

### Sandboxing terminal

`TERMINAL_BACKEND=docker` dans `.env` pour exécuter du code non-trusté dans une image dédiée :

```
TERMINAL_BACKEND=docker
TERMINAL_DOCKER_IMAGE=hermes-sandbox:latest
```

⚠ En mode container, les checks de patterns dangereux (recursive deletes, SQL drops, etc.) sont **skippés** — la lockdown de l'image devient l'unique ligne de défense.

### Allowlists messaging

Ne **jamais** mettre `GATEWAY_ALLOW_ALL_USERS=true`. Allowlists par plateforme :

```
TELEGRAM_ALLOWED_USERS=...
DISCORD_ALLOWED_USERS=...
GATEWAY_ALLOWED_USERS=...
```

### Session lifecycle

Auto-reset après idle (défaut 24h) ou quotidiennement à 4h. Ajustable dans `~/.hermes/config.yaml`. Resume par titre : `/title auth-refactor` puis `hermes -r "auth-refactor"`. Resume rapide : `hermes -c`.

### Tools agent-natives

- `delegate_task` — délégation de sous-tâches parallèles indépendantes (research multi-sujets).
- `execute_code` — batch operations en script unique plutôt qu'enchaînement de commandes.
- `/compress` — compression de la conversation history pour rester sous la limite de tokens sans rompre le prompt cache.
- `/usage`, `/insights` — monitoring tokens et coût.
- `/model` — switch de modèle en cours de session (frontier vs rapide).

### Prompt cache

Doc explicite : garder le system prompt stable (même context files, même mémoire) pour bénéficier des cache hits moins chers — argument structurel en faveur du séparation SOUL/AGENTS (les deux changent rarement) vs charge dynamique de contexte.

## My take

L'angle "agent reliability" de la release 0.13 (Kanban durable, zombie detection, hallucination gate, `/goal` persistant, Checkpoints V2) traite *exactement* les failure modes que [[context-labs-halo]] essaie de détecter post-hoc sur des traces de prod ^[inferred]. Sous cet angle, Hermes et Halo sont **complémentaires** : Hermes attaque le problème côté framework (préventif, à la construction de l'agent), Halo côté observation (curatif, sur traces existantes).

Le choix d'exposer l'agent en **endpoint OpenAI-compatible** est le pivot stratégique le plus intéressant de la doc. Plutôt que de pousser un client maison, Hermes se branche dans la prise standard de tout l'écosystème UI (Open WebUI, LobeChat, etc.) — l'utilisateur garde son frontend préféré et obtient en coulisses un agent avec outils, mémoire, skills, cron, MCP. C'est l'inverse du pari [[alloy]] (boucle minimaliste, à toi de construire l'UI) : Hermes mise sur la **standardisation du transport** pour rendre négligeable la friction d'adoption. À voir si le coût en complexité serveur (Jobs API, Runs API, Responses API state-ful, profiles multi-port…) reste maîtrisable.

La pièce structurelle la plus intéressante côté **DX agent** est la séparation **SOUL / AGENTS / `/personality`** : Hermes traite l'identité de l'agent comme une *primitive de premier ordre*, séparée du contexte projet et des overrides de session. C'est ce que Claude Code fait à demi avec `CLAUDE.md` (un seul fichier mélange tout) ^[inferred]. Le pari : la stabilité du SOUL maximise les cache hits **et** rend l'agent prévisible à travers les projets, sans imposer de reconfigurer l'identité à chaque clone. La routing rule "if it should apply everywhere, put it in SOUL.md" est exactement le genre d'heuristique simple qui dé-frictionnise l'usage quotidien.

Implication non-évidente : la **mémoire frozen mid-session** + les **bornes très serrées** (~2 200 / ~1 375 chars) imposent un workflow où le summary/take est consolidé en **fin de session**, pas pendant. Aligne mécaniquement Hermes sur un modèle "session = unit of memory write" — assez différent d'un LLM avec long context et write libre.

Le **progressive disclosure des skills** (3 niveaux : list → SKILL.md → reference files) est l'analogue côté procédural de ce que MCP fait côté tools : *zero token cost tant que non utilisé*. C'est probablement *ce qui rend économiquement viable* d'avoir un hub avec des dizaines de skills sans massacrer le token budget — sans ce pattern, charger toutes les skills à chaque session serait prohibitif. À noter : `skill_manage` rend le système **auto-extensible** par l'agent lui-même, ce qui crée une boucle de feedback non triviale (l'agent apprend, sauve, réutilise — pattern observé aussi côté Claude Code ^[inferred]).

L'**isolation entre surfaces** (API server port 8642, webhooks port 8644, messageries chacune son adapter avec son allowlist) est rare dans les agent frameworks ^[inferred] — c'est le bon design pour minimiser le rayon de blast d'une compromission. La security note webhook ("attacker-controlled data — PR titles, commit messages, and descriptions can contain malicious instructions") est l'angle d'attaque prompt injection le plus négligé en pratique ; le mentionner explicitement dans la doc est un signal positif.

Crédibilité des sources : 7 sources primaires officielles + 1 secondaire YouTube. La doc confirme la structure générale (gateway, profils, jobs/cron, MCP, mémoire bornée, skills à progressive disclosure, sandboxing Docker, webhooks séparés, messaging multi-plateforme) mais **ne dit toujours rien** sur les claims spécifiques 0.13 (codename "Tenacity", P0 vulns, modèles cités, Kanban durable multi-agents, hallucination gate, `/goal`, `/steer`, `/q`). Ces points restent à recouper avec un changelog officiel ou le repo source.

## Sources

- `raw/youtube/hermes-agent-3-aicodeking.md` — vidéo AICodeKing du 2026-05-13 sur la release 0.13. Source secondaire, faible fiabilité, à recouper sur les claims spécifiques 0.13.
- `raw/web/hermes-agent-api-server.md` — page officielle `features/api-server`, fetched 2026-05-17. Source primaire, dense, sur l'exposition OpenAI-compatible et la surface API du runtime.
- `raw/web/hermes-agent-tips.md` — page officielle `guides/tips`, fetched 2026-05-17. Source primaire, sur l'ergonomie CLI, le context layering pratique, la mémoire/skills, le sandboxing Docker et les allowlists.
- `raw/web/hermes-agent-soul-md.md` — page officielle `guides/use-soul-with-hermes`, fetched 2026-05-17. Source primaire, focalisée sur `SOUL.md` comme primary identity et sa distinction avec `AGENTS.md` et `/personality`.
- `raw/web/hermes-agent-skills.md` — page officielle `guides/work-with-skills`, fetched 2026-05-18. Source primaire, sur la gestion complète des skills (progressive disclosure, hub, plugins, `skill_manage`, per-platform).
- `raw/web/hermes-agent-webhook-github-pr-review.md` — page officielle `guides/webhook-github-pr-review`, fetched 2026-05-18. Source primaire, sur la surface webhook (port 8644, HMAC, template `{field}`, rate limiting).
- `raw/web/hermes-agent-github-pr-review-cron.md` — page officielle `guides/github-pr-review-agent`, fetched 2026-05-18. Source primaire applicative, variante cron polling pour PR review.
- `raw/web/hermes-agent-telegram.md` — page officielle `user-guide/messaging/telegram`, fetched 2026-05-18. Source primaire, sur l'adapter Telegram (privacy mode, webhook vs polling, voice STT/TTS, `/topic`, `MEDIA:` tags).

À ingérer en priorité quand disponibles : changelog officiel Hermes 0.13 (validerait codename, P0 vulns, nouveaux modèles) + repo source (URL `https://github.com/nousresearch/hermes-agent` ^[ambiguous] — non vérifiée).

## Related

- [[context-labs-halo]] — autre outil agent-reliability, angle complémentaire (observation post-hoc des failure modes que Hermes 0.13 essaie de prévenir au runtime).
- [[alloy]] — framework d'agent à la philosophie *opposée* (boucle minimaliste, "no opinions on sessions/persistence/memory/scheduling/UI"). Hermes revendique tout, Alloy revendique rien hors du loop — deux écoles à contraster.

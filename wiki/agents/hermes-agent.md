---
type: entity
summary: Framework d'agent autonome avec profils, intégrations messageries multiples, providers pluggables, MCP, et focus 0.13 sur la fiabilité long-running.
lifecycle: draft
created: 2026-05-13
updated: 2026-05-13
sources:
  - raw/youtube/hermes-agent-3-aicodeking.md
tags:
  - coding-agent
  - agent-reliability
  - multi-agent-kanban
  - mcp-integration
---

# Hermes Agent

> ⚠ Page créée à partir d'une **seule source secondaire** (vidéo YouTube auto-captionée, AICodeKing). Noms de features, versions et modèles sont à vérifier contre le repo officiel et le changelog. À enrichir d'urgence avec des sources primaires.

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

## My take

L'angle "agent reliability" de la release 0.13 (Kanban durable, zombie detection, hallucination gate, `/goal` persistant, Checkpoints V2) traite *exactement* les failure modes que [[context-labs-halo]] essaie de détecter post-hoc sur des traces de prod ^[inferred]. Sous cet angle, Hermes et Halo sont **complémentaires** : Hermes attaque le problème côté framework (préventif, à la construction de l'agent), Halo côté observation (curatif, sur traces existantes).

La source actuelle est trop bruyante pour s'appuyer dessus sans vérification — clickbait dans le titre (le speaker dit "0.13", le titre dit "3.0"), auto-caption qui mange des noms propres, channel AICodeKing connu pour l'amplification. À enrichir avec source primaire (repo + changelog officiel) avant de citer cette page ailleurs.

## Sources

- `raw/youtube/hermes-agent-3-aicodeking.md` — vidéo AICodeKing du 2026-05-13 sur la release 0.13. Source unique, secondaire, faible fiabilité. À recouper.

À ingérer en priorité quand disponibles : changelog officiel Hermes 0.13 + repo source (URL `https://github.com/nousresearch/hermes-agent` ^[ambiguous] — mentionnée par l'utilisateur mais non vérifiée).

## Related

- [[context-labs-halo]] — autre outil agent-reliability, angle complémentaire (observation post-hoc des failure modes que Hermes 0.13 essaie de prévenir au runtime).

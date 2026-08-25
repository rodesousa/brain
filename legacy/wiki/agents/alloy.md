---
type: entity
summary: Boucle d'agent minimaliste OTP-native pour Elixir — completion/tool-call et rien d'autre. 6 providers, GenServer supervisé, memory comme behaviour, design boundary explicite.
lifecycle: reviewed
created: 2026-05-13
updated: 2026-05-13
sources:
  - raw/repos/alloy-ex-alloy.md
tags:
  - elixir-otp
  - agent-loop-minimal
  - multi-provider-llm
  - genserver-agent
  - memory-primitive
---

# Alloy

Boucle d'agent **OTP-native pour Elixir**, édité par `alloy-ex`. Pitch en une phrase :

> Alloy is the completion-tool-call loop and nothing else.

~7 500 LOC. Inspiré explicitement par [Pi Agent](https://github.com/badlogic/pi-mono) (badlogic / Mario Zechner) pour la philosophie minimaliste, mais sur BEAM avec les avantages OTP : supervision, fault isolation, exécution parallèle réelle des tools.

## Design boundary — c'est *la* signature

Le README contient une section dédiée "Design Boundary" qui dit littéralement ce qui appartient à Alloy et ce qui n'y appartient pas.

**Belongs in Alloy** : traduction wire-format des providers, mécanique de la boucle tool-call/completion, messages normalisés, state opaque côté provider (response IDs), métadata de réponse provider (citations, telemetry server-side).

**Does not belong** : sessions et politique de persistence, indexation/retrieval, UI, scheduling, multi-tenant, billing, hosted infra.

Rule of thumb donnée par le README :

> if the feature is required to speak a provider API correctly, and could help any Alloy consumer, it likely belongs here. If it needs a database table, product defaults, UI decisions, or tenancy logic, it belongs in your application layer.

C'est une heuristique opérable, falsifiable cluster par cluster — pas un slogan.

## Architecture

```
Alloy.run/2              One-shot agent loop (pure function)
Alloy.Agent.Server       GenServer wrapper (stateful, supervisable)
Alloy.Agent.Turn         Single turn: call provider → execute tools → return
Alloy.Provider           Behaviour: wire format ↔ Alloy.Message
Alloy.Tool               Behaviour: name, description, input_schema, execute
Alloy.Middleware         Pipeline: custom hooks, tool blocking
Alloy.Context.Compactor  Automatic conversation summarization
```

Tripartition stateless / stateful clé :

- **`Alloy.Agent.Turn`** — primitive *tour unique* (provider → tools → retour). Testable seule sans process.
- **`Alloy.run/2`** — fonction pure, one-shot, orchestre les turns.
- **`Alloy.Agent.Server`** — GenServer wrapper supervisable pour les conversations longues.

Trois behaviours d'extension : `Alloy.Provider`, `Alloy.Tool`, `Alloy.Middleware`.

Distribution en **deux packages** : `:alloy` (~7500 LOC, core pur) + `:alloy_agent` optionnel (runtime supervisé, sessions, async dispatch, memory stores). Pattern Phoenix-like : core minimal + couches de confort empilables.

## Provider system

| Vendor | Module | Notes |
|---|---|---|
| Anthropic | `Alloy.Provider.Anthropic` | Native, cache=true, memory_20250818 |
| Gemini | `Alloy.Provider.Gemini` | GenerateContent API native |
| OpenAI / xAI | `Alloy.Provider.OpenAI` | Responses API native, `api_url:` overridable |
| Codex | `Alloy.Provider.Codex` | (mentionné dans le pitch) |
| OpenAI-compatible | `Alloy.Provider.OpenAICompat` | Ollama, OpenRouter, DeepSeek, Mistral, Groq, Together, Moonshot, Qwen, GLM, etc. |

Swap d'un provider en une ligne — le tuple `{ProviderModule, opts}` est l'unité de config, tools et messages restent inchangés.

Trois normalisations non triviales :

1. **Reasoning blocks normalisés** — DeepSeek-R1 / Grok reasoning renvoient `reasoning_content`, Anthropic renvoie `thinking`. Alloy expose les deux comme des blocks `thinking` de première classe dans `Alloy.Message`. La différence provider est gommée.
2. **Provider-owned state** — stored response IDs (OpenAI/xAI) exposés dans `result.metadata.provider_state`, re-passables au prochain turn. Permet de continuer une conversation provider-native sans dupliquer le contexte client.
3. **Citations** — `result.metadata.provider_response.citations` + annotations inline dans les text blocks pour les spans (xAI search, etc.).

`extra_body` mergé en dernier — peut override n'importe quel champ par défaut. Permet de toucher des params provider-specific (`reasoning_effort`, `response_format`, `temperature`) sans attendre une release d'Alloy.

## Memory comme behaviour — `Alloy.Memory`

Cas d'école du design boundary appliqué au tool `memory_20250818` d'Anthropic :

- **Wire protocol** (6 commandes : `view`, `create`, `str_replace`, `insert`, `delete`, `rename`, sur un arbre `/memories/`, format de retour, path validation) → Alloy.
- **Backing store** (disk, Postgres, S3, in-memory) → app, via un module qui implémente `@behaviour Alloy.Memory`.
- **Session scoping** → app (thread `session_id` toi-même).

Quand `:memory` est set, Alloy injecte l'outil dans la requête Anthropic, ajoute le beta header `context-management-2025-06-27`, et route les memory tool calls via `Alloy.Memory.Router` séparé du tool executor général (typed-tool contract propre).

> No bytes touch Anthropic's servers.

Anthropic-only en 0.12 — configurer `:memory` avec un autre provider raise. Honnête.

## Surface opérationnelle (sélection)

- **Streaming** unifié : `Alloy.stream/3` et `Alloy.Agent.Server.stream_chat/4`. Fallback automatique `complete/3` si un provider custom n'implémente pas `stream/4`.
- **Async dispatch via Phoenix.PubSub** : `send_message/2` fire-and-forget, résultat livré en `handle_info`. Match parfait avec LiveView.
- **Prompt caching Anthropic** (`cache: true`) — Alloy place les breakpoints `cache_control` sur le system prompt et la dernière tool def. Gain annoncé 60-90 % input tokens, usage tracé dans `result.usage.cache_*`.
- **Cost guard** (`max_budget_cents`) — status `:budget_exceeded` quand atteint.
- **Telemetry** — events `[:alloy, :run|:turn|:provider|:compaction|:tool]`, attachables via `:telemetry.attach_many` standard BEAM.
- **`until_tool`** — force la boucle à continuer jusqu'à appel d'un tool nommé (structured output côté validation API plutôt que via `response_format`).
- **Middleware** — `:before_tool_call` peut renvoyer `{:edit, modified_call}` pour réécrire un appel avant exécution. Policy enforcement / sanitization.
- **Tool safety** — `concurrent?/0`, `max_result_chars/0`, prompt-too-long auto-recovery.
- **Compaction** — summary-based, `reserve_tokens` + `keep_recent_tokens` + `fallback: :truncate`. Budget dérivé automatiquement du modèle, override possible via `model_metadata_overrides:`.

Toutes ces features partagent une propriété : elles vivent au **niveau loop ou provider**, jamais au niveau "produit". Cost guard = mécanique de loop, pas billing. Telemetry = events, pas dashboard. Middleware = pipeline, pas policy engine UI. Cohérent avec la rule of thumb.

## My take

L'angle de loin le plus intéressant d'Alloy est **le contraste avec [[hermes-agent]]** — deux frameworks d'agent, l'un revendique tout (Hermes : profils, sessions persistantes, intégrations messageries multi, IDE adapters, MCP, kanban durable…), l'autre revendique *rien hors du loop* (Alloy : "no opinions on sessions, persistence, memory, scheduling, or UI"). Ce ne sont pas des concurrents directs, ce sont **deux philosophies opposées du framework agent**.

- Hermes répond à : "je veux un agent qui tourne en prod avec des intégrations, des profils, du kanban, et qui s'auto-recover".
- Alloy répond à : "je veux la boucle, je colle moi-même le reste à mon app Phoenix".

Pi Agent (badlogic/pi-mono) est cité comme source de la philosophie minimaliste — à ingérer pour avoir l'autre exemple du pattern. ^[inferred] : c'est probablement la même idée portée sur la stack TypeScript / Node, avec sans doute moins de levier que ce qu'Alloy obtient via OTP.

OTP comme socle change le calcul vs Python : supervision tree, fault isolation, hot reload, parallel tool execution = gratuit. Pour quelqu'un qui ferait du Python, ce sont des features à recoder ; en BEAM, c'est l'environnement. Avantage structurel net pour "agent long-running en prod" — c'est probablement *là* qu'Alloy + Phoenix peut battre Hermes sur la fiabilité, en hébergeant moins de complexité dans le framework lui-même et plus dans la plateforme.

Sur le design boundary : la "rule of thumb" du README mérite d'être généralisée comme principe de design pour ce genre de lib — *"required to speak a provider API correctly + helps any consumer"* est une heuristique falsifiable, pas un slogan. Réutilisable pour évaluer toute lib qui se veut "minimaliste".

Mémoire comme behaviour est mon détail préféré côté impl : Alloy te fait participer au protocole Anthropic `memory_20250818` mais garde ta donnée chez toi. Inverse du défaut (mémoire managée chez le provider). C'est exactement le levier que je voudrais activer pour des données sensibles.

Ce qui me reste à creuser :
- Pi Agent (source de la philosophie) — à snapshoter.
- Anvil (`alloy-ex/anvil`, reference Phoenix app) — voir comment "tout ce qui ne belongs pas in Alloy" est concrètement implémenté côté app.
- Comparaison concrète Alloy + Phoenix vs Hermes sur un cas d'usage agent prod long-running.

## Sources

- `raw/repos/alloy-ex-alloy.md` — README repo officiel snapshoté le 2026-05-13. Source primaire unique.

Facets kept (5) :
- `raw/clusters/repos/alloy-ex-alloy/cluster-01-purpose-design-boundary.md`
- `raw/clusters/repos/alloy-ex-alloy/cluster-02-architecture.md`
- `raw/clusters/repos/alloy-ex-alloy/cluster-03-provider-system.md`
- `raw/clusters/repos/alloy-ex-alloy/cluster-04-memory-primitive.md`
- `raw/clusters/repos/alloy-ex-alloy/cluster-05-operational-surface.md`

Facets écartées (1) : `cluster-06-quickstart-and-tables` (boilerplate Hex.pm, faible signal).

À ingérer ensuite : Pi Agent (philosophie source), Anvil (app de référence côté layer applicatif).

## Related

- [[hermes-agent]] — framework agent à la philosophie opposée (tout-inclus vs Alloy minimaliste). Contraste à exploiter pour comprendre les deux écoles.
- [[context-labs-halo]] — outil d'analyse post-hoc des failure modes d'agent. Compatible avec Alloy *au sens trace* : la telemetry Alloy peut nourrir un pipeline type HALO si on déploie un agent Alloy à l'échelle.

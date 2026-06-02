---
type: repo-cluster
status: kept
created: 2026-05-13
---

# Facet : architecture

## Module diagram (extrait du README)

```
Alloy.run/2                    One-shot agent loop (pure function)
Alloy.Agent.Server             GenServer wrapper (stateful, supervisable)
Alloy.Agent.Turn               Single turn: call provider → execute tools → return
Alloy.Provider                 Behaviour: translate wire format ↔ Alloy.Message
Alloy.Tool                     Behaviour: name, description, input_schema, execute
Alloy.Middleware               Pipeline: custom hooks, tool blocking
Alloy.Context.Compactor        Automatic conversation summarization
```

## Découpe stateless / stateful

- **`Alloy.run/2`** — fonction pure, one-shot. Sans état, sans process.
- **`Alloy.Agent.Server`** — GenServer wrapper supervisable, persistant, message-passing. Garde la conversation.
- **`Alloy.Agent.Turn`** — la primitive *tour unique* : appel provider → exécution tools → retour. C'est l'unité que les deux APIs ci-dessus orchestrent.

Cette tripartition (turn / run / server) est intéressante : la primitive (turn) est isolée et donc testable seule, sans avoir à monter un GenServer.

## Trois behaviours d'extension

1. **`Alloy.Provider`** — traduction wire format ↔ `Alloy.Message`. Implémentations livrées : Anthropic, Gemini, OpenAI, Codex, xAI, OpenAICompat.
2. **`Alloy.Tool`** — `name/0`, `description/0`, `input_schema/0`, `execute/2`. Plus `concurrent?/0` et `max_result_chars/0` côté safety.
3. **`Alloy.Middleware`** — pipeline avec hooks (`:before_tool_call` etc.), peut bloquer ou éditer un appel.

## Wrapper `alloy_agent`

Package séparé `:alloy_agent` (optionnel) pour le runtime supervisé : sessions, async dispatch, memory stores.

```elixir
{:alloy, "~> 0.12"},
{:alloy_agent, "~> 0.1"}
```

Séparation du core minimal et de la "convenience runtime layer" en deux packages — cohérent avec le design boundary.

## Compaction de contexte

`Alloy.Context.Compactor` fait du **summary-based compaction** quand on approche les limites de tokens du modèle. Configurable :

```elixir
compaction: [
  reserve_tokens: 12_000,
  keep_recent_tokens: 8_000,
  fallback: :truncate
]
```

Budget dérivé automatiquement du modèle si Alloy connaît son context window. Override via `model_metadata_overrides:` pour les modèles trop récents.

## My take

Le module diagram exposé tel quel dans le README est un signal de maturité — l'auteur sait dire où sont les couches. La séparation `Turn` / `run` / `Agent.Server` est exactement ce qu'on veut quand on écrit un agent : pouvoir tester le tour unique sans process, puis monter le GenServer quand on veut de la persistence.

OTP comme socle change le calcul vs les libs Python : supervision tree, fault isolation par défaut, parallel tool execution gratuit, hot code reloading. Pour quelqu'un qui ferait du Python, ce sont des features à recoder ; en BEAM, c'est l'environnement. Avantage structurel net pour le cas "agent en prod long-running".

Le split `alloy` (~7500 LOC, pur) + `alloy_agent` (wrapper runtime supervisé) imite le pattern Phoenix : core minimal + couches de confort empilables. Permet à un user de prendre seulement `Alloy.run/2` sans embarquer un GenServer s'il n'en veut pas.

Compaction par summary-based plutôt que truncate-only, avec fallback truncate : pertinent. Réserve tokens + keep_recent_tokens donne deux leviers indépendants — j'aime ce design (pas un seul nombre magique).

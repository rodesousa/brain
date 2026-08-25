---
type: repo-cluster
status: kept
created: 2026-05-13
---

# Facet : operational-surface

Features opérationnelles livrées dans la 0.12, au-delà de la boucle d'appel pure.

## Streaming

- `Alloy.stream/3` — one-shot streaming token-par-token.
- `Alloy.Agent.Server.stream_chat/4` — streaming sur un GenServer persistant.
- Si un provider custom n'implémente pas `stream/4`, fallback automatique sur `complete/3`.

Streaming unifié sur tous les providers.

## Async dispatch — `send_message/2` + PubSub

Pour LiveView / background jobs : fire-and-forget côté caller, résultat livré via `Phoenix.PubSub` :

```elixir
Phoenix.PubSub.subscribe(MyApp.PubSub, "agent:#{session_id}:responses")
{:ok, req_id} = Alloy.Agent.Server.send_message(agent, "Summarise...", request_id: "req-123")

def handle_info({:agent_response, %{text: text, request_id: "req-123"}}, socket), do: ...
```

Match parfait avec le pattern LiveView (push asynchrone).

## Prompt caching (Anthropic)

```elixir
provider: {Alloy.Provider.Anthropic, ..., cache: true}
```

Alloy place automatiquement les breakpoints `cache_control` sur **le system prompt et la dernière tool definition**. Gain annoncé : 60-90 % sur les input tokens. Usage tracé dans `result.usage.cache_creation_input_tokens` / `cache_read_input_tokens`.

## Cost guard

```elixir
max_budget_cents: 50
```

Stoppe la boucle avant overspend. Status retourné : `:budget_exceeded` (vs `:completed`). `nil` = pas de limite (défaut).

## Telemetry

Events `[:alloy, :run, :start|stop]`, `[:alloy, :turn, :start|stop]`, `[:alloy, :provider, :request]`, `[:alloy, :compaction, :done]`, `[:alloy, :tool, :start|stop]`, `[:alloy, :event]`.

Mesures + métadata structurées. Attachable via `:telemetry.attach_many` standard BEAM. Cible : OTEL, logging, metrics custom.

## `until_tool` — structured output forcé

```elixir
until_tool: "submit_answer"
```

Force la boucle à continuer jusqu'à ce qu'un tool spécifique soit appelé. Plus fiable que `response_format` parce que le schéma du tool est validé côté API.

## Middleware — éditer un tool call avant exécution

`:before_tool_call` peut renvoyer `{:edit, modified_call}` pour réécrire les arguments — policy enforcement, sanitization, blocage.

Exemple : intercepter `bash` avec `rm` et le remplacer par un echo.

## Tool safety

Sur le behaviour `Alloy.Tool` :
- **`concurrent?/0`** — autorise l'exécution parallèle (BEAM = vraie concurrence).
- **`max_result_chars/0`** — cap la taille du résultat retourné au modèle.
- **prompt-too-long auto-recovery** — recovery automatique quand un tool résultat dépasse le contexte.

## Code execution server-side (Anthropic)

```elixir
code_execution: true
```

Active le sandbox Anthropic — pas d'implémentation locale.

## My take

Beaucoup de features mais elles ont toutes la même propriété : **elles vivent au niveau du loop ou du provider, jamais au niveau "produit"**. Cost guard = mécanique de loop (combien on a dépensé, faut-il s'arrêter), pas de billing. Telemetry = events, pas de dashboard. Middleware = pipeline, pas de policy engine UI. `until_tool` = mécanique de loop. Caching = transport-level vers Anthropic.

C'est cohérent avec le design boundary du cluster 1 — chaque feature passe la "rule of thumb" du README : `helps any consumer + speaks the provider API correctly`.

Async dispatch via Phoenix.PubSub est le meilleur exemple de "OTP-native" qu'on peut faire : pas un wrapper bricolé, c'est *exactement* le pattern LiveView attendu. La friction d'intégration tend vers zéro pour un dev Phoenix.

Compaction + cost guard + telemetry + middleware = la base d'un agent qu'on peut vraiment monitorer et contrôler en prod. C'est ce qui rend Alloy candidat à du "agent en prod" malgré sa minimalité — pas du jouet.

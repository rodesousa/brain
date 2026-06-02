---
type: repo-cluster
status: kept
created: 2026-05-13
---

# Facet : memory-primitive

## Le contrat

`Alloy.Memory` est un **behaviour** qui définit le protocole de l'outil `memory_20250818` d'Anthropic, mais laisse le **store** au user.

> Alloy exposes memory as a behaviour — `Alloy.Memory` — matching the split Anthropic uses in their own Python SDK: Alloy owns the protocol (six commands on a `/memories/` tree, return-string formats, path validation); your code owns the backing store. No bytes touch Anthropic's servers.

Les 6 commandes :

```elixir
defmodule MyApp.Memory.Disk do
  @behaviour Alloy.Memory

  @impl true
  def view(store, path), do: ...
  @impl true
  def create(store, path, text), do: ...
  @impl true
  def str_replace(store, path, old, new), do: ...
  @impl true
  def insert(store, path, line, text), do: ...
  @impl true
  def delete(store, path), do: ...
  @impl true
  def rename(store, old_path, new_path), do: ...
end
```

## Activation

```elixir
Alloy.run("Remember the user prefers SI units",
  provider: {Alloy.Provider.Anthropic, ..., model: "claude-sonnet-4-6"},
  memory: {MyApp.Memory.Disk, root: "/var/agent/memories"}
)
```

Quand `:memory` est set, Alloy :
- injecte l'outil `memory_20250818` dans la requête Anthropic,
- ajoute le beta header `context-management-2025-06-27`,
- route les memory tool calls via `Alloy.Memory.Router` (pas le tool executor général), pour garder le typed-tool contract propre.

## Store opaque

Le second élément du tuple `{module, opts}` est **opaque** côté Alloy : keyword list, map, pid, struct — au choix. Pas de session scoping baked in :

> if you want per-session memory trees, thread `session_id: "..."` through your store opts and namespace inside your implementation.

## Contraintes 0.12

- **Anthropic only** au moment de la 0.12. Configurer `:memory` avec un autre provider raise à `Alloy.run/2`.
- D'autres providers seront wirés au fur et à mesure qu'ils livrent leur propre primitive memory.

## My take

C'est un cas d'école du design boundary appliqué :
- **Wire protocol** (6 commandes, paths, return strings) → Alloy.
- **Storage decision** (disk / Postgres / S3 / in-memory) → app.
- **Session scoping** → app (thread `session_id` toi-même).

"No bytes touch Anthropic's servers" est l'argument vendable : tu utilises le tool `memory_20250818` côté Claude mais ta donnée reste chez toi. C'est l'inverse de la valeur par défaut Anthropic (mémoire managée chez eux). Alloy te donne le levier sans te forcer.

Le routing via `Alloy.Memory.Router` séparé du tool executor général est un détail d'implémentation important : ça veut dire que les tools custom de l'app ne peuvent pas marcher sur les pieds du protocole memory (typage clair, surface séparée). Bon hygiène.

Anthropic-only en 0.12 est honnête (raise plutôt que silencieusement no-op). Le pattern est en revanche déjà la bonne abstraction pour quand OpenAI / Gemini livreront leur primitive — il y aura sans doute un `Alloy.Memory.Router` par provider, derrière le même behaviour.

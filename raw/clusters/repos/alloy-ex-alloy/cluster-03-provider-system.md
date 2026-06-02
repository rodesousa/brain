---
type: repo-cluster
status: kept
created: 2026-05-13
---

# Facet : provider-system

## 6 providers livrés

| Vendor | Module | Notes |
|---|---|---|
| Anthropic | `Alloy.Provider.Anthropic` | claude-opus-4-6, sonnet-4-6, haiku-4-5 |
| Gemini | `Alloy.Provider.Gemini` | GenerateContent API native |
| OpenAI | `Alloy.Provider.OpenAI` | Responses API native, gpt-5.4 |
| xAI | `Alloy.Provider.OpenAI` + `api_url: "https://api.x.ai"` | grok-4.20, grok-4.1-fast-reasoning |
| Codex | `Alloy.Provider.Codex` | (cité dans le pitch, pas dans la table providers) |
| OpenAI-compatible catch-all | `Alloy.Provider.OpenAICompat` | Ollama, OpenRouter, DeepSeek, Mistral, Groq, Together, Moonshot kimi-k2.6, qwen3-coder-plus 1M ctx, glm-4.6, etc. |

## Swap d'un provider en une ligne

```elixir
opts = [tools: [Alloy.Tool.Core.Read], max_turns: 10]

Alloy.run("Read mix.exs", [{:provider, {Alloy.Provider.Anthropic, api_key: "...", model: "claude-sonnet-4-6"}} | opts])
Alloy.run("Read mix.exs", [{:provider, {Alloy.Provider.OpenAI,    api_key: "...", model: "gpt-5.4"}} | opts])
Alloy.run("Read mix.exs", [{:provider, {Alloy.Provider.Gemini,    api_key: "...", model: "gemini-2.5-flash"}} | opts])
```

Le tuple `{ProviderModule, opts}` est l'unité de configuration. Les tools et la conversation sont inchangés.

## Trois choses non-triviales que le système gère

### 1. Provider-owned state (stored response IDs)

Certaines APIs exposent du state serveur (response IDs). Alloy reconnaît ce concept et l'expose dans `result.metadata.provider_state`, qu'on peut re-passer à la prochaine call :

```elixir
provider_state = result.metadata.provider_state

Alloy.run("Keep going",
  messages: result.messages,
  provider: {Alloy.Provider.OpenAI, ..., provider_state: provider_state}
)
```

Permet de continuer une conversation provider-native sans dupliquer le contexte côté client.

### 2. Reasoning blocks normalisés

Les modèles de reasoning OpenAI-compatibles qui renvoient `reasoning_content` (DeepSeek-R1, Grok reasoning) sont parsés en **thinking blocks de première classe** :

```elixir
[thinking, text] = hd(result.messages).content
thinking.type     #=> "thinking"
thinking.thinking #=> "Step 1: Let me consider..."
```

Même surface utilisateur que les blocks `thinking` d'Anthropic — la différence provider est gommée.

### 3. Citations / annotations

Pour les providers Responses-compatibles avec server-side search (xAI search par ex.), les citations sont exposées :
- `result.metadata.provider_response.citations` pour le bloc provider-level
- annotations inline dans les text blocks pour les spans

### `extra_body` passthrough

```elixir
extra_body: %{
  "response_format" => %{"type" => "json_object"},
  "temperature" => 0.3,
  "reasoning_effort" => "high"
}
```

Mergé en dernier — peut override n'importe quel champ par défaut. Permet de toucher des params provider-specific sans attendre une release d'Alloy.

## My take

Le vrai différenciateur n'est pas "6 providers" (c'est une checkbox) mais **la qualité de la normalisation** :

1. **`OpenAICompat` catch-all** — couvre Ollama, OpenRouter, DeepSeek, Groq, Together, plus quasiment tout ce qui n'a pas d'API native. En une seule abstraction.
2. **Reasoning blocks normalisés** — c'est subtil et précieux. La pluspart des wrappers exposent `reasoning_content` brut côté OpenAI-compat et `thinking` côté Anthropic, laissant le user merger. Alloy unifie côté `Alloy.Message`.
3. **Provider state passthrough** — reconnaît que certaines optimisations (stored response IDs OpenAI/xAI) sont serveur-side et ne doivent pas être ré-implémentées côté client. Élégant.
4. **`extra_body` mergé en dernier** — accepte d'être incomplet et te donne l'échappatoire. Plutôt que de bloquer sur "Alloy ne supporte pas reasoning_effort", tu le passes.

C'est un système de provider qui respecte le design boundary (cf. cluster purpose) : il traduit, il ne décide pas.

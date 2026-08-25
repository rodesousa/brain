---
type: repo-cluster
status: discarded
created: 2026-05-13
---

# Facet : quickstart-and-tables

## Contenu

- Installation `mix.exs` + dépendance `:alloy ~> 0.12` + `:alloy_agent ~> 0.1` optionnel.
- Snippets "Simple completion", "Agent with tools", "Swap providers", "Streaming".
- Table providers (Anthropic / Gemini / OpenAI / xAI / OpenAICompat) avec modèles d'exemple.
- Table built-in tools (read / write / edit / bash + modules).
- Snippet "Custom tools" (boilerplate `@behaviour Alloy.Tool`).

## Raison du discard

Boilerplate d'onboarding standard pour une lib publiée sur Hex.pm. La table providers et la table tools sont de la référence pure — utile à recopier dans la doc d'usage, sans signal différenciant pour le wiki.

Les modèles cités (claude-sonnet-4-6, gpt-5.4, gemini-2.5-flash-lite, grok-4.20…) changeront à la prochaine release et ne sont pas le sujet d'Alloy.

Si je veux la liste exhaustive un jour, je relis `raw/repos/alloy-ex-alloy.md`.

---
type: repo-cluster
status: kept
created: 2026-05-13
---

# Facet : purpose-design-boundary

## Pitch

> **Minimal, OTP-native agent loop for Elixir.**
>
> Alloy is the completion-tool-call loop and nothing else. Send messages to any LLM, execute tool calls, loop until done. Swap providers with one line. Run agents as supervised GenServers. No opinions on sessions, persistence, memory, scheduling, or UI — those belong in your application.

Inspiré explicitement par [Pi Agent](https://github.com/badlogic/pi-mono) (minimalisme).

## Design boundary explicite — section dédiée du README

Le README contient une section "Design Boundary" qui dit littéralement ce qui appartient et ce qui n'appartient pas à Alloy.

**Belongs in Alloy** :
- Provider wire-format translation
- Tool-call / completion loop mechanics
- Normalized message blocks
- Opaque provider-owned state (stored response IDs etc.)
- Provider response metadata (citations, server-side tool telemetry)

**Does not belong** :
- Sessions and persistence policy
- File storage, indexing, retrieval workflows
- UI rendering pour citations / search / artifacts
- Scheduling, background jobs, dashboards
- Tenant plans, quotas, billing, hosted infra policy

**Règle énoncée** :

> Rule of thumb: if the feature is required to speak a provider API correctly, and could help any Alloy consumer, it likely belongs here. If it needs a database table, product defaults, UI decisions, or tenancy logic, it belongs in your application layer.

## Taille déclarée

> ~7,500 lines — small enough to read, understand, and extend

## My take

C'est *la* signature d'Alloy et ce qui le distingue clairement d'à peu près tout le reste de l'écosystème. La majorité des frameworks d'agent essaient d'être un produit (sessions, RAG, mémoire, multi-agent, UI dashboard). Alloy refuse explicitement ce périmètre — il ne livre que la mécanique de la boucle et la traduction vers les wire formats des providers.

La "Rule of thumb" est une heuristique opérable, pas du vœu pieu : *"required to speak a provider API correctly + helps any consumer"*. C'est falsifiable cluster par cluster.

7500 LOC — c'est l'ordre de grandeur d'une lib qu'on peut lire en une journée. Cohérent avec le positionnement "read, understand, extend". À comparer avec Hermes qui est manifestement beaucoup plus gros.

Référence à **Pi Agent (badlogic/pi-mono)** comme source de la philosophie — entité à ingérer plus tard ^[inferred], probablement le même angle minimaliste mais sur la stack TypeScript (badlogic = Mario Zechner, ex-libGDX, profil créateur d'outils précis).

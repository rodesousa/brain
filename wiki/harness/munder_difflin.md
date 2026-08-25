---
summary: Munder Difflin — un harness multi-agents desktop qui enveloppe les CLIs d'agents existants (Claude Code, Codex, Grok…) en une équipe coordonnée par un orchestrateur "GOD", avec mémoire markdown-first partagée (hive), circuit breaker et un étage d'avatars Pixi.
created: 2026-08-25
updated: 2026-08-25
sources:
  - sources/munder-difflin-readme.md
  - sources/munder-difflin-hive.md
keywords: [harness, multi-agent, orchestrateur, hive, mémoire-markdown, circuit-breaker, claude-code, mem0, gbrain]
---

# Harness multi-agents — Munder Difflin

**TL;DR** — Un harness desktop (Electron) qui ne réinvente pas les agents : il enveloppe les CLIs
existants (Claude Code, Codex, Grok, Gemini, Qwen, Copilot, Cursor…) en une équipe auto-coordonnée.
La coordination vit dans des **fichiers plats + git** (le "hive"), un orchestrateur "GOD" adjudique
le trafic, et la mémoire est markdown-first avec un index sémantique optionnel. C'est un
contre-modèle instructif pour le brain : même philosophie markdown = vérité, mais tournée vers le
multi-agent temps réel plutôt que le knowledge base.

## Positionnement

- **App desktop** (Electron + React + TypeScript + Pixi.js + xterm.js + node-pty), MIT, ~4.2k★,
  prototype actif (v0.4.5, 2026-08).
- Wrappe **12 engines d'agents** : Claude Code, Antigravity (Gemini), Codex, Grok, Kimi, Gemini
  CLI, Qwen, OpenCode, Crush, pi.dev, Copilot CLI, Cursor — avec **BYOK** (bring-your-own-keys) et
  LLM locaux (Ollama/LM Studio/vLLM). Réutilise les abonnements existants sur leurs limites horaires.
- Le principe : chaque terminal-agent devient un **avatar** sur un "étage de bureau" 2D (façon
  Animal Crossing × The Office), coordonné par **Michael** (le GOD, "ton clone").

## Les 5 grosses features

### 1. Le hive — coordination sur fichiers (git), zéro DB serveur

Tout l'état vit dans un repo git local de fichiers plats :

```
hive/
  registry.json      # roster : agents, rôles, capacités, statut, siège
  board.md           # blackboard partagé (plans co-écrits, scribe unique = le GOD)
  tasks.json         # task ledger
  log.jsonl          # event feed append-only
  agents/<id>/       # par agent :
    identity.md      # qui je suis, mon rôle (lu au start)
    memory.md        # ma mémoire long-terme (lu au start, append au fil de l'apprentissage)
    inbox/ outbox/   # messages (1 fichier JSON par message, atomic rename)
    cursor.json      # anti-reprocessing
```

- **Markdown-first** : mémoire = `memory.md` par agent + blackboard. SQLite FTS si le keyword
  recall ne suffit pas. Décision explicite : pas de couche vecteur lourde (Letta/Mem0/Zep) à
  5-15 agents — "architecturally wrong" (ils veulent posséder le runtime).
- **Single-committer** : seuls le main process du harness committe (évite les corruptions
  `index.lock`). Les agents écrivent des fichiers plats, jamais git.
- **Single-writer-per-file** : chaque agent n'écrit que dans son dossier ; le routing croisé passe
  par la boîte mail (outbox → router → inbox).
- Messages au **schéma FIPA-lite** (speech acts : request/inform/propose/query/agree/refuse/done),
  avec anti-livelock (hops cap → le GOD escalade).

### 2. L'orchestrateur GOD (Michael, ton clone)

- Un agent privilégié, toujours actif, qui **adjudique** le trafic entre agents : il résout les
  demandes routinières lui-même (autonomie), n'escalade que le **critique** (dépenses, ops
  destructives, scope) vers l'humain.
- HITL natif : pas de queue d'approbation séparée — ce sont les prompts de permission Claude Code,
  approvables à distance (phone via `/remote-control`).
- La politique d'escalade vit dans son system prompt : "tune the prompt, not the code".

### 3. Mémoire : markdown-first + index sémantique optionnel

- Chaque agent a un `memory.md` qu'il lit au démarrage et append au fil de l'apprentissage.
- Un index sémantique (**MemPalace CLI**, pas MCP par décision) mine les `memory.md` dans une
  "mémoire partagée" recherchable (mtime-gated), **dégradable en no-op** si le CLI n'est pas là
  (le markdown marche sans).
- **MemoryReflector** (`reflect.ts`) : condensation périodique pour borner la croissance de
  `memory.md`. Le point "reflection/summarization" est encore ouvert (besoin d'un vrai install
  MemPalace pour valider).
- C'est exactement la philosophie validée pour le brain (D5) : markdown = vérité, index = vue
  dérivée reconstruisible, pas de service de mémoire externe.

### 4. Contrôle & visibilité : human gates + circuit breaker

- **Budgets & telemetry** : budgets token par agent, coût réel lu des transcripts (JSONL
  `~/.claude/projects/`), ledger durable (le coût est plié sur le lifetime, pas le restart),
  télémétrie OTel, tool waterfall.
- **Circuit breaker** : une échelle **steer → constrain → stop** pour les agents qui bouclent,
  inondent d'erreurs ou explosent leur budget.
- **Human gates** : spend, scope, destructive ops escaladent vers toi. Steer mid-run ou stop
  gracieux.
- Leçon v0.4.5 : le cost reporting resettait au restart (sous-estimation 59%), la mémoire
  sémantique plantait sur Apple Silicon (CoreML → NaN → embeddings pinnés CPU), et le messaging
  inter-agents était peu fiable (inbox wake watchdog ajouté). Trois "choses que tu croyais fiables
  et qui étaient fausses" corrigées.

### 5. Le floor / Command Center — l'UX

- **Étage 2D Pixi** : chaque agent = un avatar qui marche vers la station du fichier (read/write),
  le terminal (bash), le web portal (fetch/search), la mailbox (bloqué), etc. La métaphore est
  *informationnelle* : chaque animation dit quelque chose que tu ne savais pas.
- **Command Center** : kanban à dépendances, missions planifiées + heartbeat (schedules weekday,
  DST-safe), monitoring de flotte, recherche mémoire, activity log, CI watcher, Monaco IDE intégré
  avec rails git (CHANGES/HISTORY/COMPARE), catalogue de **skills** (227+), `munderdifflin://hire`
  (rôles partageables), Slack & webhooks (workers éphémères).

## Architecture : deux plans de données (la pièce la plus intéressante)

```
Renderer (React) — Floor Pixi + Terminal xterm
   ▲ avatar state         ▲ pty bytes
Event Plane (hooks→IPC)   Terminal Plane (node-pty PTYs)
   ▲ JSON events          ▲ stdin/stdout
   └────── claude / agy / codex ──────┘
```

- **Terminal plane** : chaque agent = un vrai process `node-pty`, byte-for-byte authentique.
- **Event plane** : les **hooks Claude Code** (PreToolUse, PostToolUse, Stop, Notification…)
  émettent du JSON via un socket Unix (`cth-hook` shim) → pilote les avatars et l'état du système.
- Pourquoi les deux : les hooks seuls ne donnent pas le flux brut ; le pipe tmux seul ne dit pas
  quel tool tourne. Ensemble : canvas event-driven + terminal authentique.

## Liens avec le brain / sujets liés

- Même philosophie que le brain : **markdown = vérité, index = vue dérivée reconstruisible, pas de
  service de mémoire externe à petite échelle** — validé par [[retrieval-memoire]] (gbrain,
  Mem0/Letta, munder).
- Le "hive" est l'analogue multi-agents de notre `wiki/` : fichiers plats + git comme coordination.
- Différence : munder coordonne des agents **temps réel** (mailbox, routing, GOD) ; le brain
  coordonne du **savoir durable** (retrieval flou, digest). Deux usages du même pattern markdown.
- Le **circuit breaker** (steer → constrain → stop) et le **budget/ledger** sont des idées à
  garder pour contrôler un harness — pas pertinentes pour le brain en lecture seule, mais pour
  l'exploitation d'agents.

## Voir aussi

- [[retrieval-memoire]] — la recherche qui valide le markdown-first (gbrain, Mem0, Letta, qmd)
- Sources : [[munder-difflin-readme]], [[munder-difflin-hive]]

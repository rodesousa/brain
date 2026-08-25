---
source-type: web
url: https://hermes-agent.nousresearch.com/docs/guides/work-with-skills
fetched: 2026-05-18
---

# Hermes Agent — Working with Skills (doc guides)

Snapshot de la page de documentation `guides/work-with-skills` du site officiel de Hermes Agent (Nous Research), au 2026-05-18.

## Overview

> "Skills are on-demand knowledge documents that teach Hermes how to handle specific tasks — from generating ASCII art to managing GitHub PRs."

## Finding Skills

### Lister

- En chat : `/skills`
- CLI : `hermes skills list`

Exemples de sortie :

- `ascii-art` — Generate ASCII art using pyfiglet, cowsay, boxes
- `arxiv` — Search and retrieve academic papers from arXiv
- `github-pr-workflow` — Full PR lifecycle management
- `plan` — Inspect context, write markdown plans
- `excalidraw` — Create hand-drawn style diagrams

### Searching

- Par mot-clé : `/skills search docker` ou `/skills search music`
- Hub browsing : `/skills browse` pour les skills officielles optionnelles

## Using Skills

Chaque skill installée devient automatiquement un slash command :

```
/ascii-art Make a banner that says "HELLO WORLD"
/plan Design a REST API for a todo app
/github-pr-workflow Create a PR for the auth refactor
/excalidraw
```

Les skills se chargent aussi via conversation naturelle — demander à l'agent d'utiliser une skill déclenche le tool `skill_view`.

### Progressive Disclosure Pattern

Chargement en 3 étapes pour rester token-efficient :

1. **`skills_list()`** — ~3k tokens pour toutes les skills, chargé au début de session.
2. **`skill_view(name)`** — `SKILL.md` complet, à la demande.
3. **`skill_view(name, file_path)`** — fichiers de référence spécifiques, à la demande.

> "This means skills don't cost tokens until they're actually used."

## Installing from the Hub

Les skills officielles optionnelles ship inactives par défaut. Méthodes d'installation :

```
hermes skills install official/research/arxiv
/skills install official/creative/songwriting-and-ai-music
hermes skills install https://sharethis.chat/SKILL.md
/skills install https://example.com/SKILL.md --name my-skill
```

Processus : le directory est copié vers `~/.hermes/skills/`, apparaît dans les listes, devient slash command.

> **Note** : les skills nouvellement installées s'activent dans **les nouvelles sessions**. Utiliser `/reset` ou le flag `--now` pour les rendre disponibles dans la session courante.

### Vérification

```
hermes skills list | grep arxiv
/skills search arxiv
```

## Plugin-Provided Skills

Les plugins peuvent bundler des skills avec noms namespaced (`plugin:skill`) :

```
skill_view("superpowers:writing-plans")
skill_view("writing-plans")
```

Les skills plugin ne sont **pas listées system-wide** — load explicit nécessaire. Le chargement affiche un banner avec les skills sibling du même plugin.

## Configuring Skill Settings

Les skills déclarent leurs besoins de config dans le frontmatter :

```yaml
metadata:
  hermes:
    config:
      - key: tenor.api_key
        description: "Tenor API key for GIF search"
        prompt: "Enter your Tenor API key"
        url: "https://developers.google.com/tenor/guides/quickstart"
```

Au premier chargement, Hermes prompt l'utilisateur, et stocke les valeurs dans `config.yaml` sous `skills.config.*`.

Management CLI :

```
hermes skills config gif-search
hermes config get skills.config
```

## Creating Custom Skills

Skills = markdown files avec frontmatter YAML. Process annoncé "5 minutes".

### Directory Structure

```
mkdir -p ~/.hermes/skills/my-category/my-skill
```

### SKILL.md Template

```yaml
---
name: my-skill
description: Brief description of what this skill does
version: 1.0.0
metadata:
  hermes:
    tags: [my-tag, automation]
    category: my-category
---
# My Skill

## When to Use
Use this skill when the user asks about [specific topic] or needs to [specific task].

## Procedure
1. First, check if [prerequisite] is available
2. Run `command --with-flags`
3. Parse the output and present results

## Pitfalls
- Common failure: [description]. Fix: [solution]
- Watch out for [edge case]

## Verification
Run `check-command` to confirm the result is correct.
```

### Optional Reference Files

Les skills peuvent inclure des fichiers chargés à la demande :

```
my-skill/
├── SKILL.md
├── references/
│   ├── api-docs.md
│   └── examples.md
├── templates/
│   └── config.yaml
└── scripts/
    └── setup.sh
```

Référencer depuis SKILL.md : `skill_view("my-skill", "references/api-docs.md")`.

### Testing

```
hermes chat -q "/my-skill help me with the thing"
```

Les skills apparaissent automatiquement — pas de registration nécessaire.

> L'agent peut **créer et update des skills lui-même** via `skill_manage`. Après une session de problem-solving complexe, Hermes peut proposer de sauver l'approche comme skill réutilisable.

## Per-Platform Skill Management

```
hermes skills
```

Ouvre un TUI interactif pour activer/désactiver les skills par plateforme (CLI, Telegram, Discord, etc.). Utile pour la disponibilité context-specific.

## Skills vs Memory Comparison

| Aspect | Skills | Memory |
|--------|--------|--------|
| **Content** | Procedural — how to do things | Factual — what things are |
| **Loading** | On demand, when relevant | Every session automatically |
| **Size** | Hundreds of lines OK | Should be compact |
| **Token Cost** | Zero until loaded | Small constant cost |
| **Examples** | "Deploy to Kubernetes" | "User prefers dark mode, PST timezone" |
| **Creator** | You, agent, or Hub | Agent from conversations |

> "Rule of thumb: If you'd put it in a reference document, it's a skill. If you'd put it on a sticky note, it's memory."

## Best Practices

- **Keep focused** : skills spécifiques ("Deploy Python app to Fly.io") > skills larges ("All of DevOps").
- **Agent-authored skills** : accepter les offres de sauvegarde de workflows complexes — capture les procédures exactes y compris les pitfalls découverts.
- **Use categories** : organiser en sous-répertoires (`~/.hermes/skills/devops/`, `~/.hermes/skills/research/`). Améliore manageability et discovery par l'agent.
- **Maintenance** : updater les skills stales quand des problèmes surviennent. "Skills that aren't maintained become liabilities."

---

Cross-reference : Skills System reference (`/docs/user-guide/features/skills`) pour les détails techniques complets.

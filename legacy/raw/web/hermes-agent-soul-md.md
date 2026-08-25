---
source-type: web
url: https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes
fetched: 2026-05-17
---

# Hermes Agent — Use SOUL.md with Hermes (doc guides)

Snapshot du contenu utile de la page de documentation `guides/use-soul-with-hermes` du site officiel de Hermes Agent (Nous Research), au 2026-05-17.

## Core Purpose

> "SOUL.md is the **primary identity** for your Hermes instance."

Le fichier occupe la **première position dans le system prompt**, définissant la personnalité de l'agent, son approche de communication et ses limites stylistiques.

## Ce qui appartient à SOUL.md

Le fichier doit adresser :

- Tone et traits de personnalité
- Préférences de style de communication
- Niveaux de chaleur / directness
- Évitements stylistiques
- Comment gérer l'incertitude et le désaccord

> **Key principle** : "if it should apply everywhere, put it in `SOUL.md`"

## Ce qui ne doit PAS être dans SOUL.md

Exclure les détails projet : conventions de code, file paths, commandes, ports de services, notes d'architecture — ces choses-là appartiennent à `AGENTS.md`.

## Emplacement du fichier

```
~/.hermes/SOUL.md
```

Ou avec un home directory personnalisé :

```
$HERMES_HOME/SOUL.md
```

## Initialisation automatique

Hermes crée automatiquement un template starter au premier run si le fichier n'existe pas. Les fichiers existants **ne sont jamais overwritten**.

## Quatre exemples de styles de personnalité

- **Pragmatic Engineer** — Direct, concis, évite le hype et la flagornerie.
- **Research Partner** — Explore les possibilités, distingue spéculation et preuve, pose des questions clarifiantes.
- **Teacher/Explainer** — Approche patiente, construit depuis l'intuition, ne présume pas la connaissance préalable.
- **Tough Reviewer** — Pointe les hypothèses faibles sans détour, priorise la correction sur l'harmonie.

## Strong vs. Weak SOUL.md

**Strong characteristics**

- Stable et largement applicable
- Voix spécifique sans instructions temporaires
- Vraie personnalité au-delà des defaults génériques

**Weak characteristics**

- Surchargé de détails projet
- Guidance contradictoire
- Reformule des defaults évidents comme "be helpful"

## Structure suggérée

```
# Identity
# Style
# Avoid
# Defaults
```

## SOUL.md vs. `/personality`

Utiliser SOUL.md pour l'identité baseline durable. La commande `/personality` permet des switches de mode temporaires en cours de session **sans modifier le base file**.

## SOUL.md vs. AGENTS.md (distinction)

**Exemples de contenu SOUL.md**

- "Be direct"
- "Avoid hype language"
- "Push back when wrong"

**Exemples de contenu AGENTS.md**

- "Use pytest, not unittest"
- "Frontend lives in `frontend/`"
- "API runs on port 8000"

## Édition

```
nano ~/.hermes/SOUL.md
```

Redémarrer Hermes ou démarrer une nouvelle session pour que les changements prennent effet.

## Workflow pratique

1. Partir du default seedé.
2. Trimmer les éléments non-essentiels.
3. Ajouter 4 à 8 lignes définissantes.
4. Tester en conversation.
5. Itérer selon les résultats.

## Troubleshooting

**Changements qui ne s'appliquent pas**

- Vérifier le bon file path édité
- Vérifier que le fichier n'est pas vide
- Confirmer le restart de session
- S'assurer que `/personality` ne l'override pas

**Hermes ignore le contenu**

- Des instructions plus prioritaires l'override
- Le fichier contient des guidance contradictoires
- Le fichier dépasse les limites de truncation
- Le contenu est flagué comme prompt-injection potentielle

**Fichier sur-spécialisé**

Bouger les instructions projet vers `AGENTS.md`, garder SOUL.md focalisé sur identité et voix.

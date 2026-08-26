# Schema — brain/

> ⚠ **EN REFONTE.** Vault passé en feuille blanche le 2026-08-25. Les décisions D1-D5 sont actées
> dans `refonte.md` ; veille & lint restent à trancher (prochaine session). Ce fichier décrit le
> schéma ACTUEL, en vigueur pour les ingests.

Ce vault est un brain personnel : une base de connaissances markdown, Obsidian-compatible, qu'un
agent (le harness) maintient pour l'utilisateur. Modèle inspiré du LLM Wiki de Karpathy
(`LLM-WIKI-CONCEPT.md`), refondu vers « un dossier par sujet, un fichier digest par défaut ».
L'ancien schéma vit dans `legacy/` et n'est plus jamais touché.

## Rôle de l'agent (harness)

- **Capture** : l'utilisateur donne une source par un geste de chat → je l'ingère.
- **Résumé** : chaque sujet a un digest consultable ; le résumé est vivant (mis à jour quand on en
  parle).
- **Retrieval** : « le truc sur X » doit retomber sur la bonne page. L'index est ma carte ; si une
  requête échoue, je **réécris la requête 2-3 façons** (synonymes, autres angles) avant de conclure
  « introuvable ».

## Structure

- `legacy/` — ancien schéma complet (wiki + raw + index/hot/improve + tools + Clippings), conservé
  tel quel, **non maintenu**, jamais touché. Git garde tout l'historique.
- `wiki/<sujet>/<sujet>.md` — le NOUVEAU schéma. **Un dossier par sujet, un fichier digest par
  défaut** qui grossit à chaque source. Fichiers supplémentaires (dont `sources/`) seulement à la
  demande de l'utilisateur, jamais de moi-même.
- `wiki/<sujet>/sources/<slug>.md` — texte brut d'une source substantielle (> ~150 mots). Jamais
  dans l'index.
- `refonte.md` — document de travail de la refonte (interview, décisions, questions ouvertes).
- `projet/` — specs des projets en cours (vide, format à préciser à la première utilisation).
- `index.md` — **LA carte du brain pour le harness.** À lire EN ENTIER au début de chaque session.
  Une ligne par sujet (avec mots-clés). Jamais les fichiers `sources/`.
- `log.md` — journal chronologique append-only des opérations (maintenu à la main).
- `decisions.md` — **le "pourquoi" durable.** Append-only. Chaque décision d'architecture actée en
  session s'écrit ici (entrée datée). Une entrée périmée se marque `superseded`, jamais supprimée.
- `LLM-WIKI-CONCEPT.md` — référence du pattern, ne pas modifier.

## Règle — Décisions (ADR)

Quand une décision d'architecture (brain ou projet) est actée, l'écrire dans `decisions.md` — pas
seulement en mémoire de session. Quand un sujet revient, jeter un œil à `decisions.md` : le
"pourquoi" s'y relit, il ne se re-réexplique pas en chat.

## Démarrage de session

1. Lire `index.md` en entier — c'est la liste de tout ce que le brain sait.
2. Si l'utilisateur pose une question, faire le fuzzy match entre la demande et le nom + mots-clés
   d'une ligne de l'index, puis ouvrir `wiki/<sujet>/<sujet>.md` (le digest).
3. Si la réponse a besoin d'une source brute, l'ouvrir dans `wiki/<sujet>/sources/`.

## Conventions de pages (digest)

### Langue

Français par défaut (langue de l'utilisateur).

### Liens

Wikilinks Obsidian natifs : `[[nom-de-page]]`. Pas de liens markdown relatifs. Un lien vers une
source se fait vers son slug (`[[<slug-source>]]`).

### Frontmatter (digest)

```yaml
---
summary: Une phrase décrivant ce que le sujet contient. Doit toujours être à jour.
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - sources/<slug>.md
keywords: [mot-cle, autre-mot-cle]
---
```

- `summary` — la phrase qui répond à une query sans ouvrir le fichier. **Toujours à jour.**
- `sources` — chemins relatifs vers les fichiers bruts dans `sources/`.
- `keywords` — le vocabulaire des requêtes orales de l'utilisateur, pour le fuzzy match de l'index.

### Structure du digest

- `# <sujet>` — titre.
- **TL;DR** — 2-3 lignes en haut (couche 2 de progressive summarization).
- Sections par thème (points clés, décisions, liens…).
- `## Voir aussi` — wikilinks vers les sujets liés + les sources brutes.
- Pas de lifecycle, pas de marqueurs `^[inferred]`, pas de `## My take` (supprimés par la refonte).

### Dépréciation

Un sujet remplacé/obsolète : le dossier et le fichier restent (consultables), l'index le marque
`(deprecated)`.

## Workflow — Ingest

1. **Lire** la source (URL via web, chemin de fichier, ou texte collé).
2. **Triage `should_compile`** : `yes` / `no` / `maybe` + raison en 1 ligne. Si `no`, on s'arrête
   (la source ne rentre pas).
3. **Confirmer avant d'écrire** : présenter à l'utilisateur un résumé de la source + le triage
   `should_compile`, et attendre son « oui » explicite avant de créer/mettre à jour quoi que ce soit
   (digest, source, index, log). Aucun fichier n'est touché avant ce feu vert.
4. **Repérer le sujet** : regarder `index.md`. Sujet existant → on ajoute dans son digest ; sinon on
   crée `wiki/<sujet>/<sujet>.md`.
5. Si la source fait > ~150 mots → la sauver en texte brut dans `wiki/<sujet>/sources/<slug>.md`.
   Sinon, intégrer directement dans le digest.
6. **Écrire le digest** : TL;DR, points clés, mise à jour de `updated:`/`summary:`/`keywords`.
7. Mettre à jour la ligne dans `index.md` (nom, one-liner, mots-clés).
8. Append dans `log.md` : `## [YYYY-MM-DD] ingest | <titre source>`.
9. Si la source est à cheval sur deux sujets : poser UNE question max, puis file.

## Workflow — Query

1. Lire `index.md` (déjà fait au démarrage) → repérer les sujets candidats.
2. Ouvrir les digests candidats.
3. Synthétiser, **citer les sources** (wikilinks) utilisées.
4. Si la réponse a de la valeur durable et que l'utilisateur est d'accord → crystallize en nouveau
   sujet (digest + index + log).

## Workflow — Lint (à redéfinir, voir refonte.md)

Rien d'acté pour l'instant. En attendant : garder `index.md` cohérent (pas de ligne sans page, pas
de page sans ligne), `summary:` à jour, `log.md` append-only.

## Format du log

Chaque entrée commence par `## [YYYY-MM-DD] <action> | <details>` :

```
## [2026-08-25] ingest | Premier sujet — retrieval-memoire
## [2026-08-25] update | index.md réécrit comme carte du harness
```

Actions valides : `init | ingest | query | lint | crystallize | update | note`.

## Notes

- Ce schéma est vivant. Toute évolution de convention se fait par discussion avec l'utilisateur,
  puis modification de ce fichier (et entrée dans `log.md` avec action `update`).
- Pas de génération autonome silencieuse : confirmer avant de toucher beaucoup de pages.
- Si une règle de ce schéma rentre en conflit avec une situation concrète, **demander** plutôt
  que d'improviser.
- **AGENTS.md ne doit pas grossir** : il est lu à chaque session (~6 KB, ~1 500-2 000 tokens).
  Le détail va dans les pages wiki ; ce fichier reste le contrat compact.
- **Index sub-grouping** : si une section de `index.md` dépasse ~15 entrées, la sub-diviser par
  thème dominant dans `index.md` (pas de migration de fichiers).

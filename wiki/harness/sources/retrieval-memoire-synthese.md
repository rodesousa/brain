# Optimiser l'index et la mémoire d'un brain markdown-only — synthèse de recherche

> Recherche web (2026-08-25) — input pour la refonte de `brain/` (voir `refonte.md`).
> Stack cible : markdown + git + Obsidian, **pas de DB** en production à ce stade.

## Constat de départ (ce que le brain fait déjà bien)

Le brain est un LLM Wiki (pattern Karpathy) dont la query path est déjà **"LLM comme retriever sur catalogue compressé"** :
`CLAUDE.md` → lire `index.md` (54 lignes, ~1-2k tokens) → lire les `summary:` des frontmatters candidats → n'ouvrir que les pages pertinentes.
C'est exactement le bon pattern pour <200 pages : l'index plat + résumé une ligne **tient dans le contexte**, et le LLM fait le fuzzy matching ("le truc sur X" → bonne page) sans embeddings. La littérature confirme que c'est le bon premier échelon — pas une béquille.

---

## (a) Moteurs / index locaux pour markdown

### qmd (github.com/tobi/qmd) — le plus directement pertinent
Moteur de recherche CLI **100% local** pour collections markdown (docs, notes, KB). Pipeline hybride, tout en local via node-llama-cpp (GGUF) :
- **BM25** (SQLite FTS5) + **vector search** (embeddings locaux, ex. EmbeddingGemma) + **LLM reranker** (qwen3-reranker, cross-encoder) ;
- **Query expansion** : un petit LLM (qwen3) génère 2 variantes de la requête (HyDE), fusées avec la requête originale ;
- **Fusion par Reciprocal Rank Fusion (RRF)** : score = Σ 1/(k+rank), requête originale pondérée ×2 ;
- Trois modes : `qmd search` (BM25 pur), `qmd vsearch` (vecteur pur), `qmd query` (hybride complet). CLI **+ serveur MCP** (branchable à Hermes/Claude).
- **Chiffre clé de son propre bench** (fixture d'exemple) : `bm25 ~0.50`, `vector ~0.70`, `hybrid/full ~1.00` — la fusion bat chaque backend seul. ~29k★.

Pour une stack markdown-only, qmd est l'évolution naturelle quand l'index plat ne suffit plus : pas de DB, les `.md` restent la source de vérité, l'index (FTS + vecteurs) est un artefact **reconstruisible** (`qmd index`).

### Le milieu de terrain "zéro install lourd" : ripgrep / fzf / SQLite FTS5
- **ripgrep + fzf** : le duo déjà disponible partout. Exact-string + fuzzy sur les titres. Gratuit, instantané, zéro infra.
- **SQLite FTS5** : si on veut du vrai full-text ranké (BM25) sans DB serveur, un simple `.sqlite` dans le repo suffit — markdown reste la vérité, FTS5 est un index reconstruisible. C'est exactement le pattern que les outils markdown-MCP (ex. `markdown-vault-mcp`) implémentent.
- **Obsidian** : la recherche intégrée est déjà rg-like et suffit pour la lecture humaine. Pour l'agent, c'est le moteur externe qui manque.

### Obsidian, pour du sémantique sans sortir du vault
- **Smart Connections** (brianpetro/obsidian-smart-connections) : embeddings **locaux** dans le vault, pas d'API, "notes liées par le sens". Alternative open-source citée : **Neural Composer**.
- **Dataview** : génère des vues d'index **dérivées** depuis les frontmatters (utile pour remplacer/combler `index.md` par une vue).
- À noter : ces plugins servent la **lecture humaine** dans Obsidian ; pour l'**agent**, mieux vaut exposer une recherche via tool (grep/search_files) ou un serveur qmd/MCP.

### gbrain (github.com/garrytan/gbrain) — l'architecture de référence (déjà citée dans refonte.md)
Le brain de Garry Tan (YC) tourne sur OpenClaw/Hermes, et c'est le modèle le plus proche de ce que refonte.md veut faire :
- **Markdown-first, DB-synced** : la vérité est dans le repo git en markdown ; la DB (Postgres/PGLite) n'est **qu'un index de retrieval reconstruisible**. → séparer stockage et recherche.
- **Graphe typé auto-câblé, zéro appel LLM** : les arêtes (`works_at`, `founded`, `invested_in`…) sont extraites à l'écriture. Mesuré : **P@5 49.1%, R@5 97.9%** sur un corpus de 240 pages, **+31.4 points de P@5** vs la variante sans graphe ET vs "ripgrep-BM25 + RAG vecteur seul".
- **Deux modes de lecture** : `search` (hybride vecteur+BM25, retourne des pages à skimmer) et `think` (réponse synthétisée avec citations **+ gap analysis** : ce que le brain ne sait pas encore).
- **Inbox** : fichiers déposés dans `~/.gbrain/inbox/` + webhook `/ingest` → capture sans friction (`gbrain capture` → page dans la DB **et sur disque**, slug `inbox/YYYY-MM-DD-<hash8>`).
- **Dream cycle** (cron 24/7) : dédup, réparation de citations, **scoring de salience, détection de contradictions**.
- **Mise en garde de l'auteur lui-même** : "Gbrain is mostly useful at **10,000+ markdown files**" (post X). → en dessous, l'index plat + grep suffisent ; la machinerie DB/graphe ne paie qu'à l'échelle.

### Patterns humains : progressive summarization (Tiago Forte) + memory files
- **Progressive summarization** (fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes) : une note est rendue "découvrable" par **couches successives** — capture (brut) → **gras** sur les phrases clés → **highlight** → **résumé exécutif** (4 couches max). Chaque couche est un sous-ensemble de la précédente, donc la note reste skimmable à n'importe quel niveau de détail. C'est le mécanisme humain que le `summary:` du frontmatter ne fait qu'à moitié (une seule couche). Pour un brain maintenu par agent : implémenter 2 couches (résumé 1 ligne en frontmatter + `## TL;DR`/gras dans le corps) et les **re-compresser à chaque relecture** — c'est le "résumé vivant" que refonte.md veut (C4).
- **CLAUDE.md / MEMORY.md** (pattern déjà documenté dans `wiki/concepts/claude-md-pattern.md`) : fichier lu à chaque session → defaults + behavior + **MEMORY.md** (decision log append-only : what/why/what-rejected) + **ERRORS.md** (failure log après >2 tentatives). **Limite documentée** : un fichier lu en entier à chaque session ne scale pas — quand il grossit, il remplit le contexte de bruit (thread "claude.md doesn't scale", r/ClaudeCode). → Le memory file doit rester **court** (top ~1-2k tokens) et pointe vers les pages détaillées plutôt que tout contenir.

---

## (b) Systèmes de mémoire d'agents — les mécanismes réutilisables en markdown

### MemGPT / Letta (arXiv:2310.08560, "Towards LLMs as Operating Systems")
Architecture mémoire **inspirée d'un OS**, hiérarchie à deux niveaux :
- **Core memory** (in-context, taille fixe) : les faits durables, éditables par l'agent via tool calls (`core_memory_append`) — "RAM".
- **Recall memory** (historique de conversation, persistant) + **Archival memory** (stockage externe, interrogé par outil) — "disque".
- **Memory pressure** : quand le contexte est presque plein, **interrupt** → résumé récursif des messages évincés → archivage → éviction. L'agent gère lui-même son paginage.
- **Réutilisable en markdown** : c'est une validation directe du pattern "petit fichier toujours en contexte (MEMORY.md / index.md) + pages = mémoire archivistique + consolidation par résumé quand ça grossit". Le brain n'a pas besoin d'un OS virtuel : le **fichier mémoire court en contexte + le wiki en archive + la consolidation à la demande** reproduit la même chose avec des fichiers.

### Mem0 (arXiv:2504.19413, "Building Production-Ready AI Agents with Scalable Long-Term Memory")
Couche mémoire "first-class object" (contenu + métadonnées + score + timestamps), scoping par `user_id`/`agent_id`. Les mécanismes réellement réutilisables :
- **Extraction, pas stockage** : le LLM décide **quoi** mémoriser d'une conversation — il ne stocke pas tout en vrac. → À l'ingest, n'écrire que les **faits distillés** dans la page sujet (pas le blob brut) — déjà le sens de la décision D1 de refonte.md.
- **Algorithme 2026 : ADD-only single-pass** : une seule passe LLM, **pas d'UPDATE/DELETE** — les mémoires s'accumulent, rien n'est écrasé. → En markdown : append-only + git history = la même garantie anti-régression.
- **Typologie mémoire** : working / factual / episodic / semantic / procedural. → Utile pour structurer un `memory/` : faits stables (préférences, décisions) vs épisodes datés (log.md) vs connaissance généralisée (pages wiki).
- **Mémoire ≠ RAG** : le RAG répond mieux (grounding externe), la mémoire fait **comporter** mieux (continuité, préférences). Le brain a besoin des deux : RAG = les pages wiki, mémoire = MEMORY.md + log.md.

### Zep / Graphiti (arXiv:2501.13956, "A Temporal Knowledge Graph Architecture for Agent Memory")
Mémoire à **graphe de connaissance temporel** (bi-temporel : "valid time" + "ingestion time") :
- Chaque fait = arête avec fenêtre de validité + **provenance** vers l'épisode source.
- **Invalidation automatique** : une info nouvelle qui contredit une ancienne **invalide** l'ancienne (ne la supprime pas) → pas de fait contradictoire servi à l'agent. C'est le point que le vecteur pur rate (la ville de Munich reste "sémantiquement parfaite et factuellement morte").
- Sous-graphes épisodique / sémantique / communauté (résumés de domaine) — hiérarchie qui rappelle la mémoire humaine.
- Bench : DMR 94.8% vs MemGPT 93.4% ; +18.5% sur LongMemEval ; -90% de latence.
- **Réutilisable en markdown** : sans graphe DB, on peut capter **l'essentiel** — (1) la **provenance** est déjà là (`sources:` en frontmatter, URL dans l'inbox) ; (2) la **contradiction** se gère par une passe de consolidation qui marque `^[superseded]` / met à jour `updated:` ; (3) l'historique temporel est dans **git** (un fait périmé reste consultable dans l'historique, comme une fenêtre de validité). Le full temporal KG (Graphiti, sur Neo4j/FalkorDB) est une surcharge injustifiable à cette échelle.

### Le résultat qui change tout : Letta, "Benchmarking AI Agent Memory: Is a Filesystem All You Need?" (letta.com/blog, 08/2025)
Letta (l'équipe MemGPT) a mis l'historique LoCoMo dans **un simple fichier**, attaché à un agent avec des outils `grep` / `search_files` / `open`, et l'agent a **battu les outils mémoire spécialisés** : **74.0% sur LoCoMo** (GPT-4o-mini, prompting minimal) contre **68.5%** rapportés par Mem0 pour sa meilleure variante graphe. Conclusions :
- La capacité de l'agent à **utiliser** un outil (savoir quand et comment chercher) importe plus que le mécanisme de retrieval (vecteur vs graphe vs BM25).
- Les outils filesystem sont **surreprésentés dans les données d'entraînement** → les agents les utilisent mieux que des APIs mémoire exotiques.
- Un agent peut **générer ses propres requêtes** et **itérer** ("Calvin motivation setbacks" au lieu de la question brute), là où un retriever one-shot s'arrête.
- **Conséquence directe pour le brain** : le vrai levier n'est PAS d'ajouter une DB vectorielle. C'est de donner à l'agent de bons outils de recherche (search_files, grep, lecture de frontmatters) et de lui **apprendre à itérer**. C'est moins cher, plus fiable, et ça a le benchmark pour lui.

---

## (c) Règles de décision retrieval pour <200 pages

| Échelon | Quand ça suffit | Symptôme qu'il faut monter d'un cran |
|---|---|---|
| **1. Index plat (index.md + summary une ligne)** | ~≤300-500 entrées. L'index tient dans le contexte (~1-2k tokens), le LLM fait le fuzzy match "le truc sur X" → page. C'est le point de départ **optimal** à 54 pages. | Des requêtes échouent alors que la page existe (le titre/ligne ne matche pas le vocabulaire de la question). |
| **2. Full-text (ripgrep / SQLite FTS5 / `qmd search`)** | Quand le vocabulaire diverge du titre, ou que l'index déborde du contexte. BM25 excelle sur les termes rares/distinctifs (IDs, acronymes, noms propres) — précisément ce que le vecteur rate. | Ajouter en tool au lieu de tout mettre dans l'index. Coût : nul. |
| **3. Hybrid BM25+vecteur (+rerank) — qmd `query`** | ~>1 000 pages, ou quand les synonymes/paraphrases dominent. Le vecteur apporte la **généralisation** (match sémantique), BM25 la **précision** (mots rares), le rerank trie le top. Bench qmd : hybride ~1.00 vs bm25 ~0.50 / vecteur ~0.70. RRF = fusion sans entraînement (Cormack/Clarke/Büttcher 2009 ; implémenté par défaut dans Weaviate, Azure AI Search, Elastic). | Le brain est à **54 pages** : ce n'est **pas** le moment. |
| **4. Graphe (gbrain / Graphiti)** | Quand les requêtes deviennent **relationnelles** ("qui travaille chez X ?", "qu'a investi Bob ce trimestre ?"). +31.4 P@5 dans le bench gbrain (240 pages). Garry : utile à **10k+ fichiers**. | Pas avant très longtemps pour un brain perso <500 pages. |

**Règle d'or à cette échelle** : l'index plat + summary + grep est le bon système. Les embeddings résolvent le *vocabulary mismatch* — mais sur un petit corpus, le LLM le résout déjà en lisant un index de 2k tokens, et l'agent peut **réécrire sa propre requête et itérer** (résultat Letta). Les embeddings ajoutent une vraie dette d'ops (modèle d'embed, reindex à chaque changement, stockage) pour un gain qui ne se manifeste qu'à l'échelle.

---

## Recommandations concrètes (maintenant, markdown-only sans DB)

**1. Upgrade `index.md`, pas le remplacer.** Ajouter des **alias/mots-clés** par ligne (le vocabulaire de tes requêtes orales), trier par **salience** (section prioritaire ou timestamp last-touched), garder le one-liner = la réponse si possible. Le sub-grouping par tag dès 15 entrées/section (déjà prévu dans CLAUDE.md) est la bonne réponse à la croissance. Coût : quasi nul, ROI immédiat.

**2. Donner à l'agent des outils de recherche + lui apprendre à itérer** (leçon Letta). Le workflow Query actuel (index → frontmatters → ouvrir) est bon ; lui ajouter **grep/search_files comme fallback** quand l'index ne matche pas, et une règle : "réécris la requête 2-3 façons avant de conclure 'introuvable'". C'est l'équivalent markdown du query expansion + itération de qmd/Letta, sans aucune infra.

**3. Ajouter un `memory/` (pattern CLAUDE.md/MEMORY.md + Mem0), court.** `memory/MEMORY.md` append-only (décisions, faits stables, préférences — what/why/what-rejected), `memory/ERRORS.md` (échecs récurrents). Garder le tout **≤ ~1-2k tokens** en contexte (limite documentée du CLAUDE.md qui ne scale pas) ; le détail va dans les pages wiki.

**4. Appliquer Mem0-style extraction à l'ingest.** N'écrire que les **faits distillés** dans la page sujet (une source → 0 ou 1 fichier, décision D1 de refonte.md), append-only, provenance par URL en frontmatter. C'est déjà ta trajectoire — la recherche la valide.

**5. Implémenter la "couche 2" de progressive summarization + le résumé vivant.** Une couche `## TL;DR` (2-3 lignes) + gras sur les phrases clés dans chaque page ; à chaque relecture/discussion, **re-compresser** le résumé (refonte C4). Le `summary:` frontmatter reste le niveau 1.

**6. Passe de consolidation périodique = "dream cycle" markdown.** Un cron léger (ou une routine git) qui : met à jour `updated:`/`summary:`, marque les faits contredits `^[superseded]` (mécanisme Zep sans graphe), repère les pages orphelines/stale, et **git commit**. L'historique git joue le rôle de la mémoire temporelle : rien n'est perdu, tout est daté.

**7. Ne PAS faire maintenant :** DB vectorielle, graphe DB, Mem0/Zep/Letta comme services. Arguments : 54 pages ; Garry dit 10k fichiers ; Letta montre que filesystem + agent itératif bat déjà les outils spécialisés. Ajouter une de ces briques aujourd'hui, c'est de la dette d'ops sans gain mesurable.

**8. Évolution si/quand ça coince :** (1) SQLite FTS5 ou `qmd search` pour le full-text (toujours markdown-first, index reconstruisible) ; (2) `qmd query` hybride + rerank quand l'index plat déborde du contexte ; (3) éventuellement un PGLite/Postgres **comme index reconstruisible à la gbrain** — jamais comme source de vérité ; (4) graphe typé (gbrain) uniquement quand les requêtes relationnelles apparaissent.

---

## Sources
- qmd — https://github.com/tobi/qmd (benchmark hybride ~0.50/~0.70/~1.00) ; issue #331 (usage sur ~20 fichiers markdown perso)
- gbrain — https://github.com/garrytan/gbrain (P@5 49.1%, +31.4 pts, dream cycle, inbox, search/think) ; post X "mostly useful at 10,000+ markdown files" — https://x.com/garrytan/status/2071910876496757145
- MemGPT — https://arxiv.org/abs/2310.08560 ; Mem0 — https://arxiv.org/abs/2504.19413 et https://mem0.ai/blog/memory-in-agents-what-why-and-how (extraction, types de mémoire, ADD-only 2026)
- Zep/Graphiti — https://arxiv.org/abs/2501.13956 ; https://www.getzep.com/ai-agents/temporal-knowledge-graph/ (bi-temporel, invalidation, provenance)
- Letta — "Benchmarking AI Agent Memory: Is a Filesystem All You Need?" https://www.letta.com/blog/benchmarking-ai-agent-memory/ (74.0% vs 68.5% sur LoCoMo)
- RRF — Cormack/Clarke/Büttcher 2009 ; explication + implémentations : https://blog.serghei.pl/posts/reciprocal-rank-fusion-explained/ ; Elastic/Azure/Weaviate
- Hybrid retrieval BM25+vecteur — https://www.infoq.com/articles/vector-search-hybrid-retrieval-rag/ ("embeddings = généralisation, BM25 = précision")
- Progressive summarization — https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/
- CLAUDE.md/MEMORY.md — https://code.claude.com/docs/en/memory ; limite de scaling : https://www.reddit.com/r/ClaudeCode/comments/1qr9dws/claudemd_doesnt_scale_built_a_memory_agent_for/
- Obsidian : Smart Connections https://github.com/brianpetro/obsidian-smart-connections ; Dataview ; alternatives (Neural Composer) r/ObsidianMD

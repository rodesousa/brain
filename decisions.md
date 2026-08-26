# Décisions

Journal append-only des décisions du brain et des choix d'architecture discutés.
Une entrée par décision durable — le "pourquoi" qu'on ne veut pas réexpliquer
deux fois. Chaque entrée est datée et, si elle tombe en désuétude, marquée
`superseded` plutôt que supprimée.

## 2026-08-25 — ADR (Architecture Decision Record) comme volet du brain

**Contexte** — Un post de geoff (@GeoffreyHuntley, 24/08/2026) vante le pattern : dès le jour 0
d'un projet, demander à l'agent de créer des ADR en tant que skill, puis l'agent les consulte et
les maintient récursivement à chaque session de dev/planning. Répliques clés du fil : utiliser
`agents.md` comme une "lookup table" (lazy loading du contexte, "page in vs malloc"), et ne plus
avoir à re-prompt ("c'est hands-off, même dans des sessions/contextes sans rapport").

**Décision** — Un seul fichier append-only `decisions.md` dans le brain, alimenté à la demande
("enregistre cette décision") ou quand une décision d'architecture est actée. Pas de dossier
`decisions/` : un fichier suffit à ce stade. Le schéma du brain garde index.md = carte (sujets),
log.md = journal, sessions.md = IDs de sessions, decisions.md = le "pourquoi" durable.

**Pourquoi / alternatives**
- Dossier `decisions/` par sujet (ADR-001…) → sur-ingénierie tant que le nombre reste faible ;
  un fichier append-only suffit et colle au style log.md.
- Le brain a déjà l'équivalent de la "lookup table" du post : index.md lu en entier en début de
  session, pages chargées à la demande. decisions.md ajoute la **boucle de maintenance** : l'agent
  relit et met à jour la décision quand elle change, au lieu de tout re-réexpliquer.

**Conséquences** — Quand une décision d'architecture est actée en session, elle s'écrit ici (une
entrée datée), pas seulement en mémoire de session. L'agent doit y jeter un œil quand un sujet
revient. Une entrée périmée se marque `superseded`, jamais supprimée.

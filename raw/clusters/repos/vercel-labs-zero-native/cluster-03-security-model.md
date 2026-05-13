---
type: repo-cluster
status: kept
created: 2026-05-13
---

# Facet : security-model

> The WebView is treated as untrusted by default. Native commands, permissions, navigation, external links, and window APIs are opt-in and policy controlled.

## Surface couverte par la policy

- **Native commands** (bridge handlers) — opt-in via enregistrement explicite côté Zig.
- **Permissions** — déclarées dans `app.zon` (ex. `permissions = .{ "window" }`).
- **Capabilities** — séparées des permissions (ex. `capabilities = .{ "webview", "js_bridge" }`).
- **Navigation** — `allowed_origins` whitelist explicite. Exemple :
  ```zig
  .security = .{
      .navigation = .{
          .allowed_origins = .{ "zero://app", "http://127.0.0.1:5173" },
      },
  },
  ```
- **External links** — opt-in (non détaillé dans le README mais listé dans les surfaces couvertes).
- **Window APIs** — opt-in.

## Bridge `window.zero.invoke()` — checks par appel

- size-limited
- origin checked
- permission checked
- routed only to registered handlers

## My take

Posture "deny by default" assumée — c'est l'inverse d'Electron où tout est accessible par défaut côté renderer et où il faut désactiver explicitement (nodeIntegration = false, contextIsolation = true) pour durcir. Ici, le WebView est traité **comme un browser tab non fiable**, ce qui correspond à la réalité d'une appli desktop web-based qui charge potentiellement du contenu remote.

Sépération `permissions` vs `capabilities` dans `app.zon` est intéressante mais pas expliquée dans le README — hypothèse ^[inferred] : `capabilities` = quelles surfaces du runtime sont *activées* (webview, js_bridge), `permissions` = ce que le code de l'app a le droit *de faire* (window, network, fs…). À confirmer en lisant la doc `/security`.

Les 4 checks du bridge (size / origin / permission / handler-routing) couvrent les attaques classiques : flood, cross-origin, escalation, surface inattendue. Ressemble fortement au modèle Tauri ^[inferred] — à comparer concrètement.

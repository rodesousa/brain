---
type: repo-cluster
status: kept
created: 2026-05-13
---

# Facet : architecture

Modèle objet exposé par le README.

## Core concepts

- **`App`** — objet Zig minimal qui décrit l'application : nom, source WebView, hooks de cycle de vie, services natifs optionnels.
- **`Runtime`** — possède la event loop, les windows, le dispatch du bridge, les hooks d'automation, le tracing, et les services plateforme.
- **`WebViewSource`** — dit au runtime quoi charger : HTML inline, URL, ou assets frontend packagés servis depuis un origin local (`zero://app`).
- **`app.zon`** — manifeste de l'app. Déclare métadonnées, icônes, windows, assets frontend, choix de moteur web, security policy, permissions de bridge, inputs de packaging.
- **`window.zero.invoke()`** — bridge JS→Zig. Appels size-limited, origin-checked, permission-checked, routés uniquement vers des handlers enregistrés.

## Exemple `app.zon`

```zig
.{
    .id = "com.example.my-app",
    .name = "my-app",
    .display_name = "My App",
    .version = "0.1.0",
    .web_engine = "system",
    .permissions = .{ "window" },
    .capabilities = .{ "webview", "js_bridge" },
    .security = .{
        .navigation = .{
            .allowed_origins = .{ "zero://app", "http://127.0.0.1:5173" },
        },
    },
    .windows = .{
        .{ .label = "main", .title = "My App", .width = 960, .height = 640 },
    },
}
```

## CLI / dev loop

```bash
npm install -g zero-native
zero-native init my_app --frontend next
cd my_app
zig build run
```

CLI distribuée via **npm** (pas via Zig package manager) — première interaction côté dev. `zig build run` ensuite côté natif.

## My take

Trois choses notables :

1. **`app.zon` (Zig Object Notation) en config plutôt que JSON/TOML/YAML** — choix typé, vérifié à la compile du shell natif. C'est aligné avec la philosophie Zig (config = data structurée du langage, pas string parsée à runtime). Coût pour le dev web : doit comprendre la syntaxe Zig pour configurer son app.
2. **CLI distribuée via npm** alors que le natif est en Zig — pragmatisme : le dev cible est déjà dans l'écosystème JS, pas dans Zig. Réduit la friction d'onboarding (npm i + zig build, pas zig install + zig install plus).
3. **Origin local `zero://app`** explicite — pas du `file://` ni du `http://localhost`. Réduit la surface d'attaque (origin contrôlé, séparé de tout autre origin web) et permet une policy de sécurité claire (voir facet security-model).

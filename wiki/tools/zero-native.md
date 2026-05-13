---
type: entity
summary: Framework Vercel Labs (Zig + WebView) pour desktop natives ET module embarqué dans apps mobiles natives via C ABI. Engine WebView (système ou Chromium) au choix.
lifecycle: draft
created: 2026-05-13
updated: 2026-05-13
sources:
  - raw/web/zero-native-landing.md
  - raw/repos/vercel-labs-zero-native.md
tags:
  - desktop-apps
  - zig-language
  - webview-runtime
  - tiny-binaries
  - vercel-labs
---

# zero-native

Framework édité par **Vercel Labs** pour construire des applications de bureau natives avec une UI web. Stack : **Zig** côté natif + **WebView** côté UI. Positionnement quasi identique à Tauri ^[inferred] (binaires sub-Mo, WebView, langage système au lieu de runtime Node) — différences notables : choix de Zig plutôt que Rust, choix d'engine WebView exposé au dev, et mode d'embedding mobile via C ABI.

> ⚠ Page basée sur 2 sources du même éditeur (landing + README repo). Pas de test pratique, pas de comparaison réelle vs Tauri. Lifecycle reste `draft`.

## Pitch

> Build native desktop apps with web UI. Tiny binaries. Minimal memory. Instant rebuilds.

Trois promesses : taille de binaire, empreinte mémoire, vitesse de rebuild.

## Choix d'engine — système vs Chromium

Le framework expose deux modes selon le compromis souhaité :

| Mode | Trade-off |
|---|---|
| WebView système (`web_engine = "system"`) | Binaire minimal, rendu dépend de l'OS — WKWebView sur macOS, WebKitGTK sur Linux |
| Chromium embarqué via CEF (`web_engine = "chromium"`) | Pixel-perfect cross-OS, runtime plus lourd |

C'est le point le plus intéressant côté positionnement : la plupart des frameworks concurrents (Tauri, Electron) imposent un choix par défaut ; zero-native expose le levier au dev, par projet, dans `app.zon`.

## Architecture — core concepts

Cinq objets exposés par le framework :

- **`App`** — objet Zig qui décrit l'application : nom, source WebView, hooks de cycle de vie, services natifs optionnels.
- **`Runtime`** — possède l'event loop, les windows, le dispatch du bridge, les hooks d'automation, le tracing, les services plateforme.
- **`WebViewSource`** — dit au runtime quoi charger : HTML inline, URL, ou assets frontend packagés servis depuis un origin local `zero://app`.
- **`app.zon`** — manifeste de l'app, en Zig Object Notation. Déclare métadonnées, icônes, windows, assets frontend, choix d'engine, security policy, permissions, capabilities, inputs de packaging.
- **`window.zero.invoke()`** — bridge JS→Zig, avec quatre checks par appel : size-limited, origin-checked, permission-checked, routed only to registered handlers.

Modèle de surface très proche de Tauri (invoke / commands) ^[inferred].

### CLI / dev loop

```bash
npm install -g zero-native
zero-native init my_app --frontend next
cd my_app
zig build run
```

CLI distribuée via **npm** alors que le runtime est en Zig — pragmatisme côté onboarding (le dev cible est déjà dans l'écosystème JS).

### Exemple `app.zon`

```zig
.{
    .id = "com.example.my-app",
    .name = "my-app",
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

## Modèle de sécurité

> The WebView is treated as untrusted by default. Native commands, permissions, navigation, external links, and window APIs are opt-in and policy controlled.

Posture **deny-by-default** assumée — l'inverse d'Electron où tout est accessible côté renderer et où il faut désactiver explicitement pour durcir.

Surface couverte par la policy :

- **Native commands** — opt-in via enregistrement explicite côté Zig.
- **Permissions** — déclarées dans `app.zon` (ex. `"window"`).
- **Capabilities** — séparées des permissions (ex. `"webview"`, `"js_bridge"`).
- **Navigation** — `allowed_origins` whitelist explicite, y compris le dev server local.
- **External links / Window APIs** — opt-in (non détaillé dans le README).

Séparation `permissions` vs `capabilities` non documentée dans le README. Hypothèse ^[inferred] : `capabilities` = quelles surfaces du runtime sont *activées*, `permissions` = ce que le code de l'app a le droit *de faire*. À confirmer dans la doc `/security`.

## Mobile embedding — C ABI

Surprise du README, absente de la landing : zero-native **n'est pas que desktop**. Le repo contient `examples/ios` et `examples/android` qui montrent une app native hôte linker la bibliothèque statique **`libzero-native.a`** via son C ABI.

Asymétrie révélatrice du positionnement réel :

- Sur **desktop**, zero-native est *le shell* de l'app — il porte la fenêtre, le runtime, le bridge.
- Sur **mobile**, zero-native est *un composant linké* dans une app native existante (Swift/Kotlin app qui linke `libzero-native.a`).

Implication ^[inferred] : la cible n'est pas le dev qui veut shipper une app standalone cross-platform, c'est l'équipe qui a déjà une app mobile native et veut y embarquer une vue web bridge-able tout en réutilisant le même code Zig+web côté desktop. Différenciation vs Tauri Mobile (qui vise plutôt du standalone).

C ABI exposée — intégrable en théorie depuis n'importe quel langage qui parle C, pas réservé à Swift/Kotlin ^[inferred].

## Status

Pre-release. Desktop couvre **macOS 11+, Linux, et Windows build paths** (le README parle de "build paths" sur Windows — pas encore complet). Chromium/CEF distribué comme runtime plateforme-spécifique.

## My take

Trois angles vraiment originaux, dans l'ordre d'importance :

1. **Choix d'engine WebView exposé au dev** (système ↔ Chromium embarqué, par projet, dans `app.zon`). Tauri force le système, Electron force Chromium. zero-native est la première proposition que je vois qui te dit "fais le call par projet". Résout le vrai dilemme du desktop web-based : binaire petit *vs.* rendu cohérent.
2. **Mobile via C ABI, pas via shell standalone**. Positionnement complètement différent de Tauri Mobile / Capacitor / RN. Vise des équipes mobile-native qui veulent embarquer du web, pas l'inverse.
3. **`app.zon` en config typée Zig + posture deny-by-default**. Cohérent. Coût pour le dev web : doit comprendre la syntaxe Zig de base. Bénéfice : la config est vérifiée à la compile du shell natif, pas à runtime.

Ce qui me rend prudent : "Vercel Labs" = signal d'incubation, pas de produit prod (cf. README "pre-release"). Windows annoncé en "build paths" pas complet. Écosystème Zig encore jeune (le langage lui-même pas 1.0). Pas pertinent pour shipper un produit aujourd'hui — pertinent pour expérimenter une appli locale ou tester l'angle "module embarqué dans une app mobile native".

Pas de connexion directe avec les autres entités du vault (qui sont sur le terrain agent/AI) — zero-native est le premier élément d'un domaine "frameworks/desktop+mobile". Note pour plus tard : si je crée d'autres pages dans ce domaine (Tauri, Wails, Electron…), une page `comparisons/desktop-web-frameworks.md` aurait du sens, et le point de comparaison à creuser en priorité serait la dimension mobile-embedding.

## Sources

- `raw/web/zero-native-landing.md` — landing page snapshotée le 2026-05-13. Marketing.
- `raw/repos/vercel-labs-zero-native.md` — README repo officiel snapshoté le 2026-05-13. Source primaire, technique.

Facets kept (clusters) :
- `raw/clusters/repos/vercel-labs-zero-native/cluster-02-architecture.md`
- `raw/clusters/repos/vercel-labs-zero-native/cluster-03-security-model.md`
- `raw/clusters/repos/vercel-labs-zero-native/cluster-04-mobile-embedding.md`

Facets écartées : `cluster-01-purpose` (doublon landing), `cluster-05-examples-ecosystem` (starters génériques sans signal).

À ingérer ensuite si besoin de plus de profondeur : docs `/security`, `/bridge`, `/app-model`, `/web-engines`, `/packaging` sur zero-native.dev.

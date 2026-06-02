---
type: entity
summary: Framework Rust+WebView stable pour binaires desktop/mobile tiny via `tao`/`wry`. Bundler intégré (NSIS/WiX/dmg/AppImage), self-updater, custom protocol sans serveur HTTP local.
lifecycle: reviewed
created: 2026-05-13
updated: 2026-05-13
sources:
  - raw/repos/tauri-apps-tauri.md
tags:
  - desktop-apps
  - rust-language
  - webview-runtime
  - tiny-binaries
  - cross-platform-mobile
---

# Tauri

Framework **stable** (badge officiel) du Commons Conservancy pour construire des applications desktop et mobile avec un backend Rust et un frontend HTML/JS/CSS framework-agnostic. Le mètre-étalon du segment "WebView natif + langage système".

## Pitch

> Tauri is a framework for building tiny, blazingly fast binaries for all major desktop platforms. Developers can integrate any front-end framework that compiles to HTML, JS and CSS for building their user interface. The backend of the application is a rust-sourced binary with an API that the front-end can interact with.

Pitch volontairement mince : Tauri se contente de dire ce que la lib fait. Pas de marketing.

## Architecture — `tao` + `wry` + Rust backend

Trois composants explicitement nommés dans le README :

| Composant | Rôle |
|---|---|
| **`tao`** ([docs.rs/tao](https://docs.rs/tao)) | Window handling library multi-OS (macOS, Windows, Linux, Android, iOS) |
| **`wry`** ([github.com/tauri-apps/wry](https://github.com/tauri-apps/wry)) | Interface unifiée vers le WebView système |
| **Backend Rust** | Le `rust-sourced binary` qui expose une API au frontend |

`wry` unifie sous une seule abstraction Rust :

- **WKWebView** sur macOS et iOS
- **WebView2** sur Windows
- **WebKitGTK** sur Linux
- **Android System WebView** sur Android

**Pas de mode Chromium embarqué** mentionné dans le README. Tauri canonise le WebView système comme *le* mode par défaut. Si tu veux du Chromium pixel-perfect cross-OS, Tauri n'est pas l'outil — il faut zero-native en mode Chromium ou Electron.

`tao` et `wry` sont publiés comme libs autonomes — consommables sans tout l'écosystème Tauri.

## Bundler & distribution — différenciateur fort

Bundler intégré au framework, formats listés explicitement par le README :

- **macOS** : `.app`, `.dmg`
- **Linux** : `.deb`, `.rpm`, `.AppImage`
- **Windows** : `.exe` (via **NSIS**), `.msi` (via **WiX**)

Plus :

- **Self-updater** intégré (desktop only).
- **System tray icons**, **native notifications**.
- **GitHub Action** dédiée pour CI/release multi-plateforme.
- **Extension VS Code** officielle.

C'est la chaîne de distribution la plus complète du segment. NSIS + WiX intégrés signifient qu'on peut signer et packager un installer Windows depuis le projet sans aller chercher Inno Setup / Advanced Installer / etc.

## Plateformes supportées

| Plateforme | Versions |
|---|---|
| Windows | 7+ |
| macOS | 10.15+ |
| Linux | webkit2gtk 4.0 (Tauri v1, ex. Ubuntu 18.04) ; webkit2gtk 4.1 (Tauri v2, ex. Ubuntu 22.04) |
| iOS / iPadOS | 9+ |
| Android | 7+ (actuellement 8+) |

Sur mobile, Tauri est **le shell de l'app** (app standalone livrée via les stores) — pas un module embarqué. Différence philosophique majeure avec [[zero-native]] sur le mobile (cf. *My take*).

Le mention `webkit2gtk 4.0 → 4.1` est le seul signal v1/v2 dans le README. Implication : Tauri a une notion de version majeure avec breaking changes sur les deps système. Les vieilles distros Linux sont coincées en v1.

## Modèle de sécurité — custom WebView protocol

Phrase parenthétique du README qui mérite d'être soulignée :

> Native WebView Protocol (tauri doesn't create a localhost http(s) server to serve the WebView contents)

Tauri sert les assets frontend via un **custom protocol intégré au WebView**, pas via un serveur HTTP local sur `127.0.0.1:<port>`. Conséquence : pas d'écoute réseau locale, pas de surface d'attaque visible depuis d'autres processus de la machine.

Le README ne détaille pas le modèle de permissions / capabilities, contrairement à zero-native qui expose sa policy `app.zon` (navigation/permissions/capabilities). Tauri a ce système — ARCHITECTURE.md sur la branche `dev` le décrit ^[inferred] — juste pas dans le README.

## My take

Tauri est **le standard de fait du segment** et la principale référence à laquelle [[zero-native]] s'oppose. La comparaison directe vaut le coup :

| Axe | Tauri | zero-native |
|---|---|---|
| Langage natif | Rust | Zig |
| Engine WebView | Système uniquement (`wry`) | Choix exposé : système OU Chromium embarqué (CEF) |
| Modèle mobile | App standalone (Tauri = shell) | Module linké (`libzero-native.a`) dans app native hôte |
| Maturité | Stable, prod-ready, Commons Conservancy | Pre-release, Vercel Labs, Windows en build paths |
| Bundler | Intégré exhaustif (NSIS/WiX/dmg/deb/rpm/AppImage) | Packaging mentionné, formats non détaillés |
| Pas de localhost HTTP | Custom protocol | Custom protocol (`zero://app`) |

**Mes lectures du contraste :**

1. **Choix d'engine WebView** — c'est l'unique vraie carte de zero-native vs Tauri. Tauri assume le WebView système ; si la cohérence pixel-perfect cross-OS est critique, Tauri n'est pas le bon outil. zero-native te laisse la porte ouverte.
2. **Modèle mobile** — c'est l'autre carte de zero-native. Tauri Mobile suppose que tu veux remplacer ta stack mobile native. zero-native suppose que tu veux y greffer une vue web. Deux cas d'usage disjoints.
3. **Maturité écosystème** — sur tout le reste, Tauri gagne par défaut. Bundler exhaustif, GitHub Action officielle, VS Code extension, plateformes prod-ready depuis des années, fondation porteuse. zero-native devra rattraper plusieurs années de feedback CI/signing/notarization pour rivaliser.
4. **Le custom protocol au lieu de serveur HTTP** — point de convergence des deux frameworks. C'est l'approche canonique moderne (vs Electron historique). Confirme que c'est la bonne pratique de fond.

**Quand je choisirais quoi** :

- App standalone cross-OS à shipper ce trimestre : Tauri, sans hésitation.
- Prototype où je veux explorer la dimension "embedded dans une app native existante" : zero-native (Tauri ne le permet pas de la même façon).
- Besoin de Chromium pixel-perfect : zero-native (mode Chromium) ou Electron.
- Apprentissage / curiosité Zig : zero-native pour le sport.

Le segment a maintenant trois niveaux dans le vault :
- [[zero-native]] (le challenger, Vercel Labs, Zig, choix d'engine + mobile embedded).
- Tauri (le titulaire, Rust, prod-ready).
- *À ajouter ensuite* : Wails (Go + WebView), Electron (pour situer le baseline historique), Dioxus (Rust mais full-Rust UI, pas WebView).

Une page `wiki/comparisons/desktop-web-frameworks.md` aurait du sens dès qu'on aura ≥3 frameworks dans le vault — on y est presque.

## Sources

- `raw/repos/tauri-apps-tauri.md` — README repo officiel snapshoté le 2026-05-13. Source primaire unique, courte (le projet a sa propre doc à `tauri.app`).

Facets kept (5) :
- `raw/clusters/repos/tauri-apps-tauri/cluster-01-purpose-positioning.md`
- `raw/clusters/repos/tauri-apps-tauri/cluster-02-architecture-stack.md`
- `raw/clusters/repos/tauri-apps-tauri/cluster-03-bundler-distribution.md`
- `raw/clusters/repos/tauri-apps-tauri/cluster-04-platforms-coverage.md`
- `raw/clusters/repos/tauri-apps-tauri/cluster-05-security-webview-protocol.md`

Facet écartée : `cluster-06-governance-licensing` (organisation/branding, hors sujet).

À ingérer ensuite si besoin de profondeur : `ARCHITECTURE.md` (branche dev), doc tauri.app/v2, modèle capabilities Tauri v2.

## Related

- [[zero-native]] — challenger direct sur le segment WebView+langage-système. Différences clés : Zig au lieu de Rust, choix d'engine WebView exposé (système OU Chromium), modèle mobile *embedded* vs Tauri Mobile *standalone*. Voir le tableau comparatif dans *My take*.

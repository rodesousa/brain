---
type: repo-cluster
status: kept
created: 2026-05-13
---

# Facet : architecture-stack

## Trois composants explicitement nommés

Le README expose la stack de façon directe — pas de mystère côté impl.

| Composant | Rôle |
|---|---|
| **`tao`** (docs.rs/tao) | Window handling library multi-OS : macOS, Windows, Linux, Android, iOS |
| **`wry`** (github.com/tauri-apps/wry) | Interface unifiée vers le WebView système |
| **Backend Rust** | Le "rust-sourced binary" qui expose une API au frontend |

## Ce que `wry` unifie

WebView système par plateforme (un seul) :

- **WKWebView** sur macOS et iOS
- **WebView2** sur Windows
- **WebKitGTK** sur Linux
- **Android System WebView** sur Android

**Pas de mode "Chromium embarqué"** mentionné dans le README. Tauri canonise le choix du WebView système comme *le* mode par défaut. Si tu veux du Chromium pixel-perfect cross-OS, c'est pas Tauri.

## Documentation pointer

Le README pointe vers `ARCHITECTURE.md` sur la branche `dev` pour les détails (`github.com/tauri-apps/tauri/blob/dev/ARCHITECTURE.md`). À ingérer si on veut creuser la couche IPC, le modèle de capability, etc.

## My take

La décomposition en `tao` + `wry` séparés est intéressante côté écosystème : ces deux libs peuvent être consommées sans Tauri. `wry` en particulier est une lib autonome qui unifie les WebViews systèmes en une seule abstraction Rust — utile pour des projets qui ne veulent pas tout l'écosystème Tauri (bundler, API IPC…).

**Différence structurelle vs `zero-native`** : Tauri force le mode WebView système. zero-native expose le choix système↔Chromium au dev. C'est *exactement* le levier sur lequel zero-native essaie de se différencier de Tauri. Trade-off à clarifier :
- WebView système (Tauri, zero-native option par défaut) → binaire minimal, mais rendu et features dépendent de l'OS hôte (WebKit ≠ Blink, Android WebView fragmenté…).
- Chromium embarqué (zero-native option, Electron par défaut) → cohérence pixel-perfect, mais binaire plus gros.

Si la cohérence cross-OS du rendu est critique pour le produit, Tauri n'est pas le bon outil ; il faut soit zero-native en mode Chromium, soit Electron.

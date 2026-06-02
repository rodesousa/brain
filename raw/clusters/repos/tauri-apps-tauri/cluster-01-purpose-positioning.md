---
type: repo-cluster
status: kept
created: 2026-05-13
---

# Facet : purpose-positioning

## Pitch (README intro)

> Tauri is a framework for building tiny, blazingly fast binaries for all major desktop platforms. Developers can integrate any front-end framework that compiles to HTML, JS and CSS for building their user interface. The backend of the application is a rust-sourced binary with an API that the front-end can interact with.

## Promesses clés

- **Tiny binaries** — même mot d'ordre que la concurrence WebView native (zero-native, Wails…).
- **Backend en Rust** — choix de langage assumé, levier de sécurité mémoire et perf.
- **Frontend framework-agnostic** — accepte n'importe quel framework qui compile vers HTML/JS/CSS.
- **API native exposée au frontend** — modèle invoke/commands (standard de l'écosystème).

## Statut

- Badge `status: stable` (vs `pre-release` pour zero-native ou `pre-1.0` pour beaucoup d'autres).
- Licence dual MIT / Apache-2.0.
- Programme du **Commons Conservancy**.

## My take

Tauri est le mètre-étalon "WebView natif + langage système" du marché. Pitch ultra-mince mais ce n'est pas du marketing — c'est ce que la lib fait. Le fait que ce soit stable (badge officiel) et porté par une fondation ouverte (Commons Conservancy) change le profil de risque vs un Vercel Labs ou un projet solo.

Le "frontend framework-agnostic" est une formulation honnête : Tauri ne livre pas de starter par framework comme zero-native (next/react/svelte/vue) ; il se contente du protocole et laisse l'outillage à `create-tauri-app`.

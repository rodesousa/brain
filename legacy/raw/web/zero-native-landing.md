---
source-type: web
url: https://zero-native.dev/
fetched: 2026-05-13
---

# zero-native — landing page

Snapshot du contenu utile de la page d'accueil de https://zero-native.dev/ au 2026-05-13.

## Pitch

> Build native desktop apps with web UI. Tiny binaries. Minimal memory. Instant rebuilds.

Framework permettant de construire des applications de bureau natives en combinant **Zig** (langage de programmation) et **WebView**. Édité par **Vercel Labs**.

## Promesses

- **Binaires sub-mégaoctet** — pas de runtime embarqué par défaut.
- **Empreinte mémoire minimale** comparée aux frameworks traditionnels (Electron etc., non nommés mais implicites).
- **Compilations ultra-rapides** grâce à Zig.
- **Hot-reload** côté frontend + rebuilds binaires rapides.

## Choix d'engine WebView

Deux modes proposés selon le besoin :

- **WebView système** — applications très légères, dépend de la stack OS.
- **Chromium via CEF** — pour cohérence visuelle pixel-perfect multi-plateforme.

## Intégration native

Zig permet l'appel **direct** de bibliothèques C, sans couche de binding intermédiaire. Cas cités :

- SDKs natifs
- Codecs audio
- Runtimes ML

## Architecture

- Couche native minimaliste en Zig.
- Interface WebView familière aux développeurs web.
- Système de pont (`bridge`) pour appeler des commandes natives depuis JavaScript.

## Fonctionnalités

- CLI pour initialiser et gérer les projets.
- Multi-plateforme : macOS, Linux ; Windows en développement au moment du snapshot.
- Hot-reload frontend + rebuilds rapides.
- Primitives intégrées : dialogs, system tray, sécurité.
- Auto-update des applications.
- Packaging + signature de code.

## À vérifier ultérieurement

- Modèle de licence (non vu sur la landing).
- Statut Windows précis.
- Maturité réelle vs marketing (Vercel Labs = incubation, pas produit fini par défaut).
- Comparaison concrète vs Tauri (positionnement quasi identique : binaires petits, WebView, langage système au lieu de runtime Node).

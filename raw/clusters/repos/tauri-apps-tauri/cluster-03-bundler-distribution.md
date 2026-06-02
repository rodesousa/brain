---
type: repo-cluster
status: kept
created: 2026-05-13
---

# Facet : bundler-distribution

## Bundler intégré — formats supportés

Le README liste explicitement :

- macOS : `.app`, `.dmg`
- Linux : `.deb`, `.rpm`, `.AppImage`
- Windows : `.exe` via **NSIS**, `.msi` via **WiX**

Tous packagés par le bundler natif Tauri — pas besoin de chaîne d'outils externe à plugger.

## Self-updater (desktop only)

Self-updater livré dans le framework, pas un add-on. Limité au desktop (mobile passe par les stores).

## Autres primitives de distribution / dev

- **System tray icons** — primitive native.
- **Native notifications** — primitive native.
- **GitHub Action** dédiée pour CI/release streamliné.
- **Extension VS Code** officielle.

## My take

C'est *le* différenciateur côté maturité produit. Tauri n'est pas qu'un framework de runtime, c'est aussi une chaîne de distribution. NSIS + WiX intégrés au bundler signifient qu'on peut signer et packager un installer Windows depuis le projet Tauri sans aller chercher Inno Setup / Advanced Installer / etc. à la main.

Comparaison vs **zero-native** (cf. cluster `mobile-embedding`) : la landing zero-native mentionne "Packaging + signature de code" mais sans détailler les formats supportés. Tauri ici est explicite et exhaustif. Probablement le point où l'écart de maturité est le plus visible — Tauri tourne en prod depuis des années, zero-native est pre-release.

GitHub Action officielle pour CI = signal de maturité fort. C'est un truc qui demande des années de feedback pour bien faire (signing, notarization macOS, code-sign Windows, génération multi-platform en parallèle…).

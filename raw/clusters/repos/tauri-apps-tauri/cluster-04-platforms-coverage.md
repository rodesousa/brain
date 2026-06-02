---
type: repo-cluster
status: kept
created: 2026-05-13
---

# Facet : platforms-coverage

## Table officielle (README)

| Platform | Versions |
|---|---|
| Windows | 7 and above |
| macOS | 10.15 and above |
| Linux | webkit2gtk 4.0 (Tauri v1, ex. Ubuntu 18.04). webkit2gtk 4.1 (Tauri v2, ex. Ubuntu 22.04) |
| iOS/iPadOS | 9 and above |
| Android | 7 and above (currently 8 and above) |

## Mobile = standalone apps

Pas explicitement dit dans le README mais c'est la lecture par défaut : Tauri sur iOS/Android est *le* shell de l'app, pas un module embarqué. `tao` gère les windows mobiles, `wry` gère le WebView mobile, et l'app est livrée comme app standalone via les stores.

Contraste fort avec zero-native qui sur mobile est *une lib statique linkée par une app native hôte* (cf. `cluster-04-mobile-embedding` zero-native).

## Distinction v1 / v2

Le README mentionne webkit2gtk **4.0 pour v1**, **4.1 pour v2** côté Linux. C'est le seul endroit où la dichotomie v1/v2 est rendue visible — implication : Tauri a une notion de version majeure avec des breaking changes sur les dépendances système. Tauri v2 est le track actif (`v2.tauri.app` pour prerequisites).

## My take

Couverture multi-plateforme **complète et production-ready** — c'est l'autre indicateur de maturité majeur. Windows 7+, macOS 10.15+, iOS 9+, Android 7+ → on parle d'une longue traîne de devices supportés. Aucun autre framework "Rust + WebView" n'a ce niveau de couverture (ex. Dioxus encore en alpha sur mobile, zero-native en pre-release).

Le positionnement mobile **standalone** plutôt que **embedded module** est le vrai split philosophique vs zero-native :
- Tauri Mobile vise les équipes qui veulent shipper une app cross-OS via une codebase unique.
- zero-native mobile vise les équipes qui ont déjà une app native et veulent y greffer une vue web bridge-able.

Ce ne sont pas les mêmes cas d'usage. Un dev qui se pose la question "Tauri ou zero-native" doit d'abord se demander "est-ce que je veux remplacer ma stack mobile native, ou m'y intégrer ?".

Side note : `webkit2gtk 4.0 → 4.1` pour Linux indique que les vieilles distros (Ubuntu 18.04) sont coincées en Tauri v1. À considérer pour des apps grand public Linux où l'utilisateur lambda peut être sur une distro plus ancienne.

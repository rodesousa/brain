---
type: repo-cluster
status: kept
created: 2026-05-13
---

# Facet : mobile-embedding

Surprise du README : zero-native **n'est pas que desktop**. Le repo contient des exemples d'embedding mobile.

## Ce que dit le README

> Mobile embedding examples are available too:
>
> - `examples/ios`
> - `examples/android`
>
> These show how an iOS or Android host app links the zero-native C ABI from `libzero-native.a`.

## Modèle d'intégration

- Bibliothèque statique C : **`libzero-native.a`**.
- L'app mobile hôte (iOS/Android) *link* cette lib, elle n'est pas l'app entière.
- Cas d'usage implicite ^[inferred] : embarquer un module fait avec zero-native dans une app native existante, pas remplacer l'app.

## My take

Positionnement important qui n'apparaît nulle part sur la landing :

- Sur **desktop**, zero-native est *le shell* de l'app — il porte la fenêtre, le runtime, le bridge.
- Sur **mobile**, zero-native est *un composant linké* dans une app native existante (Swift/Kotlin app qui linke `libzero-native.a`).

C'est une asymétrie révélatrice du domaine cible réel : ^[inferred] des équipes qui ont déjà des apps mobiles natives mais veulent ajouter une vue web bridge-able sans embarquer Electron Mobile / CapacitorJS / React Native, et qui peuvent réutiliser le même code Zig+web côté desktop comme "app standalone".

Ça change le positionnement vs Tauri : Tauri Mobile vise des apps standalone (Tauri *est* l'app). zero-native mobile vise des *modules embarqués*. À recouper avec la doc — la landing ne mentionne pas du tout cette dimension.

C ABI exposée — implication : intégrable en théorie depuis n'importe quel langage qui parle C (pas réservé à Swift/Kotlin), même côté serveur ou dans un binding Rust ^[inferred].

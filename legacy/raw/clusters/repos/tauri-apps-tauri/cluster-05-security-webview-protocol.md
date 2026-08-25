---
type: repo-cluster
status: kept
created: 2026-05-13
---

# Facet : security-webview-protocol

## Citation directe

Dans la liste des features du README :

> Native WebView Protocol (tauri doesn't create a localhost http(s) server to serve the WebView contents)

C'est une phrase entre parenthèses mais c'est un détail de sécurité majeur.

## Ce que ça veut dire

La plupart des wrappers "WebView + native bridge" servent les assets frontend via un serveur HTTP local sur `127.0.0.1:<port>`. Conséquences :

- Le serveur écoute sur une interface locale — théoriquement accessible à d'autres processus de la même machine.
- Le port est binding-dépendant et peut conflicter.
- Toute requête loopback (y compris depuis un autre browser ou un script tiers) peut le toucher.

Tauri utilise un **custom WebView protocol** (probablement `tauri://`, `asset://` ou équivalent ^[inferred]) qui sert les assets *à l'intérieur* du WebView via les hooks de l'API plateforme. Pas d'écoute réseau locale, pas de port à scanner.

## Lien avec zero-native

zero-native fait la même chose — origin local `zero://app` (cf. cluster architecture). Les deux sont d'accord sur ce point. C'est devenu le standard de fait pour les frameworks WebView-natifs modernes (vs Electron historique qui lui *fait* tourner un serveur).

## My take

Détail apparemment mineur, conséquence sécurité majeure : la surface d'attaque réseau locale est nulle. Un attaquant ne peut pas viser ton app depuis un autre process avec une requête `http://localhost:1420`. Une appli Electron-style mal configurée peut être probed depuis une page web qui fait fetch `localhost`, ou depuis un malware qui scan les ports.

Le fait que **Tauri et zero-native convergent sur ce point** (custom protocol au lieu de serveur HTTP) confirme que c'est l'approche canonique pour qui se soucie sérieusement de sécurité. C'est aussi probablement la principale critique de fond contre Electron — Electron *peut* être configuré sans server HTTP local (via `file://` ou custom protocol), mais le défaut historique a été problématique.

À noter : le README Tauri ne développe pas le modèle de permissions / capabilities, contrairement à zero-native qui détaille sa policy `app.zon` avec navigation/permissions/capabilities. Tauri a ce système (ARCHITECTURE.md sur la branche dev le décrit ^[inferred]), juste pas dans le README.

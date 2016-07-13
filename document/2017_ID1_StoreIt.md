StoreIt - Stockage dans le cloud décentralisé
=============================================


Titre | Date | Sujet
------|----- | -----
2017_ID1_StoreIt.pdf | 1/5/2016 | Documentation d'installation

Tableau des révisions

Date | Auteur | Section(s) | commentaire
------|----- | -----
1/5/2016 | Groupe StoreIt | Toutes | Rédaction initiale

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [StoreIt - Stockage dans le cloud décentralisé](#storeit---stockage-dans-le-cloud-d%C3%A9centralis%C3%A9)
- [Le serveur](#le-serveur)
      - [Prérequis:](#pr%C3%A9requis)
      - [Installation du serveur](#installation-du-serveur)
      - [Lancement du serveur](#lancement-du-serveur)
- [Appli iOS: Installation de l'environnement](#appli-ios-installation-de-lenvironnement)
- [Installation de l'appli Android](#installation-de-lappli-android)
- [Web-App: Installation](#web-app-installation)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


Le serveur
==========

Le serveur StoreIt s'utilise en ligne de commande et ne fonctionne que sur les systèmes UNIX.

#### Prérequis:

* git (https://git-scm.com)
* node-js (https://nodejs.com)
* mysql (https://mysql.com)

#### Installation du serveur

```bash
$> git clone https://github.com/Sevauk/storeit
$> cd storeit/src/server
$> npm install # for local installation/development
$> npm install -g # for global installation
```
#### Lancement du serveur

```bash
$> node main.js # local installation
$> storeit-srv # global installation
```

### Appli iOS: Installation de l'environnement

* Posséder un Mac afin d’installer la dernière version Xcode
* Installer Cocoapods [Tutoriel sur le Site de Cocoapods ici](https://cocoapods.org)
* Cloner le dépôt git
* Depuis le dépôt, installer les dépendances `pod install`
* Ouvrir le projet dans Xcode `open StoreIt.xcworkspace`
* Compilier le projet avant de lancer l'émulateur !

## Installation de l'appli Android ##

L'application StoreIt sera disponible sur le Google Play Store. Tout utilisateur ayant un compte google et un appareil compatible pourra installer l'application via le Play Store.


Web-App: Installation
=====================

Installer Node.js version 5 ou plus et npm version 3 ou plus.

Une fois le repository cloné, lancer la commande suivante depuis `src/web-app`:
```
npm install
```

Vous pouvez lancer l'application avec:
```
npm start
```

Vous pouvez tester l'application avec:
```
npm test
```

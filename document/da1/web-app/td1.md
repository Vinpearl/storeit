Documentation Web-App: Aspects techniques
=========================================

Technologies:
-------------

* Langage: JavaScript (ES2015 + Tc39 stage-3)
* Framework: AngularJS 1.5+
* Templates: Jade
* Stylesheets: PostCss
* Gestionnaire de dépendances: JSPM
* Automatiseur de tâches: Gulp
* Testing: Karma + Mocha + Chai + Istanbul

Structure:
----------

Les sources de l'application sont organisées en `Modules` Angular.
L'application contient 2 types de modules:

1. **Components**: Route + Controlleur + Vue (Template et Style). Un component est intimement lié à ça vue, mais peut être composé à partir de component plus petits.

2. **Core**: Contient de la logique réutilisable (principalement des services et models)

Example de component:
```
home
|  home.js
|  home.jade
|  home.css
|
|__sidebar
   | sidebar.js
   | sidebar.jade
   | sidebar.css
```

Développement:
--------------
Suivre les instructions d'installation, puis utilisez:

```
npm run dev
```

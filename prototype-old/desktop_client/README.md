Storeit Desktop Client
======================

Table des matières
------------------
1. [Description](#description)
2. [Prérequis](#prérequis)
3. [Installation](#installation)
3. [Liens utiles](#liens-utiles)

Description
------------
TODO

Prérequis
------------
* node.js & npm
* git

Configurer npm
---------------
Il est important que le dossier d'installation de npm soit un dossier sur lequel l'utilisateur à les droits en écriture. Cela a fin d'éviter de lancer npm avec des droits privilégiés (souvent npm vous engueulera si vous le lancez avec *sudo*).
Bref, pour connaître le dossier d'installation courant :

    npm config get prefix

Sous Windows, la configuartion par défaut est suffisante. En revanche sous Linux/OS X, le chemin par défaut est */usr/local*. Pour le changer utilisez : 

    npm config set prefix <new_path>

Sans oublier de modifier votre PATH. Par exemple: vous souhaiter utiliser le dossier *~/.npm*. Il suffit d'ajouter cette ligne à votre *.bashrc* :

    PATH=$PATH:$HOME/.npm/bin

Notez le */bin* (nécessaire sous Linux/OS X).

Installation
------------
1. Clonez le dépôt et configurez npm
2. Depuis un terminal, rendez-vous dans le dossier "*desktop_client*"
3. Lancez l'installation :


    npm link

4. Pour vérifier que l'installation c'est bien effectuée, dans votre terminal tapez :


    storeit_client

5. Si la commande est introuvable, le problème vient de votre PATH. Encore une fois :


    npm config get prefix 

Vérifiez que ce chemin est bien présent dans le PATH (ajouter */bin* sous Linux/OS X)

Liens utiles
------------
* [API Http](http://78.192.138.139/swagger-ui/dist/)

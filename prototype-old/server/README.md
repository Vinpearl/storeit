Bonjour. Voici les instructions pour lancer le serveur.

1. De quoi avez vous besoin ?
=============================

- python3
- module python psycopg2 (sudo pip3 install psycopg2)
- module python colorlog (sudo pip3 install colorlog)
- psql (postgre sql)

2. Comment configurer le serveur pour la première fois ?
========================================================

Il faut créer la base de donnée. Inutile si vous passez par le script launch_envir.sh.

```bash
  cd database
  ./init_database.sh
```

Vous allez peut être gélérer pour faire marcher postgres. Il faut avoir un utilisateur admin je crois.


3. Comment utiliser le serveur ?
================================

Deux méthodes :

3. 1. Lancer le serveur à la main
---------------------------------

N'oubliez pas de lancer la base de donnée postgre avant de lancer le serveur. 

Il faut juste le lancer :

```bash
./main.py 
```

N'oubliez pas de configurer votre routeur si vous voulez vous y connecter depuis l'extérieur.

L'output devrait être:

```python
  INFO     Serving on ('127.0.0.1', 7641)
```

3. 2. Lancer le serveur via le script de test
---------------------------------------------

Il y a un script appelé launch_envir.sh qui facilite le lancement du serveur et éventuellement connecte automatiquement des clients de test.
La configuration se fait via simulation.sh. Vous devez appeler des fonctions dans ce script, qui sera appelé par launch_envir.sh. Par exemple :

Contenu de simulation.sh :

```bash
run_client cli1
run_client cli2
sleep 1
kill_client cli1
sleep 1
run_client cli1
```

Vous n'avez qu'à faire ./launch_envir.sh pour tester votre simulation. Vous avez besoin de tmux pour que ça marche (dispo que sous unix).

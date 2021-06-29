Ce script permets une copie de sauvegarde des fichiers contenus dans un répertoire local vers un serveur distant dans un but de sauvegarde.

Auteur : Jérémie Voïta, étudiant à Openclassrooms

Le script fonctionne avec les versions 3.8+ de Python et a été testé sur Windows uniquement.
il ne copie que les fichiers, les répertoires et leur sous-dossiers placés dans le répertoire défini comme source entraîneront une erreur et un arrêt du script.


les modules suivants doivent être installés sur la machine source avec pip install:
-paramiko
-pysftp


ni Python ni modules ne sont nécessaires sur la machine de destination.
Aucun droit admin n'est nécessaire au bon fonctionnement du script.
Le fichier de configuration doit être présent sur la machine source, dans le même répertoire que le script principal.

le script utilise deux fichiers :
backup_main.py : le script en lui même
configuration.py : fichier permettant de renseigner les éléments et identifiants propres à chacun.
Aucune modification n'est nécessaire sur le script principal afin d'éviter toute fausse manipulation.

une connexion SSH est établie avec un serveur distant veuillez renseigner les information de connexion et vérifier que le serveur distant est accessible et accepte un login SSH.

La copie des éléments est réalisée comme suit:

->les fichiers manquants sont copiés, sauf exclusion(s) selon une liste définie par l'utilisateur

->/!\ en cas de nouvelle version d'un fichier sur la source, les fichiers plus anciens sur le répertoire distant sont écrasés directement sans message d'avertissement /!\

Il s'agit de mon premier script en Python, il a été testé et est fonctionnel. Toutefois, si vous avez des propositions de modifications, optimisations, adaptations pour les autres plateformes, je serai très heureux de pouvoir les implanter et faire évoluer ce projet!

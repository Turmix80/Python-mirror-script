#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Le script fonctionnne avec les versions 3.8+ de Python et a été testé sur Windows uniquement.

les modules suivants doivent être installés sur la machine source avec pip install:
-paramiko
-pysftp

Ce fichier contient les éléments paramétrables selon l'utilisation de chacun.

La copie des éléments est réalisée comme suit:

->les fichiers manquants sont copiés(sauf exclusion(s))

->/!\ en cas de nouvelle version d'un fichier sur la source
les fichiers plus anciens sur le répertoire distant
sont écrasés directement sans message d'erreur /!\

une connexion SSH est établie avec un serveur distant
veuillez renseigner les information de connexion et
vérifier que le serveur distant est accessible et accepte un login SSH.
Une connexion root n'est pas nécessaire au bon fonctionnement du script.

Ce fichier de configuration doit être présent sur la machine source, dans le même répertoire que le script principal.
'''

#renseigner ici la terminaison des fichiers à exclure, ou un élément contenu dans son nom (date, élément..)
# séparez les éléments par une virgule si il y en à plusieurs
_EXCLUSION = '.ini' #('.ini', '.txt')

#chemin du répertoire source sur la machine locale /!\ sur Windows, attention aux séparateurs
# mettre \\ à la place de /
_SOURCE = ""

#chemin du répertoire de destination sur la machine distante /!\ sur Windows, attention aux séparateurs
# mettre \\ à la place de /
_DEST = ""

#nom d'utilisateur SSH sur la machine distante
_USR = ''

#adresse de la machine distante
_RMTHOST =''

#mot de passe de connexion SSH à la machine distante
_DESTPASS=''

#port de connexion SSH, modifier en cas de port personnalisé
_PORT=22



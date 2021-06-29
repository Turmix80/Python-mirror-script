#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import paramiko
import pysftp
import shutil
import socket
import sys
from pprint import pprint

# importation des variables globales
from configuration import _USR, _RMTHOST, _DESTPASS, _PORT, _SOURCE, _DEST, _EXCLUSION

# Définition de la variable globale nécessaire à la création du dussier temporaire de copie
_SOURCE_TEMP = (_SOURCE + "temp")

# effacer dossier temporaire en cas d'erreur du script précédent
if os.path.exists(_SOURCE_TEMP):
    shutil.rmtree(_SOURCE_TEMP)

# énoncé du script
print("\ncopie miroir du dossier: " + _SOURCE + "  vers:" + _RMTHOST + ":" + _DEST)

print("\n**********************************************************************************************************\n")

# ### VERIFICATIONS AVANT DEBUT DU SCRIPT ###

# vérifier présence du fichier de configuration

try:
    with open('configuration.py'):
        pass
        print("le fichier de configuration est présent et valide")
except IOError:
    sys.exit("Erreur: le fichier de configuration n’est pas present, annulation du backup")

print("\n**********************************************************************************************************\n")

# Vérifier la possibilité d'accès au fichier source

if os.path.exists(_SOURCE):
    print("le dossier source: ", _SOURCE, "est valide et accessible \n")
else:
    print("le dossier source: ", _SOURCE, "n\’est pas valide/existant \n")
    sys.exit("annulation de la sauvegarde")

print("\n**********************************************************************************************************\n")

# test de connexion au serveur distant

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((_RMTHOST, _PORT))
        s.sendall(b'Hello, world')
        data = s.recv(1024)
        print('communication réussie avec le serveur ' + _RMTHOST, repr(data) + '\n \n')

    except IOError as ex:
        sys.exit("impossible de se connecter au serveur, vérifiez l'adresse/ le port\n "
              "\n************************ \n\nannulation de la sauvegarde")

print("**********************************************************************************************************\n")

# ### CREATION DE LA LISTE LOCALE DES FICHIERS A COPIER ###

# définition de la liste de fichiers locaux
localfilestime = os.scandir(_SOURCE)

# création du dictionnaire intégrant les attributs spécifiques composant le nom de chaque fichier à comparer

loc_files = {}
for f in localfilestime:
    size = f.stat().st_size
    time = int(f.stat().st_mtime)
    name = f.name
    loc_files[(size, time, name)] = f

# affichage des fichiers locaux avec leur attributs

print("fichiers sur répertoire source: \n ")
pprint(loc_files)

print("**********************************************************************************************************\n")

### CREATION DE LA LISTE DISTANTE DES FICHIERS A COPIER ###

# définition du module utilisé pour connexion au serveur distant
ssh = paramiko.SSHClient()

# acceptation auto de clé de connexion avec le client si nécessaire
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# connexion ssh au serveur distant
try:
    ssh.connect(_RMTHOST, username=_USR, password=_DESTPASS)
    sftp = ssh.open_sftp()
    print("le dossier de destination est valide et accessible\n")

except Exception as ex:
    sys.exit("Erreur: le dossier de destination n'est pas valide/accessible\n "
              "\n************************ \n\nannulation de la sauvegarde")

# définition de la liste de fichiers distants

sftp.listdir_attr(_DEST)
distfilestime = sftp.listdir_attr(_DEST)



print("**********************************************************************************************************\n")

# création du dictionnaire intégrant les attributs spécifiques composant le nom de chaque fichier à comparer
dst_files = {}
for f in distfilestime:
    size = f.st_size
    time = f.st_mtime
    name = f.filename
    dst_files[(size, time, name)] = f

# affichage des fichiers distants avec leur attributs
print("fichiers sur répertoire de destination: \n")
pprint(dst_files)

# clôture de la connexion avec le serveur distant
ssh.close()
sftp.close()

print("**********************************************************************************************************\n")

### FICHIERS A TRANSFERER ###

# définition de la liste de comparaison des fichiers locaux et distants

comparaison = [loc_files[x] for x in loc_files if x not in dst_files]

# affichage des fichiers absents/obsolètes sur le répertoire distant
print("les fichiers suivants sont absents du répertoire de destination, "
      "ou une version plus ancienne est présente et sera remplaçée: \n ")
print(comparaison)

print("**********************************************************************************************************\n")


# définition du chemin de création du répertoire temporaire
_SOURCE_TEMP = (_SOURCE + "temp")

# création du repertoire temporaire
if not os.path.exists(_SOURCE_TEMP):
    os.makedirs(_SOURCE_TEMP, exist_ok=True)

# copie des fichiers à transférer sur répertoire temporaire
for files in comparaison:
    shutil.copy2(files, _SOURCE_TEMP)

# ##EXCLURE FICHIERS SELON LISTE D'EXCLUSION LE CAS ÉCHÉANT###

# se rendre sur le répertoire temporaire
os.chdir(_SOURCE_TEMP)

# définition des fichiers à exclure selon paramètre d'exclusion
files = [f for f in os.listdir('.') if os.path.isfile(f)]

for f in files:
    if f.endswith(_EXCLUSION):
        print(f, "ne sera pas copié selon la liste d'exclusion")
        os.remove(f)

# changer de répertoire pour libérer le répertoire afin de permettre son effacement en fin de script ( ERR.WIN32 )
os.chdir(_SOURCE)

print("\n**********************************************************************************************************\n")

### COPIE DES FICHIERS DE LA SOURCE VERS LA DESTINATION ###

# connexion sftp au serveur de destination
with pysftp.Connection(host=_RMTHOST, username=_USR, password=_DESTPASS) as sftp:
    # copie des fichiers depuis le répertoire temporaire vers le répertoire de destination
    sftp.put_r(_SOURCE_TEMP, _DEST, preserve_mtime=True)
    # clôture de la connexion sftp
    sftp.close()

# effacement du répertoire temporaire
if os.path.exists(_SOURCE_TEMP):
    shutil.rmtree(_SOURCE_TEMP + "\\")

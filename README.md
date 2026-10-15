Cette page liste les tests a faire.

# Tests de base.
- [x] Se logguer

# Dashboard
- [x] Créer une utilisateur
- [x] Créer un groupe
- [x] Créer des groupes en fonction des camemberts
# Kiosk
A voir une fois le module terminé.

# Utilisateurs
- [x] Créer un utilisateur
- [x] Supprimer un utilisateur
- [x] Éditer un utilisateur
- [x] Créer un utilisateur en double
- [x] Sauvegarder un utilisateur

# Groups
- [x] Créer un groupe
- [x] Voir un groupe
- [x] Éditer un groupe
- [x] Supprimer un groupe

# Vue Machines
- [x] Afficher toutes les pages
- [x] Afficher l'inventaire d'une machine
- [x] Afficher le monitoring d'une machine
- [x] Lancer la PMAD d'une machine
- [x] Lancer le module de sauvegarde
- [x] Lancer la page de déploiement ( le déploiement est fait dans un autre test ).
- [x] Lancer la page d'imaging ( l'imaging est fait dans un autre test ).
- [x] Lancer la page de la console XMPP
- [x] Lancer la page de file browser
- [x] Lancer la page de file viewer
- [x] Lancer la page d'édition de fichier de configuration
- [x] Lancer la page de quick Action
- [x] Supprimer une machine

## Création de groupe dynamique - GLPI
- [x] Créer un groupe de machine basé sur le nom
- [x] Créer un groupe de machine basé sur la description
- [x] Créer un groupe de machine basé sur la numero d'inventaire
- [x] Créer un groupe de machine basé sur un groupe Glpi
- [x] Créer un groupe de machine basé sur un nom de périphérique
- [x] Créer un groupe de machine basé sur un serial de périphériquecomputers_groups
- [x] Créer un groupe de machine basé sur le type de machine
- [x] Créer un groupe de machine basé sur le fabricant du poste
- [x] Créer un groupe de machine basé sur le modele du poste
- [x] Créer un groupe de machine basé sur l' utilisateur de la machine
- [x] Créer un groupe de machine basé sur le derniere utilisateur connecté
- [x] Créer un groupe de machine basé sur l'emplacement de l'utilisateur
- [x] Créer un groupe de machine basé sur l'emplacement de la machine
- [x] Créer un groupe de machine basé sur l'état de la machine ( production, réparation, rebut, ...)
- [x] Créer un groupe de machine basé sur l'entité à laquelle appartient la machine
- [x] Créer un groupe de machine basé sur le Systeme d'exploitation
- [x] Créer un groupe de machine basé sur le logiciel install
- [x] Créer un groupe de machine basé sur le nom du logiciel et la version
- [x] Créer un groupe de machine basé sur la version de l'OS
- [x] Créer un groupe de machine basé sur l'architecture de l'OS
- [x] Créer un groupe de machine basé sur des clef de registre
- [x] Créer un groupe de machine basé sur des valeurs de clef de registre
- [x] Créer un groupe de machine basé sur la présence online/offline d'une machine

## Création de groupe dynamique - XMPPMASTER
- [x] Créer un groupe de machine basé sur l'OU User
- [x] Créer un groupe de machine basé sur l'OU Machine
## Création de groupe dynamique - DYNGROUP
- [x] Créer un groupe sur un groupe existant
- [x] Création de groupe statique
- [x] Création de groupe avec import csv

## Création de groupe autre cas
- [x] Créer un groupe alors qu'il existe déjà
- [x] Supprimer un groupe 
- [x] Partager un groupe
- [x] Montrer le contenu du groupe
- [x] Editer le groupe


# Imaging
- [x] Afficher toutes les pages du module

# Packages
- [x] Créer un package
- [x] Supprimer un package
- [x] Afficher un package
- [x] Modifier un package.

- [x] Faire un package et les 3 autres étapes pour tout les types de packages.

# Audit
- [x] Afficher toutes les pages du module.

# Updates
A faire une fois le module terminé

# Sauvegarde
A faire une fois le module terminé

# Services
- [x] Afficher toutes les pages du module.

# History
- [x] Afficher toutes les pages du module.

# Admin
- [x] Afficher les relays
- [x] Lister les clusters
- [x] Créer un nouveau cluster
- [x] Créer une règle
- [x] Modifier l'ordre d'une règle

# Comment lancer les tests.

Au préalable il faut installer playwright et playwright-pytest

pip install playwright
pip install pytest-playwright

Ensuite il faut configurer playwright, pour cela il faut "l'installer"

playwright install

Pour lancer les tests il faut utiliser la commande suivante:

python3 -m pytest . --headed --slowmo 500 -o log_cli=true --log-cli-level=DEBUG

au lieu du . qui signifie lancer tout les tests du dossier on peut utiliser unitairement un test précis.

# Configuration

Les valeurs de `functional/config.ini` sont des exemples. Ne pas y commiter de vrais identifiants.

Pour tester plusieurs serveurs en local, créer un fichier par serveur, par exemple
`functional/config.preprod.ini` (ignoré par git), et le choisir avec `MEDULLA_CONFIG` :

    MEDULLA_CONFIG=functional/config.preprod.ini python3 -m pytest

Les variables d'environnement suivantes remplacent les valeurs du fichier :

| Variable | Clé de config.ini | Rôle |
|---|---|---|
| `MEDULLA_URL` | `name` | Racine du serveur web, sans `/mmc` (ex. `https://qa.medulla-tech.io`) |
| `MEDULLA_USER` / `MEDULLA_PASSWORD` | `login` / `password` | Compte de l'interface web |
| `MEDULLA_HOST` | `ssh` | Hôte utilisé pour les vérifications MySQL et SSH |
| `MYSQL_PORT` / `MYSQL_USER` / `MYSQL_PASSWORD` | `port` / `mysqluser` / `mysqlpass` | Accès MySQL |
| `MEDULLA_MACHINE` | `machinename` | Machine Windows avec agent Medulla |
| `SSH_KEY_PATH` / `SSH_KEY_PASSPHRASE` | `passkey_path` / `passphrase` | Clé SSH root sur `MEDULLA_HOST` (tests de paquets) |

Installation des dépendances (Ubuntu) :

    sudo apt install pkg-config default-libmysqlclient-dev
    pip install -r requirements.txt
    playwright install --with-deps chromium

# CI

`.github/workflows/functional.yml` :

- **Pull requests** : vérifie seulement que les tests se chargent (`pytest --collect-only`).
- **Push sur `ci/functional-tests`** (temporaire, à retirer avant le merge) : vérifie que les tests se chargent
  et lance tous les tests sur l'Environment `qa`, sans mettre le serveur à jour.
- **À la demande** (onglet Actions → *Run workflow*) : lance les tests sur le serveur choisi. On peut aussi
  choisir le runner et les tests à lancer.
- **Chaque nuit** (du lundi au vendredi, 2h UTC) : lance les tests sur chaque serveur de la liste, en parallèle.

### Mise à jour du serveur

Comme l'ancien job Jenkins, le workflow peut d'abord mettre à jour le serveur pour tester les derniers paquets
publiés : `apt update && apt upgrade` puis `/usr/sbin/restart-pulse-services` en SSH (root sur `MEDULLA_HOST`),
puis il attend que l'interface web réponde (5 minutes au plus).
Toujours fait la nuit ; au lancement manuel, cocher *update_server*. Demande les secrets `SSH_PRIVATE_KEY`
et `MEDULLA_HOST`.

## Un serveur = un Environment GitHub

Chaque serveur cible est un **Environment** GitHub (Settings → Environments), par exemple `qa`, `preprod`.
Chaque Environment a ses propres secrets et variables, sous les mêmes noms :

- Secrets : `MEDULLA_URL`, `MEDULLA_USER`, `MEDULLA_PASSWORD`, `MEDULLA_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`,
  `SSH_PRIVATE_KEY`, `SSH_KEY_PASSPHRASE`
- Variables : `MEDULLA_MACHINE`, `MYSQL_PORT`

Ajouter un serveur = créer un Environment et remplir ses secrets. Le workflow ne change pas.

Variables du dépôt (Settings → Secrets and variables → Actions → Variables) :

| Variable | Exemple | Rôle |
|---|---|---|
| `FUNCTIONAL_ENVIRONMENTS` | `["qa", "preprod"]` | Serveurs testés chaque nuit (défaut : `["qa"]`) |
| `FUNCTIONAL_RUNNERS` | `{"qa": "proxmox-qa"}` | Runner de chaque serveur (défaut : `ubuntu-latest`) |

## Runner

Les tests modifient les données du serveur et ont besoin de MySQL et de SSH : ils doivent tourner sur un
runner auto-hébergé du même réseau que le serveur. Sur ce runner, installer une fois
`pkg-config default-libmysqlclient-dev python3-venv` et les dépendances de Chromium
(`playwright install-deps chromium`), car le runner n'a pas sudo.

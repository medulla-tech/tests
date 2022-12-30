Cette page liste les tests a faire.

# Tests de base.
- [x] Se logguer

# Dashboard
- [x] Créer une utilisateur
- [x] Créer un groupe
- [ ] Créer des groupes en fonction des camemberts ( ne semble pas possible, a voir avec les devs ).

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
- [x] Créer un groupe de machine basé sur un serial de périphérique
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
- [ ] Créer un groupe sur un groupe existant
- [ ] Création de groupe statique
- [ ] Création de groupe avec import csv

## Création de groupe autre cas
- [ ] Créer un groupe alors qu'il existe déjà
- [ ] Supprimer un groupe 
- [ ] Partager un groupe
- [ ] Montrer le contenu du groupe
- [ ] Editer le groupe


# Imaging
- [x] Afficher toutes les pages du module

# Packages
- [x] Créer un package
- [x] Supprimer un package
- [ ] Afficher un package ( WIP )
- [ ] Modifier un package.

- [ ] Faire un package et les 3 autres étapes pour tout les types de packages.

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
- [ ] Créer un nouveau cluster en double ( possible bug trouvé )
- [x] Créer une règle
- [ ] Modifier l'ordre d'une règle ( En attente d'IDs )



# Comment lancer les tests.

Au préalable il faut installer playwright et playwright-pytest

pip install playwright
pip install pytest-playwright

Ensuite il faut configurer playwright, pour cela il faut "l'installer"

playwright install

Pour lancer les tests il faut utiliser la commande suivante:

python3 -m pytest . --headed --slowmo 500 -o log_cli=true --log-cli-level=DEBUG

au lieu du . qui signifie lancer tout les tests du dossier on peut utiliser unitairement un test précis.

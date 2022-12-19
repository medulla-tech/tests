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
- [ ] Créer un utilisateur en double
- [ ] Sauvegarder un utilisateur

# Groups
- [x] Créer un groupe
- [ ] Voir un groupe
- [ ] Éditer un groupe
- [ ] Supprimer un groupe

# Vue Machines
- [x] Afficher toutes les pages
- [ ] Afficher l'inventaire d'une machine ( en attente des IDs )
- [ ] Afficher le monitoring d'une machine  ( en attente des IDs )
- [ ] Lancer la PMAD d'une machine  ( en attente des IDs )
- [ ] Lancer le module de sauvegarde ( en attente des IDs )
- [ ] Lancer la page de déploiement ( le déploiement est fait dans un autre test ). ( en attente des IDs )
- [ ] Lancer la page d'iamging ( l'imaging est fait dans un autre test ). ( en attente des IDs )
- [ ] Lancer la page de la console XMPP ( en attente des IDs )
- [ ] Lancer la page de file browser ( en attente des IDs )
- [ ] Lancer la page de file viewer ( en attente des IDs )
- [ ] Lancer la page d'édition de fichier de configuration ( en attente des IDs )
- [ ] Lancer la page de quick Action ( en attente des IDs )
- [ ] Supprimer une machine ( en attente des IDs )

## Création de groupe dynamique - GLPI
- [x] Créer un groupe de machine basé sur le nom
- [x] Créer un groupe de machine basé sur la description
- [x] Créer un groupe de machine basé sur la numero d'inventaire
- [x] Créer un groupe de machine basé sur un groupe Glpi
- [x] Créer un groupe de machine basé sur un nom de périphérique
- [x] Créer un groupe de machine basé sur un serial de périphérique
- [x] Créer un groupe de machine basé sur le type de machine
- [x] Créer un groupe de machine basé sur le nom du logiciel et la version
## Création de groupe dynamique - XMPPMASTER
- [x] Créer un groupe de machine basé sur l'OU User
- [ ] Créer un groupe de machine basé sur l'OU Machine
## Création de groupe dynamique - DYNGROUP
- [ ] Créer un groupe sur un groupe existant
- [ ] Création de groupe statique
- [ ] Création de groupe avec import csv

### Création de groupe autre cas
- [ ] Créer un groupe alors qu'il existe déjà
- [ ] Supprimer un groupe 
- [ ] Partager un groupe
- [ ] Montrer le contenu du groupe
- [ ] Editer le groupe
### Logiciel
- [ ] Crééer un package logiciel
- [ ] Supprimer un package logiciel
- [ ] Tester la suppression d'une machine si l'extension fusion est désactivée
- [x] Convertir les tests pour pouvoir les utiliser avec pytest

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

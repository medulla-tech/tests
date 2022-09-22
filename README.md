# Cette page liste les tests a faire.

- [x] Se logguer
- [x] Ouvrir la page d'inventaire
- [x] Ouvrir la page des utilisateurs
### Création de groupe dynamique - GLPI
- [x] Créer un groupe de machine basé sur le nom
- [x] Créer un groupe de machine basé sur la description
- [x] Créer un groupe de machine basé sur la numero d'inventaire
- [x] Créer un groupe de machine basé sur un groupe Glpi
- [x] Créer un groupe de machine basé sur un nom de périphérique
- [x] Créer un groupe de machine basé sur un serial de périphérique
- [x] Créer un groupe de machine basé sur le type de machine
- [ ] Créer un groupe de machine basé sur le nom du logiciel et la version
### Création de groupe dynamique - XMPPMASTER
- [ ] Créer un groupe de machine basé sur l'OU User
- [ ] Créer un groupe de machine basé sur l'OU Machine
### Création de groupe dynamique - DYNGROUP
- [ ] Créer un groupe sur un groupe existant
### Création de groupe statique
### Création de groupe avec import csv
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


# Comment lancer les tests.

Au préalable il faut installer playwright et playwright-pytest

pip install playwright
pip install pytest-playwright

Ensuite il faut configurer playwright, pour cela il faut "l'installer"

playwright install

Pour lancer les tests il faut utiliser la commande suivante:

python3 -m pytest . --headed --slowmo 500 -o log_cli=true

au lieu du . qui signifie lancer tout les tests du dossier on peut utiliser unitairement un test précis.

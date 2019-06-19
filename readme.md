# DataCraft


## Licence
Le travail original réalisé pour cette étude est sous licence Creative Commons Attribution-ShareAlike 4.0 International License
Cette etude utilise des ressources Open Source qui disposent de leurs propres licences notamment :

python-minetest : https://github.com/LeMagnesium/python-minetest
stl-to-voxel : https://github.com/cpederkoff/stl-to-voxel


## Mods pour minetest

Une etude des possibilités de visualisation de données avec le jeu vidéo minetest en collaboration avec 3HitCombo

### rennesdatacraft

Un mod pour minetest qui permet de lire les statistiques de depôt de matière dans les décheteries de Rennes Metropole
Ce mod recupère les données depuis le site https://data.rennesmetropole.fr et visualise les données de déchêts de l'ensemble des déchetteries de la ville de Rennes


### visite

Un mod pour minetest qui permet de se téléporter vers des endroits interessants sur un monde mminetest

## outils en python
Divers scripts python pour créer ou modifier des mondes minetest en fonction de données disponibles sur le site https://data.rennesmetropole.fr

La liste des dépendances necessaires se trouve dans requirement.txt. L'utilisation d'un virtualenv python 3.6 ou supérieur est recommandé

### script create_empty_map.py
Crée une carte vide ou vide une carte existante !!!
create_empty_map <map path>
map path: chemin de la carte minetest (base de donnée sqlite)

### script add_commune.py
Ajoute le contour de la commune de la ville de Rennes sur une carte minetest
add_commune.py <map path> <geojson path> floor_level[-30000,30000] floor[0/1]
map path: chemin de la carte minetest (base de donnée sqlite)
geojson path: chemin du fichier geojson contenant le contour des communes de Rennes Metropole
floor_level: altitude de creation du contour de la commune. Utile pour les mondes "a plusieurs étages"
floor: Option pout générer un sol sous le contour. 0 pas de sol. 1 cretion du sol (attention c'est long, compter plusieurs heures)

le fichier geojson peut être optenu ici : https://data.rennesmetropole.fr/explore/dataset/limites-communales-referentielles-de-rennes-metropole-polygones/map/?location=10,48.12046,-1.71446&basemap=0a029a


###  script add_relai_park_voxel.py
Ajoute une visualisation du taux d'occupation des parcs relais du réseau STAR: https://data.rennesmetropole.fr/explore/dataset/etat-des-parcs-relais-du-reseau-star-en-temps-reel/information/
add_relai_park_voxel.py <map path> <stl path> floor_level[-30000,30000]
map path: chemin de la carte minetest (base de donnée sqlite)
stl path: chemin du fichier objet 3d utilisé pour la representation du taux d'occupation
floor_level : altitude de la representation (la position des parcs est lue depuis l'API)

###  script build_bati_goutiere_level.py
Construit une carte representant le contours des batiments. La donnée de hauteur de goutiere est utilisée pour fixer la hauteur des batiments sur la carte
build_bati_goutiere_level.py <map path> <geojson path> floor_level[-30000,30000] floor [0/1] prune[0/1]")
map path: chemin de la carte minetest (base de donnée sqlite)
geojson path : chemin du fichier geojson contenant les données. https://data.rennesmetropole.fr/explore/dataset/constructions-baties/information/?refine.code_insee=35238&location=19,48.09221,-1.66381&basemap=0a029a pour la commune de Rennes
floor_level: altitude de creation du contour de la commune. Utile pour les mondes "a plusieurs étages"
floor: Option pout générer un sol sous le contour. 0 pas de sol. 1 cretion du sol (attention c'est long, compter 8 heures sur un Core I7 3Ghz)
prune: Option qui permet d'effectuer tout le traitement sans modifier la carte. Utile pour tester l'interpretation du fichier geojson

### script create_bati.py
Crée une map a l'altitude 0 qui represente les contours des batiments d'un fichier geojson https://data.rennesmetropole.fr/explore/dataset/referentiel-batiment/information/
le fichier de données en entré est nommé referentiel-batiment_35238.geojson


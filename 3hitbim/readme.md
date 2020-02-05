Mode d'emploi du mod BIM
========================

Utilisation
-----------
Sélectionner l'outil "BIM tool" dans l'inventaire
Pour positionner le 1er point de repere utiliser le bouton de gauche en designant un bloc
Pour positionner le 2eme point de repere utiliser le bouton de droite en designant un bloc

Lorsque les points 1 et 2 sont définis, le volume de bloc séléctionné est affiché avec une bordure.
Il est alors possible d'afficher le comptage de blocs en designant le bloc 1 ou le bloc 2 puis en effectuant un clic gauche





Configuration
-------------
Le mod bim realise affiche la somme des valeurs des blocs par catégorie. Les blocs pris en compte dans le calcul 
sont les blocs présents dand le volume compris entre le repere 1 et le repere 2. 
La configuration consiste en une suite de catégorie, pour chaque catégorie on indique son nom,
la liste des noms de bloc de la catégorie et la valeur du bloc dans cette catégorie

exemple de configuration :
threehitbim.categories = {
	{
	name="Bois",											-- identification de la catégorie
	bloc={													-- liste des blocs de la catégorie
				["default:wood"]=1,							-- nom du bloc (node minetest) = valeur du bloc
				["default:pine_tree"]=1,
				["default:tree"]=1,
				["default:aspen_wood"]=1,
				["stairs:stairs_aspen_wood"]=1,
				["default:acacia_tree"]=1

		}
	},
	{
	name="Verre",											-- categorie suivante
	bloc={
				["xpanes:pane_flat"]=1,
				["default:glass"]=1;
		}
	}
}

Remarque
--------
Si toutes les valeurs de blocs sont a 1, la valeur calculée pour la catégorie est le nombre de blocs appartenant à celle ci dans
le volume défini entre les reperes 1 et 2.
Il est possible d'utiliser le même nom de bloc dans des catégories differentes, eventuellement avec des valeurs differentes

## Explication des fonctions de perturbation

### Suppression de bâtiments
Ce code n'utilise pas le module ArcPy d'ArcGIS, il manipule uniquement un fichier json.
Le fichier json d'entrée est l'export json d'une couche shapefile, c'est l'argument "data".
Le taux de suppression des bâtiments est un réel entre 0 et 1, c'est l'argument "tauxSuppr".

La fonction crée une liste vide puis la remplit avec des indices pris au hasard. On vérifie que chaque indice ajouté n'est pas déja dans la liste, cela fausserait le compte total.
Ensuite, on supprime les éléments correspondants à ces indices.

### Modification de géométrie	
Ce code utilise la librairie shapely. Il manipule également des fichiers json, sans utiliser ArcPy.
  -Il permet de modifier la géométrie de tous les bâtiments d'une couche, en changeant la position de tous les sommets du polygone représentant le bâti. Les sommets sont translatés, avec une erreur moyenne rentrée en argument mais suivant une loi normale, selon une direction aléatoire, indépendante d'un sommet à un autre.
  -Il peut aussi changer la hauteur des bâtiments. Attention, les données OSM n'ont, la plupart du temps, pas de hauteurs. Cette perturbation n'est donc pas applicable.
  -Il est décomposé en plusieurs fonctions, coordonnees_loi_normale, hauteur_loi_normale, coordonnees_loi_normale_v2, changement_sommet et changement_hauteur.

coordonnees_loi_normale : Cette fonction tire un nombre suivant la loi normale de moyenne "mu", et d'écart-type "ecart_type". On interprètre cette valeur comme la distance positive de l'erreur commise. Ainsi, si le nombre tiré est négatif, on prend 0. Une borne est présente pour éviter de tirer des nombres trop éloignés de ce que l'on voulait. Ensuite, on tire au hasard un angle, qui sera l'orientation de la translation. 

hauteur_loi_normale : Elle fonctionne de la même façon que coordonnees_loi_normale.

coordonnees_loi_normale_v2 : Il s'agit de la même fonction que coordonnees_loi_normale, avec une loi normale modifiée différemment. En effet on prend la valeur absolue de la loi normale.

### Fusion de bâtiments
Ce code utilise la librairie arcpy.
A partir d'une couche vectorielle d'Arcgis, il renvoie une autre couche, contenant les entités de la couche d'entrée fusionnées. Il ne modifie pas la couche d'entrée.
Attention, la fusion de bâtiments n'est pas une perturbation en soi (les limites des zones bâties restent les mêmes). Il s'agit simplement d'une manière d'obtenir des valeurs de périmètres différentes, modifiant ainsi certains indicateurs comme le facteur de forme sans réellement modifier la géométrie.

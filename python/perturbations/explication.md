## Explication des fonctions de perturbations

### Suppression de bâtiments
Ce code n'utilise pas Arcpy d'ArcGIS, il manipule uniquement un fichier json.
Le fichier json d'entrée est l'export json d'une couche shapefile, c'est l'argument "data".
Le taux de suppression des bâtiment est un réel entre 0 et 1, c'est l'argument "tauxSuppr".

La fonction crée une liste vide puis la remplit avec des indices pris au hasard. On vérifie que chaque indice ajouté n'est pas déja dans la liste, cela fausserait le compte total.
Ensuite, on supprime les éléments correspondants à ces indices.

### Modification de géométrie	



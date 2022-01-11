# Analyse de Sensibilité, Projet Recherche


## Table des matières
1. [Partie 1](#)
2. [Partie 2](#)
3. [Partie 3](#)

## 1. Architecture du projet Git
### 1. Données d'entrée
Les données d'entrée sont présentes sous forme de shapefile dans les dossiers *donneesZoneOSM* et *donneesZoneBDTOPO*. Les fichiers présents dans ces dossiers sont des fichiers Shapefile. Ces fichiers sont présents mais en ce qui concerne les codes pour les paramètres **Facteur de forme**, **Aire** et **Volume**, ceux sont les fichiers JSON du dossier *Fichier_JSON* qui sont utilisés.

Zones sélectionnées (Zone Mixte, Zone Centre et Zone Périphérique de Toulouse )

1. Zone Centre ( Zone située au centre-ville de Toulouse 400m sur 400m )
2. Zone Mixte ( Zone située juste à l'extérieur du centre-ville de Toulouse 400m sur 400m )
3. Zone Périphérique ( Zone située en banlieue pavillonaire de Toulouse 400m sur 400m )

Ci-dessous, une carte présentant les zones utilisées
![Carte des zones à Toulouse](/Annexes/Autres/zone.png "Les 3 zones utilisées dans les tests pour ce projet").

*Nappe3D* est un dossier qui présente des nappes obtenues avec ***plotly*** tandis que le code de notre projet se situe dans le dossier *python*. 
A l'ouverture du dossier *python*, on trouve un code par indicateur ainsi que des dossiers *perturbations* et *traitement* qui comporte des codes réutilisables qui correspondent au traitement sur les fichiers JSON. Il s'agit de traitements sur les fichiers JSON correspondant aux couches précédentes.

## 2. Indicateurs sélectionnés et perturbations

Les indicateurs ont été choisis avec en explorant les indicateurs du projet[OrbisGeoclimate](https://github.com/orbisgis/geoclimate/wiki/Output-data). 
Parmis ceux que nous avons implémentés, on trouve les indicateurs suivants:

**FormFactor** (aire d'un bâtiment divisée par son périmètre au carré, pour plus de renseignements sur cet indicateur voir [interpretation_formfactor.md](/Annexes/FormFactor/interpretation_formfactor.md) )
**Aire** (Aire des bâtiments de la couche -- somme des aires des bâtiments de la couche)
**Volume** ( Volume des bâtiments de la couche -- somme des volumes des bâtiments de la couche )

Pour chaque indicateur, on peut trouver des perturbations intéressantes à appliquer pour effectuer ensuite une analyse de sensibilité. Le tableau ci-dessous récapitule les choix que nous avons effectués.

(pour le fonctionnement des codes des perturbations, voir le fichier [explication.md](/python/perturbations/explication.md)

|   Tableau des couples  Indicateur - Perturbation  |                          | Facteur de Forme |     Aire      | Volume  | Distance  Bati-Bati | Distance  Bati-Route |
|:-------------------------------------------------:|--------------------------|------------------|:-------------:|---------|:-------------------:|----------------------|
|              Suppression  de bâtiments            |                          |                  | OSM & BD TOPO | BD TOPO |                     |                      |
|               Modification de géométrie           |  Sommets  des  polygones |   OSM & BD TOPO  | OSM & BD TOPO | BD TOPO |                     |                      |
|                                                   | Hauteurs  des  bâtiments |                  |               | BD TOPO |                     |                      |
|              Translation de bâtiments             |                          |                  |               |         |                     |                      |
|              Dichotomie de bâtiments              |                          |                  |               |         |                     |                      |
|              Fusion de bâtiments                  |                          |                  |               |         |                     |                      |

## 3. Résulats
### 3.1 Facteur de forme et modification de géométrie
### 3.2 Aire et suppression de bâtiments
### 3.3 Aire et modification de géométrie
### 3.4 Volume et suppression de bâtiments 
### 3.5 Volume et modification de géométrie
### 3.6 Nappes 3D 
### 3.7 Commentaires sur les autres indicateurs et perturbations
## 4. Librairies et outils utilisés pour le développement

Les logiciels et ressources suivantes ont été utilisés pour le développement du projet:

* [Spyder]() - Editeur de code
* Shapely - Géométrie des polygones
* Plotly - Production de graphes

Pour les couches de données
* BD TOPO (www.ign.fr)
* OSM (openstreetmap)

## 3. Versions
0.5
## 4. Auteurs

* **Vincent Heau** [VincentHeau](https://github.com/VincentHeau)
* **Tristan Fillon**[TFillon](https://github.com/TFillon)
* **Félix Bal** [fe73](https://github.com/fe73)

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
2. Zone Mixte ( Zone située en proche banlieue de Toulouse 400m sur 400m )
3. Zone Périphérique ( Zone située en banlieue pavillonaire de Toulouse 400m sur 400m )

Ci-dessous, une carte présentant les zones utilisées
![Carte des zones à Toulouse](/Annexes/Autres/zone.png "Les 3 zones utilisées dans les tests pour ce projet").

|   Tableau des couples  Indicateur - Perturbation  |                          | Facteur de Forme |     Aire      | Volume  | Distance  Bati-Bati | Distance  Bati-Route |
|:-------------------------------------------------:|--------------------------|------------------|:-------------:|---------|:-------------------:|----------------------|
|              Suppression  de bâtiments            |                          |                  | OSM & BD TOPO | BD TOPO |                     |                      |
|               Modification de géométrie           |  Sommets  des  polygones |   OSM & BD TOPO  |               | BD TOPO |                     |                      |
|                                                   | Hauteurs  des  bâtiments |                  |               | BD TOPO |                     |                      |
|              Translation de bâtiments             |                          |                  |               |         |                     |                      |

## 2. Librairies et outils utilisés pour le développement

Les logiciels et ressource suivantes ont été utilisés pour le développement du projet:

* [Spyder]() - Editeur de code

*nom-d'environnement*
## 3. Versions
0.5
## 4. Auteurs

* **Vincent Heau** [VincentHeau](https://github.com/VincentHeau)
* **Tristan Fillon**[TFillon](https://github.com/TFillon)
* **Félix Bal** [fe73](https://github.com/fe73)

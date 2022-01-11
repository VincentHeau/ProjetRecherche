# Analyse de Sensibilité, Projet Recherche


## Table des matières
1. [Architecture du projet Git](##1)
2. [Indicateurs sélectionnés et perturbations](##2)
3. [Résultats](##3)

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

Les indicateurs ont été choisis avec en explorant les indicateurs du projet [OrbisGeoclimate](https://github.com/orbisgis/geoclimate/wiki/Output-data). 
Parmis ceux que nous avons implémentés, on trouve les indicateurs suivants:

* **FormFactor** (aire d'un bâtiment divisée par son périmètre au carré, pour plus de renseignements sur cet indicateur voir [interpretation_formfactor.md](/Annexes/FormFactor/interpretation_formfactor.md) )
* 
* **Aire** (Aire des bâtiments de la couche -- somme des aires des bâtiments de la couche)
* 
* **Volume** ( Volume des bâtiments de la couche -- somme des volumes des bâtiments de la couche )

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

## 3. Résultats
### 3.1 Facteur de forme et modification de géométrie
** Pour les données de la BD TOPO **
![Résultats pour la BDTOPO](/Annexes/Autres/Formfactor_BDTOPO.png "Résultats sur le facteur de forme pour la BD TOPO")
** Pour les données OSM **
![Résultats pour OSM](/Annexes/Autres/Formfactor_OSM.png "Résulats sur le facteur de forme pour OSM")
Tout d'abord, les courbes sont décroissantes : plus l'erreur de positionnement est importante, plus le facteur de forme sera petit. Cela s'expliquer par le fait que les géométries obtenues sont de plus en plus tordues, et les angles deviennent très aigus ou obtus. Les bâtiments deviennent alors moins compactes, et leur facteur de forme diminue. Le facteur de forme est plus grand pour la zone périphérique car les bâtiments originellement plus carrés que ceux du centre ville. Ensuite, si l'on normalise les trois courbes, on se rend compte que celle de la zone périphérique décroît plus vite que les autres.


**Aucune différence apparente entre les deux sources de données** 
La réction des deux sources de données lorsque l'on calcule cet indicateur en modifiant la géométrie est similaire.
      
### 3.2 Aire et suppression de bâtiments
![Aire en fonction de la suppression de bâtiments](/Annexes/Autres/aire_suppression.png "Comparaison OSM-BDTOPO pour la suppression de bâtiments")
**Réaction intéressante car elle dépend de la source de données** 
Que ce soit pour OSM comme pour BD TOPO, on calcule l'aire totale des bâtiments de la couche initiale (taux de suppression à 0). Ensuite, on perturbe les données en supprimant un taux de bâtiments. (ce taux est la valeur présente sur l'axe des abscisses). La valeur en abscisse lui correspondant est obtenue par le schéma suivant:
A chaque taux de suppression, on effectue 20 tirages aléatoires de bâtiments à supprimer dans la couche. Et pour chacun de ces tirages, on calcule la nouvelle aire totale.
On fait ensuite la moyenne de ces 20 tirages pour obtenir la nouvelle aire moyenne. La dernière opération consiste à faire le rapport entre cette nouvelle aire moyenne et l'aire totale de la couche initiale. 

On observe clairement sur ce graphique que les réactions aux suppressions sont différentes, et cela s'explique par la façon dont sont acquises et fabriquées les données de la BD TOPO et celles d'OSM
![Couche OSM vs BD TOPO](/Annexes/Autres/aire_suppression.png "Comparaison de couches OSM-BDTOPO pour la suppression de bâtiments")

### 3.3 Aire et modification de géométrie
![Aire/Modifgeom](Annexes/Aire/aire_modification_ZoneMixte_taux0.0.html "Etude de l'indicateur Aire en fonction de la suppression de bâtiments")
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

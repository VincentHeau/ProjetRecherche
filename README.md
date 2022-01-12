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

On observe clairement sur ce graphique que les réactions aux suppressions sont différentes, et cela s'explique par la façon dont sont acquises et fabriquées les données de la BD TOPO et celles d'OSM. Pour l'expliquer, concentrons-nous sur la zone centre (*représentée en bleu sur les graphes*). 

Sur ces zones, on observe pour la BD TOPO, un pallier proche de 1 pour des taux de suppression faibles. Ainsi, lorsque l'on tire au hasard un faible nombre de bâtiments à supprimer, et que l'on calcule l'aire après suppression, cette dernière est proche de l'aire initiale. Pour mieux le comprendre, il faut visualiser une représentation cartographique de la zone Centre. Pour la BD TOPO, on y observe **460 bâtiments**. Parmi ces bâtiments, on en compte quelques uns assez imposants et beaucoup de petits qui sont côte à côte et qui forment des îlots urbains. La forme de cette courbe indique que tant que l'on ne supprime pas plus de 5% des bâtiments de la zone Centre, on a une aire proche de l'aire initiale. Comme les bâtiments à supprimer sont tirés au hasard, on a beaucoup de chance de n'en supprimer que des petits qui n'influencent pas beaucoup l'aire totale. Dès que l'on dépasse 5% (environ) de suppression, on a plus de chance de supprimer les gros bâtiments ce qui explique la décroissance importante à plus de 5% de suppression.

Pour les données OSM, le comportement est très différents, ce pallier n'est pas présents. Lorsque l'on regarde la couche de données OSM sur la même emprise, on ne perçoit pas au premier abord ce qui peut expliquer ce comportement différent. En regardant, les entités de la couche, on  observe **388 bâtiments soit presque 100 de moins que pour la BD TOPO**. Or, l'emprise est la même et en regardant rapidement les deux couches, celles-ci semblent identiques.
Mais, en zoomant précisant sur les îlots urbains, on observe qu'un îlot urbain est divisé en plus de bâtiments pour la BD TOPO que pour OSM.

*On le voit en particulier sur la figure suivante*
![Couche OSM vs BD TOPO](/Annexes/Autres/comparaison_airesup.png "Comparaison de couches OSM-BDTOPO pour la suppression de bâtiments")

**Comment expliquer ces différences de découpages ?**
Date des données utilisées :  * BDTOPO Haute Garonne (31) ( Mars 2021 )
                              * OSM 
C'est dans la manière dont sont produites les données que l'on peut observer comprendre les différences qui existe entre les données OpenStreetMap et celles de l'IGN

**Qu'en conclure sur la qualité des données ?**
Si l'on a besoin de calculer l'indicateur AIRE TOTAL pour une couche de bâtiments, alors on a intérêt à prendre les données de la BD TOPO plutôt que les données OSM. Avec la BD TOPO, si des erreurs d'insertion sont présentes, l'AIRE TOTALE a de forte chance d'être proche de l'AIRE TOTALE VRAIE, c'est à dire celle d'une couche de données parafaitement juste. Ce n'est pas le cas avec OSM. De plus, cela est d'autant plus vrai en centre-ville où 
### 3.3 Aire et modification de géométrie
![Aire/Modifgeom](Annexes/Aire/aire_modification_ZoneMixte_taux0.0.html "Etude de l'indicateur Aire en fonction de la suppression de bâtiments")
### 3.4 Volume et suppression de bâtiments 
![Logo](/Annexes/Autres/volume_suppression.png "logo")
### 3.5 Volume et modification de géométrie

### 3.6 Volume avec modification de géométrie et suppression de bâtiments
![Aire/Modifgeom](Annexes/Autres/Volume_suppression&modification_zonecentre.png "Volume en fonction de la suppression et modification de bâtiments")

Comme on l'observe ci-dessus, nous avons fait le choix d'afficher ici le résultat sur la zone Centre de Toulouse. Pour les autres zones, le comportement est le même.
Sur ce graphe, on observe que l'influence du taux de suppression sur le volume total de la couche de bâtiments est bien plus prépondérante que celle de la modification de géométrie. Si l'on s'intéresse à **l'intersection** entre le plan qui correspond à 5% d'erreur et la nappe obtenue, on a une légère courbure. Cependant malgré cela, on constate tout de même la forte influence du taux de suppression. *Il est prépondérant*. En comparant les nappes pour les 3 zones, on aurait du mal à en tirer des conclusions différentes de celles de la partie 3.5.

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

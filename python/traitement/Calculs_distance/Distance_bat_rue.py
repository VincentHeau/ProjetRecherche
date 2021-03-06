"""
Auteurs : Tristan FILLON, Vincent HEAU, Félix BAL
Pour chaque bâtiment de la couche Arcgis stockée dans zone (ligne 23), ce programme remplit l'attribut NEAR_DIST, contenant la distance à la rue la plus proche. Les rues sont stockées dans la variable Routes_Toulouse_OSM (ligne 24).
Etapes nécessaires à l'utilisation de ce script :
    -Ouvrir un fichier Arcgis et y insérer le fichier Routes_Toulouse_OSM.shp (présent sur ce Git dans ProjetRecherche/donneesRouteOSM)
    -Y insérer également les fichiers .shp contenant les bâtiments des différentes zones traitées (dans ProjetRecherche/donneesZonesOSM et ProjetRecherche/donneesZonesBDTOPO)
    -Remplir le contenu des variables scratchWorkspace et workspace (ligne 38). Ils correspondent à l'emplacement de la geodatabase (et se terminent donc par .gdb) du fichier Arcgis créé.
    -Insérer ce script dans Arcgis et le lancer.
"""

import arcpy

def Calcul_dist_bat_rue():
    """
    Calcule la distance entre un bâtiment et la rue la plus proche.
    Les bâtiments et les routes se trouvent dans des fichiers .shp, importés via les variables zone et Routes_Toulouse_OSM respectivement.
    L'algorithme utilise les fonctions du logiciel Arcgis, importées via le module arcpy.
    """

    #To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    zone = "zoneCentre" #Mettre la zone que l'on souhaite
    Routes_Toulouse_OSM = "Routes_Toulouse_OSM" #zone et Routes_Toulouse_OSM ont été trouvées dans le workspace défini ligne 38.

    #Calculer la distance bat-rue 
    arcpy.analysis.Near(zone, Routes_Toulouse_OSM, "100 Meters") #Renvoie pour chaque bâtiment, dans la colonne NEAR_DIST (il la crée si elle n'existe pas), la distance à la route la plus proche, (entre les points de chacune des entités permettant la distance la plus courte, et non les barycentres).
    #et renvoie -1 si celle-ci se trouve à plus de 100 m du bâtiment.

    #Fixer les distances "trop grandes" à 100.
    with arcpy.da.UpdateCursor(zone, field_names=["NEAR_DIST"]) as cursor:
        for row in cursor: #La variable row parcourt toutes les lignes de la table d'attributs
            if row[0] == -1:
                row[0] = 100 #Chaque fois qu'arcpy.analysis.Near a renvoyé -1, on fixe la distance correspondante à 100.
            cursor.updateRow(row)

if __name__ == '__main__':
    with arcpy.EnvManager(scratchWorkspace="", workspace=""): #Ajouter dans scratchWorkspace et workspace l'emplacement des données source une fois ce fichier téléchargé.
        #Il sera nécessaire de créer un fichier Arcgis, et d'insérer dans sa geodatabase (gdb) la couche que l'on souhaite traiter. Ces scratchWorkspace et workspace correspondront à l'emplacement de cette gdb.
        Calcul_dist_bat_rue()

"""
Auteurs : Tristan FILLON, Vincent HEAU, Félix BAL
Pour chaque bâtiment de la couche Arcgis stockée dans entree (ligne 22), ce programmme remplit l'attribut NEAR_DIST, contenant la distance au bâtiment le plus proche.
Etapes nécessaires à l'utilisation de ce script :
    -Ouvrir un fichier Arcgis et y insérer les fichiers .shp contenant les bâtiments des différentes zones traitées (dans ProjetRecherche/donneesZonesOSM et ProjetRecherche/donneesZonesBDTOPO)
    -Remplir le contenu des variables scratchWorkspace et workspace (ligne 28). Ils correspondent à l'emplacement de la geodatabase (et se terminent donc par .gdb) du fichier Arcgis créé.
    -Insérer ce script dans Arcgis et le lancer.
"""

import arcpy

def Calcul_dist_bat_bat():
    """
    Calcule la distance entre un bâtiment et le bâtiment le plus proche dans la même zone.
    Les bâtiments se trouvent dans des fichiers .shp, et sont importés via la variable entree.
    L'algorithme utilise les fonctions du logiciel Arcgis, importées via le module arcpy.
    """
    
    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    entree = "zonePeri" #Mettre la couche que l'on souhaite.
    #entree a été trouvée dans le workspace défini ligne 19.
    
    arcpy.analysis.Near(entree, entree, "100 Meters") #Renvoie pour chaque bâtiment, dans la colonne NEAR_DIST (il la crée si elle n'existe pas), la distance au bâtiment le plus proche, (entre les points de chacune des entités permettant la distance la plus courte, et non les barycentres).

if __name__ == '__main__':
    with arcpy.EnvManager(scratchWorkspace="", workspace=""): #Ajouter dans scratchWorkspace et workspace l'emplacement des données source une fois ce fichier téléchargé.
        #Il sera nécessaire de créer un fichier Arcgis, et d'insérer dans sa geodatabase (gdb) la couche que l'on souhaite traiter. Ces scratchWorkspace et workspace correspondront à l'emplacement de cette gdb.
        Calcul_dist_bat_bat()

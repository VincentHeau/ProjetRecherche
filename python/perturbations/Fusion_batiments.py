"""
Auteurs : Tristan FILLON, Vincent HEAU, Félix BAL
Pour chaque bâtiment de la couche Arcgis stockée dans entree (ligne 17), ce crée la couche sortie, obtenue par fusion des entités en entrée.
Etapes nécessaires à l'utilisation de ce script :
    -Ouvrir un fichier Arcgis et y insérer les fichiers .shp contenant les bâtiments des différentes zones traitées (dans ProjetRecherche/donneesZonesOSM et ProjetRecherche/donneesZonesBDTOPO)
    -Remplir le contenu des variables scratchWorkspace et workspace (ligne 28). Ils correspondent à l'emplacement de la geodatabase (et se terminent donc par .gdb) du fichier Arcgis créé.
    -Insérer ce script dans Arcgis et le lancer.
"""

import arcpy

def Fusion_de_batiments():
    """
    Fusionne les bâtiments de la couche entree.
    Ces bâtiments se trouvent dans des fichiers .shp, et sont importés via la variable entree.
    L'algorithme utilise les fonctions du logiciel Arcgis, importées via le module arcpy.
    """

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    entree = "zoneCentre" #Mettre la couche que l'on souhaite.
    #entree a été trouvée dans le workspace défini ligne 30.

    sortie = "" #Indiquer l'emplacement et le nom du fichier qi stockera l'entité fusionnée
    arcpy.Dissolve_management(entree, sortie) #Fusionne les entités de entree dans la nouvelle couche sortie.

if __name__ == '__main__': #Ajouter dans scratchWorkspace et workspace l'emplacement des données source une fois ce fichier téléchargé.
    #Il sera nécessaire de créer un fichier Arcgis, et d'insérer dans sa geodatabase (gdb) la couche que l'on souhaite traiter. Ces scratchWorkspace et workspace correspondront à l'emplacement de cette gdb.
    with arcpy.EnvManager(scratchWorkspace="", workspace=""):
        Fusion_de_batiments()

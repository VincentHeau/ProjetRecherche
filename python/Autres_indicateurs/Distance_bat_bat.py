import arcpy

def Model():  # Model

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    entree = "donneesZones\donneesZones\zonePeri.shp" #Mettre la couche que l'on souhaite.
    
    arcpy.analysis.Near(entree, entree, "100 Meters")

if __name__ == '__main__':
    # Penser à modifier le scratchWorkspace et le workspace
    with arcpy.EnvManager(scratchWorkspace=r"\\del1306n018\nethome\ing20\TFillon\PIR\Carte_OSM_Toulouse\Carte_OSM_Toulouse.gdb", workspace=r"\\del1306n018\nethome\ing20\TFillon\PIR\Carte_OSM_Toulouse\Carte_OSM_Toulouse.gdb"):
        Model()

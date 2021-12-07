import arcpy

def Model():  # Model

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    batiments_toulouse_bdtopo = "batiments_toulouse_bdtopo"
    Routes_Toulouse_OSM = "Routes_Toulouse_OSM"

    # Process: Calculer la distance bat-rue 
    arcpy.analysis.Near(batiments_toulouse_bdtopo, Routes_Toulouse_OSM, "100 Meters")

    #Process: Fixer les distances "trop grandes" à 100
    with arcpy.da.UpdateCursor(batiments_toulouse_bdtopo, field_names=["NEAR_DIST"]) as cursor:
        for row in cursor:
            if row[0] == -1:
                row[0] = 100
            cursor.updateRow(row)

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"\\del1306n018\nethome\ing20\TFillon\PIR\Carte_OSM_Toulouse\Carte_OSM_Toulouse.gdb", workspace=r"\\del1306n018\nethome\ing20\TFillon\PIR\Carte_OSM_Toulouse\Carte_OSM_Toulouse.gdb"):
        Model()

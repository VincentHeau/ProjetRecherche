import json
import random as rd


def suppressionBatiment(tauxSuppr,nomFichier):
    """
    Supprime au hasard un pourcentage de batiment voulu
    
    tauxSuppr : entier entre 0 et 1
    
    nomFichier : chaine de caractère correspondant au fichier JSON des bâtiments
    """
    #on ouvre le fichier json
    with open(nomFichier) as mon_fichier:
        data = json.load(mon_fichier)
        
        
    nbBat = len(data['features'])
    
    #on calcule le nombre de bâtiments à supprimer et on utilise une liste d'indice au hasard à supprimer
    nbElementASupr = round(tauxSuppr*nbBat)    
    
    listeASuppr = []
    
    #on tire au sort les indices à supprimer
    for i in range(nbElementASupr):
        index = rd.randint(0,nbElementASupr-1)
        while index in listeASuppr:
            index = rd.randint(0,nbElementASupr-1)
        listeASuppr.append(index)
    

    #on supprime les bâtiments correspondants aux indices de la liste listeASuppr
    for index in listeASuppr:
        del data['features'][index]
        
    mon_fichier.close()
    
    
    #on remplace notre fichier de départ par notre fichier modifié
    with open(nomFichier,'w') as donneeDepart:
        json.dump(data, donneeDepart)
        
        donneeDepart.close()
        
        

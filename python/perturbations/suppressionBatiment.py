

import random as rd
import numpy as np




def suppression(tauxSuppr,data):
    """
    Supprime au hasard un pourcentage de batiment voulu
    
    tauxSuppr : entier entre 0 et 1
    
    data : dictionnaire correspondant à l'intérieur du fichier JSON des bâtiments
    """
          
    nbBat = len(data['features'])
    
    #on calcule le nombre de bâtiments à supprimer et on utilise une liste d'indice au hasard à supprimer
    nbElementASupr = round(tauxSuppr*nbBat)    
    
    
    for i in range(nbElementASupr):
        index=rd.randint(0,len(data['features'])-1)
        del data['features'][index]
    
    
    
        

    
    #on remplace notre fichier de départ par notre fichier modifié
    #ecrit_json(data,fichier)
      
    return data

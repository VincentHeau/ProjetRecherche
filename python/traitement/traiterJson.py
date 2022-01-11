# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 21:21:31 2021

@author: HEAU BAL FILLON
Bibliothèque d'ouverture et d'écriture de fichier JSON

"""
import json

def ouvre_json(fichier):
    """
    Fonction qui ouvre un fichier json et qui renvoie son contenu sous forme d'une variable
    ----------
    fichier : json
      fichier json en entree

    Returns
    -------
    data : dict
        Dictionnaire correspondant à l'intérieur du fichier json

    """
    
    with open(fichier) as mon_fichier:
        data = json.load(mon_fichier)
    
    mon_fichier.close()
        
    return data


def ecrit_json(data,fichier):
    """
    Fonction qui écrit un fichier JSON à partir d'un dictionnaire et d'un fichier
    ----------
    data : dict
        contenu du fichier JSON
    fichier : fichier
        le fichier dans lequel on écrit data

    Returns
    -------
    None.

    """
    
    with open(fichier,'w') as mon_fichier:
       json.dump(data,mon_fichier)
    
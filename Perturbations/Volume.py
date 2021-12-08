# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 21:07:23 2021

@author: HEAU
"""

# importation des librairies
import perturbations.suppressionBatiment as sup
import traitement.traiterJson as js

import random as rd
from shapely.geometry import Polygon
import numpy as np
import matplotlib.pyplot as plt
import math as ma
import os


def volume_total(data):
    V=0
    for i in range(len(data['features'])):
        
        h=data['features'][i]['attributes']['HAUTEUR']
        a=data['features'][i]['attributes']['Shape_Area']
        
        V+=a*h
    return V  


def analyse_suppression(fichier,tirages):
    """
    Fonction qui effectue l'analyse de sensibilité selon la loi normale
    ----------
    fichier : file
        fichier json
        
    X : list
        Ensemble des valeurs prises par l'erreur moyenne mu'
        
        
    sigma : float
         ecart-type
    
    tirages : int
         nombre de tirages effectués pour chaque mu

    Returns list
    -------
    list des moyennes du form factor

    """  
    volume_norm=volume_total(js.ouvre_json(fichier))
    
    
    listeVolume =[]
    
    for taux in X:
        #On fait varier le taux de suppression
        v=0
        for i in range(tirages):
            new_data=sup.suppression(taux,js.ouvre_json(fichier))
            v+=volume_total(new_data)
        volume=v/tirages
        volume=volume/volume_norm
        listeVolume.append(volume)
          
        print("fin tour avec un taux de :",taux) 

    plt.plot(X,listeVolume)
    plt.xlabel("Taux de suppression des bâtiments")
    plt.ylabel("Volume total occupé par les bâtiments")
    plt.title("Evolution du volume total occupé par les bâtiments \nen fonction du taux de suppression des bâtiments.")
    plt.savefig("Annexes/Volume/graphique_volume_suppression_bis__{0}.png".format(n))
    
    
    
    return listeVolume

 
if __name__ == '__main__':
    
    
    os.chdir("..")
        
    fichier1='Fichier_JSON/zoneMixte.json'
    fichier2='Fichier_JSON/zoneCentre.json'
    fichier3='Fichier_JSON/zonePeri.json'
    
    
    
    plt.figure(1)
       
    X=[i/1000 for i in range(200)]
    
    tirages=20
    
    n='ZoneMixte'
    plt.plot(X,analyse_suppression(fichier1,tirages),label='ZoneMixte',color='red')
    n='ZoneCentre'
    plt.plot(X,analyse_suppression(fichier2,tirages),label='ZoneCentre',color='blue')
    n='ZonePeri'
    plt.plot(X,analyse_suppression(fichier3,tirages),label='ZonePeri',color='black')
    
    plt.legend()
    plt.grid()
    plt.xlabel("Taux de suppression des bâtiments")
    plt.ylabel("Volume total occupé par les bâtiments")
    plt.title("Evolution du volume total occupé par les bâtiments \nen fonction du taux de suppression des bâtiments.")
    plt.savefig("Annexes/Volume/graphique_volume_suppression_finale_bis.png")
    
    
    
    
    
   
"""
fichier='testt_FeaturesToJSON3.json'
data_initial=ouvre_json(fichier)    
changement_sommet(ouvre_json(fichier),5,0.3)
    
ecrit_json(changement_sommet(ouvre_json(fichier),5,0.3),fichier) 
"""
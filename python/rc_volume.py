# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 09:59:55 2021


Programme permettant de calculer comment faire varier les paramètres de suppression, d'imprécision xy et d'imprécision 
sur la hauteur pour avoir un taux d'erreur de 10%'
"""

# importation des librairies
import perturbations.suppressionBatiment as sup
import perturbations.modificationgeomBatiment as md
import traitement.traiterJson as js
import Volume as V


import random as rd
from shapely.geometry import Polygon
import numpy as np
import matplotlib.pyplot as plt
import math as ma
import os
from mpl_toolkits.mplot3d import axes3d  # Fonction pour la 3D



def taux_erreur(volume_ini,volume_nv):
    return (volume_ini-volume_nv)/volume_ini



def calcul_volume_nv(data,t,mu_g,sigma_g,mu_h,sigma_h):
    """
    Fonction qui calcule le nouveau volume en prennant en compte les différentes perturbations
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
    # Perturbation qui consiste à supprimer des bâtiments
    ### paramètre qui varie (taux de suppression t)
    data=sup.suppression(t,data)

    # Perturbation qui consiste à modifier la géométrie
    ### paramètres qui varient (mu_g et sigma_g )
    data=md.changement_sommet(data,mu_g,sigma_g)
    
    
    # Perturbation qui consiste à modifier la géométrie
    ### paramètres qui varient (mu_h et sigma_h )
    data=md.changement_hauteur(data,mu_h,sigma_h)
    
    
    volume=V.volume_total(data)
    
    return volume
    

    

 


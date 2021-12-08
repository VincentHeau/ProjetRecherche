# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 21:37:16 2021

@author: HEAU
"""

from shapely.geometry import Polygon
import numpy as np
import random


def coordonnees_loi_normale(mu, ecart_type): 
    normale = np.random.normal(mu,ecart_type,1)[0] 
    if normale<0: 
        normale = 0 
    teta = np.random.uniform(-np.pi,np.pi) 
    x = normale * np.sin(teta) 
    y = normale * np.cos(teta) 
    return (x,y)

def hauteur_loi_normale(mu, ecart_type): 
    #cette fonction tire un h grâce à la loi normale que l'on borne à 0 
    normale = np.random.normal(mu,ecart_type,1)[0] 
    if normale<0: 
        normale = 0
        
    #on a un h positif ou négatif 
    h = [-1,1][random.randint(0,1)]*normale
    
    return h


def coordonnees_loi_normale_v2(mu, ecart_type): 
    normale = abs(np.random.normal(mu,ecart_type,1)[0]) 
    y = np.random.normal(mu,ecart_type,1)[0]
    
    teta = np.random.uniform(-np.pi,np.pi) 
    x = normale * np.sin(teta) 
    y = normale * np.cos(teta) 
    return (x,y)

def changement_sommet(data,mu,ecart_type):
    """
    
    Fonction qui modifie le jeu de données JSON en changeant la géométrie des objets selon une loi 
    normale
    ----------
    data : dict
        contenu JSON
    mu : float
        moyenne de la loi normale
    ecart_type : float
        ecart-type de la loi normale

    Returns
    -------
    data : dict
        Le jeu de données modifié

    """

    for i in range(len(data['features'])):
        
        aire=0
        perimetre=0
        
        for j in range(len(data['features'][i]['geometry']['rings'])):
            
            for k in range(len(data['features'][i]['geometry']['rings'][j])):
                
                #x= rd.randint(1,3)
                #y= rd.randint(1,3)
                (a,b)=coordonnees_loi_normale(mu,ecart_type)
                
                data['features'][i]['geometry']['rings'][j][k][0]+=a
                data['features'][i]['geometry']['rings'][j][k][1]+=b
                
            #Mise à jour du périmètre et de l'aire
            polygon=Polygon(data['features'][i]['geometry']['rings'][j])
            
            if aire==0:
                aire+=polygon.area
            else:
                aire-=polygon.area
                
            perimetre+=polygon.length
            
        #Mise à jour des attributs de géométrie de la couche
        data['features'][i]['attributes'].update({'Shape_Leng':perimetre})
        
        data['features'][i]['attributes'].update({'Shape_Area':aire})
        
    
    return data

def changement_hauteur(data,mu,ecart_type):
    """
    
    Fonction qui modifie le jeu de données JSON en changeant la hauteur selon une loi 
    normale
    ----------
    data : dict
        contenu JSON
    mu : float
        moyenne de la loi normale
    ecart_type : float
        ecart-type de la loi normale

    Returns
    -------
    data : dict
        Le jeu de données modifié

    """

    for i in range(len(data['features'])):
        
        h=hauteur_loi_normale(mu,ecart_type)
                
        new_HAUTEUR=data['features'][i]['attributes']['HAUTEUR']+h 
        
        #Mise à jour des attributs de géométrie de la couche
        data['features'][i]['attributes'].update({'HAUTEUR':new_HAUTEUR})
        
                  
    
    return data
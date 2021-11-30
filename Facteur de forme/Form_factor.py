# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 07:20:57 2021

@author: HEAU
"""


#'petit_test_FeaturesToJSON.json



# importation des librairies
import json
import random as rd
from shapely.geometry import Polygon
import numpy as np
import matplotlib.pyplot as plt
import math as ma




def coordonnees_loi_normale(mu, ecart_type): 
    normale = np.random.normal(mu,ecart_type,1)[0] 
    if normale<0: 
        normale = 0 
    teta = np.random.uniform(-np.pi,np.pi) 
    x = normale * np.sin(teta) 
    y = normale * np.cos(teta) 
    return (x,y)


def coordonnees_loi_normale_vincent(mu, ecart_type): 
    normale = abs(np.random.normal(mu,ecart_type,1)[0]) 
    y = np.random.normal(mu,ecart_type,1)[0]
    
    teta = np.random.uniform(-np.pi,np.pi) 
    x = normale * np.sin(teta) 
    y = normale * np.cos(teta) 
    return (x,y)
    


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
    
    with open(fichier,'w') as mon_fichier:
       json.dump(data,mon_fichier)
    
    

def changement_sommet(data,mu,ecart_type):
    
        
    ### Ajout du champ FormFactor
    alias={"FormFact" : "Form_Fact"}
    
    data['fieldAliases'].update(alias)
    
    
    Champ={
      "name" : "FormFact",
      "type" : "esriFieldTypeDouble",
      "alias" : "FormFact"
      }
    data["fields"].append(Champ)
    
    ### Calcul du champ Form factor
    
    ## Initialisation des paramètres statistiques
    n=0
    moyenne=0
        
    
    for i in range(len(data['features'])):
        
        aire=0
        perimetre=0
        
        for j in range(len(data['features'][i]['geometry']['rings'])):
            
            
            
            
            for k in range(len(data['features'][i]['geometry']['rings'][j])):
                
                
                #x= rd.randint(1,3)
                #y= rd.randint(1,3)
                (a,b)=coordonnees_loi_normale_vincent(mu,ecart_type)
                
                data['features'][i]['geometry']['rings'][j][k][0]+=a
                data['features'][i]['geometry']['rings'][j][k][1]+=b
                
            #Mise à jour du périmètre et de l'aire
            polygon=Polygon(data['features'][i]['geometry']['rings'][j])
            
            if aire==0:
                aire+=polygon.area
            else:
                aire-=polygon.area
                
            perimetre+=polygon.length
            
        #print("###")
        #print(perimetre)
        #print("###")
        data['features'][i]['attributes'].update({'Shape_Leng':perimetre})
        #print("###")
        #print(data['features'][i]['attributes']['Shape_Length'])
        #print("###")
        data['features'][i]['attributes'].update({'Shape_Area':aire})
        
        f=aire/(perimetre*perimetre)
        
        attribut={"FormFact":f}
        data['features'][i]['attributes'].update(attribut)
        
        #Mise à jour des paramètres statistiques
        n+=1
        moyenne+=f
                      
    
    #Mise en forme finale des paramètres statistiques
    
    m=moyenne/n
    
    return m

 
if __name__ == '__main__':
    
    
    fichier='zoneMixte.json'
    data_initial=ouvre_json(fichier)
    
    moy=changement_sommet(ouvre_json(fichier),0,0)
    
    listeF =[]
    X=[i/10 for i in range(20)]
    for k in X: 
        listeFormFactor =[]
        
        for i in range(40):
            MOY=changement_sommet(ouvre_json(fichier),k,0.15)
            listeFormFactor.append(MOY)
                       

        listeF.append(np.mean(listeFormFactor)) 
        print("fin tour avec mu=",k) 


    print(listeF)
    
    plt.plot(X,listeF)
   
"""
fichier='testt_FeaturesToJSON3.json'
data_initial=ouvre_json(fichier)    
changement_sommet(ouvre_json(fichier),5,0.3)
    
ecrit_json(changement_sommet(ouvre_json(fichier),5,0.3),fichier) 
"""    
    
   
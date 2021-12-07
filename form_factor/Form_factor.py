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
import os




def coordonnees_loi_normale(mu, ecart_type): 
    normale = np.random.normal(mu,ecart_type,1)[0] 
    if normale<0: 
        normale = 0 
    teta = np.random.uniform(-np.pi,np.pi) 
    x = normale * np.sin(teta) 
    y = normale * np.cos(teta) 
    return (x,y)


def coordonnees_loi_normale_v2(mu, ecart_type): 
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
    m : float
        La moyenne du form factor de la couche des batiments

    """
    
        
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


def analyse_loiNormale(fichier,X,sigma,nb_tirages):
    """
    Fonction qui effectue l'analyse de sensibilité selon la loi normale
    ----------
    fichier : file
        fichier json
        
    X : list
        Ensemble des valeurs prises par l'erreur moyenne mu'
        
        
    sigma : float
         ecart-type
    
    nb_tiarges : int
         nombre de tirages effectués pour chaque mu

    Returns list
    -------
    list des moyennes du form factor

    """
    #Moyenne avec mu=0 et sigma=0    
    moy=changement_sommet(ouvre_json(fichier),0,0)
    
    
    listeF =[]
    
    for k in X:
        #On fait varier la moyenne k (erreur en moyenne )
        listeFormFactor=[]
        
        for i in range(nb_tirages):
            # On prend nb_tirages tirages aléatoires avec un ecart-type sigma
            MOY=changement_sommet(ouvre_json(fichier),k,sigma)
            listeFormFactor.append(MOY)
            ##on calcule pour chaque tirage la moyenne des facteurs de forme de la couche
                       

        listeF.append(np.mean(listeFormFactor))
        ## on fait la moyenne des résultats des tirages précédents pour chaque k
        print("fin tour avec mu=",k) 


    print(listeF)
    
    plt.plot(X,listeF)
    plt.xlabel("Erreur moyenne mu en mètre")
    plt.ylabel("Moyenne des facteurs de forme\n({0} tirages effectués à chaque mu )".format(nb_tirages))
    plt.title("Evolution de la moyenne du facteur forme \nen fonction de l'erreur de position appliquée aux sommets des bâtiments.\n(loi normale(mu,{0}))".format(sigma))
    plt.savefig("form_factor/Annexes/graphique_form_factor.png")
    
    return listeF

 
if __name__ == '__main__':
    
    os.chdir("..")
        
    fichier1='Fichier_JSON/zoneMixte.json'
    fichier2='Fichier_JSON/zoneCentre.json'
    fichier3='Fichier_JSON/zonePeri.json'

    
    plt.figure(1)
    ## Application de la loi binomiale    
    X=[i for i in range(10)]
    #analyse_loiNormale(fichier,X,0.15,10)
    plt.plot(X,analyse_loiNormale(fichier1,X,0.15,10),label='ZoneMixte')
    plt.plot(X,analyse_loiNormale(fichier2,X,0.15,10),label='ZoneCentre')
    plt.plot(X,analyse_loiNormale(fichier3,X,0.15,10),label='ZonePeri')
    plt.legend()
    plt.grid()
    plt.xlabel("Erreur moyenne mu en mètre")
    plt.ylabel("Moyenne des facteurs de forme\n(10 tirages effectués à chaque mu )")
    plt.title("Evolution de la moyenne du facteur forme \nen fonction de l'erreur de position appliquée aux sommets des bâtiments.\n(loi normale(mu,0;15))")
    plt.savefig("form_factor/Annexes/graphique_form_factor.png")
    
    
    
   
"""
fichier='testt_FeaturesToJSON3.json'
data_initial=ouvre_json(fichier)    
changement_sommet(ouvre_json(fichier),5,0.3)
    
ecrit_json(changement_sommet(ouvre_json(fichier),5,0.3),fichier) 
"""    
    
   
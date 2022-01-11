# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 07:20:57 2021

@author: HEAU BAL FILLON

Script calcule la moyenne du paramètre FACTEUR DE FORME (FORM FACTOR) 
sur les 3 zones (Centre, Périphérique et Mixte) de Toulouse

Possibilité de choisir la source de données OSM ou BD_TOPO en tapant 1 ou 2
"""



# importation des librairies
import traitement.traiterJson as js
import perturbations.modificationgeomBatiment as md

from shapely.geometry import Polygon
import numpy as np
import matplotlib.pyplot as plt
import math as ma
import os



from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot



    

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
    
        
    ### Ajout du champ FormFactor dans la couche
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
        
        #On boucle sur les polygones puis ensuite sur les sommets des polygones
        for j in range(len(data['features'][i]['geometry']['rings'])):
        
            for k in range(len(data['features'][i]['geometry']['rings'][j])):
                
               
                # Borne fixée à 10m (bien trop grand) Au delà de cette borne, la 
                # perturbation n'est plus réaliste
                
                (a,b)=md.coordonnees_loi_normale(mu,ecart_type,10)
                
                data['features'][i]['geometry']['rings'][j][k][0]+=a
                data['features'][i]['geometry']['rings'][j][k][1]+=b
                
                
                
            #Mise à jour du périmètre et de l'aire
            polygon=Polygon(data['features'][i]['geometry']['rings'][j])
            
            if aire==0:
                aire+=polygon.area
            else:
                aire-=polygon.area
                
            perimetre+=polygon.length
            
        
        data['features'][i]['attributes'].update({'Shape_Leng':perimetre})
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
        fichier json de la maille ou zone étudiée
        
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
    moy=changement_sommet(js.ouvre_json(fichier),0,0)
    
    
    listeF =[]
    
    for k in X:
        #On fait varier la moyenne k (erreur en moyenne )
        listeFormFactor=[]
        
        for i in range(nb_tirages):
            # On prend nb_tirages tirages aléatoires avec un ecart-type sigma
            MOY=changement_sommet(js.ouvre_json(fichier),k,sigma)
            listeFormFactor.append(MOY)
            ##on calcule pour chaque tirage la moyenne des facteurs de forme de la couche
                       

        listeF.append(np.mean(listeFormFactor))
        ## on fait la moyenne des résultats des tirages précédents pour chaque k
        print("fin tour avec mu=",k) 

    
    return listeF

 
if __name__ == '__main__':
    
    os.chdir('..')
    print("Choisissez votre source de données:")
    print("1. BD TOPO ign")
    print("2. OSM openstreetmap")
    src=input("Tapez 1 ou 2 : ")
    if src=='1':
        fichier1='Fichier_JSON/zoneMixte.json'
        fichier2='Fichier_JSON/zoneCentre.json'
        fichier3='Fichier_JSON/zonePeri.json'
    elif src=='2':
        fichier1='Fichier_JSON/zoneMixteOSM.json'
        fichier2='Fichier_JSON/zoneCentreOSM.json'
        fichier3='Fichier_JSON/zonePeriOSM.json'

     
    X=[i/10 for i in range(60)]
    
    # Avec un écart-type de 0.15
    Sig015 = [go.Scatter(x=X,
                             y=analyse_loiNormale(fichier1,X,0.15,20),
                             mode='lines',
                             name='Zone Mixte',
                             line=dict(width=2,color='rgb(0,240,122)')),
                  go.Scatter(x=X,
                             y=analyse_loiNormale(fichier2,X,0.15,20),
                             mode='lines',
                             name='Zone Centre',
                             line=dict(width=2,color='rgb(25,24,122)')),
                  go.Scatter(x=X,
                             y=analyse_loiNormale(fichier3,X,0.15,20),
                             mode='lines',
                             name='Zone Périphérique',
                             line=dict(width=2,color='rgb(255,24,0)'))]
                             
    
    Fig015 = go.Figure(data=Sig015)
    
    # Avec un écart-type de 1
    Sig1 = [go.Scatter(x=X,
                             y=analyse_loiNormale(fichier1,X,1,20),
                             mode='lines',
                             showlegend=False,
                             line=dict(width=2,color='rgb(0,240,122)')),
                  go.Scatter(x=X,
                             y=analyse_loiNormale(fichier2,X,1,20),
                             mode='lines',
                             showlegend=False,
                             line=dict(width=2,color='rgb(25,24,122)')),
                  go.Scatter(x=X,
                             y=analyse_loiNormale(fichier3,X,1,20),
                             mode='lines',
                             showlegend=False,
                             line=dict(width=2,color='rgb(255,24,0)'))]
    
    Fig1 = go.Figure(data=Sig1)
    
    
    metric_figure = make_subplots(
        rows=1, cols=2,
        x_title='Erreur moyenne mu en mètre',
        y_title='Moyenne des facteurs de forme<br>(20 tirages pour chaque mu )',
        specs=[[{}, {}]],
        subplot_titles=("Avec Sigma=0.15 , faible dispersion",
                        "Avec Sigma=1"))
    metric_figure.update_layout(title_text="<em>Evolution de la moyenne du facteur de forme en fonction de l'erreur de position appliquée aux sommets des bâtiments</em>")
    
    for t in Fig015.data:
        metric_figure.append_trace(t, row=1, col=1)
    for t in Fig1.data:
        metric_figure.append_trace(t, row=1, col=2)
    
    if src=='1':
        plot(metric_figure, filename='Annexes/FormFactor/formfactor_BD_TOPO.html')
        print("Voir le fichier 'Annexes/FormFactor/formfactor_BD_TOPO.html'")
    elif src=='2':
        plot(metric_figure, filename='Annexes/FormFactor/formfactor_OSM.html')
        print("Voir le fichier 'Annexes/FormFactor/formfactor_OSM.html'")
    
    
   
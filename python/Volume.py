# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 21:07:23 2021

@author: HEAU BAL FILLON

INDICATEUR : Volume
Script permettant d'observer les effets de diverses perturbations sur le volume des bâtiments
"""

# importation des librairies
import perturbations.suppressionBatiment as sup
import perturbations.modificationgeomBatiment as md
import traitement.traiterJson as js

import random as rd
from shapely.geometry import Polygon
import numpy as np
import matplotlib.pyplot as plt
import math as ma
import os


from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot


def volume_total(data):
    """
    Calcul du volume total (somme des volumes de tous les bâtiments) pour un fichier JSON
    Il est nécessaire de connaître les hauteurs des bâtiments dans les attributs. 
    ----------
    data : TYPE
        DESCRIPTION.

    Returns
    -------
    V : TYPE
        DESCRIPTION.

    """
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

    
    return listeVolume


"""
Programme permettant de calculer comment faire varier les paramètres de suppression, d'imprécision xy et d'imprécision 
sur la hauteur pour avoir un taux d'erreur de 10%'
"""

def taux_erreur(volume_ini,volume_nv):
    return (abs(volume_ini-volume_nv))/volume_ini


def calcul_volume_nv(data,t,mu_g,sigma_g,mu_h,sigma_h,borne):
    """
    Fonction qui calcule le nouveau volume total en prennant en compte les différentes perturbations
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
    data=md.changement_sommet(data,mu_g,sigma_g,borne)
    
    
    # Perturbation qui consiste à modifier la géométrie
    ### paramètres qui varient (mu_h et sigma_h )
    data=md.changement_hauteur(data,mu_h,sigma_h)
    
    
    volume=volume_total(data)
    
    return volume
    

def calcul_volume_nv_moyen(data,t,mu_g,sigma_g,mu_h,sigma_h,borne):
    """
    Fonction qui calcule le nouveau volume moyen en prennant en compte les différentes perturbations
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
    data=md.changement_sommet(data,mu_g,sigma_g,borne)
    
    
    # Perturbation qui consiste à modifier la géométrie
    ### paramètres qui varient (mu_h et sigma_h )
    data=md.changement_hauteur(data,mu_h,sigma_h)
    
    # on compte le nombre de bâtiments
    nbBat = len(data['features'])
    
    volume_moyen=volume_total(data)/nbBat
    
    return volume_moyen


 
if __name__ == '__main__':
    
    os.chdir('..') 
    
    fichier1='Fichier_JSON/zoneMixte.json'
    fichier2='Fichier_JSON/zoneCentre.json'
    fichier3='Fichier_JSON/zonePeri.json'
    
    ## pas de fichier OSM, la hauteur des bâtiments n'y est pas présente, le volume n'est donc pas calculable
    

    ### Selection de la perturbation à appliquer
    print("INDICATEUR GEOCLIMATIQUE : Volume ")
    print('')
    print('Comment voulez-vous le perturber ?')
    print("Voir readme pour plus d'informations sur nos indicateurs et perturbations")
    print('')
    print(" 1 Suppression de bâtiments ")
    print(" 2 Modification de géométrie ")
    print(" 3 Les deux ")
    print('')
    perturbation=input('Tapez 1,2 ou 3\n')
    
    if perturbation=='1':
        X=[i/1000 for i in range(200)]
        tirages=20
        
        analyse_volume_BD_TOPO = [go.Scatter(x=X,
                                 y=analyse_suppression(fichier1,tirages),
                                 mode='lines',
                                 name='Zone Mixte',
                                 line=dict(width=2,color='rgb(0,240,122)')),
                      go.Scatter(x=X,
                                 y=analyse_suppression(fichier2,tirages),
                                 mode='lines',
                                 name='Zone Centre',
                                 line=dict(width=2,color='rgb(25,24,122)')),
                      go.Scatter(x=X,
                                 y=analyse_suppression(fichier3,tirages),
                                 mode='lines',
                                 name='Zone Périphérique',
                                 line=dict(width=2,color='rgb(255,24,0)'))]
                                 
        
        FigTOPO = go.Figure(data=analyse_volume_BD_TOPO)
        
        
        metric_figure = make_subplots(
            rows=1, cols=1,
            x_title='Taux de suppression des bâtiments',
            y_title="Rapport entre le volume total après la suppression <br>et le volume total avant la suppression",
            subplot_titles=("Avec les données BD_TOPO"))
            
        metric_figure.update_layout(title_text="<em>Evolution du volume total occupé par les bâtiments en fonction du taux de suppression des bâtiments (20 tirages pour chaque taux)</em>")
        
        for t in FigTOPO.data:
            metric_figure.append_trace(t, row=1, col=1)
        
        
        
        plot(metric_figure, filename='Annexes/Volume/volume_suppression.html')
        print("Voir le fichier 'Annexes/Volume/volume_suppression.html'")
        
        
        
    elif perturbation=='2':
        
        
        print("Choisissez le taux de suppression(0 si aucune suppression souhaitée et <0.3)")
        taux=float(input("Taux: "))
        print('')
        print('Choisissez la zone souhaitée')
        print('')
        print(" 1 Zone Mixte ")
        print(" 2 Zone Centre ")
        print(" 3 Zone Périphérique ")
        print('')
        zone=input('Tapez 1,2 ou 3\n')
        
        # Intervalles sur Sigma et Mu (pour la modification de géométries)
        SI=[i/10 for i in range(2)]
        MU=[i/10 for i in range(5)]
        
        if zone=='1':
            fichier=fichier1
            z='ZoneMixte'
        elif zone=='2':
            fichier=fichier2
            z='ZoneCentre'
        elif zone=='3':
            fichier=fichier3
            z='ZonePeripherique'
            
        data=js.ouvre_json(fichier)    
        Volume_INITIAL=volume_total(data)
        
    
        List_ERREUR=[]
    
        v=len(SI)*len(MU)
        w=0
        
        for m in MU:
            print('-- --')
            l=[]
            for s in SI:
                w+=1
                print("{} %".format(round((w/v)*100,3)))
                Volume_NV=0
                for _ in range(10):
                    # Pour chaque moyenne m et ecart-type s, le nouveau volume calculé est 
                    #la moyenne de 10 tirages
                    data=js.ouvre_json(fichier)
                    incre=calcul_volume_nv(data,taux,m,s,m,s,7)
                    Volume_NV+=incre
                Volume_NV/=10
                TAUX_ERREUR=taux_erreur(Volume_INITIAL,Volume_NV)
                l.append(TAUX_ERREUR)
            List_ERREUR.append(l)    
        print(List_ERREUR)
        
        
              
        heatmap = go.Figure(data =
            go.Contour(
                z=List_ERREUR,
                x=MU, # horizontal axis
                y=SI # vertical axis
            ),)
        
         
        
        fig= make_subplots(
            rows=1, cols=1,
            x_title='Erreur moyenne mu en mètre',
            y_title='Ecart-type Sigma',
            subplot_titles=("Taux de suppression fixé à {}".format(taux)))
        fig.update_layout(title_text="<em>Erreur sur le volume moyen sous forme carte de chaleur</em> <br> (Taux de suppression fixé à 0 et moyenne de 10 tirages aléatoires pour chaque point de la nappe de chaleur)")
        
       
        fig.add_trace(go.Contour(z=List_ERREUR, x=MU, y=SI), 1, 1)
        
        plot(fig, filename='Annexes/Volume/volume_modification_{}_taux{}.html'.format(z,taux))
        print("Voir le fichier 'Annexes/Volume/volume_modification.html'")
        
    elif perturbation=='3':
        
        
        print("Pour cette partie, l'affichage est simplement un échantillon, pour plus d'informations sur ce mode, voir le readme")
        
        print('Choisissez la zone souhaitée')
        print('')
        print(" 1 Zone Mixte ")
        print(" 2 Zone Centre ")
        print(" 3 Zone Périphérique ")
        print('')
        zone=input('Tapez 1,2 ou 3\n')
        print("Sigma est fixé à 1 pour avoir la moyenne MU et le taux comme paramètres")
        
        # Intervalles sur Sigma et Mu et T (pour la modification de géométries)
        T=T=[i/400 for i in range(4)]
        #SI=[i/10 for i in range(2)]
        MU=[i/10 for i in range(5)]
        
        if zone=='1':
            fichier=fichier1
            z='ZoneMixte'
        elif zone=='2':
            fichier=fichier2
            z='ZoneCentre'
        elif zone=='3':
            fichier=fichier3
            z='ZonePeripherique'
            
        data=js.ouvre_json(fichier)    
        Volume_INITIAL=volume_total(data)
        
    
        List_ERREUR=[]
    
        v=len(T)*len(MU)
        w=0
        
        for m in MU:
            print('-- --')
            l=[]
            for t in T:
                w+=1
                print("{} %".format(round((w/v)*100,3)))
                Volume_NV=0
                for _ in range(10):
                    data=js.ouvre_json(fichier)
                    incre=calcul_volume_nv(data,t,m,1,m,1,7)
                    Volume_NV+=incre
                Volume_NV/=10
                TAUX_ERREUR=taux_erreur(Volume_INITIAL,Volume_NV)
                l.append(TAUX_ERREUR)
            List_ERREUR.append(l)    
        print(List_ERREUR)
        
        
              
        layout = go.Layout(
        title="Taux d'erreur sur le volume total<br> 10 tirages à chaque valeur<br>{}<br>x : Taux de suppression <br>y : Moyenne Mu ".format(z),
        legend_title=z,autosize=False,
        width=600, height=600,
        margin=dict(l=65, r=50, b=65, t=90)
        )
        
        
        
    
        tr1=go.Surface(x=T, y=MU, z=List_ERREUR, colorscale='Viridis', showscale=False)
        
        
        
        fig = make_subplots(
        rows=1, cols=1,
        x_title='Erreur moyenne mu en mètre',
        y_title='Taux de suppression',
        subplot_titles=("Ecart-type fixé à 1"))
        
        # Taux d'erreur à 5%
        Z = np.ones(np.shape(List_ERREUR))*0.05
        tr2=go.Surface(x=T, y=MU, z=Z, colorscale='Viridis', showscale=False)
        
        
    
        
        data=[tr1,tr2]
        fig = go.Figure(data=data, layout=layout)
        fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                      highlightcolor="limegreen", project_z=True))
       
        
        plot(fig, filename='Annexes/Volume/volume_modification&suppression_{}.html'.format(z))
        print("Voir le fichier 'Annexes/Volume/volume_modification&suppression.html'")
        
        
        
        
        
        
        
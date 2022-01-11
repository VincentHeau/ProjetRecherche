# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 11:27:24 2022

@author: HEAU BAL FILLON

Script permettant de visualiser les l'influence de différentes perturbations sur le paramètre AIRE
(voir paramètre AIRE dans le readme)

Différentes perturbations peuvent-être choisies au début du script
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


def aire_total(data):
    A=0
    for i in range(len(data['features'])):

        a=data['features'][i]['attributes']['Shape_Area']
        
        A+=a
    return A 


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
    aire_norm=aire_total(js.ouvre_json(fichier))
    
    
    listeAire =[]
    
    for taux in X:
        #On fait varier le taux de suppression
        a=0
        for i in range(tirages):
            new_data=sup.suppression(taux,js.ouvre_json(fichier))
            a+=aire_total(new_data)
        aire=a/tirages
        aire=aire/aire_norm
        listeAire.append(aire)
          
        print("fin tour avec un taux de :",taux) 
    """
    plt.plot(X,listeAire)
    plt.xlabel("Taux de suppression des bâtiments")
    plt.ylabel("Aire total occupé par les bâtiments")
    plt.title("Evolution de l'aire total occupé par les bâtiments \nen fonction du taux de suppression des bâtiments.")
    plt.savefig("Annexes/Volume/graphique_volume_suppression_bis__{0}.png".format(n))
    """
    
    
    return listeAire

"""
Programme permettant de calculer comment faire varier les paramètres de suppression, d'imprécision xy et d'imprécision 
sur la hauteur pour avoir un taux d'erreur de 10%'
"""

def taux_erreur(aire_ini,aire_nv):
    return (abs(aire_ini-aire_nv))/aire_ini


def calcul_aire_nv(data,t,mu_g,sigma_g,mu_h,sigma_h,borne):
    """
    Fonction qui calcule la nouvelle aire en prennant en compte les différentes perturbations
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
    
    
    aire=aire_total(data)
    
    return aire
    

def calcul_aire_nv_moyen(data,t,mu_g,sigma_g,mu_h,sigma_h,borne):
    """
    Fonction qui calcule la nouvelle aire moyenne en prennant en compte les différentes perturbations
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
    
    aire_moyen=aire_total(data)/nbBat
    
    return aire_moyen


 
    
 
if __name__ == '__main__':
    
    os.chdir('..') 
    
    fichier1='Fichier_JSON/zoneMixte.json'
    fichier2='Fichier_JSON/zoneCentre.json'
    fichier3='Fichier_JSON/zonePeri.json'
    
    fichier11='Fichier_JSON/zoneMixteOSM.json'
    fichier22='Fichier_JSON/zoneCentreOSM.json'
    fichier33='Fichier_JSON/zonePeriOSM.json'

    ### Selection de la perturbation à appliquer
    print("INDICATEUR GEOCLIMATIQUE : Aire ")
    print('')
    print('Comment voulez-vous la perturber ?')
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
        
        analyse_aire_BD_TOPO = [go.Scatter(x=X,
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
                                 
        analyse_aire_OSM = [go.Scatter(x=X,
                                 y=analyse_suppression(fichier11,tirages),
                                 mode='lines',
                                 name='Zone Mixte',
                                 line=dict(width=2,color='rgb(0,240,122)'),
                                 showlegend=False),
                      go.Scatter(x=X,
                                 y=analyse_suppression(fichier22,tirages),
                                 mode='lines',
                                 name='Zone Centre',
                                 line=dict(width=2,color='rgb(25,24,122)'),
                                 showlegend=False),
                      go.Scatter(x=X,
                                 y=analyse_suppression(fichier33,tirages),
                                 mode='lines',
                                 name='Zone Périphérique',
                                 line=dict(width=2,color='rgb(255,24,0)'),
                                 showlegend=False)]
        
        FigTOPO = go.Figure(data=analyse_aire_BD_TOPO)
        FigOSM  = go.Figure(data=analyse_aire_OSM)
        
        
        metric_figure = make_subplots(
            rows=1, cols=2,
            x_title='Taux de suppression des bâtiments',
            y_title="Rapport entre l'aire totale après la suppression et l'aire totale avant la suppression",
            specs=[[{}, {}]],
            subplot_titles=("Avec les données BD_TOPO",
                            "Avec les données OSM"))
            
        metric_figure.update_layout(title_text="<em>Evolution de l'aire totale occupée par les bâtiments en fonction du taux de suppression des bâtiments (20 tirages pour chaque taux)</em>")
        
        for t in FigTOPO.data:
            metric_figure.append_trace(t, row=1, col=1)
        for t in FigOSM.data:
            metric_figure.append_trace(t, row=1, col=2)
        
        
        
        plot(metric_figure, filename='Annexes/Aire/aire_suppression.html') 
        print("Voir le fichier 'Annexes/Aire/aire_suppression.html'")
        
        
        
    elif perturbation=='2':
        
        
        print("Choisissez le taux de suppression (0 si aucune suppression souhaitée et <0.3)")
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
        SI=[i/10 for i in range(20)]
        MU=[i/10 for i in range(50)]
        
        if zone=='1':
            fichierTOPO=fichier1
            fichierOSM=fichier11
            z='ZoneMixte'
        elif zone=='2':
            fichierTOPO=fichier2
            fichierOSM=fichier22
            z='ZoneCentre'
        elif zone=='3':
            fichierTOPO=fichier3
            fichierOSM=fichier33
            z='ZonePeripherique'
            
        dataTOPO=js.ouvre_json(fichierTOPO)
        dataOSM=js.ouvre_json(fichierOSM)
        
        Aire_INITIALE_TOPO=aire_total(dataTOPO)
        Aire_INITIALE_OSM=aire_total(dataOSM)
        
    
        List_ERREUR_TOPO,List_ERREUR_OSM=[],[]
    
        v=len(SI)*len(MU)
        w=0
        
        for m in MU:
            print('-- --')
            OSM,TOPO=[],[]
            for s in SI:
                w+=1
                print("{} %".format(round((w/v)*100,3)))
                Aire_NV_TOPO,Aire_NV_OSM=0,0
                for _ in range(10):
                    
                    dataTOPO=js.ouvre_json(fichierTOPO)
                    dataOSM=js.ouvre_json(fichierOSM)
                    
                    incre_TOPO=calcul_aire_nv(dataTOPO,taux,m,s,m,s,7)
                    incre_OSM=calcul_aire_nv(dataOSM,taux,m,s,m,s,7)
                    
                    Aire_NV_TOPO+=incre_TOPO
                    Aire_NV_OSM+=incre_OSM
                    
                Aire_NV_TOPO/=10
                Aire_NV_OSM/=10
                
                
                TAUX_ERREUR_TOPO=taux_erreur(Aire_INITIALE_TOPO,Aire_NV_TOPO)
                TAUX_ERREUR_OSM=taux_erreur(Aire_INITIALE_OSM,Aire_NV_OSM)
                
                
                TOPO.append(TAUX_ERREUR_TOPO)
                OSM.append(TAUX_ERREUR_OSM)
                
            List_ERREUR_TOPO.append(TOPO)
            List_ERREUR_OSM.append(OSM)  
            
            Diff=list(np.array(List_ERREUR_TOPO)-np.array(List_ERREUR_OSM))
            
        print(List_ERREUR_TOPO,List_ERREUR_OSM,Diff)
        
        
        """     
        heatmap_TOPO = go.Figure(data =
            go.Contour(
                z=List_ERREUR_TOPO,
                x=MU, # horizontal axis
                y=SI # vertical axis
            ),)
        
        heatmap_OSM = go.Figure(data =
            go.Contour(
                z=List_ERREUR_OSM,
                x=MU, # horizontal axis
                y=SI # vertical axis
            ),)
        
        heatmap_Diff = go.Figure(data =
            go.Contour(
                z=Diff,
                x=MU, # horizontal axis
                y=SI # vertical axis
            ),)
        
         """
        
        fig= make_subplots(
            rows=2, cols=2,
            x_title='Ecart-type Sigma',
            y_title='Erreur moyenne mu en mètre',
            specs=[[{},{}],[{},{}]],
            subplot_titles=("Avec les données BD_TOPO",
                            "Avec les données OSM",
                            "Différence des deux nappes"))
            
    
        fig.update_layout(height=1500, width=1400,title_text="<em>Erreur sur l'aire moyenne sous forme carte de chaleur</em> <br> (Taux de suppression fixé à {} et moyenne de 10 tirages aléatoires pour chaque point de la nappe de chaleur)".format(taux))
        
       
        fig.add_trace(go.Contour(z=List_ERREUR_TOPO, x=MU, y=SI,colorbar=dict(yanchor="bottom")), 1, 1)
        fig.add_trace(go.Contour(z=List_ERREUR_OSM, x=MU, y=SI,showscale=False), 1, 2)
        fig.add_trace(go.Contour(z=Diff, x=MU, y=SI,colorbar=dict(yanchor="top"),colorscale='Viridis'), 2, 1)
        
        plot(fig, filename='Annexes/Aire/aire_modification_{}_taux{}.html'.format(z,taux))
        print("Voir le fichier 'Annexes/Aire/aire_modification.html'")
        
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
            
        dataTOPO=js.ouvre_json(fichierTOPO)
        dataOSM=js.ouvre_json(fichierOSM)
        
        Aire_INITIALE_TOPO=aire_total(dataTOPO)
        Aire_INITIALE_OSM=aire_total(dataOSM)
        
    
        List_ERREUR_TOPO,List_ERREUR_OSM=[],[]
        
    
        v=len(T)*len(MU)
        w=0
        
        for m in MU:
            print('-- --')
            OSM,TOPO=[],[]
            for t in T:
                w+=1
                print("{} %".format(round((w/v)*100,3)))
                Aire_NV_TOPO,Aire_NV_OSM=0,0
                for _ in range(10):
                    
                    dataTOPO=js.ouvre_json(fichierTOPO)
                    dataOSM=js.ouvre_json(fichierOSM)
                    
                    incre_TOPO=calcul_aire_nv(dataTOPO,t,m,1,m,1,7)
                    incre_OSM=calcul_aire_nv(dataOSM,t,m,1,m,1,7)
                    
                    Aire_NV_TOPO+=incre_TOPO
                    Aire_NV_OSM+=incre_OSM
                    
                Aire_NV_TOPO/=10
                Aire_NV_OSM/=10
                
                
                TAUX_ERREUR_TOPO=taux_erreur(Aire_INITIALE_TOPO,Aire_NV_TOPO)
                TAUX_ERREUR_OSM=taux_erreur(Aire_INITIALE_OSM,Aire_NV_OSM)
                
                
                TOPO.append(TAUX_ERREUR_TOPO)
                OSM.append(TAUX_ERREUR_OSM)
                
            List_ERREUR_TOPO.append(TOPO)
            List_ERREUR_OSM.append(OSM)  
            
            Diff=list(np.array(List_ERREUR_TOPO)-np.array(List_ERREUR_OSM))
            
        print(List_ERREUR_TOPO,List_ERREUR_OSM,Diff)
              
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
    
    
   
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 13:28:23 2021

@author: HEAU
"""

from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
from plotly.graph_objs import *
import rc_volume as rc
import traitement.traiterJson as tt
import Volume as V
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go
init_notebook_mode()




if __name__ == '__main__':
    
    
    os.chdir("..")
        
    fichier1='Fichier_JSON/zoneMixte.json'
    fichier2='Fichier_JSON/zoneCentre.json'
    fichier3='Fichier_JSON/zonePeri.json'
    
    data1=tt.ouvre_json(fichier1)
    data2=tt.ouvre_json(fichier2)
    data3=tt.ouvre_json(fichier3)
    
    T=[i/100 for i in range(50)]
    MU=[i/100 for i in range(30)]
    
    Volume_INITIAL=V.volume_total(data1)
    
    
    List_ERREUR=[]
    
    for taux in T:
        print('-- --')
        l=[]
        for mu in MU:
            print("____")
            Volume_NV=rc.calcul_volume_nv(data1,taux,mu,0.15,mu,0.15)
            TAUX_ERREUR=rc.taux_erreur(Volume_INITIAL,Volume_NV)
            l.append(TAUX_ERREUR)
        List_ERREUR.append(l)    
    print(List_ERREUR)
    
    
    layout = Layout(
    title='La nappe', autosize=False,
    width=500, height=500,
    margin=dict(l=65, r=50, b=65, t=90)
    )


    fig = dict( data=[go.Surface(
        x = T,
        y = MU,
        z = List_ERREUR
        )], layout=layout )
    
    plot(fig) 

    
    
    
    
    
    
    
    
    
    
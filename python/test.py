# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 13:28:23 2021

@author: HEAU
"""

from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
from plotly.graph_objs import *
from plotly.subplots import make_subplots
import rc_volume as rc
import plotly.express as px

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
    
    T=[i/100 for i in range(40)]
    MU1=[i/100 for i in range(20)]
    MU2=[i for i in range(10)]
    
    Volume_INITIAL=V.volume_total(data1)
    
    
    List_ERREUR=[]
    
    for m2 in MU2:
        print('-- --')
        l=[]
        for t in T:
            print("____")
            data1=tt.ouvre_json(fichier1)
            Volume_NV=rc.calcul_volume_nv(data1,t,m2,0.15,m2,0.15)
            TAUX_ERREUR=rc.taux_erreur(Volume_INITIAL,Volume_NV)
            l.append(TAUX_ERREUR)
        List_ERREUR.append(l)    
    print(List_ERREUR)
    
    
    layout = Layout(
    title='La nappe', autosize=False,
    width=600, height=600,
    margin=dict(l=65, r=50, b=65, t=90)
    )
    
    
    

    tr1=go.Surface(x=T, y=MU2, z=List_ERREUR, colorscale='Viridis', showscale=False)
    
    
    
    fig = make_subplots(
    rows=2, cols=2,
    specs=[[{'type': 'surface'}, {'type': 'surface'}],
           [{'type': 'surface'}, {'type': 'surface'}]])
    
    # Taux d'erreur à 10%
    z = np.ones(np.shape(List_ERREUR))*0.1
    
    
    tr2=go.Surface(x=T, y=MU2, z=z, colorscale='Viridis', showscale=False)
    # adding surfaces to subplots.
    """
    fig.add_trace(
        go.Surface(x=T, y=MU, z=List_ERREUR, colorscale='Viridis', showscale=False),
        row=1, col=1)
    
    fig.add_trace(
        go.Surface(x=x, y=y, z=z, colorscale='RdBu', showscale=False),
        row=1, col=2)
    
    fig.add_trace(
        go.Surface(x=x, y=y, z=z, colorscale='YlOrRd', showscale=False),
        row=2, col=1)
    
    fig.add_trace(
        go.Surface(x=x, y=y, z=z, colorscale='YlGnBu', showscale=False),
        row=2, col=2)
    
    fig.update_layout(
        title_text='3D subplots with different colorscales',
        height=800,
        width=800
    )
    
    """

    
    data=[tr1,tr2]
    fig = go.Figure(data=data, layout=layout)
    fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                  highlightcolor="limegreen", project_z=True))
    """
    fig.add_trace(
        go.Surface(x=T, y=MU2, z=List_ERREUR, colorscale='YlGnBu', showscale=False),
        row=1, col=1)
    """
    
    fig.update_xaxes(title_text='Taux de suppression des bâtiments')
    fig.update_yaxes(title_text='Variation du mu lors de la modification des bâtiments')
    plot(fig)
    

    #plot(fig) 

    
    
    
    
    
    
    
    
    
    
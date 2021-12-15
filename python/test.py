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
    
    T=[i/400 for i in range(140)]
    MU1=[i/100 for i in range(20)]
    MU2=[i/10 for i in range(100)]
    
    MU=[i/20 for i in range(100)]
    
    Volume_INITIAL=V.volume_total(data1)
    
    
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
                data1=tt.ouvre_json(fichier1)
                incre=rc.calcul_volume_nv(data1,t,m,0.15,m,0.15)
                Volume_NV+=incre
            Volume_NV/=10
            TAUX_ERREUR=rc.taux_erreur(Volume_INITIAL,Volume_NV)
            l.append(TAUX_ERREUR)
        List_ERREUR.append(l)    
    print(List_ERREUR)
    
    
    layout = Layout(
    title="Zone Mixte",
    legend_title="Zone Mixte",autosize=False,
    width=600, height=600,
    margin=dict(l=65, r=50, b=65, t=90)
    )
    


    
    

    tr1=go.Surface(x=T, y=MU, z=List_ERREUR, colorscale='Viridis', showscale=False)
    
    
    
    fig = make_subplots(
    rows=2, cols=2,
    specs=[[{'type': 'surface'}, {'type': 'surface'}],
           [{'type': 'surface'}, {'type': 'surface'}]])
    
    # Taux d'erreur à 10%
    z = np.ones(np.shape(List_ERREUR))*0.05
    
    
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
        go.Surface(x=T, y=MU, z=List_ERREUR, colorscale='YlGnBu', showscale=False),
        row=2, col=2)
    """

    
    plot(fig)
    


    
    
    
    
    
    
    
    
    
    
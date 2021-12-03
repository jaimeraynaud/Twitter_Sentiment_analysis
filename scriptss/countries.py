import plotly.graph_objs as go
import dash
from dash.dcc.Graph import Graph
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
from scriptss.database import DataBase
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

    
def getCountryList(data, db):
    df = data[['geo_location', 'label']]
    countries = df.geo_location.unique().tolist()
    newDf = pd.DataFrame({'Countries': countries})
    for i in countries:
        labels = ['pos', 'neg', 'neu']
        total = len(df[(df.geo_location == i)])
        for x in labels:
            counting = len(df[(df.geo_location == i) & (df.label == x)])
            count = round(counting/total*100)
            newDf.loc[newDf.Countries == i, x] = count

            
    df = newDf
    #maxValue= df[['pos','neg','neu']].max(axis=1)
    # df['col name'] = df[['pos','neg','neu']].idxmax(axis=1)
    df['diff'] = df['pos'] - df['neg']
    db.upload_data(df, name='countrySentiment', error='replace')
    print(df)

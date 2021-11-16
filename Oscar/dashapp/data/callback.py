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

app = dash.Dash(__name__)
@app.callback(dash.dependencies.Output('graph', 'figure'),
        [dash.dependencies.Input('Country', 'value')])


def graph_update(selected_value):
    print(selected_value)
    #columns = ['Positive_reviews', 'Negative_reviews']


    if selected_value == 'allCntry':
        fig = {'data': [{'x': df['Countries'], 'y': df['pos'], 'type': 'bar',
                         'name': 'Positive reviews per Country'}]}
        return fig
    else:
        data = df.loc[df['Countries'] == selected_value]
        cols = ['pos', 'neg', 'neu']
        # fig = data.plot(x='Country', y=cols, kind='bar')
        fig = {'data': [
            {'x': selected_value, 'y': df.loc[df['Countries'] == selected_value, 'pos'],
                'type': 'bar', 'name': 'Positive reviews per Country'}]}

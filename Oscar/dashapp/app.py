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

# app = dash.Dash(__name__)
# @app.callback(dash.dependencies.Output('graph', 'figure'),
#         [dash.dependencies.Input('Country', 'value')])

def graph_update(selected_value):
    df = pd.DataFrame({'Country': ["Germany", "England", "Spain"],
                    'Positive_reviews': [8000, 12000, 9000],
                    'Negative_reviews': [3000, 4000, 2000]})
    if selected_value == 'allCntry':
        fig = {'data': [{'x': df['Country'], 'y': df['Positive_reviews'], 'type': 'bar',
                         'name': 'Positive reviews per Country'}]}
        return fig
    else:
        fig = {'data': [
            {'x': selected_value, 'y': df.loc[df['Country'] == selected_value, 'Positive_reviews'],
                'type': 'bar', 'name': 'Positive reviews per Country'}]}
        return fig

def dashboard(data):
    df = data[['geo_location', 'label']]
    countries = df.geo_location.unique().tolist()
    newDf = pd.DataFrame({'Countries': countries})
    newDf2 = pd.DataFrame({'Countries': countries})
    for i in countries:
        labels = ['pos', 'neg', 'neu']
        total = len(df[(df.geo_location == i)])
        for x in labels:
            counting = len(df[(df.geo_location == i) & (df.label == x)])
            count = round(counting/total*100)
            newDf.loc[newDf.Countries == i, x] = count
            newDf2.loc[newDf2.Countries == i, x] = counting
    df2 = newDf2
    df = newDf

    # ger = df.query("Country == 'Germany'")
    # eng = df.query("Country == 'England'")
    # sp = df.query("Country == 'Spain'")

    #query = df.iloc.columns("Country == 'Germany'")
    #print(query.columns['Positive_reviews'])
    #allCntry = {'data': [{'x': df['Countries'], 'y': df['pos'], 'type': 'bar', 'name': 'Positive reviews per Country'}]}
    ger = {'data': [{'x': df.loc[df['Countries'] == 'Germany'], 'y': df['pos'], 'type': 'bar', 'name': 'Positive reviews per Country'}]}
    negCntry = {'data': [{'x': df['Countries'], 'y': df['neg'], 'type': 'bar', 'name': 'Positive reviews per Country'}]}
    #allCntry = px.bar(df, x="Countries", y="pos", barmode="group")
    #allCntry = df.plot.bar(rot=0)
    allCntry = px.bar(df, x="Countries", y=['pos','neg','neu'], title="Positive, Negative and Neutral Tweets")
    allCntryNum = px.bar(df2, x="Countries", y=['pos','neg','neu'], title="Positive, Negative and Neutral Tweets")
    # Initialise the app# Initialize the app
    app = dash.Dash(__name__)
    app.config.suppress_callback_exceptions = True

    # Define the app
    app.layout = html.Div(
        children=[
            html.Div(className='row',
                    children=[
                        html.Div(className='four columns div-user-controls',
                                children=[
                                    html.H2('Positive reviews per country'),
                                    # html.P('Visualising time series with Plotly - Dash.'),
                                    # html.P('Pick a country from the dropdown below.'),
                                    # html.Div(
                                    #     className='countryselector',
                                    #     children=[dcc.Dropdown(
                                    #         id="Country",
                                    #         options=[
                                    #             {'label': 'All Countries', 'value': 'allCntry'},
                                    #             {'label': 'Germany', 'value': 'Germany'},
                                    #             {'label': 'England', 'value': 'England'},
                                    #             {'label': 'Spain', 'value': 'Spain'}
                                    #         ],
                                    #         style={'color': '#1E1E1E'},
                                    #         optionHeight=35,
                                    #         value='allCntry',
                                    #         multi=False,
                                    #         searchable=False,
                                    #         placeholder='Select a country',
                                    #         clearable=False, )
                                    #     ]
                                    # ),
                                    html.Div(className='eight columns div-for-charts bg-grey',
                                            children=[
                                                dcc.Graph(id='graph', figure=allCntry)
                                            ]),
                                    html.Div(className='eight columns div-for-charts bg-grey',
                                            children=[
                                                dcc.Graph(id='graph2', figure=allCntryNum)
                                            ]),
                                ]),
        ]

    )
        ])
    

    app.run_server(debug=True)
    
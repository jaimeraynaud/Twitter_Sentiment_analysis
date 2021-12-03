import dash
from dash.dcc.Graph import Graph
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import pandas as pd


"""Monthly/weekly/daily representation where refugees are
   Prediction where refugees will be in a week.
   Preferably on a map with an average location or the country where the refugees are
   Some statistics about how many, age, etc.
   """
global product_df
data = pd.DataFrame({'Country': ["Germany", "England", "Spain"], 'Positive reviews': [8234, 7654, 4312]})
product_df = pd.DataFrame(data)


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
        html.H1(children="Dashboard"),
        html.P(children="Wouter gey"),
        dcc.Dropdown(id='demo-dropdown',
        options=[
            {'label': 'Germany', 'value': 'GER'},
            {'label': 'England', 'value': 'ENG'},
            {'label': 'Spain', 'value': 'SP'}
        ],
        value='Germany'),
        dcc.Graph(
            figure={
                    "data": [
                        {
                            "x": data["Country"],
                            "y": data["Positive reviews"],
                            "type": "bar",
                        },
                    ],
                    "layout": {"title": "Positive reviews per country"},
                },
            ),
    html.Div(id='dd-output-container')],
)

@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)


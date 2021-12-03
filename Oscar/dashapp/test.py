import plotly.graph_objs as go
import dash
from dash.dcc.Graph import Graph
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
#from scripts.database import DataBase
import pandas as pd
import plotly.express as px

# app.layout = html.Div([
#     html.H2("Sales Funnel Report"),
#     html.Div(
#         [
#             dcc.Dropdown(
#                 id="Manager",
#                 options=[{
#                     'label': i,
#                     'value': i
#                 } for i in mgr_options],
#                 value='All Managers'),
#         ],
#         style={'width': '25%',
#                'display': 'inline-block'}),
#     dcc.Graph(id='funnel-graph'),
# ])

#DataFrame containing the values of the positive and negative reviews of each country
df = pd.DataFrame({'Country': ["Germany", "England", "Spain", "Germany", "England", "Spain"],
                   'Reviews': [8000, 12000, 9000, 3000, 4000, 2000],
                   'Label': ['Positive reviews', 'Positive reviews', 'Positive reviews', 'Negative reviews',
                             'Negative reviews', 'Negative reviews']})

#DataFrame bar figures
fig = px.bar(df, x="Country", y="Reviews", color="Label", barmode="group")
figger = px.bar(df, x="Country", y="Reviews", color="Label", barmode="group")
#Selecting between countries
cntry_options = pd.DataFrame({'Countries': ['All', 'Germany', 'England', 'Spain']})

#Start dash and dash server
app = dash.Dash(__name__)
server = app.server

#HTML Layout
app.layout = html.Div(children=[
    html.H1(children="Dashboard"),
    html.P(children="Wouter gey"),
    html.Div(
        [
            dcc.Dropdown(
                id="Countries",
                options=[{
                    'label': i,
                    'value': i
                } for i in cntry_options],
                value='All Countries'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),

    dcc.Graph(
        id='funnel-graph',
        figure=fig
    ),
    html.Div(id='dd-output-container')],
)


@app.callback(
    dash.dependencies.Output('my-output', 'children'),
    [dash.dependencies.Input('my-input', 'value')])

def update_graph(Countries):
    if Countries == 'All':
        df_plot = df.copy()
    else:
        df_plot = df[df['Countries'] == Countries]

    pv = pd.pivot_table(
        df_plot,
        index=['Countries'],
        columns=["Reviews"],
        values=['Quantity'],
        aggfunc=sum,
        fill_value=0)

    trace1 = go.Bar(x=pv.index, y=pv[('Quantity', 'declined')], name='Declined')
    trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pending')], name='Pending')
    trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presented')], name='Presented')
    trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'won')], name='Won')

    return {
        'data': [trace1, trace2, trace3, trace4],
        'layout':
        go.Layout(
            title='Customer Order Status for {}'.format(Countries),
            barmode='stack')
    }


if __name__ == '__main__':
    app.run_server(debug=True)
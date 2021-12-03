import plotly.graph_objs as go
import dash
from dash.dcc.Graph import Graph
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
# from scripts.database import DataBase
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

df = pd.DataFrame({'Country': ["Germany", "England", "Spain"],
                   'Positive_reviews': [8000, 12000, 9000],
                   'Negative_reviews': [3000, 4000, 2000]})

allCntry = px.bar(df, x="Country", y="Positive_reviews", barmode="group")
allCntry.show()



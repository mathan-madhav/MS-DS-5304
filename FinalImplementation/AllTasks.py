import plotly.express as px
import plotly.graph_objs as go
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
from FinalImplementation.app import app
from FinalImplementation.helpers import *

from FinalImplementation.Task1 import yearly_layout
from FinalImplementation.Task2 import map_layout
from FinalImplementation.Task3 import rank_layout

tab_style = {
            'borderBottom': '1px solid #d6d6d6',
            'padding': '6px',
            'fontWeight': 'bold'
        }

tab_selected_style = {
            'borderTop': '1px solid #d6d6d6',
            'borderBottom': '1px solid #d6d6d6',
            'backgroundColor': '#119DFF',
            'color': 'white',
            'padding': '6px'
        }


final_layout = html.Div([
    
   
        html.H1('Final Project: World Happiness Report - Data Visualization', style = {'display': 'inline-block','margin-left': '35px'}),
    
         dcc.Tabs(id="tab-dashboard", value='Country Rankings', 
                children=[
                    dcc.Tab(label='Country Rankings', 
                        value='Country Rankings', 
                        style=tab_style, 
                        selected_style=tab_selected_style,
                        children=yearly_layout),
                    dcc.Tab(label='Geo-Plot', 
                        value='Geo-Plot', 
                        style=tab_style, 
                        selected_style=tab_selected_style,
                        children=map_layout),
                    dcc.Tab(label='YoY Standings', 
                        value='YoY Standings', 
                        style=tab_style, 
                        selected_style=tab_selected_style,
                        children=rank_layout)
                ])
])
      
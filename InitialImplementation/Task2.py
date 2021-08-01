import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from InitialImplementation.app import app
from InitialImplementation.helpers import *


PREFIX = 'task2-'


map_layout = html.Div([
  
        html.Br(),
    
        dcc.Graph(id=PREFIX+'geo-map'),
                
        html.H3('Filters:'),
    
        html.Div([
            
                html.Label('Year'),
                html.Br(),
            
                dcc.Dropdown(
                    id=PREFIX+'map-year', 
                    clearable=False,
                    value=years[0],
                    options=[{'label': c, 'value': c} for c in years]
                )
            ],
            
            style = dropdown_style
        
        ),
        
        html.Div([
            
                html.Label('Metric'),
                html.Br(),
            
                dcc.Dropdown(
                    id=PREFIX+'map-metric', 
                    clearable=False,
                    value=metrics[0], 
                    options=[{'label': c, 'value': c} for c in metrics]
                )
            ],
            
            style = dropdown_style
        
        ),
    
        html.Br(),
        html.Br(),
    
        html.H3('Table View:'),

        html.Br(),
    
        dash_table.DataTable(
                    id=PREFIX+'map-table',
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    page_action="native",
                    export_format='xlsx',
                    style_cell={'textAlign': 'center', 'minWidth':'130%'},  
                    style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }
                    ],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    style_table={'overflowX': 'auto'}
            ),
         
    ])



@app.callback(
    Output(PREFIX+'geo-map', 'figure'),
    Output(PREFIX+'map-table', 'columns'),
    Output(PREFIX+'map-table', 'data'),
    [Input(PREFIX+"map-year", "value"),
     Input(PREFIX+"map-metric", "value")]
)
def update_map(year,metric):
    
    
    work_df = data.copy()
    work_df = data.query(f'year == {year}')

    d = dict (
        type = 'choropleth',
        locations = work_df['Country'],
        locationmode='country names',
        z=work_df[metric]
    )

    geo_plot = go.Figure(data=[d])
    
    geo_plot.update_layout(title={
        'text': "Geoplot - Happiness Report Summary - "+ str(year)+ " : " + metric + " <br>",
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
       title_font_size=20,
       margin={"r":0,"t":30,"l":0,"b":0}
     )
    
    table_columns = [{'name': c, 'id': c} for c in work_df.columns]
    table_data    =  work_df.to_dict('records')
   
    return geo_plot,table_columns,table_data


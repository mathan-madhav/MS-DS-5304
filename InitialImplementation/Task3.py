import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from InitialImplementation.app import app
from InitialImplementation.helpers import *
import dash_table

PREFIX = 'task3-'

rank_layout = html.Div([
  
        html.Br(),
    
        dcc.Graph(id=PREFIX+'graph'),
                
        html.H3('Filters:'),
    
        html.Div([
            
                html.Label('Countries'),
                html.Br(),
            
                dcc.Dropdown(
                    id=PREFIX+'country', 
                    clearable=False,
                    value=['Australia','India','United States','United Kingdom','China','Brazil'],
                    multi=True,
                    options=[{'label': c, 'value': c} for c in countries]
                )
            ],
            
            style = dropdown_style
        
        ),
        
        html.Div([
            
                html.Label('Metric'),
                html.Br(),
            
                dcc.Dropdown(
                    id=PREFIX+'metric', 
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
                    id=PREFIX+'table',
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
            )

    ])




@app.callback(
    Output(PREFIX+"graph", "figure"), 
    Output(PREFIX+"table", "columns"), 
    Output(PREFIX+"table", "data"), 
    [Input(PREFIX+"country", "value"),
     Input(PREFIX+"metric", "value")]
)

def display_animated_graph(countries,metric):
    
    work_df = data.copy()
    work_df = work_df[work_df['Country'].isin(countries)].sort_values(by=['Country','year'])\
                    .query('year > 2005')
           
    r_min = 0.9*work_df[metric].min()
    r_max = 1.1*work_df[metric].max()
    
    fig = px.scatter(work_df, x=metric, y='Country', animation_frame="year", 
                        size=metric, color="Country", 
                        hover_name="Country", log_x=False, range_x=[r_min,r_max],range_y=[-1,len(countries)])
            
    fig.update_layout(title={
        'text': "World Happiness Report  : " + metric + " - YoY Standings Animation <br>",
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
       title_font_size=20,
       margin={"r":0,"t":30,"l":0,"b":0}
     )
    
    table_columns = [{'name': c, 'id': c} for c in work_df.columns]
    table_data    = work_df.to_dict('records')
    
    return fig,table_columns,table_data



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

work_df = data.copy()

PREFIX = "task1-"


yearly_layout = html.Div([
  
        html.Br(),
    
        dcc.Graph(id=PREFIX+'graph'),
        
        html.Label(id=PREFIX+'label'),
        html.Br(),
    
        html.H3('Filters:'),
        html.Div([
            
                html.Label('Top'),
                html.Br(),
            
                dcc.Dropdown(
                    id=PREFIX+'rank', 
                    clearable=False,
                    value=3,
                    options=[{'label': c, 'value': c} for c in list(range(1,8))]
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
    
        html.Div([
            
                html.Label('Highlight Country'),
                html.Br(),
            
                dcc.Dropdown(
                    id=PREFIX+'highlight', 
                    clearable=False,
                    value='Denmark',
                    options=[{'label': c, 'value': c} for c in ['Denmark','None']]
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
                    page_current= 0,
                    page_size=7,
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    style_table={'overflowX': 'auto'}
            ),
    
        html.H4('Note(s):'),
        html.Ol([
            html.Li("Use 'Top' filter that allows single selection for choosing Top 'n' ranked countries. "),
            html.Li("Use 'Metric' filter that allows single selection for choosing the metric of your interest for analysis."),
            html.Li("Use 'Highlight Country' that allows single selection for highlighting the number of occurences of a country in the top 'n' positions."),
            html.Li("Use 'Export' button under table view section to download the data as Excel sheet.")
            
        ])

    ])
        
        
    
@app.callback(
    Output(PREFIX+'graph', 'figure'),
    Output(PREFIX+'table', 'columns'),
    Output(PREFIX+'table', 'data'),
    Output(PREFIX+'highlight', 'options'),
    Output(PREFIX+'label', 'children'),
    [Input(PREFIX+"rank", "value"),
     Input(PREFIX+"metric", "value"),
    Input(PREFIX+"highlight", "value")]
)
def update_figure(rank,metric,highlight):
        
    work_df = data.copy()
    work_df = work_df.sort_values(by=['year',metric],ascending=[True,False]).groupby('year').head(rank)
    work_df['rank']  =list(range(1,rank+1))*(abs(years[0]-years[-1])+1)  
    
    fig =  go.Figure(px.line(work_df, x="year",y=metric, line_group='rank',text='Country'))
    
    if highlight != 'None':
        df2 = work_df.query(f"Country == '{highlight}'")
        
        k = len(df2)
        
        fig.add_trace(go.Scatter(x=df2['year'],y=df2[metric],mode='markers',
                             marker=dict(size=[25]*k,
                                         color=['#f0fc05']*k,
                                         ),
                            name=highlight)
                 )
        
        note = f'Note: {highlight} has ranked {k} time(s) in the Top {rank} position(s) in the WHR - {metric} (2005-2020).'
        
        global highlighted_countries
        
    highlighted_countries = [{'label': c, 'value': c} for c in list(work_df['Country'].drop_duplicates())+['None']]
        
    fig.update_traces(textposition='top center')

    fig.update_layout(title={
        'text': f"Happiness Report Summary: Top {rank} countries by {metric} <br>",
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
       title_font_size=20,
       yaxis_title=metric,
       xaxis_title='Year',
       hovermode='x unified',               
       uniformtext_mode='hide',
       xaxis=dict(tickangle = 0),
       margin=dict(pad=4)
     )
    
    
    table_columns = [{'name': c, 'id': c} for c in work_df.columns]
    table_data    =  work_df.to_dict('records')
       
    return fig,table_columns,table_data,highlighted_countries,note


import pandas as pd

data = pd.read_csv('data/WHR.csv')

years = sorted(list(data['year'].drop_duplicates()))
countries = list(data['Country'].drop_duplicates())

metrics = ['Life Ladder', 
           'Log GDP per capita',
           'Social support', 
           'Healthy life expectancy at birth',
           'Freedom to make life choices',
           'Generosity',
           'Perceptions of corruption', 
           'Positive affect', 
           'Negative affect']


dropdown_style = {'width': '33%', 'display': 'inline-block'}

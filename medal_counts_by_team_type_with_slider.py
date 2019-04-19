import pandas as pd
import numpy as np
import sqlite3
import cufflinks as cf
import plotly.plotly as py
import plotly.tools as tls
from plotly.tools import FigureFactory as FF 
import plotly.graph_objs as go
import math

conn = sqlite3.connect('bootcamp/project2_olympics/olympics.db')

cursor = conn.cursor()

df = pd.read_sql_query("select team, Medal, count(medal) as Total, year from olympic_games group by year order by count(medal) desc;", conn)

years = (df.groupby(['Year'])['Year'].nunique()).index
teams = (df.groupby(['Team'])['Team'].nunique()).index
# make figure
figure = {
    'data': [],
    'layout': {},
    'frames': []
}

# fill in most of layout
figure['layout']['xaxis'] = {'range': [0, 200], 'title': 'Medals'}
figure['layout']['yaxis'] = {'range': [20, 200],'title': 'Year'}
figure['layout']['hovermode'] = 'closest'
figure['layout']['showlegend'] = False
figure['layout']['sliders'] = {
    'args': [
        'transition', {
            'duration': 400,
            'easing': 'cubic-in-out'
        }
    ],
    'initialValue': '1896',
    'plotlycommand': 'animate',
    'values': years,
    'visible': True
}

figure['layout']['updatemenus'] = [
    {
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 500, 'redraw': False},
                         'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }
]
sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'Year:',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
}
# make data
year = 1896
for Team in teams:
    df_by_year = df[df['Year'] == year]
    df_by_year_and_season = df_by_year[df_by_year['Team'] == Team]

    data_dict = {
        'x': list(df_by_year_and_season['Year']),
        'y': list(df_by_year_and_season['Team']),
        'mode': 'markers',
        'text': list(df_by_year_and_season['Medal']),
        'marker': {
            'sizemode': 'area',
            'sizeref': 1,
            'size': list(df_by_year_and_season['Total'])
        },
        'name': Team
    }
    figure['data'].append(data_dict)
# make frames
for year in years:
    frame = {'data': [], 'name': str(year)}
    for Team in teams:
        df_by_year = df[df['Year'] == int(year)]
        df_by_year_and_season = df_by_year[df_by_year['Team'] == Team]

        data_dict = {
            'x': list(df_by_year_and_season['Year']),
            'y': list(df_by_year_and_season['Team']),
            'mode': 'markers',
            'text': list(df_by_year_and_season['Medal']),
            'marker': {
                'sizemode': 'area',
                'sizeref': 1,
                'size':  list(df_by_year_and_season['Total'])
            },
            'name': Team
        }
        frame['data'].append(data_dict)

    figure['frames'].append(frame)
    slider_step = {'args': [
        [year],
        {'frame': {'duration': 300, 'redraw': False},
         'mode': 'immediate',
       'transition': {'duration': 300}}
     ],
     'label': year,
     'method': 'animate'}
    sliders_dict['steps'].append(slider_step)
figure['layout']['sliders'] = [sliders_dict]
py.iplot(figure)
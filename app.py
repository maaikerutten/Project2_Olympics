from flask import Flask, render_template

import json
import plotly

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly import tools
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
   
    return render_template('layouts/index.html')


@app.route('/ProjectProcess.html')
def t():
   
    return render_template('layouts/ProjectProcess.html')

@app.route('/charts')
def charts():
    conn = sqlite3.connect('olympics.db')

    cursor = conn.cursor()

    df = pd.read_sql_query("select team, count(medal) as Medals from olympic_games group by team order by medals desc limit 10;", conn)

    trace0 = go.Bar(
      x=['US', 'Soviet Union', 'Germany', 'Great Britain', 'France', 'Italy', 'Australia', 'Canada', 'Sweden', 'Russia'],
      y=[3113, 1484, 1070, 1027, 862, 836, 793, 788, 681, 600],
      marker=dict(
      color='rgb(158,202,225)',
      line=dict(
         color='rgb(8,48,107)',
        width=1.5,
      )
    ),
    opacity=0.6
    )

    data = [trace0]
    layout = go.Layout(
      title='Top 10 Countries - Total Medal Count',
    )

    fig =dict(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('layouts/Charts.html', graphJSON=graphJSON)

@app.route('/timelapse')
def timelapse():
    conn = sqlite3.connect('olympics.db')

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
    graphJSON = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('layouts/Timelapsmedalcount.html', graphJSON=graphJSON)

    
@app.route('/goldmedals')
def goldmedals():
    conn = sqlite3.connect('olympics.db')

    cursor = conn.cursor()

    df = pd.read_sql_query("select medal, season, count(medal) as Total_Won, team, hostcity, hostcountry, year, sex from olympic_games group by team, medal, sex order by year, count(medal) desc;", conn)  

    dfS = df[df['Season']=='Summer']; dfW = df[df['Season']=='Winter']

    traceS = go.Bar(
    x = dfS['Team'],y = dfS['Total_Won'],
    name="Summer Games",
     marker=dict(
                color='rgb(238,23,11)',
                line=dict(
                    color='red',
                    width=1),
                opacity=0.5,
            ),
    text= dfS['HostCity'],
    )
    traceW = go.Bar(
    x = dfW['Team'],y = dfW['Total_Won'],
    name="Winter Games",
    marker=dict(
                color='rgb(11,23,245)',
                line=dict(
                    color='blue',
                    width=1),
                opacity=0.5,
            ),
    text=dfS['HostCity']
    )

    data = [traceS, traceW]
    layout = dict(title = 'Medal Counts by Country/Season',
          xaxis = dict(title = 'Team', showticklabels=True), 
          yaxis = dict(title = 'Total_Won'),
          hovermode = 'closest',
          barmode='stack'
         )
    fig =dict(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('layouts/Goldmedals.html', graphJSON=graphJSON)

@app.route('/hostcity')
def hostcity():
    conn = sqlite3.connect('olympics.db')

    cursor = conn.cursor()

    df = pd.read_sql_query("select hostcountry, hostcity, season, year from olympic_games group by year;", conn)

    trace = go.Choropleth(
            locations = df['Hostcountry'],
            locationmode='country names',
            z = df['Year'],
            text = df['Hostcountry'],
            autocolorscale =False,
            reversescale = True,
            colorscale = 'rainbow',
            marker = dict(
                line = dict(
                    color = 'rgb(0,0,0)',
                    width = 0.5)
            ),
            colorbar = dict(
                title = 'Year',
                tickprefix = '')
        )

    data = [trace]
    layout = go.Layout(
    title = 'Olympic Countries',
    geo = dict(
        showframe = True,
        showlakes = False,
        showcoastlines = True,
        projection = dict(
            type = 'natural earth'
        )
    )
    )
    fig =dict(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('layouts/Hostcity.html', graphJSON=graphJSON)


if __name__ == '__main__':
    app.run(debug=True)
import pandas as pd
import numpy as np
import sqlite3
import cufflinks as cf
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

conn = sqlite3.connect('bootcamp/project2_olympics/olympics.db')

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
fig = dict(data=data, layout=layout)
py.iplot(fig, filename='events-sports1')

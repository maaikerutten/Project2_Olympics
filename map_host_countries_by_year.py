import pandas as pd
import numpy as np
import sqlite3
import cufflinks as cf
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

conn = sqlite3.connect('bootcamp/project2_olympics/olympics.db')

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

fig = dict( data=data, layout=layout )
py.iplot(fig)
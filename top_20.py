import pandas as pd
import numpy as np
import sqlite3
import cufflinks as cf
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

tls.set_credentials_file(username='eugene.brink' , api_key='pDG7rj5oQjsPeg4FrRkj')

conn = sqlite3.connect('bootcamp/project2_olympics/olympics.db')

cursor = conn.cursor()

df = pd.read_sql_query("select medal, team from olympic_games;", conn)

df_medals=df.ix[df['Medal']=='Gold']

cnt_srs = df_medals['Team'].value_counts().head(20)

trace = go.Bar(
    x=cnt_srs.index,
    y=cnt_srs.values,
    marker=dict(
        color="blue",
        #colorscale = 'Blues',
        reversescale = True
    ),
)

layout = go.Layout(
    title='Top 20 countries with Maximum Gold Medals'
)

data = [trace]
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename="medal")  
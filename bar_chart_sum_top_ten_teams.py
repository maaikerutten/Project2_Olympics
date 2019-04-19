import pandas as pd
import numpy as np
import cufflinks as cf
import sqlite3
import cufflinks as cf
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import json

tls.set_credentials_file(username='eugene.brink' , api_key='pDG7rj5oQjsPeg4FrRkj')

conn = sqlite3.connect('bootcamp/project2_olympics/olympics.db')

cursor = conn.cursor()

df = pd.read_sql_query("select team, count(medal) as Medals from olympic_games group by team order by medals desc limit 10;", conn)

trace0 = go.Bar(
    x=['US', 'Soviet Union', 'Germany', 'Great Britain', 'France', 'Italy', 'Australia', 'Canada', 'Sweden', 'Russia'],
    y=[3113, 1484, 1070, 1027, 862, 836, 793, 788, 681, 600],
    ##text=['27% market share', '24% market share', '19% market share'],
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

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='text-hover-bar')
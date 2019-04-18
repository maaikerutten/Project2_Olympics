import pandas as pd
import numpy as np
import sqlite3
import cufflinks as cf
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

conn = sqlite3.connect('bootcamp/project2_olympics/olympics.db')

cursor = conn.cursor()

metals_query = "select team, medal, count(medal), season, year from olympic_games group by year order by count(medal) desc;"

cursor.execute(metals_query)

result=cursor.fetchall()

for row in result:
    print(row)
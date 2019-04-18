import pandas as pd
import numpy as np
import sqlite3
import cufflinks as cf
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

tls.set_credentials_file(username='eugene.brink' , api_key='pDG7rj5oQjsPeg4FrRkj')

a = np.linspace(start=0, stop=36, num =36)

np.random.seed(25)
b = np.random.uniform(low=0.0, high=1.0, size=36)
trace = go.Scatter(x=a, y=b)

data = [trace]

py.iplot(data,file='basic-line-chart')
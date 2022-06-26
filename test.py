import pandas as pd
from dfeditm import dfedit
from sqlalchemy import create_engine
import numpy as np
import pydeck as pdk

root = '/Users/viktorwalter/Library/Mobile Documents/com~apple~CloudDocs/Studium/Wirtschaftsingenieurwesen B.Sc./8. Semester SS22/Thesis/Praxis/Database/database_0519.db'

df = dfedit.create_df('stopPointList', root)
df_points = df.drop(['StopPointName', 'LocationName'], axis=1)
df_points = df_points.rename(columns={'Longitude': 'lon', 'Latitude': 'lat'})
midpoint = (np.average(df_points['lat']), np.average(df_points['lon']))

print(midpoint[0])
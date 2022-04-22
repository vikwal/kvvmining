import pandas as pd
from sqlalchemy import create_engine
from dfeditm import dfedit
import plost

root = ''

df = dfedit.df_edit(root)

df1 = df.filter(items=['start', 'start_delay'])

print(df1)

# plost.line_chart(
#     df,
#     x='start_dela'
#     y='start_delay'
# )

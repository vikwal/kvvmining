import pandas as pd
from sqlalchemy import create_engine
from dfeditm import dfedit
import plost

root = '/Users/viktorwalter/Library/Mobile Documents/com~apple~CloudDocs/Studium/Wirtschaftsingenieurwesen B.Sc./8. Semester SS22/Thesis/Praxis/Database/database_0421.db'

df = dfedit.df_edit(root)

#df1 = df.filter(items=['start', 'start_delay'])
df['Direction'] = df['Direction'].str.split('-').str[-1]
print(df['Direction'])

# plost.line_chart(
#     df,
#     x='start_dela'
#     y='start_delay'
# )

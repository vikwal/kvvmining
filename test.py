import pandas as pd
from sqlalchemy import create_engine
from dfeditm import dfedit

root = '/Users/viktorwalter/Library/Mobile Documents/com~apple~CloudDocs/Studium/Wirtschaftsingenieurwesen B.Sc./8. Semester SS22/Thesis/Praxis/Database/database_0416.db'

df = dfedit.df_edit(root)

print(df)

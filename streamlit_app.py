"""
# KVVMining
Bahnmining am Beispiel des lokalen Nahverkerhs in Karlsruhe
"""

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.write('Hello, *World!* :sunglasses:')

def create_df(table, root):

  engine = create_engine('sqlite:///' + root)
  df = pd.read_sql(table, engine)
                                    
  return df

#create_df('Fahrtanfragen', st.secrets['root'])
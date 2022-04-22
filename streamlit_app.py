"""
# KVVMining
Bahnmining am Beispiel des lokalen Nahverkerhs in Karlsruhe
"""

import streamlit as st
import pandas as pd
from dfeditm import dfedit
import plost
from sqlalchemy import create_engine

st.write('**KVV Mining Dashboard**')

#df = dfedit.create_df('Fahrtanfragen', st.secrets['root'])

root = ''

df = dfedit.df_edit(root)
df = df.dropna(subset=['start_ist', 'end_ist', 'Linie'])

container = st.sidebar.container()
all_lines = st.sidebar.checkbox('Select all lines')

#line_choice = st.sidebar.multiselect('Select line:', df['Linie'].drop_duplicates().sort_values())

if all_lines: line_choice = container.multiselect('Select line:', df['Linie'].drop_duplicates().sort_values(), df['Linie'].drop_duplicates().sort_values())
else: line_choice = container.multiselect('Select line:', df['Linie'].drop_duplicates().sort_values())
#line_choice_2 = st.sidebar.checkbox('Linie 2')
#line_choice = st.sidebar.selectbox('Select parameters:', df['Linie'].drop_duplicates().sort_values())

#st.write(line_choice[0])
st.dataframe(df[df['Linie'].isin(line_choice)])

# df1 = df.filter(items=['start', 'StartLocation', 'start_delay'])
# df1 = df1[df1['start_delay'].notna()]
# df1 = df1.groupby(['StartLocation']).mean()
# df1 = df1.round(0)

# plost.line_chart(
#      df1,
#      x='StartLocation',
#      y='start_delay',
# )
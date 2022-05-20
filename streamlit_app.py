"""
# KVVMining
Bahnmining am Beispiel des lokalen Nahverkerhs in Karlsruhe
"""

from operator import index
import streamlit as st
import pandas as pd
from dfeditm import dfedit
from sqlalchemy import create_engine

root = ''

df = dfedit.df_edit(root)
df_lines = df.dropna(subset=['start_ist', 'end_ist', 'Linie', 'StartSeq', 'EndSeq'])
df_all_lines = df.dropna(subset=['start_ist', 'end_ist'])

st.title('**KVV Mining Dashboard**')

#df = dfedit.create_df('Fahrtanfragen', st.secrets['root'])

#Select period
st.sidebar.write('**Select period**')
d_start = st.sidebar.date_input('From:')
d_end = st.sidebar.date_input('To:')
st.sidebar.write('')
#Select tramway
st.sidebar.write('**Select tramway**')
container_line = st.sidebar.container()
all_lines = st.sidebar.checkbox('Select all lines')
if all_lines: line_choice = container_line.multiselect('Line:', df_lines['Linie'].drop_duplicates().sort_values(), df_lines['Linie'].drop_duplicates().sort_values())
else: line_choice = container_line.multiselect('Line:', df_lines['Linie'].drop_duplicates().sort_values())
st.sidebar.write('')
#Select bay
st.sidebar.write('**Select bay**')
u_bahn = st.sidebar.checkbox('U-Bahn')
o_bahn = st.sidebar.checkbox('O-Bahn')
#if u_bahn: 
#if o_bahn:

#Tabelle mit gefilterten Rohdaten
df_lines['start_delay'] = df_lines['start_delay'].astype('int')
df_lines['end_delay'] = df_lines['end_delay'].astype('int')
df_lines['StartSeq'] = df_lines['StartSeq'].astype('int')
df_lines['EndSeq'] = df_lines['EndSeq'].astype('int')
st.dataframe(df_lines[['StartName', 'EndName', 'start_soll', 'start_ist', 'end_soll', 'end_ist', 'start_delay', 'end_delay', 'start_bay', 'end_bay', 'Linie', 'Direction', 'StartSeq', 'EndSeq', 'pt_mode']])
st.write('Found ' + format(df_lines.shape[0], ',d') + ' records') 

#Delay overall
st.write('**Delay overall**')
st.write('Delay of all lines, independent from period of time')
delay_all = df_all_lines[
(df_all_lines['start_ist'] > pd.to_datetime(d_start)) & 
(df_all_lines['start_ist'] < pd.to_datetime(d_end))][['start_ist', 'StartName', 'EndName','start_delay', 'Linie', 'start_bay', 'end_bay']]
df_delay_overall = delay_all.groupby(delay_all['start_ist'].dt.date).mean()
df_delay_overall = df_delay_overall.rename(columns={'start_delay': 'delay'})
st.line_chart(df_delay_overall)
st.write('Average delay for all lines from ' + str(d_start) + ' to ' + str(d_end) + ' : ' + str(df_delay_overall['delay'].mean().astype('int')) + ' seconds')

#Delay per line
st.write('**Delay per line**')
c = 0
df0 = df_lines.groupby([df_lines['start_ist'].dt.date]).mean().index.to_frame()
df0 = df0.rename(columns={'start_ist': 'date'})
for i in line_choice:
    delay_line = df_lines[
    (df_lines['Linie'].isin(list(i))) &
    (df_lines['start_ist'] > pd.to_datetime(d_start)) & 
    (df_lines['start_ist'] < pd.to_datetime(d_end))].groupby([df_lines['start_ist'].dt.date]).mean()
    delay_line = delay_line.rename(columns={'start_delay': i})
    df1 = delay_line[i]
    df0 = df0.join(df1)
df0 = df0.drop(['date'], axis=1)
df_mean = df0.copy()
df_mean['index'] = 1
df_mean = df_mean.groupby(['index']).mean().round(1)
df_mean = df_mean.rename(index = {1: 'avg(delay)'})

st.line_chart(df0)
st.write('Average delay in seconds per line for selected period:')
st.dataframe(df_mean.style.format('{:.0f}'))

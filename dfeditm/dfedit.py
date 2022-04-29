import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

#Erstellt einen Dataframe aus einem sqlite database file
def create_df(table, root):
  engine = create_engine('sqlite:///' + root)
  df = pd.read_sql(table, engine)                              
  return df

#Funktion, die einem großen Dataframe erstellt, aus den Tabellen der Datenbank
@st.cache
def df_edit(root):
    #Zuerst erstellt man aus allen Tabellen der Datenbank jeweils einen Dataframe
    df0 = create_df('Fahrtanfragen', root)
    dflines = create_df('Linien', root)
    dfroute = create_df('RouteStops', root)
    dfstops = create_df('stopPointList', root)
    #Dann werden die Dataframes bearbeitet
    start_delay = (df0['start_ist'] - df0['start_soll']).dt.total_seconds()
    end_delay = (df0['end_ist'] - df0['end_soll']).dt.total_seconds()
    dflines = dflines.drop(['StartID', 'EndID'], axis = 1)
    dfroute1 = dfroute.rename(columns={'Station': "start"})
    dfroute1['Direction'] = dfroute1['Direction'].str.split('-').str[-1]
    dfroute1 = dfroute1.drop_duplicates(subset=['start', 'line_ref','route'])
    dfroute2 = dfroute.rename(columns={'Station': "end"})
    dfroute2['Direction'] = dfroute2['Direction'].str.split('-').str[-1]
    dfroute2 = dfroute2.drop_duplicates(subset=['end', 'line_ref','route'])
    dfstops1 = dfstops.rename(columns={'Station': "start"})
    dfstops1['StopPointName'] = dfstops1['StopPointName'] + ", " + dfstops1['LocationName']
    dfstops1 = dfstops1.drop(['LocationName'], axis=1)
    dfstops2 = dfstops.rename(columns={'Station': "end"})
    dfstops2['StopPointName'] = dfstops2['StopPointName'] + ", " + dfstops2['LocationName']
    dfstops2 = dfstops2.drop(['LocationName'], axis=1)
    #Verbinden der Dataframes zu einem großen sowie Umbenennung der Spalten, falls nötig
    df = pd.concat([df0, start_delay, end_delay], axis=1)
    df = df.rename(columns={0: "start_delay", 1: "end_delay"})
    df = pd.merge(df, dflines, on='line_ref', how='left')
    df = pd.merge(df, dfroute1, on=['start', 'line_ref','route'], how='left')
    df = df.rename(columns={'StopSeq': "StartSeq"})
    df = pd.merge(df, dfroute2, on=['end', 'line_ref','route', 'Direction'], how='left')
    df = df.rename(columns={'StopSeq': "EndSeq"})
    df = pd.merge(df, dfstops1, on='start', how='left')
    df = df.rename(columns={'StopPointName': 'StartName', 'Longitude': 'StartLong', 'Latitude': 'StartLat'})
    df = pd.merge(df, dfstops2, on='end', how='left')
    df = df.rename(columns={'StopPointName': 'EndName', 'Longitude': 'EndLong', 'Latitude': 'EndLat'})
    return df
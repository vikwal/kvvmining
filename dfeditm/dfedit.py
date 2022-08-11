import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, desc

#Erstellt einen Dataframe aus einem sqlite database file
@st.cache
def create_df(table, root):
  #engine = create_engine('sqlite:///' + root) #Auskommentiert, da Sample-Datensatz aus CSV eingelesen wird zu Demnonstrationszwecken
  #df = pd.read_sql(table, engine)             #Auskommentiert, da Sample-Datensatz aus CSV eingelesen wird zu Demnonstrationszwecken
  df = pd.read_csv(table)
  df.loc[(df.Linie == None),'Linie'] = 'Sonstige'                              
  return df

#Funktion, die DataFrame für die Karte erstellt
def create_map(df, table, zeitfilter, date, day, line_choice, stop_choice):
  if zeitfilter == 'Datum': df = df[df['Datum'].isin(date)]
  else: df = df[df['Wochentag'].isin(day)]
  df = df[df['Linie'].isin(line_choice)]
  df = df[df['Haltestelle_Ort'].isin(stop_choice)]
  if table == 'Fahrtanfragen_avg': df = df.groupby(['Haltestelle_Ort']).mean()
  else: df = df.groupby(['Haltestelle_Ort']).median()
  df.index.name = 'Haltestelle_Ort'
  df = df.reset_index()
  df['Verspätung_in_Sekunden'] = df['Verspätung_in_Sekunden'].round(0)
  df_result = df.sort_values(by=['Verspätung_in_Sekunden'], ascending=False)
  return df_result

#Funktion, die DataFrame für Historgamm erstellt
def create_hist(df, table, zeitfilter, date, day, line_choice, stop_choice):
  if zeitfilter == 'Datum': df = df[df['Datum'].isin(date)]
  else: df = df[df['Wochentag'].isin(day)]
  df = df[df['Linie'].isin(line_choice)]
  df = df[df['Haltestelle_Ort'].isin(stop_choice)]
  if table == 'Fahrtanfragen_avg': df = df.groupby(['Stunde_des_Tages']).mean()
  else: df = df.groupby(['Stunde_des_Tages']).median()
  df = df.drop(['lng', 'lat'], axis=1)
  df = df.round(0)
  df_result = df.reset_index()
  return df_result

#Funktion, die ein Numpy Array aus Haltestellen erstellt
@st.cache
def create_stoplist(root):
  df = create_df('Fahrtanfragen_avg', root)
  df = df['Haltestelle_Ort'].unique()
  arr = np.sort(df)
  return arr

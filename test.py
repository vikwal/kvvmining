import pandas as pd
from sqlalchemy import create_engine

#Erstellt einen Dataframe aus einem sqlite database file
def create_df(table, root):
  engine = create_engine('sqlite:///' + root)
  df = pd.read_sql(table, engine)                              
  return df

#Funktion, die einem Dataframe die Verspätung in Sekunden hinzufügt sowie Namen für die Haltestellen
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
    dflines = dflines.rename(columns={'LineRef': "line_ref"})
    #Verbinden der Dataframes zu einem großen sowie Umbenennung der Spalten, falls nötig
    df = pd.concat([df0, start_delay, end_delay], axis=1)
    df = df.rename(columns={0: "start_delay", 1: "end_delay"})
    return df

root = ''

df = df_edit(root)
df = df.drop(['timestamp', 'start', 'end', 'start_soll', 'start_ist', 'end_soll', 'end_ist'], axis = 1)

print(df)

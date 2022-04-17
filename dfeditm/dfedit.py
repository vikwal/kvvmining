import pandas as pd
from sqlalchemy import create_engine

#Erstellt einen Dataframe aus einem sqlite database file
def create_df(table, root):
  engine = create_engine('sqlite:///' + root)
  df = pd.read_sql(table, engine)                              
  return df

#Funktion, die einem Dataframe die Verspätung in Sekunden hinzufügt sowie Namen für die Haltestellen
def df_edit(df, dfstops):
    #Zuerst erstellt man aus allen Tabellen der Datenbank jeweils einen Dataframe
    start_delay = (df['start_ist'] - df['start_soll']).dt.total_seconds()
    end_delay = (df['end_ist'] - df['end_soll']).dt.total_seconds()
    dfstops = dfstops.drop(['StartID', 'EndID'], axis = 1)

    #Verbinden der Dataframes zu einem großen sowie Umbenennung der Spalten, falls nötig
    df1 = pd.concat([df, start_delay, end_delay], axis=1, join="inner")
    df1 = df1.rename(columns={0: "start_delay", 1: "end_delay"})
    return df1
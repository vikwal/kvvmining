import sqlite3
import pandas as pd
import sqlalchemy
from datetime import datetime, timedelta
import time

#Funktion, die SQL Befehle auf der DB ausführt.
def sqlite_cmd(route, cmd):
    
    conn = sqlite3.connect(route)

    c = conn.cursor()

    c.execute(cmd)

    conn.commit()

    conn.close()

#Liest SQL und speichert Ergebnis in einem Pandas DataFrame
def create_df(table, root):
  engine = sqlalchemy.create_engine('sqlite:///' + root)
  df = pd.read_sql(table, engine)                              
  return df
    
#Funktion, die die gecrawlten Daten einliest, ein Pandas-Objekt ersteltt, Duplikate entfernt und in die Master DB speichert.
def data_edit(rootraw, root, rawtable, finaletable):
    
    engine_raw = sqlalchemy.create_engine("sqlite:///"+rootraw)
    engine = sqlalchemy.create_engine("sqlite:///"+root)
    df = pd.read_sql(rawtable, engine_raw)
    
    df = df.drop_duplicates(subset=['start', 'end', 'start_soll', 'end_soll'], keep='last')
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['start_soll'] = pd.to_datetime(df['start_soll'], errors='coerce')
    df['start_ist'] = pd.to_datetime(df['start_ist'], errors='coerce')
    df['end_soll'] = pd.to_datetime(df['end_soll'], errors='coerce')
    df['end_ist'] = pd.to_datetime(df['end_ist'], errors='coerce')
    
    df.to_sql(finaletable, engine, if_exists='append', index=False)
    
    sqlite_cmd(root, """update """+finaletable+""" set start_ist = Null where start_ist = 'NaT';""")
    sqlite_cmd(root, """update """+finaletable+""" set end_ist = Null where end_ist = 'NaT';""")
    sqlite_cmd(root, """update """+finaletable+""" set start_ist = Null where start_ist = 'None';""")
    sqlite_cmd(root, """update """+finaletable+""" set end_ist = Null where end_ist = 'None';""")

#Funktion, die vorgefilterte Daten als Durchschnitt aggregiert, für Streamlit Dashboard relevantes Format erzeugt und auf der Datenbank persistiert.
def data_streamlit_avg(root, target):
    engine = sqlalchemy.create_engine("sqlite:///"+target)
    df = create_df('Fahrtanfragen', root)
    date_y = pd.Timestamp((datetime.today() - timedelta(days=1)).date())
    date_t = pd.Timestamp(datetime.today().date())
    df = df.loc[(df.timestamp >= date_y) & (df.timestamp < date_t)]
    df = df.drop_duplicates(subset=['start', 'end', 'start_soll', 'end_soll'], keep='last')
    df['Datum'] = pd.to_datetime(df['start_soll']).dt.date
    df['Wochentag'] = pd.to_datetime(df['Datum']).dt.weekday
    df.loc[(df.Wochentag == 0),'Wochentag'] = 'Montag'
    df.loc[(df.Wochentag == 1),'Wochentag'] = 'Dienstag'
    df.loc[(df.Wochentag == 2),'Wochentag'] = 'Mittwoch'
    df.loc[(df.Wochentag == 3),'Wochentag'] = 'Donnerstag'
    df.loc[(df.Wochentag == 4),'Wochentag'] = 'Freitag'
    df.loc[(df.Wochentag == 5),'Wochentag'] = 'Samstag'
    df.loc[(df.Wochentag == 6),'Wochentag'] = 'Sonntag'
    df['Stunde_des_Tages'] = pd.to_datetime(df['start_soll']).dt.hour
    start_delay = (df['start_ist'] - df['start_soll']).dt.total_seconds()
    df = pd.concat([df, start_delay], axis=1)
    df = df.rename(columns={0: 'Verspätung_in_Sekunden'})
    df = df.drop(['journey_nr'], axis=1)
    df = df.groupby(['start', 'line_ref', 'Datum', 'Wochentag', 'Stunde_des_Tages']).mean()
    df = df.reset_index()
    #Haltestellenspalte und Tramlinienspalte müssen noch angepasst werden
    dfstops = create_df('stopPointList', root)
    dfstops = dfstops.rename(columns={'Station': "start"})
    dfstops['StopPointName'] = dfstops['StopPointName'] + ", " + dfstops['LocationName']
    dfstops = dfstops.drop(['LocationName'], axis=1)
    df = pd.merge(df, dfstops, on='start', how='left')
    df = df.rename(columns={'StopPointName': 'Haltestelle_Ort', 'Longitude': 'lng', 'Latitude': 'lat'})
    dflines = create_df('Linien', root)
    dflines = dflines.drop(['StartID', 'EndID'], axis = 1)
    df = pd.merge(df, dflines, on='line_ref', how='left')
    df = df.drop(['line_ref'], axis=1)
    df = df.drop(['start'], axis=1)
    df = df[['Haltestelle_Ort', 'lng', 'lat', 'Linie', 'Datum', 'Wochentag', 'Stunde_des_Tages', 'Verspätung_in_Sekunden']]
    
    df.to_sql('Fahrtanfragen_avg', engine, if_exists='append', index=False)

#Funktion, die vorgefilterte Daten als Durchschnitt aggregiert, für Streamlit Dashboard relevantes Format erzeugt und auf der Datenbank persistiert.
def data_streamlit_med(root, target):
    engine = sqlalchemy.create_engine("sqlite:///"+target)
    df = create_df('Fahrtanfragen', root)
    date_y = pd.Timestamp((datetime.today() - timedelta(days=1)).date())
    date_t = pd.Timestamp(datetime.today().date())
    df = df.loc[(df.timestamp >= date_y) & (df.timestamp < date_t)]
    df = df.drop_duplicates(subset=['start', 'end', 'start_soll', 'end_soll'], keep='last')
    df['Datum'] = pd.to_datetime(df['start_soll']).dt.date
    df['Wochentag'] = pd.to_datetime(df['Datum']).dt.weekday
    df.loc[(df.Wochentag == 0),'Wochentag'] = 'Montag'
    df.loc[(df.Wochentag == 1),'Wochentag'] = 'Dienstag'
    df.loc[(df.Wochentag == 2),'Wochentag'] = 'Mittwoch'
    df.loc[(df.Wochentag == 3),'Wochentag'] = 'Donnerstag'
    df.loc[(df.Wochentag == 4),'Wochentag'] = 'Freitag'
    df.loc[(df.Wochentag == 5),'Wochentag'] = 'Samstag'
    df.loc[(df.Wochentag == 6),'Wochentag'] = 'Sonntag'
    df['Stunde_des_Tages'] = pd.to_datetime(df['start_soll']).dt.hour
    start_delay = (df['start_ist'] - df['start_soll']).dt.total_seconds()
    df = pd.concat([df, start_delay], axis=1)
    df = df.rename(columns={0: 'Verspätung_in_Sekunden'})
    df = df.drop(['journey_nr'], axis=1)
    df = df.groupby(['start', 'line_ref', 'Datum', 'Wochentag', 'Stunde_des_Tages']).median()
    df = df.reset_index()
    #Haltestellenspalte und Tramlinienspalte müssen noch angepasst werden
    dfstops = create_df('stopPointList', root)
    dfstops = dfstops.rename(columns={'Station': "start"})
    dfstops['StopPointName'] = dfstops['StopPointName'] + ", " + dfstops['LocationName']
    dfstops = dfstops.drop(['LocationName'], axis=1)
    df = pd.merge(df, dfstops, on='start', how='left')
    df = df.rename(columns={'StopPointName': 'Haltestelle_Ort', 'Longitude': 'lng', 'Latitude': 'lat'})
    dflines = create_df('Linien', root)
    dflines = dflines.drop(['StartID', 'EndID'], axis = 1)
    df = pd.merge(df, dflines, on='line_ref', how='left')
    df = df.drop(['line_ref'], axis=1)
    df = df.drop(['start'], axis=1)
    df = df[['Haltestelle_Ort', 'lng', 'lat', 'Linie', 'Datum', 'Wochentag', 'Stunde_des_Tages', 'Verspätung_in_Sekunden']]
    
    df.to_sql('Fahrtanfragen_med', engine, if_exists='append', index=False)

#Funktion, die die gecrawlten Daten einliest, ein Pandas-Objekt ersteltt, Duplikate entfernt und in die Master DB speichert.
def data_edit(rootraw, root, rawtable, finaletable):
    
    engine_raw = sqlalchemy.create_engine("sqlite:///"+rootraw)
    engine = sqlalchemy.create_engine("sqlite:///"+root)
    df = pd.read_sql(rawtable, engine_raw)
    
    df = df.drop_duplicates(subset=['start', 'end', 'start_soll', 'end_soll'], keep='last')
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['start_soll'] = pd.to_datetime(df['start_soll'], errors='coerce')
    df['start_ist'] = pd.to_datetime(df['start_ist'], errors='coerce')
    df['end_soll'] = pd.to_datetime(df['end_soll'], errors='coerce')
    df['end_ist'] = pd.to_datetime(df['end_ist'], errors='coerce')
    
    df.to_sql(finaletable, engine, if_exists='append', index=False)
    
    sqlite_cmd(root, """update """+finaletable+""" set start_ist = Null where start_ist = 'NaT';""")
    sqlite_cmd(root, """update """+finaletable+""" set end_ist = Null where end_ist = 'NaT';""")
    sqlite_cmd(root, """update """+finaletable+""" set start_ist = Null where start_ist = 'None';""")
    sqlite_cmd(root, """update """+finaletable+""" set end_ist = Null where end_ist = 'None';""")

# Funktion, die den Datentransport zyklisch durchführt    
def data_transfer(rootraw, root, target, finaletable, n=1, date = datetime.now()):
    engine = sqlalchemy.create_engine("sqlite:///"+rootraw)
    
    now = datetime.now().date()

    try:
        while True:
            if now != datetime.now().date():
                time.sleep(90)
                now = datetime.now().date()
                print("_____________")
                #Rohdaten vorfiltern und in database.db file schreiben
                for i in range(1,7):
                    data_edit(rootraw, root, "Crawler"+str(i)+"_"+str((datetime.today() - timedelta(days=1)).date()), finaletable)
                    print("Crawler" + str(i) + "_" + str((datetime.today() - timedelta(days=1)).date()) + " erfolgreich importiert um: " + str(datetime.now()))
                print("Datentransport in database.db erfolgreich um: " + str(datetime.now()))
                time.sleep(60)
                #Vorgefilterte Daten als Durchschnitt aggregieren und in datebase_streamlit.db schreiben
                data_streamlit_avg(root, target)
                print("Datentransport (avg) in database_streamlit.db erfolgreich um: " + str(datetime.now()))
                print("_____________")
                time.sleep(60)
                #Vorgefilterte Daten als Median aggregieren und in datebase_streamlit.db schreiben
                data_streamlit_med(root, target)
                print("Datentransport (med) in database_streamlit.db erfolgreich um: " + str(datetime.now()))
                print("_____________")
            else: 
                print("Datentransport wird initialisiert: " + str(datetime.now()))
                time.sleep(60*120)
    except:
        if n < 5:
            if ((datetime.now() - date).total_seconds()) > 3600:
                print("Fehler um: " + str(datetime.now()) +  " / Letzter Fehler vor > 1 Stunde")
                time.sleep(30)
                n = 1
                data_transfer(rootraw, root, finaletable, n, datetime.now())
            else:
                print(str(n) + ". Fehler innerhalb von einer Stunde um: " + str(datetime.now()))
                time.sleep(30)
                data_transfer(rootraw, root, finaletable, n+1, datetime.now())
        else: 
            print("Failed " + str(n) + " times during 1 hour at: " + str(datetime.now()))
            
            
            
            
            
            
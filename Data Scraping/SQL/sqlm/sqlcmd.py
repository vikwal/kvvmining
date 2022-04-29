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
    
#Funktion die die gecrawlten Daten einliest, ein Pandas-Objekt ersteltt, Duplikate entfernt und in die Master DB speichert.
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
def data_transfer(rootraw, root, finaletable, n=1, date = datetime.now()):
    engine = sqlalchemy.create_engine("sqlite:///"+rootraw)
    
    now = datetime.now().date()

    try:
        while True:
            if now != datetime.now().date():
                time.sleep(90)
                now = datetime.now().date()
                print("_____________")
                for i in range(1,7):
                    data_edit(rootraw, root, "Crawler"+str(i)+"_"+str((datetime.today() - timedelta(days=1)).date()), finaletable)
                    print("Crawler" + str(i) + "_" + str((datetime.today() - timedelta(days=1)).date()) + " erfolgreich importiert um: " + str(datetime.now()))
                print("Datentransport erfolgreich um: " + str(datetime.now()))
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
            
            
            
            
            
            
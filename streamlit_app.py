"""
# KVVMining
Bahnmining am Beispiel des lokalen Nahverkerhs in Karlsruhe
"""

import streamlit as st
import pandas as pd
from dfeditm import dfedit
import numpy as np
import pydeck as pdk
import altair as alt
from datetime import datetime, timedelta

#Pfad zur Datenbank
root = '/Database/database_streamlit.db'

st.title('**KVV Mining Dashboard**')
st.write('Das KVV Mining Dashboard ermöglicht einen Einblick in historische Daten zu Pünktlichkeit an Haltestellen und Linien im KVV')
st.write('Folgende Einschränkungen wurden im Rahmen der Datenerhebung gemacht:')
lst = ['Es wurden nur zu folgenden Linien Daten ausgewertet: 1, 2, 3, 4, 5, S1, S10, S11, S12, S2, S4, S5, S51, S31, S32. Vereinzelte Sonderlinien (nicht alle) sind als Sonstige aufgeführt.',
       'Es wurden nur die Haltestellen betrachtet, die regulär von den ausgewählten Linien befahren werden.',
       'Die Pünktlichkeit einer Haltestelle ist nur von den ausgewählten Linien abhängig, auch wenn die Haltestelle noch von Bussen oder anderen Linien befahren wird.',
       'Bei der Verspätung handelt es sich um eine verspätete Abfahrt von der Haltestelle. Die verspätete Ankunft kann näherungsweise gleichgesetzt werden.',
       'Fahrtausfälle werden nicht berücksichtigt und gehen somit auch nicht in die Statistik mit ein.',
       'Dieses Dashboard dient Anschauungszwecken und bildet daher nur Daten ab für den Zeitraum: 18.05.2022 - 19.06.2022']
s = ''
for i in lst:
    s += '- ' + i + '\n'
st.markdown(s)
st.write('___')

#Liste erstellen mit Haltestellen
df_stops = dfedit.create_stoplist(root)
#Datetime-Objekt von gestrigem Tag erstellen
yesterday = (datetime.today() - timedelta(days=1)).date()

## Sidebar
st.sidebar.title('_Parametrisieren_')
st.sidebar.write('___')
#Lageparameter auswählen
st.sidebar.write('**Lagerparameter auswählen**')
lageparameter = st.sidebar.radio('Lageparameter:', ('Arithmetisches Mittel', 'Median'))
if lageparameter == 'Median': 
    table = 'Fahrtanfragen_med'
    #Ungefilterten Dataframe in Zwischenspeicher laden
    df = dfedit.create_df(table, root) 
else: 
    table = 'Fahrtanfragen_avg'
    #Ungefilterten Dataframe in Zwischenspeicher laden
    df = dfedit.create_df(table, root)
st.sidebar.write('___')
#Zeit(raum)filter setzen
st.sidebar.write('**Filter nach Datum bzw. Wochentag auswählen**')
zeitfilter = st.sidebar.radio('Zeitfilter:', ('Datum', 'Wochentag'))
st.sidebar.write('___')
#Datum auswählen
if zeitfilter == 'Datum': 
    st.sidebar.write('**Datum auswählen**')
    all_date = st.sidebar.checkbox('Gesamten Zeitraum anzeigen', value=True)
    date = [0]
    if all_date: 
        date = df['Datum'].apply(lambda x: x.strftime('%Y-%m-%d')).unique()
        date_input_disabled =  st.sidebar.date_input('Datum:' , None, disabled=True)
    else: date[0] = st.sidebar.date_input('Datum:', yesterday)
    day = ''
#Wochentag auswählen
else:
    st.sidebar.write('**Wochentage auswählen**')
    all_week = st.sidebar.checkbox('Alle Tage auswählen', value=True)
    container_day = st.sidebar.container()
    if all_week: day = container_day.multiselect('Wochentage:', ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'], ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'])
    else: day = container_day.multiselect('Wochentage:', ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'])
    date = ''
st.sidebar.write('___')
#Tram/S-Bahn Linie auswählen
st.sidebar.write('**Tram/S-Bahn auswählen**')
all_lines = st.sidebar.checkbox('Alle Linien auswählen', value=True)
container_line = st.sidebar.container()
Sonstige = None
if all_lines: line_choice = container_line.multiselect('Linien:', ['1','2','3','4','5','S1','S10','S11','S12','S2','S4','S5','S51','S31','S32', 'Sonstige'], ['1','2','3','4','5','S1','S10','S11','S12','S2','S4','S5','S51','S31','S32', 'Sonstige'])
else: line_choice = container_line.multiselect('Linien:', ['1','2','3','4','5','S1','S10','S11','S12','S2','S4','S5','S51','S31','S32', 'Sonstige'])
st.sidebar.write('___')
#Haltestelle auswählen
st.sidebar.write('**Haltestellen auswählen**')
all_stops = st.sidebar.checkbox('Alle Haltestellen auswählen', value=True)
container_stop = st.sidebar.container()
if all_stops: stop_choice = container_stop.multiselect('Haltestelle:', df_stops, df_stops)
else: stop_choice = container_stop.multiselect('Haltestelle:', df_stops)
st.sidebar.write('')

#Dataframes erzeugen
df_map = dfedit.create_map(df, table, zeitfilter, date, day, line_choice, stop_choice)
df_hist = dfedit.create_hist(df, table, zeitfilter, date, day, line_choice, stop_choice)

#Tabelle mit Haltestellen und durchschnittlicher Verspätung
st.write('**Tabelle mit Verspätungen im ausgewählten Zeitraum an Haltestellen, die von den ausgewählten Linien befahren werden*, absteigend sortiert nach der größten Verspätung*')
st.dataframe(df_map[['Haltestelle_Ort', 'Verspätung_in_Sekunden']].style.set_precision(0))
st.write('___')

#Karte mit Haltestellen
st.write('**Karte mit Haltestellen, die von den ausgewählten Linien angefahren werden**')
st.write('Je höher die Säule, desto höher die Verspätung bzw. je dunkler die Säule, desto geringer die Verspätung.')

st.pydeck_chart(pdk.Deck(
    map_provider='mapbox',
    map_style='mapbox://styles/mapbox/streets-v11',
    tooltip={
        "html": "An der Haltestelle <b>{Haltestelle_Ort}</b>, fährt die Bahn mit <b>{Verspätung_in_Sekunden}</b> Sekunden Verspätung ab.",
        "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
    },
    initial_view_state=pdk.ViewState(
        latitude=49.0097,
        longitude=8.4024,
        pitch=45
    ),
    layers=[
        pdk.Layer(
            "ColumnLayer",
            data=df_map,
            get_position=['lng', 'lat'],
            get_elevation = "Verspätung_in_Sekunden",
            elevation_scale=10,
            radius=80,
            get_fill_color=["Verspätung_in_Sekunden * 2.2", "Verspätung_in_Sekunden * 0.1", "Verspätung_in_Sekunden * 5", 140],
            #elevation_range=[0, 500],
            pickable=True,
            auto_highlight=True,
        )
    ]
))
st.write('___')

#Historgamm über durchschnittliche Verspätung im Tagesverlauf
st.write('**Verspätung in Sekunden im Tagesverlauf in Abhängigkeit von ausgewählten Parametern**')

st.dataframe(df.loc[(df.Linie == 'S11')].sort_values(by='Verspätung_in_Sekunden', ascending=False).groupby(by='Stunde_des_Tages').mean())

bar_chart = alt.Chart(df_hist).mark_bar().encode(
    x=alt.X('Stunde_des_Tages', scale=alt.Scale(domain=[0,23]), title='Stunde eines Tages'),
    y=alt.Y('Verspätung_in_Sekunden', sort='ascending', title='Verspätung in Sekunden')
)
st.altair_chart(bar_chart, use_container_width=True)

st.write('___')

st.write('Data Science project at Hochschule Karlsruhe - University of Applied Sciences')

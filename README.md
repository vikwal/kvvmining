# kvvmining

**Scraping und Datamining von Fahrtdaten des Karlsruher Verkehrsverbunds KVV sowie Visualisierung der Daten in einer Streamlit App**

'dfeditm' ist ein Modul und steht für 'dataframe edit module'. Es enthält wichtige Funktion, um pandas-DataFrames zu erstellen und zu bearbeiten.<br> Dieses Modul ist relevant für das Streamlit-Dashboard 'streamlit_app.py'.

**Link zum Dashboard:**
https://vikwal-kvvmining-streamlit-app-0bina6.streamlitapp.com/ <br>
Das Dashboard dient zur Anschauung und bilder daher nur Daten ab, für den Zeitraum: 18.05.2022 - 19.06.2022.

**API-KEY**
Im '*crawlerm.py*' Modul sowie in der '*Crawler_Haltestellen.py*' muss noch der richtige API-Key eingesetzt werden, um auf die Schnittstelle zugreifen zu können.<br>
Gekennzeichnet durch einen Platzhalter '*XXX*'. Einzufügen im XML-Code unter: '*<siri:RequestorRef>XXX</siri:RequestorRef>*' sowie in der header-Variable des POST-Requests.

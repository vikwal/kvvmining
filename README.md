# kvvmining

**Scraping und Datamining von Fahrtdaten des Karlsruher Verkehrsverbunds KVV sowie Visualisierung der Daten in einer Streamlit App**

'dfeditm' ist ein Modul und steht für 'dataframe edit module'. Es enthält wichtige Funktion, um pandas-DataFrames zu erstellen und zu bearbeiten. Dieses Modul ist relevant für das Streamlit-Dashboard 'streamlit_app.py'.

**Link zum Dashboard:**
https://vikwal-kvvmining-streamlit-app-0bina6.streamlitapp.com/

**API-KEY**
Im 'crawlerm.py' Modul sowie in der 'Crawler_Haltestellen.py' muss noch der richtige API-Key eingesetzt werden, um auf die Schnittstelle zugreifen zu können.
Gekennzeichnet durch einen Platzhalter 'XXX'. Einzufügen im XML-Code unter: '<siri:RequestorRef>XXX</siri:RequestorRef>' sowie in der header-Variable des posts.

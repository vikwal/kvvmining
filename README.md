# kvvmining

Scraping und Datamining von Fahrtdaten des Karlsruher Verkehrsverbunds KVV sowie Visualisierung der Daten in einer Streamlit App

'dfeditm' ist ein Modul und steht für 'dataframe edit module'. Es enthält wichtige Funktion, um Pandas-Dataframes zu erstellen und zu bearbeiten.

**API-KEY**
Im 'crawler.py' Modul sowie in der 'Crawler_Haltestellen.py' muss noch der richtige API-Key eingesetzt werden, um auf die Schnittstelle zugreifen zu können.
Gekennzeichnet durch einen Platzhalter 'XXX'. Einzufügen im XML-Code unter: '<siri:RequestorRef>XXX</siri:RequestorRef>' sowie in der header-Variable des posts.

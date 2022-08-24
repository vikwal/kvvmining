# kvvmining

**Scraping und Datamining von Fahrtdaten des Karlsruher Verkehrsverbunds KVV sowie Visualisierung der Daten in einer Streamlit App**

**Link zum Dashboard:**<br>
https://vikwal-kvvmining-streamlit-app-0bina6.streamlitapp.com/ <br>
Das Dashboard dient zur Anschauung und bilder daher nur Daten ab, für den Zeitraum: 18.05.2022 - 19.06.2022.

**./Data Scraping**<br>
Der Ordner *Data Scraping* enthält alle wichtigen Dateien zur Datenbeschaffung und Datenspeicherung von gescrapten Daten

**./Data_Analysis_KVV/Data_Analysis_KVV.md**<br>
Markdown-Datei eines Jupyter Notebooks zur Datenanalyse von gescrapten Daten des KVV (Betrachtungszeitraum 11.04.2022 - 16.08.2022)

**./Data Scraping/Crawler**<br>
Der Ordner *Crawler* enthält alle notwendigen Dateien zur Datenbeschaffung.

**./Data Scraping/Crawler/crawlerm**<br>
Der Ordner *crawlerm* enthält das Modul, das notwendige Funktionen und Klassen zur Datenbeschaffung beinhaltet.

**./Data Scraping/Crawler/main.py**<br>
Das Python-Skript *main.py* ist das ausführende Programm, welches automatisiert Anfragen an die Schnittstelle stellt, XML Code parsed und Daten auf eine Zieldatenbank schreibt. Die dafür notwendigen Funktionen sind in *./Data Scraping/Crawler/crawlerm/crawlerm.py* definiert. Einmal angestoßen läuft das Programm bis es beendet wird.

**./Data Scraping/Database/**<br>
Hier liegen die relevanten SQLite Datenbankdateien, Tabellen sind angelegt, enthalten jedoch keine Daten. <br>
1. *rawdata.db* - Datenbank, die Informationen zu jedem gestellten Request enthält.
2. *database_raw.db* - Datenbank, die Informationen zur jeder einzelnen Fahrt beinhaltet
3. *database_streamlit* - Datenbank, die gruppierte Daten enthält nach Durchschnitt und Median, relevant für Dashboard.

Die Granularität der Daten in den Datenbanken sinkt von oben nach unten.
  
**./Data Scraping/Database/HaltePaare**<br>
Die hier gespeicherten CSV Dateien haben jeweils zwei Spalten und beinhalten Haltestellenpaare, wobei ein Haltestellenpaar aus zwei benachbarten Haltestellen besteht. Es handelt sich um 6 CSV-Dateien, da das *main.py* 6 parallellaufende Threads ausführt, weshalb jeder Thread eine eigene Liste mit Haltestellenpaaren benötigt. Diese Haltestellenpaare sind die Grundlage für die Requests. Ein Request wird für eine Zeile einer CSV-Datei ausgeführt, in dem der erste Wert des Tupels der Starthaltestellle und der zweite Wert der Endhaltestelle entspricht.

**./Data Scraping/Database/SQL**<br>
Dieser Ordner beinhaltet ein Programm zur Verarbeitung der generierten Rohdaten *rawdata.db*. Der Unterordner *sqlm* ist ein Modul und beinhaltet wichtige Funktionen, die im Zuge der weiteren Datenverarbeitung wichtig sind.

**./Data Scraping/Database/SQL/Datentransporter.py**<br>
Dieses Python-Skript führt einen Datentransport aus, indem es Rohdaten als pandas-DataFrame einliest und diese bearbeitet. Die aufbereiteten Daten werden dann entweder auf die Datenbank *database_raw.db' oder 'database_streamlit.db* geschrieben. Einmal angestoßen läuft das Programm bis es beendet wird. Der eigentliche Datentransport findet nur alle 24 Stunden stat, wobei bei Tageswechsel die Daten des Vortages bearbeitet werden.

**./Data Scraping/dfeditm**<br>
'*dfeditm*' ist ein Modul und steht für 'dataframe edit module'. Es enthält wichtige Funktion, um pandas-DataFrames zu erstellen und zu bearbeiten.<br> Dieses Modul ist relevant für das Streamlit-Dashboard '*streamlit_app.py*'.

**./Data Scraping/Fahrtanfragen_avg**<br>
Dieser Datensatz soll als Beispiel für das Dashboard dienen und enthält nur eine begrenzte Anzahl an Daten (Zeitraum 18.05.2022 bis 19.06.2022). Das gleiche gilt für *Fahrtanfragen_med*.

**./Data Scraping/Pipfile**<br>
Die beiden Dateien *Pipfile* bzw. *Pipfile.lock* beinhalten die erforderlichen Module, die Streamlit bei Initialisierung des Dashboards herunterlädt und installiert.

**./Data Scraping/streamlit_app.py**<br>
Beinhaltet den Quellcode des Dashboards.

**API-KEY**<br>
Für den Fall, eigene Requests durchführen zu wollen, muss im '*crawlerm.py*' Modul sowie in der '*Crawler_Haltestellen.py*'noch der richtige API-Key eingesetzt werden, um auf die Schnittstelle zugreifen zu können.<br>
Gekennzeichnet durch einen Platzhalter '*XXX*'. Einzufügen im XML-Code unter: '*<siri:RequestorRef>XXX</siri:RequestorRef>*' sowie in der header-Variable des POST-Requests.

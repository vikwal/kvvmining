import requests
from datetime import datetime, timedelta
import time
import pandas as pd
import xml.etree.ElementTree as ET
import sqlalchemy

# Funktion, die überprüft, ob der Integer hinter dem zweiten Doppelpunkt in der StopPointRef eindeutig ist.
def stopPointRef_ueberpruefung(root):
    list = []
    for i in root[0][5][0]:
        list.append(i[0][0][0].text.split(":")[2])
    list.sort()
    
    return list

# Funktion, die die Anzahl aller Haltestellen im KVV ausgibt.
def anzahl_haltestellen(root):
    counter = 0
    for i in root[0][5][0]:
            counter += 1
    
    return counter

# Funktion, die Sonderzeichen formatiert
def umlaute_formate(word, n=0):
    
    umlaute = ["ß", "ä", "ö", "ü", "Ä", "Ö", "Ü"]
    code = ["Ã", "Ã¤", "Ã¶", "Ã¼", "Ã", "Ã", "Ã"]
    
    if n == len(code):
        return word
    else:
        result = word
        code = code[n]
        umlaut = umlaute[n]
        if code in word:
            l = word.split(code)
            r = len(l) - 1
            for k in range(0,r):
                l[k] += umlaut
                result = "".join(l)   
            return umlaute_formate(result, n + 1)
        else:
            return umlaute_formate(result, n + 1)
        
# Funktion, die einen Zeitpunkt in ein für die API verständliches Format formatiert
# Also aus dem datetime-Objekt 2022-04-04 09:12:00 wird der String "2022-04-04T09:12:00"
def date_api():
    dt = datetime.now().date()
    hr = datetime.now().hour
    if hr < 10: 
        hr = str(hr)
        hr = "0"+str(hr)
    else: hr = str(hr)
    mnt = datetime.now().minute
    if mnt < 10: 
        mnt = str(mnt)
        mnt = "0"+str(mnt)
    else: mnt = str(mnt)
    sec = datetime.now().second
    if sec < 10: 
        sec = str(sec)
        sec = "0"+str(sec)
    else: sec = str(sec)
    
    return str(dt)+"T"+hr+":"+mnt+":"+sec

# Funktion, die aus dem Zeitpunkt, den die Schnittstelle liefert, ein datetime-Objekt liefert:
# Also aus dem String "2022-04-04T09:12:00" wird das datetime-Objekt 2022-04-04 09:12:00
def date_api_todate(date):
    year = int(date[:4])
    mon = int(date[5:7])
    day = int(date[8:10])
    hr = int(date[11:13])
    mnt = int(date[14:16])
    sec = int(date[17:19])
    
    return datetime(year, mon, day, hr, mnt, sec)

# Funktion, die aus einem API-Zeitpunkt-String einen String macht, der genau die Form eines datetime-Objektes hat
# Also aus einem String "2022-04-04T09:12:00" wird der String "2022-04-04 09:12:00"
def datetime_api_toString(datetime):
    date = datetime[:10]
    time = datetime[11:19]
    
     
    return date + " " + time

# Funktion, die aus einer CSV-Datei eine Liste mit Haltestellen-Tupeln erstellt
def haltepaare_erstellen(haltePaare):
    pa = pd.read_csv(haltePaare)
    pa.head()
    paar1 = []
    paar2 = []

    def merge2(list1, list2):
        merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
        return merged_list

    for i in pa.iterrows():
        paar1.append(i[1][0].split(";")[1])
        paar2.append(i[1][0].split(";")[2])

    return merge2(paar1, paar2)

# Request-Funktion mit eTree-Objekt als Ergebnis
def request_general(xml):
    headers = {'Authorization': 'XXX', 'Content-Type': 'application/xml'}
    response = requests.post('https://projekte.kvv-efa.de/waltertrias/trias', data=xml, headers=headers, timeout=55)
    root = ET.fromstring(response.text)
    
    return root

# Request-Funktion mit String als Ergebnis
def request_general_text(xml):
    headers = {'Authorization': 'XXX', 'Content-Type': 'application/xml'}
    response = requests.post('https://projekte.kvv-efa.de/waltertrias/trias', data=xml, headers=headers, timeout=55)
    
    return response.text

#Returend Response als Etree-Objekt
def request(origin, destination, time):
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <Trias version="1.1" xmlns="http://www.vdv.de/trias" xmlns:siri="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.vdv.de/trias file:///C:/development/HEAD/extras/TRIAS/TRIAS_1.1/Trias.xsd">
        <ServiceRequest>
            <siri:RequestTimeStamp>2022-03-16T19:55:00</siri:RequestTimeStamp>
            <siri:RequestorRef>XXX</siri:RequestorRef>
            <RequestPayload>
                <TripRequest>
                    <Origin>
                        <LocationRef>
                            <StopPlaceRef>"""+origin+"""</StopPlaceRef>
                        </LocationRef>
                        <DepArrTime>"""+time+"""</DepArrTime>
                    </Origin>
                    <Destination>
                        <LocationRef>
                            <StopPlaceRef>"""+destination+"""</StopPlaceRef>
                        </LocationRef>
                    </Destination>
                    <Params>
                        <NumberOfResults>1</NumberOfResults>
                        <IncludeIntermediateStops>true</IncludeIntermediateStops>
                        <IncludeEstimatedTimes>true</IncludeEstimatedTimes>
                        <InterchangeLimit>1</InterchangeLimit>
                    </Params>
                </TripRequest>
            </RequestPayload>
        </ServiceRequest>
    </Trias>"""
    headers = {'Authorization': 'XXX', 'Content-Type': 'application/xml'}
    response = requests.post('https://projekte.kvv-efa.de/waltertrias/trias', data=xml, headers=headers, timeout=55)
    root = ET.fromstring(response.text)
    
    return root

# returned Response als String
def request_text(origin, destination, time):
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <Trias version="1.1" xmlns="http://www.vdv.de/trias" xmlns:siri="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.vdv.de/trias file:///C:/development/HEAD/extras/TRIAS/TRIAS_1.1/Trias.xsd">
        <ServiceRequest>
            <siri:RequestTimeStamp>2022-03-16T19:55:00</siri:RequestTimeStamp>
            <siri:RequestorRef>XXX</siri:RequestorRef>
            <RequestPayload>
                <TripRequest>
                    <Origin>
                        <LocationRef>
                            <StopPlaceRef>"""+origin+"""</StopPlaceRef>
                        </LocationRef>
                        <DepArrTime>"""+time+"""</DepArrTime>
                    </Origin>
                    <Destination>
                        <LocationRef>
                            <StopPlaceRef>"""+destination+"""</StopPlaceRef>
                        </LocationRef>
                    </Destination>
                    <Params>
                        <NumberOfResults>1</NumberOfResults>
                        <IncludeIntermediateStops>false</IncludeIntermediateStops>
                        <IncludeEstimatedTimes>true</IncludeEstimatedTimes>
                        <InterchangeLimit>1</InterchangeLimit>
                    </Params>
                </TripRequest>
            </RequestPayload>
        </ServiceRequest>
    </Trias>"""
    headers = {'Authorization': 'XXX', 'Content-Type': 'application/xml'}
    response = requests.post('https://projekte.kvv-efa.de/waltertrias/trias', data=xml, headers=headers, timeout=55)
    
    return response.text

# Die eigentliche Crawler Funktion
def crawler_function(date, arr):
    
    seq = []
    t = {}
    #Vorwärts
    
    timestamp = datetime_api_toString(date)
    
    for req in arr:
        start = req[0]
        ziel = req[1]

        root = request(start, ziel, date)

        try:
            intch = root[0][5][0][1][1][4].text
            if int(intch) != 0: continue
        except:
            continue
        try:
            start = root[0][5][0][1][1][6][1][0][0].text
        except:
            start = None
            continue
        try:
            end = root[0][5][0][1][1][6][1][1][0].text
        except:
            end = None

        try:
            x = root[0][5][0][1][1][6][1][0][2][0].text
            if len(x) < 15:
                if x[-3:] == "(U)": start_bay = "U"
                else: start_bay = "O"
                try:
                    start_soll = datetime_api_toString(root[0][5][0][1][1][6][1][0][3][0].text)
                except:
                    start_soll = None
                try:
                    start_ist = datetime_api_toString(root[0][5][0][1][1][6][1][0][3][1].text)
                except:
                    start_ist = None
            else: 
                start_bay = None
                start_soll = datetime_api_toString(x)
                try:
                    start_ist = datetime_api_toString(root[0][5][0][1][1][6][1][0][2][1].text)
                except:
                    start_ist = None      
        except:
            start_bay = None

        try:
            x = root[0][5][0][1][1][6][1][1][2][0].text
            if len(x) < 15:
                if x[-3:] == "(U)": end_bay = "U"
                else: end_bay = "O"
                try:
                    end_soll = datetime_api_toString(root[0][5][0][1][1][6][1][1][3][0].text)
                except:
                    end_soll = None
                try:
                    end_ist = datetime_api_toString(root[0][5][0][1][1][6][1][1][3][1].text)
                except:
                    end_ist = None
            else:
                end_bay = None
                end_soll = datetime_api_toString(x)
                try:
                    end_ist = datetime_api_toString(root[0][5][0][1][1][6][1][1][2][1].text)
                except:
                    end_ist = None
        except:
            end_bay = None

        try:
            line_ref = root[0][5][0][1][1][6][1][2][1].text.split(":")[1]
        except:
            line_ref = None
        try:
            route = root[0][5][0][1][1][6][1][2][1].text.split(":")[3]
        except:
            route = None
        try:
            journey_nr = root[0][5][0][1][1][6][1][2][1].text.split(":")[5]
        except:
            journe_nr = None
        try:
            pt_mode = root[0][5][0][1][1][6][1][2][4][0].text
            if pt_mode == "bus": continue
            if len(pt_mode) > 5: pt_mode = None
        except:
            continue

        t = {"timestamp": timestamp, "start": start, "end": end, "start_bay": start_bay, "end_bay": end_bay, "start_soll": 
             start_soll, "start_ist": start_ist, "end_soll": end_soll, "end_ist": end_ist, "line_ref": line_ref, "route": route, 
             "journey_nr": journey_nr, "pt_mode": pt_mode}
        seq.append(t)
    
    #Rückwärts
    
    for req in arr:
        start = req[1]
        ziel = req[0]

        root = request(start, ziel, date)

        try:
            intch = root[0][5][0][1][1][4].text
            if int(intch) != 0: continue
        except:
            continue
        try:
            start = root[0][5][0][1][1][6][1][0][0].text
        except:
            start = None
            continue
        try:
            end = root[0][5][0][1][1][6][1][1][0].text
        except:
            end = None

        try:
            x = root[0][5][0][1][1][6][1][0][2][0].text
            if len(x) < 15: 
                if x[-3:] == "(U)": start_bay = "U"
                else: start_bay = "O"
                try:
                    start_soll = datetime_api_toString(root[0][5][0][1][1][6][1][0][3][0].text)
                except:
                    start_soll = None
                try:
                    start_ist = datetime_api_toString(root[0][5][0][1][1][6][1][0][3][1].text)
                except:
                    start_ist = None
            else: 
                start_bay = None
                start_soll = datetime_api_toString(x)
                try:
                    start_ist = datetime_api_toString(root[0][5][0][1][1][6][1][0][2][1].text)
                except:
                    start_ist = None      
        except:
            start_bay = None

        try:
            x = root[0][5][0][1][1][6][1][1][2][0].text
            if len(x) < 15:
                if x[-3:] == "(U)": end_bay = "U"
                else: end_bay = "O"
                try:
                    end_soll = datetime_api_toString(root[0][5][0][1][1][6][1][1][3][0].text)
                except:
                    end_soll = None
                try:
                    end_ist = datetime_api_toString(root[0][5][0][1][1][6][1][1][3][1].text)
                except:
                    end_ist = None
            else:
                end_bay = None
                end_soll = datetime_api_toString(x)
                try:
                    end_ist = datetime_api_toString(root[0][5][0][1][1][6][1][1][2][1].text)
                except:
                    end_ist = None
        except:
            end_bay = None

        try:
            line_ref = root[0][5][0][1][1][6][1][2][1].text.split(":")[1]
        except:
            line_ref = None
        try:
            route = root[0][5][0][1][1][6][1][2][1].text.split(":")[3]
        except:
            route = None
        try:
            journey_nr = root[0][5][0][1][1][6][1][2][1].text.split(":")[5]
        except:
            journe_nr = None
        try:
            pt_mode = root[0][5][0][1][1][6][1][2][4][0].text
            if pt_mode == "bus": continue
            if len(pt_mode) > 5: pt_mode = None
        except:
            continue

        t = {"timestamp": timestamp, "start": start, "end": end, "start_bay": start_bay, "end_bay": end_bay, "start_soll": 
             start_soll, "start_ist": start_ist, "end_soll": end_soll, "end_ist": end_ist, "line_ref": line_ref, "route": route, 
             "journey_nr": journey_nr, "pt_mode": pt_mode}
        seq.append(t)
    
    return seq

# Funktion, die die crawler_function() ausführt und Daten auf Datenbank schreibt
def crawl(crawlernr, csv, root, n=1, date = datetime.now()):
    paare = haltepaare_erstellen(csv)
    engine = sqlalchemy.create_engine('sqlite:///' + root)
    try:
        while True:
            time_req = date_api()
            print(crawlernr + " " + str(datetime.now()))
            df = pd.DataFrame.from_dict(crawler_function(time_req, haltepaare_erstellen(csv)))
            df.to_sql(crawlernr+"_"+str(datetime.now().date()), engine, if_exists='append', index=False)
    except:
        if n < 4: 
            if ((datetime.now() - date).total_seconds()) > 300:
                print("Fehler um: " + str(datetime.now()) +  " / Letzter Fehler vor > 5 Minuten")
                time.sleep(10)
                n = 1
                crawl(crawlernr, csv, root, n, datetime.now())
            else:
                print(str(n) + ". Fehler innerhalb von 5 Minuten um: " + str(datetime.now()))
                time.sleep(10)
                crawl(crawlernr, csv, root, n+1, datetime.now())
        else: 
            print("Failed " + str(n) + " times during 5 minutes at: " + str(datetime.now()))
            time.sleep(60*30)
            n = 1
            crawl(crawlernr, csv, root, n, datetime.now())
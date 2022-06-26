from crawlerm import *
import csv

# Request für Liste aller Haltestellen

xml = """<?xml version="1.0" encoding="UTF-8"?>
    <Trias version="1.1" xmlns="http://www.vdv.de/trias" xmlns:siri="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.vdv.de/trias file:///C:/development/HEAD/extras/TRIAS/TRIAS_1.1/Trias.xsd">
        <ServiceRequest>
            <siri:RequestTimestamp>2017-09-29T13:56:00Z</siri:RequestTimestamp>
            <siri:RequestorRef>XXX</siri:RequestorRef>
                <RequestPayload>
                    <LocationInformationRequest>
                        <InitialInput>
                            <LocationName>stopListSubnetwork=kvv</LocationName>
                        </InitialInput>
                        <Restrictions>
                            <IncludePtModes>false</IncludePtModes>
                        </Restrictions>
                    </LocationInformationRequest>
                </RequestPayload>
        </ServiceRequest>
    </Trias>"""

response = crawler.request_general(xml)

# CSV Datei schreiben
def csv_datei_schreiben():
    header = ["StopPointRef","StopPointName","LocationName","Longitude","Latitude"]
    with open("stopPointList.csv", "w") as csv_ziel:
        writer = csv.writer(csv_ziel, delimiter=';', quotechar ='"')
        writer.writerow(header)
        for haltestelle in Haltestelle.haltestellen_erstellen(response):
            writer.writerow([haltestelle.stopPointRef, haltestelle.stopPointName, haltestelle.locationName, haltestelle.longitude, haltestelle.latitude])

csv_datei_schreiben()

# Überprüfung, ob es sich bei den erstellen Haltestellen-Tupel, ausschließlich um benachbarte Haltestellen handelt
paare = crawler.haltepaare_erstellen("HaltePaare/HaltePaareFinal.csv")

seq = []
counter = 1
t = ()

for req in paare:
    start = req[0]
    ziel = req[1]
    date = crawler.date_api()
    root = crawler.request(start, ziel, date)
    try:
        stop_seq = root[0][5][0][1][1][6][1][1][4].text
    except:
        stop_seq = None  
    t = (counter, stop_seq)
    seq.append(t)
    counter += 1

print(seq)
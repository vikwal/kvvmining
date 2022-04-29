from crawlerm import *
import pandas as pd
import csv

# Request 

start = "de:08212:7"
ziel = "de:08317:33013"
date = "2022-04-22T10:00:00"
#date = crawler.date_api()

root = crawler.request(start, ziel, date)
text = crawler.request_text(start, ziel, date)

intch = root[0][5][0][1][1][4].text
leg = root[0][5][0][1][1][6][1]

# Wenn intch = 0 bedeutet das, dass der Response keine Umstiege enthält und man somit ein Ergebnis der gesamten Linie erhalten hat.
print(intch)

def csv_datei_schreiben(line):
    header = ["LineRef","Station", "Direction", "Route", "StopSeq"]
    with open("./Streckenabschnitte/RouteStops_"+line+".csv", "w") as csv_ziel:
        writer = csv.writer(csv_ziel, delimiter=';', quotechar ='"')
        writer.writerow(header)
        row = [None] * 5
        last = len(leg)-1
        counter = 1
    
        for i in leg:
            if counter < len(leg):
                row[0] = leg[last][2].text.split(":")[1]
                x = i[0].text.split(":")[0]
                y = i[0].text.split(":")[1]
                z = i[0].text.split(":")[2]
                row[1] = str(x)+":"+str(y)+":"+str(z)
                row[2] = leg[last][2].text.split(":")[3]
                row[3] = crawler.umlaute_formate(leg[last][7][0].text)
                row[4] = counter
                counter += 1
                writer.writerow(row)

#Für jede Linie einmal ausführen mit den entsprechenden Start und Endhaltestellen
csv_datei_schreiben("S7")

# Funktion, um einzelne csv Dateien zusammenzuführen - wichtig für Gesamttabelle der Streckenabschnitte

f1 = "../Streckenabschnitte/RouteStops_1.csv"
f2 = "../Streckenabschnitte/RouteStops_2.csv"
f3 = "../Streckenabschnitte/RouteStops_3.csv"
f4 = "../Streckenabschnitte/RouteStops_4.csv"
f5 = "../Streckenabschnitte/RouteStops_5.csv"
fS1 = "../Streckenabschnitte/RouteStops_S1.csv"
fS2 = "../Streckenabschnitte/RouteStops_S2.csv"
fS4 = "../Streckenabschnitte/RouteStops_S4.csv"
fS5 = "../Streckenabschnitte/RouteStops_S5.csv"
fS11 = "../Streckenabschnitte/RouteStops_S11.csv"
fS12 = "../Streckenabschnitte/RouteStops_S12.csv"
fS31 = "../Streckenabschnitte/RouteStops_S31.csv"
fS32 = "../Streckenabschnitte/RouteStops_S32.csv"
fS51 = "../Streckenabschnitte/RouteStops_S51.csv"

#df = pd.concat(map(pd.read_csv, [f1,f2,f3,f4,f5,fS1,fS2,fS4,fS5,fS11,fS12,fS31,fS32,fS51]), ignore_index = True)

header = ["LineRef","Station","Direction","Route","StopSeq"]
row = [None] * 5

# with open("../Streckenabschnitte/RouteStops.csv", "w") as file:
#     writer = csv.writer(file, delimiter=";", quotechar='"')
#     writer.writerow(header)  
#     for i in df.iterrows():
#         row[0] = i[1][0].split(";")[0]
#         row[1] = i[1][0].split(";")[1]
#         row[2] = i[1][0].split(";")[2]
#         row[3] = i[1][0].split(";")[3]
#         row[4] = i[1][0].split(";")[4]
#         writer.writerow(row)

# Funktion, um eine große Liste aus Streckenabschnitten in beide Richtungen zu erzeugen

r = "../Streckenabschnitte/RouteStops_R.csv"
h = "../Streckenabschnitte/RouteStops_H.csv"

#df = pd.concat(map(pd.read_csv, [r,h]), ignore_index = True)

header = ["LineRef","Station","Direction","Route","StopSeq"]
row = [None] * 5

# with open("./Streckenabschnitte/RouteStops.csv", "w") as file:
#     writer = csv.writer(file, delimiter=";", quotechar='"')
#     writer.writerow(header)  
#     for i in df.iterrows():
#         row[0] = i[1][0].split(";")[0]
#         row[1] = i[1][0].split(";")[1]
#         row[2] = i[1][0].split(";")[2]
#         row[3] = i[1][0].split(";")[3]
#         row[4] = i[1][0].split(";")[4]
#         writer.writerow(row)
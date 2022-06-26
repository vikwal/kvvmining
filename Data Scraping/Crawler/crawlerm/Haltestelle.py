from .crawler import umlaute_formate

class Haltestelle():
    def __init__(self, stopPointRef, stopPointName, locationName, longitude, latitude):
        self.stopPointRef = stopPointRef    # String
        self.stopPointName = stopPointName  # String
        self.locationName = locationName    # String
        self.longitude = longitude          # float
        self.latitude = latitude            # float
        
    def haltestellen_erstellen(root):
        haltestellen = []
        for i in root[0][5][0]:
            stopPointRef = i[0][0][0].text                          
            stopPointName = umlaute_formate(i[0][0][1][0].text, 0)   
            locationName = umlaute_formate(i[0][1][0].text, 0)      
            longitude = float(i[0][2][0].text)                   
            latitude = float(i[0][2][1].text)  
            haltestelle = Haltestelle(stopPointRef, stopPointName, locationName, longitude, latitude)
            haltestellen.append(haltestelle)
        return haltestellen
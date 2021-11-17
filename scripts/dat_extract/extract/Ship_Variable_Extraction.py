#Goal of this program is to extract the date and time and type of ship from data

import os
from datetime import datetime
from geopy.distance import geodesic

harp_data = "J:\HARPdataSummary_20190514.csv"

class Ship:      #Create a general ship to contain extracted variables
    def __init__(self, filepath, id,year_month,month, cpa_time, cpa_datetime, file_time, type, name, harp, mmsi, lat, lon, distance, sampletimes,cpa,temp,sal,depth,spect):
        self.filepath = filepath
        self.id = id
        self.year_month = year_month
        self.month = month
        self.cpa_time = cpa_time
        self.cpa_datetime = cpa_datetime
        self.file_time = file_time
        self.type = type
        self.name = name
        self.harp = harp
        self.mmsi = mmsi
        self.harplat = lat
        self.harplon = lon
        self.distance = distance
        self.sampletimes = sampletimes
        self.cpa = cpa
        self.temp = temp
        self.sal = sal
        self.depth = depth
        self.spect = spect
def extract(filename):
    
    rootdir = filename #set the root directory to the inputed file
    ships = [] #array to be filled with ships
    i = 0 #counter variable
    for subdir, dirs, files in os.walk(rootdir): #goes through each file not only in root but each subdirectory
        for file in files:
            #print os.path.join(subdir, file)
            filepath = subdir + os.sep + file #create filepath to each text file
            if filepath.endswith(".txt"): #only looking for text files
                newShip = Ship("path", "id","year_month", "month","cpa_time","datetime","file_time","type","name",0,0,0,0,[],[],'cpa',0,0,0,None)
                ships.append(newShip)
                
                print(filepath)
                ships[i].filepath = filepath[:34]
                ships[i].id = filepath[34:57]
                ships[i].year_month = filepath[26:33]
                ships[i].month = int(filepath[31:33])
                ships[i].file_time = filepath[51:57]
                with open(filepath, encoding="utf8",errors = 'ignore') as fp: #extract specific lines
                    for x, line in enumerate(fp):
                        
                        if x == 1: #line 1 relates to harp latitude
                            ships[i].harplat = float(line[8:].strip())
                        if x == 2: #line 2 relates to harp longitude
                            ships[i].harplon = float(line[8:].strip()) 
                        if x == 3:
                            ships[i].harp = line[11:].strip() #line 3 is harp id number
                        if x == 5: #line 5 is date
                            ships[i].cpa_time = line[24:].strip()
                            ships[i].cpa_datetime = datetime.strptime(line[13:].strip(), '%m/%d/%Y %H:%M:%S')
                        if x == 7: #line 7 relates to ship name
                            ships[i].name = line[9:].strip()
                        if x == 8:
                            ships[i].mmsi = int(line[5:].strip()) #line 8 is the ships mmsi number
                        if x == 10: #line 10 is ship type
                            ships[i].type = line[9:].strip()
                        if x > 18: #these are the coord lines using them to calc distance from harp and add to array of distances
                            sampletime = line[11:19].strip()
                            ships[i].sampletimes.append(sampletime)
                            
                            lat = float(line[20:28].strip()) #this array will be x axis of the spectrograms
                            lon = float(line[29:39].strip())
                            coords_1 = (ships[i].harplat, ships[i].harplon)
                            coords_2 = (lat, lon)
                            shipDistance = geodesic(coords_1, coords_2).km
                            ships[i].distance.append(shipDistance)
                            # if sampletime == ships[i].cpa_time:
                                # ships[i].cpa = shipDistance
                        
                i+=1 #increment counter before making new ship

    for ship in ships:
        if ship.name == 'unknown' or ship.name.strip() == '' or len(ship.distance) == 0: #clean up data
            ships.remove(ship)
    return ships            
# ships = extract("J:\ShippingCINMS_data\COP")
# txt = "Name: {}\nType: {}\nDate: {} \nTime: {}\n"
# for i in range(len(ships)):
   # print(txt.format(ships[i].name, ships[i].type, ships[i].date, ships[i].time))
    

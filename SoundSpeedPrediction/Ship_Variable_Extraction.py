# Goal of this program is to extract the date and time and type of ship from data
import os
from datetime import datetime
from geopy.distance import geodesic
import unpickle as up
from importlib import reload
import h5py 

folder = "J:\\Pickled_Data_3\\"
rootdir = "M:\ShipNoise_nnet_input"
harp_data = "J:\HARPdataSummary_20190514.csv"
print(rootdir)

class Ship:   #Create a general ship to contain extracted variables
    def __init__(self, filepath, id, year_month, month, cpa_time, cpa_datetime,
                file_time, type, CPA, COG, heading, passage, hMeanSSP,
                distVec, length, SOG, draught, width):
        self.filepath = filepath
        self.id = id
        self.year_month = year_month
        self.month = month
        self.cpa_time = cpa_time
        self.cpa_datetime = cpa_datetime

        self.file_time = file_time
        self.type = type
        self.CPA = CPA
        self.COG = COG
        self.heading = heading
        self.passage = passage
        self.hMeanSSP = hMeanSSP

        self.distVec = distVec
        self.length = length
        self.SOG = SOG
        self.draught = draught
        self.width = width
        print("self complete")



#import os
#from datetime import datetime
#from geopy.distance import geodesic
#import unpickle as up
#from importlib import reload

#folder = "J:\\Pickled_Data_3\\"
#rootdir = "J:\ShippingCINMS_data\COP"
#harp_data = "J:\HARPdataSummary_20190514.csv"
#print(rootdir)

#class Ship:  # Create a general ship to contain extracted variables
#    def __init__(self, filepath, id, year_month, month, cpa_time, cpa_datetime,
#                 file_time, type, name, harp, RL, mmsi, lat, lon,
#                 distance, sampletimes, cpa, temp, sal, depth, spect, sound_speed,
#                 encoded, length, SOG, draught, IMO):
#        self.filepath = filepath
#        self.id = id
#        self.year_month = year_month
#        self.month = month
#        self.cpa_time = cpa_time
#        self.cpa_datetime = cpa_datetime
#        self.file_time = file_time
#        self.type = type
#        self.name = name
#        self.harp = harp
#        self.RL = RL
#        self.mmsi = mmsi
#        self.harplat = lat
#        self.harplon = lon
#        self.distance = distance
#        self.sampletimes = sampletimes
#        self.cpa = cpa
#        self.temp = temp
#        self.sal = sal
#        self.depth = depth
#        self.spect = spect
#        self.sound_speed = sound_speed
#        self.encoded = encoded
#        self.length = length
#        self.SOG = SOG
#        self.draught = draught
#        self.IMO = IMO
#        print("self complete")


#def extract_ships(rootdir, folder):
#    reload(up)
#    up.clear_shelf(folder)
#    ships = []  # array to be filled with ships
#    i = 0  # counter variable
#    # goes through each file not only in root but each subdirectory
#    for subdir, dirs, files in os.walk(rootdir):
#        for file in files:
#            # print os.path.join(subdir, file)
#            filepath = subdir + os.sep + file  # create filepath to each text file
#            if filepath.endswith(".txt"):  # only looking for text files
#                newShip = Ship("path", "id", "year_month", "month", "cpa_time",
#                               "datetime", "file_time", "type", "name",
#                               0, 0, 0, 0, 0, [], [], 'cpa', 0, 0, 0, None, 0, None, 0, [], 0, 0)
#                ships.append(newShip)
#                print(folder)
#                ships[i].filepath = filepath[:34]
#                ships[i].id = filepath[34:57]
#                ships[i].year_month = filepath[26:33]
#                ships[i].month = int(filepath[31:33])
#                ships[i].file_time = datetime.strptime(
#                    filepath[44:57].strip(), "%y%m%d_%H%M%S")
#                with open(filepath, encoding="utf8", errors='ignore') as fp:  # extract specific lines
#                    for x, line in enumerate(fp):

#                        if 'HARPLat' in line:  # line 1 relates to harp latitude
#                            ships[i].harplat = float(line[8:].strip())
#                        if 'HARPLon' in line:  # line 2 relates to harp longitude
#                            ships[i].harplon = float(line[8:].strip())
#                        if 'Hydrophone' in line:
#                            # line 3 is harp id number
#                            ships[i].harp = line[11:].strip()
#                        if 'BroadBand' in line:
#                            ships[i].RL = line[17:].strip()
#                        if 'CPATime' in line:  # line 5 is date
#                            ships[i].cpa_time = line[24:].strip()
#                            ships[i].cpa_datetime = datetime.strptime(
#                                line[13:].strip(), '%m/%d/%Y %H:%M:%S')
#                        if 'IMO=' in line:
#                            ships[i].IMO = int(line[4:].strip())
#                        if 'MMSI' in line:
#                            # line 8 is the ships mmsi number
#                            ships[i].mmsi = int(line[5:].strip())
#                        if 'ShipType' in line:  # line 10 is ship type
#                            ships[i].type = line[9:].strip()
#                        if 'toBow[m]' in line:
#                            ships[i].length = float(line[9:].strip())
#                        if 'Draught[m]' in line:
#                            ships[i].draught = float(line[11:].strip())
#                        if 'CPADistance[m]' in line:
#                            ships[i].cpa = float(line[15:].strip())
#                        # these are the coord lines using them to calc distance from harp and add to array of distances
#                        if x > 18 or line[0].isdigit():
#                            sampletime = datetime.strptime(
#                                line[:19].strip(), '%m/%d/%Y %H:%M:%S')
#                            ships[i].sampletimes.append(sampletime)

#                            # this array will be x axis of the spectrograms
#                            lat = float(line[20:28].strip())
#                            lon = float(line[29:39].strip())
#                            coords_1 = (ships[i].harplat, ships[i].harplon)
#                            coords_2 = (lat, lon)
#                            shipDistance = geodesic(coords_1, coords_2).km
#                            ships[i].distance.append(shipDistance)
#                            ships[i].SOG.append(
#                                float(line.split(',')[4].strip()))

#                i += 1  # increment counter before making new ship

#    for ship in ships:
#        if ship.name == 'unknown' or ship.name.strip() == '' or len(ship.distance) < 5:  # clean up data
#            ships.remove(ship)
#    up.store(ships, folder)
## ships = extract("J:\ShippingCINMS_data\COP")
## txt = "Name: {}\nType: {}\nDate: {} \nTime: {}\n"
## for i in range(len(ships)):
#   # print(txt.format(ships[i].name, ships[i].type, ships[i].date, ships[i].time))

##extract_ships(rootdir,folder)

#Goal of this program is to extract the date and time and type of ship from data

import os
from datetime import datetime
from geopy.distance import geodesic
import unpickle as up
from importlib import reload
import h5py 

folder = "J:\\Pickled_Data_6\\"
rootdir = "M:\ShipNoise_nnet_input_CASE_only"
harp_data = "J:\HARPdataSummary_20190514.csv"
print(rootdir)

#class Ship:   #Create a general ship to contain extracted variables
#    def __init__(self, filepath, id, year_month, month, cpa_time, cpa_datetime,
#                file_time, type, CPA, COG, heading, passage, hMeanSSP,
#                distVec, length, SOG, draught, width):
#        self.filepath = filepath
#        self.id = id
#        self.year_month = year_month
#        self.month = month
#        self.cpa_time = cpa_time
#        self.cpa_datetime = cpa_datetime

#        self.file_time = file_time
#        self.type = type
#        self.CPA = CPA
#        self.COG = COG
#        self.heading = heading
#        self.passage = passage
#        self.hMeanSSP = hMeanSSP

#        self.distVec = distVec
#        self.length = length
#        self.SOG = SOG
#        self.draught = draught
#        self.width = width
#        print("self complete")



def extract_ships(rootdir, folder):
    reload(up)
    # up.clear_shelf(folder)
    ships = [] #array to be filled with ships
    i = 0 #counter variable
    print("starting extraction")
    for subdir, dirs, files in os.walk(rootdir): #goes through each file not only in root but each subdirectory
        for file in files:
            #print os.path.join(subdir, file)
            filepath = subdir + os.sep + file #create filepath to each text file
            if filepath.endswith(".mat"): #only looking for text files
                nameParts = os.path.splitext(file)
                Ship = {'filepath': nameParts[0],
                        'id': file[0:10],
                        'year_month': file[11:15],
                        'month': file[14:15]}
                
                print(file)

                try:
                    Ship['file_time']= datetime.strptime(file[11:20].strip(),"%y%m%d%H%M%S")
                except:
                    Ship['file_time']= 999

                fp = h5py.File(filepath, 'r')
                Ship['CPA'] = fp['thisCPA'][()]
                Ship['COG'] = fp['thisCOG'][()]
                Ship['distVec'] = fp['thisDistVec'][()]
                Ship['draught'] = fp['thisDraught'][()]                      
                Ship['heading'] = fp['thisHeading'][()]
                Ship['hMeanSSP'] = fp['thisHmean'][()]
                Ship['passage'] = fp['thisPassage'][()]
                Ship['profile'] = fp['thisProfile'][()]
                Ship['type'] = fp['thisShipType'][()]
                Ship['SOG'] = fp['thisSOG'][()]
                Ship['tonnage'] = fp['thisTonnage'][()]
                Ship['length'] = fp['thisLength'][()]
                Ship['MMSI'] = fp['MMSI'][()]
                Ship['passDate'] = fp['passDate'][()]
                up.store(Ship,folder)     
    #for ship in ships:
    #    if ship.type[0] == 0: #or ship.name.strip() == '' or len(ship.distance) == 0: #clean up data
    #        print("missing data: removing ship")
    #        ships.remove(ship)
    

# ships = extract("J:\ShippingCINMS_data\COP")
# txt = "Name: {}\nType: {}\nDate: {} \nTime: {}\n"
# for i in range(len(ships)):
   # print(txt.format(ships[i].name, ships[i].type, ships[i].date, ships[i].time))

extract_ships(rootdir,folder)    

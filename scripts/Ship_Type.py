import numpy as np
import os 
import unpickle as up
from dat_extract.extract.Ship_Variable_Extraction import Ship

rootdir = "J:\Pickled_Data_2\\"
all_types = []

class mmsi:
    def __init__(self,mmsi,weight,length,hp,type,deadweight):
        self.mmsi = mmsi
        self.weight = weight
        self.length = length
        self.hp = hp
        self.type = type
        self.deadweight = deadweight
        
def extract_mmsi(file):
    mmsis = []
    i=0
    with open(file, encoding="utf8",errors = 'ignore') as fp: #extract specific lines
        for x, line in enumerate(fp):
            newMMSI = mmsi(0,0,0,0,0,0)
            mmsis.append(newMMSI)
            values = [x.strip() for x in line.split(',')]
            if values[4] != 'NA':
                mmsis[i].mmsi = int(values[4]) #first value is actual mmsi
            else:
                mmsis[i].mmsi = 0
                
            if values[3] != 'NA':   
                mmsis[i].IMO = int(values[3]) #then IMO
            else:
                mmsis[i].IMO = 0
                
            if values[7] != 'NA':
                mmsis[i].length = float(values[7]) #7 value is length of ship
            else:
                mmsis[i].length = 0
            
            if values[6] != 'NA':
                mmsis[i].type = values[6] #6 value is type of ship
            else:
                mmsis[i].type = ''
            
            # if values[23] != 'NA':
                # mmsis[i].deadweight = float(values[23]) #23 value is deadweight of ship
            # else:
                # mmsis[i].deadweight = 0
            
            if values[25] != 'NA':
                mmsis[i].hp = float(values[25]) #3 value is length of ship
            else:
                mmsis[i].hp = 0
                
        
            
            i+=1
    return mmsis
    
def get_info(ship,mmsis):
    skip = True
    for mmsi in mmsis:
        if ship.mmsi == mmsi.mmsi and ship.IMO == mmsi.IMO and mmsi.length != 0:
            ship.length = mmsi.length
            ship.type = mmsi.type
            skip = False
    return skip

def get_all_types(ships):
    for ship in ships:
        if ship.type in all_types:
            # print('already got it')
            pass
        else:
            all_types.append(ship.type)
    print(all_types)
    print(len(all_types))
    return all_types

def match_type(ship,all):
    ship.type = all.index(ship.type)
    return ship

def match_all(rootdir):
    i=0
    mmsis = extract_mmsi('J:\VZDATAALL.csv')
    for ships in up.unpickle_batch(rootdir,8700,0,8700):
        for ship in ships:
            get_info(ship,mmsis)
        types = get_all_types(ships)
        
        for ship in ships:
            match_type(ship,types)
            
            # print(str(i))
            # up.one_jar(rootdir,ship,False)
            # i+=1
match_all('J:\Pickled_Data_2\\')
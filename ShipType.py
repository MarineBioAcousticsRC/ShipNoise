import unpickle as up
import numpy as np
from dat_extract.extract.Ship_Variable_Extraction import Ship

all_types = []
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
    for ships in up.unpickle_batch(rootdir,8700,0,8700):
        types = get_all_types(ships)
        for ship in ships:
            match_type(ship,types)
            # print(str(i))
            # up.one_jar(rootdir,ship,False)
            # i+=1
match_all('D:\Pickled_Data_2\\')
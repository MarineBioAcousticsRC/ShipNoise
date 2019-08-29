import time
from datetime import datetime
from dat_extract.extract.Ship_Variable_Extraction import Ship
import unpickle as up
import numpy as np

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def better_seconds(t):
    new_time = time.mktime(t.timetuple())
    return new_time

def convert_time(ship):
  
    #start_time = find_nearest(ship.sampletimes,ship.file_time) #get the start index and cut array to fit it
    start_time = 1
    start_index = 1
    times = ship.sampletimes[start_index:]
    #cpa_index = ship.sampletimes.index(ship.cpa_datetime)
    cpa_index = 1
    if ship.cpa_datetime<ship.file_time:
        bad = True
    else:
        bad = False
    result_array = []
    # for time in times:
        # result_array.append(better_seconds(time) - better_seconds(times[0])) #subtract start time
    # cpa_time = better_seconds(ship.cpa_datetime) - better_seconds(times[0]) #get new cpa_time in relation to file time
    cpa_time = 1
    return result_array, start_index, cpa_index,cpa_time,bad

def find_ship(folder):
    bad_ships = []
    ships = up.unpickle_ships(folder)
    for ship in ships:
        txtfile =  ship.filepath + ship.id + '.txt' #the original txt file
        converted_times,start,cpa_index,cpa_time,bad = convert_time(ship) #convert all times and find the file start time and cpa time
        if(bad):
           bad_ships.append(ship)
           print(txtfile)
    print(len(bad_ships))
    print(len(ships))
    print(len(bad_ships)/len(ships))
find_ship('D:\PickledData\\')
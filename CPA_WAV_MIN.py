from pydub import AudioSegment
import numpy as np
from datetime import datetime, timedelta 
import os 
import unpickle as up
from dat_extract.extract.Ship_Variable_Extraction import Ship
import time


filepath = "D:\ShippingCINMS_data\COP"
rootdir = "D:\PickledData\\"
destination_folder = "D:\CPA_WAV\\"

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def better_seconds(t):
    new_time = time.mktime(t.timetuple())
    return new_time



def convert_time(ship):
   
    start_time = find_nearest(ship.sampletimes,ship.file_time) #get the start index and cut array to fit it
    start_index = ship.sampletimes.index(start_time)
    times = ship.sampletimes[start_index:]
    cpa_index = ship.sampletimes.index(find_nearest(ship.sampletimes,ship.cpa_datetime))
    if(start_time>=ship.cpa_datetime):
        normal = False
    else:
        normal = True
    result_array = []
    for time in times:
        result_array.append(better_seconds(time) - better_seconds(times[0])) #subtract start time
    cpa_time = better_seconds(ship.cpa_datetime) - better_seconds(times[0]) #get new cpa_time in relation to file time
    
    return result_array, start_index, cpa_index,cpa_time,normal
    
def extract_cpa(cpa_time,wav):    
    
    bad = False
    og_wav = AudioSegment.from_wav(wav)
    thirty_sec = 30*1000
    cpa_time = cpa_time*1000
    print(cpa_time)
    if cpa_time>0:
        pre_cpa = og_wav[(cpa_time-thirty_sec) : cpa_time]
        post_cpa = og_wav[cpa_time : (cpa_time+thirty_sec)]

        new_wav = (pre_cpa + post_cpa)
    
        return new_wav,bad
    else:
        bad = True
        return None,bad
ships = up.unpickle_ships(rootdir)
ships = ships[1500:]


i = 0
for ship in ships:
    
    try:
        wavfilepath = ship.filepath + ship.id + '.wav' #the original wav file
        print(wavfilepath)
        destination =  destination_folder + ship.year_month +'\\' + ship.id + '.wav'
        result_array, start_index, cpa_index,cpa_time,normal = convert_time(ship)
        cpa_wav, bad = extract_cpa(cpa_time,wavfilepath)
        if bad:
            i+=1
            print('bad' + str(i))
        else:
            cpa_wav.export(destination,format="wav")
    except:
        up.one_jar(rootdir,ship,True)
        pass
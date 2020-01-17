from pydub import AudioSegment
import numpy as np
from datetime import datetime, timedelta 
import os 
import unpickle as up
from dat_extract.extract.Ship_Variable_Extraction import Ship
import time
from scipy import interpolate

filepath = "D:\ShippingCINMS_data\COP"
rootdir = "D:\Pickled_Data\\" #files with ship passages
destination_folder = "D:\CPA_WAV\\"

#class to hold all variables of mmsis
class mmsi:
    def __init__(self,mmsi,weight,length,hp):
        self.mmsi = mmsi
        self.weight = weight
        self.length = length
        self.hp = hp

def extract_mmsi(file):
    mmsis = []
    i=0
    with open(file, encoding="utf8",errors = 'ignore') as fp: #extract specific lines
        for x, line in enumerate(fp):
            newMMSI = mmsi(0,0,0,0)
            mmsis.append(newMMSI)
            values = [x.strip() for x in line.split(',')]
            if values[4] != 'NA':
                mmsis[i].mmsi = int(values[4]) #first value is actual mmsi
            else:
                mmsis[i].mmsi = 0
                
            if values[3] != 'NA':   
                mmsis[i].IMO = int(values[3])
            else:
                mmsis[i].IMO = 0
                
            # mmsis[i].weight = float(values[4]) #2 value is Dead weight
            if values[7] != 'NA':
                mmsis[i].length = float(values[7]) #3 value is length of ship
            else:
                mmsis[i].length = 0
            i+=1
    return mmsis
 #get the true length of the ship    
def get_length(ship,mmsis):
    skip = True
    for mmsi in mmsis:
        if ship.mmsi == mmsi.mmsi and ship.IMO == mmsi.IMO:
            ship.length = mmsi.length
            skip = False
    return skip
#finds nearest value in an array    
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]
#converts time to a more usable format
def better_seconds(t):
    new_time = time.mktime(t.timetuple())
    return new_time
#finds a value in an array and returns the index
def find_index(arr,value):
    result = np.where(arr == value)
    return result[0][0]

#lines up the times from timestamps in the txt file with the time in the wav file 
def convert_time(ship):
   
    start_time = find_nearest(ship.sampletimes,ship.file_time) #get the start index and cut array to fit it
    start_index = ship.sampletimes.index(start_time)
    times = ship.sampletimes[start_index:]
    cpa_index = ship.sampletimes.index(find_nearest(ship.sampletimes,ship.cpa_datetime))
    #not normal if cpa is is not in wav file
    if (start_time>=ship.cpa_datetime) or (len(times)<10):
        normal = False
    else:
        normal = True
    result_array = []
    for time in times:
        result_array.append(better_seconds(time) - better_seconds(times[0])) #subtract start time
    cpa_time = better_seconds(ship.cpa_datetime) - better_seconds(times[0]) #get new cpa_time in relation to wav file time
    
    return result_array, start_index, cpa_index,cpa_time,normal

#creates new array of distances to match wav file ship passage
def new_distances(ship,start_index,con_times):

    distances = ship.distance[start_index:]
    inter = interpolate.interp1d(con_times,distances, axis=0, fill_value="extrapolate")
    new_times = np.arange(0,con_times[len(con_times)-1],0.1)
    new_distances = inter(new_times)
    
    return new_distances,new_times
    
#uses all these pieces to find the correct times to cut the file to exactly one ship crossing
def find_ship_passage(ship,distances,new_times,cpa_time,cpa_sog):

    cpa_time = find_nearest(new_times, cpa_time)
    cpa_index = find_index(new_times,cpa_time)
    cpa_distance  =  distances[cpa_index]
    
    ship_length_km = ship.length/1000
    tan30 = 0.57735026919
    sog_kmps = cpa_sog /  1943.844
    
    pre_time = (cpa_time - ((ship_length_km * tan30)/sog_kmps))
    post_time = (cpa_time + ((ship_length_km * tan30)/sog_kmps))
    
    pre_time = find_nearest(new_times,pre_time)
    post_time = find_nearest(new_times,post_time)
    

    pre_index = find_index(new_times,pre_time)
    post_index = find_index(new_times,post_time)
    
    
    pre_dis = distances[pre_index]
    post_dis = distances[post_index]
    
    if pre_time > post_time: #case where the ship is going towards hydrophone
        hold = pre_time
        pre_time = post_time
        post_time = hold
    # print(cpa_time)
    # print(cpa_distance)
    # print(pre_dis)
    # print(post_dis)
    # print(pre_time)
    # print(post_time)
    
    return pre_time,post_time

#cuts wav file at specific times start and stop are in seconds 
#cutting happens in milliseconds
def cut_wav(start,stop,wav):
    
    start = start*1000
    stop = stop*1000
    
    wav_handle = AudioSegment.from_wav(wav)
    new_wav = wav_handle[start:stop]
    
    return new_wav

#goes through ships only cutting normal ones and saves the new wav files
def main(rootdir,destination):
    i = 0
    mmsis = extract_mmsi('D:\VZDATAALL.csv')
    for ships in up.unpickle_batch(rootdir, 100, 400, 500):
        for ship in ships:
           
            try:
                wavfilepath = ship.filepath + ship.id + '.wav' #the original wav file
                destination =  destination_folder + ship.year_month +'\\' + ship.id + '.wav'
                
                
                
                skip = get_length(ship,mmsis)
                
                converted_times, start_index, cpa_index,cpa_time,normal = convert_time(ship)
                cpa_sog = ship.SOG[cpa_index]
                if (not normal):
                    i+=1
                    print('bad ' + str(i))
                elif skip:
                    i+=1
                    print('mmsi not included ' + str(i))
                else:
                    distances, new_times = new_distances(ship, start_index, converted_times)
                    pre, post = find_ship_passage(ship,distances,new_times,cpa_time,cpa_sog)
                   
                    pass_wav = cut_wav(pre,post,wavfilepath)
                    pass_wav.export(destination,format="wav")
                    
                    print(wavfilepath)
                    pass_wav.export(destination,format="wav")
                    
            
                
            except:
                up.one_jar(rootdir,ship,True)
                print('something went wrong')
                pass
                    
main(rootdir,destination_folder)
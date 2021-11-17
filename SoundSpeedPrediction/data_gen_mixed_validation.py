import unpickle as up
import numpy as np
from keras.utils import np_utils
from dat_extract.extract.Ship_Variable_Extraction import Ship
import random
import pickle
import sys, os
# from Find_Avg_Values_Vector import Avg_Values
from Static_Avg_Values_Vector import Avg_Values

def Load_Avg(filepath):
    file = open(filepath,'rb')
    print(file)
    avg = pickle.load(file)
    return avg

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

#find all maxes in order to normalize all data also dont print stuff from this
print("Finding Avg Values")
blockPrint()
rng = Load_Avg('J:\\Range_Data.obj')
enablePrint()

global_feats = [] #list to hold all features

def Average(lst): 
    avg = sum(lst) / len(lst)
    
    if not np.isnan(avg):
        return avg
    else: 
        return 0

def get_feats():
    result = ''
    for feat in global_feats:
        result = result + ' ' + feat
    return result

def special_append(list,var,var_name):
    
    if not var_name in global_feats:
        global_feats.append(var_name)
    list.append(var)
    return list

def get_files(rootdir,start,stop):
    files = []
    
    for r, d, f in os.walk(rootdir):
        for file in f:
            if file.endswith('.obj'):
                files.append(os.path.join(r, file))
    files = files[:8500]
    random.shuffle(files) #shuffle files for even distribution of varying factors
    files = files[start:stop] #select set
    
    return files
    
#function to convert speed back to m/s
def conv(speed,i):
    return ((speed*rng.profile[1]) + rng.profile[0])
    
def eval_batch(rootdir,batch_size):
    i=0
    files = get_files(rootdir,0,batch_size)
    
    label_batch = []
    feat_batch = []
    spect_batch = []
    date_batch = []
    
    ships = []
    
    speeds_0_batch = []
    speeds_100_batch = []
    speeds_200_batch = []
    

    for b in range(batch_size):
        spect = []
        feats = []
        
        speed_0 = []
        speed_100 = []
        speed_200 = []
        
        if i==len(files):
            i=0
            random.shuffle(files) #shuffle files again when all have been used
        
        #unpickle one ship
        
        file = files[i]
        file_handler = open(file,'rb')
        ship = pickle.load(file_handler)
        ships.append(ship)
        i+=1

        #add extra data 
        ship.cpa = np.min(ship.distance)
        
        #add extra data 
        # feats.append((ship.length-g_avg.length)/g_avg.length_dev)
        feats.append((ship.month-6.5)/3.4520525295347)
        feats.append((ship.cpa-g_avg.cpa)/g_avg.cpa_dev)
        feats.append((Average(ship.SOG)-g_avg.SOG)/g_avg.SOG_dev)
        feats.append((ship.draught-g_avg.draught)/g_avg.draught_dev)
        feats.append((ship.encoded-g_avg.wspd)/g_avg.wspd_dev)
        # feats.append(ship.type)
        # feats.append(np.min(ship.distance))
        
        # feats.append(float(ship.temp[-1]))
        # feats.append(float((ship.sal[-1])[:-2]))
        # feats.append(float(ship.sound_speed/g_max.sound_speed))
        feats = np.array(feats)
        feat_batch.append(feats)

        
        # label_batch.append((float(ship.temp[0])/g_max.temp))
        # for i in range(len(ship.sound_speed)):
            # speeds.append((ship.sound_speed[i]-g_avg.sound_speed[i])/g_avg.sound_speed_dev[i])#/1500) #normalize and add soundspeed
        # label_batch.append(np.array(speeds))
      
        speed_0 = (ship.sound_speed[0]-g_avg.sound_speed[0])/(g_avg.sound_speed_dev[0])
        speeds_0_batch.append(speed_0)
        
        speed_100 = (ship.sound_speed[1]-g_avg.sound_speed[1])/(g_avg.sound_speed_dev[1])
        speeds_100_batch.append(speed_100)
        
        speed_200 = (ship.sound_speed[2]-g_avg.sound_speed[2])/(g_avg.sound_speed_dev[2])
        speeds_200_batch.append(speed_200)
        
        spect = np.asarray((ship.spect[:508,:508]).astype(float)) #PREPARE BATCH DATA
        spect /= g_avg.max_spect #use max value for spectrogram so technically normalizing because I haven't figured out how I want to standardize it yet
        spect = np.reshape(spect, (-1,508, 508,1))
        spect_batch.append(spect)
        
        # date_batch.append(ship.file_time)
        
    feat_batch = np.array(feat_batch)
    spect_batch = np.array(spect_batch)
    # Y_test = np.array(label_batch)
    speeds_0_batch = np.array(speeds_0_batch)
    speeds_100_batch = np.array(speeds_100_batch)
    speeds_200_batch = np.array(speeds_200_batch)
    Y_test = [speeds_0_batch,speeds_100_batch,speeds_200_batch]
    
    
    spect_batch = np.reshape(spect_batch, (-1,508,508,1))
        
        
    return ships, [feat_batch,spect_batch],Y_test #RETURN BATCH DATA     
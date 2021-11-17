import unpickle as up
import numpy as np
from keras.utils import np_utils
from dat_extract.extract.Ship_Variable_Extraction import Ship
import random
import pickle
import os
from Find_Max_Values import Max_Values,Find_Max
import sys, os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

#find all maxes in order to normalize all data also dont print stuff from this
print("Finding Max Values")
blockPrint()
g_max = Find_Max("D:\Pickled_Data_2\\")
print(g_max.cpa)
print(g_max.draught)
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

def conv(val):
    return val*g_max.sound_speed

def get_dev():
    std_dev = 7.318877426971886;
    return (std_dev/g_max.sound_speed)
    
def data_generator(rootdir,mode,batch_size):
    if mode=='train':
        print('train')
        #set up the file system for unpickling training data
        i=0
        files = get_files(rootdir,0,7250)
        
        #begin data generation
        while True:
            feat_batch = [] #extra data to be used in NN
            spect_batch = [] #spectrograms
            label_batch = [] #data to be predicted
            
            for b in range(batch_size):
                spect = []
                feats = []
                if i==len(files):
                    i=0
                    random.shuffle(files) #shuffle files again when all have been used
                
                #unpickle one ship
                file = files[i]
                file_handler = open(file,'rb')
                ship = pickle.load(file_handler)
                i+=1
                
                ship.cpa = np.min(ship.distance)
                
                #add extra data 
                # print('g_max.cpa '+str(g_max.cpa))
                # print('draught ' + str(g_max.draught))
                special_append(feats,(ship.length/g_max.length),'length')
                special_append(feats,(ship.month/12),'month')
                # special_append(feats,ship.type,'type')
                # feats.append((ship.cpa/g_max.cpa))
                special_append(feats,(Average(ship.SOG)/g_max.SOG),'avg SOG')
                special_append(feats,(ship.draught/g_max.draught),'draught')
                # feats.append(float(ship.sound_speed/g_max.sound_speed))
                # feats.append(float(ship.temp[0]/g_max.temp))
                # feats.append(float((ship.sal[0]/g_max.sal)))
                # feats.append(float(ship.speed))
                # print("ship cpa " + str(ship.cpa))
                special_append(feats,(ship.cpa/g_max.cpa),'cpa')
                feats = np.array(feats)
                # print('feats' + str(feats))
                feat_batch.append(feats)
                
                # print('soundspeed' + str(ship.sound_speed/g_max.sound_speed))
                label_batch.append((ship.sound_speed/g_max.sound_speed))#/1500) #normalize and add soundspeed
                # label_batch.append((float(ship.temp[0])/g_max.temp))
                
                spect = np.array((ship.spect[:508,:508]).astype(float)) #PREPARE spect DATA
                # print(spect.shape)
                spect /= g_max.spect
                # print(spect)
                spect = np.reshape(spect, (-1,508, 508,1))
                spect_batch.append(spect)
                
 
            
            #prepare batches
            
            feat_batch = np.array(feat_batch)
            spect_batch = np.array(spect_batch)
            Y_train = np.array(label_batch)
            # print(feat_batch[0].shape)
            spect_batch = np.reshape(spect_batch, (-1,508,508,1))
            
            
            yield [feat_batch,spect_batch],Y_train #RETURN BATCH DATA    
          
    if mode == 'test':
        print('test')
        # set up the file system for unpickling training data
        i=0
        files = get_files(rootdir,7250,8700)
        
        while True:
            
            label_batch = []
            feat_batch = []
            spect_batch = []
            
            for b in range(batch_size):
                spect = []
                feats = []
                
                if i==len(files):
                    i=0
                    random.shuffle(files) #shuffle files again when all have been used
                
                #unpickle one ship
                
                file = files[i]
                file_handler = open(file,'rb')
                ship = pickle.load(file_handler)
                i+=1
                
                ship.cpa = np.min(ship.distance)
                #add extra data 
                
                feats.append(ship.length/g_max.length)
                feats.append(ship.month/12)
                # feats.append(ship.type)
                # feats.append(np.min(ship.distance))
                feats.append(Average(ship.SOG)/g_max.SOG)
                feats.append(ship.draught/g_max.draught)
                # feats.append(float(ship.temp[-1]))
                # feats.append(float((ship.sal[-1])[:-2]))
                # feats.append(float(ship.sound_speed/g_max.sound_speed))
                feats.append(ship.cpa/g_max.cpa)
                feats = np.array(feats)
                feat_batch.append(feats)

                label_batch.append(ship.sound_speed/g_max.sound_speed)#/1500) #normalize and get soundspeed
                # label_batch.append((float(ship.temp[0])/g_max.temp))
              
                spect = np.asarray((ship.spect[:508,:508]).astype(float)) #PREPARE BATCH DATA
                spect /= g_max.spect
                spect = np.reshape(spect, (-1,508, 508,1))
                spect_batch.append(spect)

            feat_batch = np.array(feat_batch)
            spect_batch = np.array(spect_batch)
            Y_test = np.array(label_batch)

            spect_batch = np.reshape(spect_batch, (-1,508,508,1))
            
            
            yield [feat_batch,spect_batch],Y_test #RETURN BATCH DATA    
def one_batch(rootdir,batch_size):
    i=0
    files = get_files(rootdir,5000,7000+batch_size)


    
    label_batch = []
    feat_batch = []
    spect_batch = []
    
    for b in range(batch_size):
        spect = []
        feats = []
        
        if i==len(files):
            i=0
            random.shuffle(files) #shuffle files again when all have been used
        
        #unpickle one ship
        
        file = files[i]
        file_handler = open(file,'rb')
        ship = pickle.load(file_handler)
        i+=1

        #add extra data 
        ship.cpa = np.min(ship.distance)
        
        feats.append(ship.length/g_max.length)
        feats.append(ship.month/12)
    
        feats.append(Average(ship.SOG)/g_max.SOG)
        feats.append(ship.draught/g_max.draught)
        # feats.append(float(ship.sound_speed/g_max.sound_speed))
        feats.append(ship.cpa/g_max.cpa)
        feats = np.array(feats)
        feat_batch.append(feats)

        label_batch.append(ship.sound_speed/g_max.sound_speed)#/1500) #normalize and get soundspeed
        # label_batch.append((float(ship.temp[0])/g_max.temp))
      
        spect = np.asarray((ship.spect[:508,:508]).astype(float)) #PREPARE BATCH DATA
        spect /= g_max.spect
        spect = np.reshape(spect, (-1,508, 508,1))
        spect_batch.append(spect)

    feat_batch = np.array(feat_batch)
    spect_batch = np.array(spect_batch)
    Y_test = np.array(label_batch)

    spect_batch = np.reshape(spect_batch, (-1,508,508,1))
        
        
    return [feat_batch,spect_batch],Y_test #RETURN BATCH DATA 
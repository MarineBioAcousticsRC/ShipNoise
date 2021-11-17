import unpickle as up
import numpy as np
from keras.utils import np_utils
import random
import pickle
from Static_Avg_Values_Vector import static_range_values, Save_Avg, Load_Avg
import sys, os
import time
import matplotlib.pyplot as plt
from keras import backend as K
#from custom_losses import mape_0,corr_0

# from dat_extract.extract.MARCAD_Ship_Variable_Extraction import Ship

# source folder of ships
folder = "J:\Pickled_Data_6\\"

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

#find all maxes in order to normalize all data also dont print stuff from this
print("Finding Avg Values: ")
# blockPrint()
avg_obj_filepath = 'J:\\Range_Data.obj'

if(os.path.exists(avg_obj_filepath)):
    print("Found range file")
    rng = Load_Avg(avg_obj_filepath)
#else:
#    rng = Find_Avg(folder)
#    Save_Avg(avg_obj_filepath,rng)
enablePrint()

global_feats = [] #list to hold all features

def Average(lst): 
    avg = sum(lst) / len(lst)
    print(lst)
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
    print("Finding .obj files...")
    files = []
    
    for r, d, f in os.walk(rootdir):
        for file in f:
            if file.endswith('.obj'):
                files.append(os.path.join(r, file))
    files = files[:stop]
    random.shuffle(files) #shuffle files for even distribution of varying factors
    files = files[start:stop] #select set
    print("All .obj Files Located")
    print(np.size(files))
    return files
    
#function to convert speed back to m/s
def conv(speed):
    return ((speed * (rng.profile[1]-rng.profile[0])) + rng.profile[0])

def get_dev():
    print('Warning, standard dev not actually implemented')
    std_dev = rng.profile[0]
    return (std_dev)

g_files = get_files(folder,0,3800) #global files so all have access to same shuffled directory
# g_files = get_files(folder,0,8700) #global files so all have access to same shuffled directory
print(len(g_files))

def eval_batch(batch_size):
    # print(mode)
    i=0
    #if mode=='train':
    #    files = g_files[0:1499] # %75 of data is training %80 would be 7120
    #elif mode=='test':
    files = g_files[3301:3800] 
    
    batch_num = 0
    #begin data generation
    # tot_elapsed = 0
    feat_batch = [] #extra data to be used in NN
    spect_batch = [] #spectrograms
    label_batch = [] #data to be predicted

    all_speeds = []
    num_speeds = 1
    for b in range(batch_size):

        spect = []
        feats = []
          
        if i==len(files):
            i=0
            random.shuffle(files) #shuffle files again when all have been used
                
        #unpickle one ship
        #print('train step 1 {}: about to open file'.format(i))
        file = files[i]
        file_handler = open(file,'rb')
        # start = time.time()
        print('loading file'.format(file))
        print(file)

        ship = pickle.load(file_handler)
        # stop = time.time()
        # print(ship)

        i+=1
        #print('train step 2 {}: file opened'.format(i))
                
        #standardize and add data using formula (val - avg)/std_dev 
        # print('g_max.cpa '+str(g_max.cpa))
        # print('draught ' + str(g_max.draught))
        feats.append(2*((ship['length']-rng.length[0])/(rng.length[1]-rng.length[0]))-1)
        # special_append(feats,((ship.month-6.5)/3.4520525295347),'month')
        feats.append(2*((ship['CPA']-rng.CPA[0])/(rng.CPA[1]-rng.CPA[0]))-1)
        feats.append(2*((ship['SOG']-rng.SOG[0])/(rng.SOG[1]-rng.SOG[0]))-1)
        feats.append(2*((ship['COG']-rng.COG[0])/(rng.COG[1]-rng.COG[0]))-1)
        feats.append(2*((ship['heading']-rng.heading[0])/(rng.heading[1]-rng.heading[0]))-1)
        feats.append(2*((ship['type']-rng.type[0])/(rng.type[1]-rng.type[0]))-1)
        feats.append(2*((ship['draught']-rng.draught[0])/(rng.draught[1]-rng.draught[0]))-1)
        feats.append((ship['MMSI'])/100000000)#-rng.tonnage[0])/(rng.tonnage[1]-rng.tonnage[0]))
        #feats.append(int(str(ship['passDateStr'])))  

        feats = np.array(feats)
        feats = np.reshape(feats, (8))
        
        feat_batch.append(feats)
        # print(feats)   
          
        myProfile = (ship['profile'][0]-rng.profile[0])/(rng.profile[1]-rng.profile[0])#PREPARE spect DATA
        # print(rng.profile)
        all_speeds.append(myProfile)#/1500) #normalize and add soundspeed
        # print(all_speeds)
        # print('train step 4 {}: speeds added'.format(i))
             
        spect = np.array((ship['passage']).astype(float)) #PREPARE spect DATA
        # spect = (spect-rng.passage[0]) / (rng.passage[1]-rng.passage[0])
        # print('train step 6 {}: spect standardized'.format(i))

        # spect = g_avg.max_spect #use max value for spectrogram so technically normalizing because I haven't figured out how I want to standardize it yet
        # print(spect)
        # subsample 10 steps
        nlist = np.random.randint(0,high = 250, size = 20)
        nlist = np.sort(nlist)
        # spect = g_avg.max_spect #use max value for spectrogram so technically normalizing because I haven't figured out how I want to standardize it yet
        spect = spect[nlist,:]
        spect = np.reshape(spect, (-1,len(nlist),512))#,1,1))
   
        spect_batch.append(spect)
        #print('train step 7 {}: spect reshaped and appended'.format(i))

        file_handler.close()
          
            
    #prepare batches
    #print("done loading batch")
    #print('Size of batched spectra before array: {}'.format(len(spect_batch)))

    spect_batch = np.array(spect_batch)
    spect_batch = np.reshape(spect_batch, (-1,len(nlist),512))#,1,1))
    all_speeds = np.array(all_speeds)
    #print('Size of batched spectra after array: {}'.format(spect_batch.size))
    #print('Size of batched speeds after array: {}'.format(all_speeds.size))

    # print(feat_batch)
        
    feat_batch = np.array(feat_batch)
    # feat_batch = np.reshape(feat_batch, (batch_size,8))
    # for n in range(num_speeds):
    # np.array(all_speeds)
    # Y_train = [speeds_0_batch,speeds_100_batch,speeds_200_batch]

    # print(Y_train)
    # Y_train = np.array(label_batch)
    # print(feat_batch[0].shape)
    # spect_batch = np.reshape(spect_batch, (-1,512,512,1))
    # print('Size of batched feats before reshape: {}'.format(feat_batch.size))
    # feat_batch = np.reshape(feat_batch, (batch_size,8))
    # print('Size of batched feats after reshape: {}'.format(feat_batch.size))

    # print("Train Batch Number: {} Time Elapsed: {} Average Sample Time: {}".format(batch_num,tot_elapsed,tot_elapsed/batch_size))

    batch_num = batch_num + 1
    # if mode == 'train':
    
    # Y_test = [speeds_0_batch,speeds_100_batch,speeds_200_batch]
    Y_test = all_speeds
    # Y_train = np.array(all_speeds)
    # print('feat_batch shape is: {}'.format(feat_batch.shape))
    # print('feat_batch type is: {}'.format(type(feat_batch)))

    # print('spect_batch shape is: {}'.format(spect_batch.shape))
    # print('Y_test type is: {}'.format(type(Y_test)))
    # print(Y_test)
    # print(conv(Y_test))
    # return [feat_batch,spect_batch],Y_test #RETURN BATCH DATA    
    # return [feat_batch,spect_batch],Y_test #RETURN BATCH DATA    
    return [spect_batch],Y_test #RETURN BATCH DATA    


# x_data, true_speeds =eval_batch(2)  
# print(true_speeds)
# corr_0(true_speeds[0],true_speeds[1])

def data_generator(mode,batch_size):
    print(mode)
    i=0
    if mode=='train':
        files = g_files[0:3300] # %75 of data is training %80 would be 7120
    elif mode=='test':
        files = g_files[3301:3800] 
    
    batch_num = 0
    #begin data generation
    while True:
        # tot_elapsed = 0
        feat_batch = [] #extra data to be used in NN
        spect_batch = [] #spectrograms
        label_batch = [] #data to be predicted

        all_speeds = []
        num_speeds = 1
        # for s in range(num_speeds):
        #    all_speeds.append([])
        for b in range(batch_size):

            spect = []
            feats = []
            
            if i==len(files):
                i=0
                random.shuffle(files) #shuffle files again when all have been used
                
            #unpickle one ship
            #print('train step 1 {}: about to open file'.format(i))
            file = files[i]
            file_handler = open(file,'rb')
            # start = time.time()
            #print('loading file'.format(file))
            #print(file)

            ship = pickle.load(file_handler)
            # stop = time.time()
            # print(ship)

            i+=1
            #print('train step 2 {}: file opened'.format(i))
                
            #standardize and add data using formula (val - avg)/std_dev 
            # print('g_max.cpa '+str(g_max.cpa))
            # print('draught ' + str(g_max.draught))
            feats.append(2*((ship['length']-rng.length[0])/(rng.length[1]-rng.length[0]))-1)
            # special_append(feats,((ship.month-6.5)/3.4520525295347),'month')
            feats.append(2*((ship['CPA']-rng.CPA[0])/(rng.CPA[1]-rng.CPA[0]))-1)
            feats.append(2*((ship['SOG']-rng.SOG[0])/(rng.SOG[1]-rng.SOG[0]))-1)
            feats.append(2*((ship['COG']-rng.COG[0])/(rng.COG[1]-rng.COG[0]))-1)
            feats.append(2*((ship['heading']-rng.heading[0])/(rng.heading[1]-rng.heading[0]))-1)
            feats.append(2*((ship['type']-rng.type[0])/(rng.type[1]-rng.type[0]))-1)
            feats.append(2*((ship['draught']-rng.draught[0])/(rng.draught[1]-rng.draught[0]))-1)
            # feats.append((ship['MMSI'])/100000000)#-rng.tonnage[0])/(rng.tonnage[1]-rng.tonnage[0]))
            #feats.append(int(np.reshape(ship['passDateStr']),[1,]))  

            #print(feats)   
                
            feats = np.array(feats)
            feats = np.reshape(feats, (7))
        
            feat_batch.append(feats)
                   
            myProfile = (ship['profile'][0]-rng.profile[0])/(rng.profile[1]-rng.profile[0])#PREPARE spect DATA
            # print(myProfile)
            all_speeds.append(myProfile)#/1500) #normalize and add soundspeed
            # print(all_speeds)
            #print('train step 4 {}: speeds added'.format(i))
             
            spect = np.array((ship['passage']).astype(float)) #PREPARE spect DATA
            # spect = np.array((ship.spect[:508,:508]).astype(float)) #PREPARE spect DATA
            # spect = (spect - g_avg.avg_spect) / (g_avg.spect_dev) #standardize spects based on the average values from each one
            spect = (spect-rng.passage[0]) / (rng.passage[1]-rng.passage[0])
            #print('train step 6 {}: spect standardized'.format(i))
            # subsample 10 steps
            nlist = np.random.randint(0,high = 250, size = 20)
            nlist = np.sort(nlist)
            # spect = g_avg.max_spect #use max value for spectrogram so technically normalizing because I haven't figured out how I want to standardize it yet
            spect = spect[nlist,:]
            spect = np.reshape(spect, (-1,len(nlist),512))#,1,1))
            
            # spect = np.reshape(spect, (-1,508, 508,1))
            spect_batch.append(spect)
            #print('train step 7 {}: spect reshaped and appended'.format(i))

            file_handler.close()
                
            # elapsed = stop - start
            # tot_elapsed = tot_elapsed + elapsed
 
            
        #prepare batches
        #print("done loading batch")
        # print('Size of batched spectra before array: {}'.format(len(spect_batch)))

        spect_batch = np.array(spect_batch)
        spect_batch = np.reshape(spect_batch, (-1,len(nlist),512))#,1,1))
        all_speeds = np.array(all_speeds)
        # print('Size of batched spectra after array: {}'.format(spect_batch.size))
        # print('Size of batched speeds after array: {}'.format(all_speeds.size))

        # print(feat_batch)
        
        feat_batch = np.array(feat_batch)
        #feat_batch = np.reshape(feat_batch, (batch_size,8))
        #for n in range(num_speeds):
        # np.array(all_speeds)
        # Y_train = [speeds_0_batch,speeds_100_batch,speeds_200_batch]

        # print(Y_train)
        # Y_train = np.array(label_batch)
        # print(feat_batch[0].shape)
        #spect_batch = np.reshape(spect_batch, (-1,512,512,1))
        # print('Size of batched feats before reshape: {}'.format(feat_batch.size))
        #feat_batch = np.reshape(feat_batch, (batch_size,8))
        #print('Size of batched feats after reshape: {}'.format(feat_batch.size))

        # print("Train Batch Number: {} Time Elapsed: {} Average Sample Time: {}".format(batch_num,tot_elapsed,tot_elapsed/batch_size))

        batch_num = batch_num + 1
        if mode == 'train':
            Y_train = all_speeds
            #yield [feat_batch,spect_batch],Y_train #RETURN BATCH DATA    
            yield [spect_batch],Y_train #RETURN BATCH DATA    

        elif mode == 'test':
            Y_test = all_speeds
            #yield [feat_batch,spect_batch],Y_test #RETURN BATCH DATA    
            yield [spect_batch],Y_test #RETURN BATCH DATA    

# [x,Y_test] = eval_batch(2)
# plt.plot(x[0,0,0,:,0])
#y_true = conv(Y_test[0,])
#print(y_true)

#y_pred = conv(Y_test[1,])
#print(y_pred)
#print(np.sqrt(np.sum(np.square(y_pred - y_true))))
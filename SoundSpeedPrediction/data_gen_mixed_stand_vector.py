import unpickle as up
import numpy as np
from keras.utils import np_utils
from dat_extract.extract.Ship_Variable_Extraction import Ship
import random
import pickle
from Find_Avg_Values_Vector import Avg_Values,Find_Avg, Save_Avg, Load_Avg
import sys, os
import time

# source folder of ships
folder = "J:\Pickled_Data_3\\"

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

#find all maxes in order to normalize all data also dont print stuff from this
print("Finding Avg Values: ")
# blockPrint()
avg_obj_filepath = 'J:\\Average_Data_spect_max.obj'
if(os.path.exists(avg_obj_filepath)):
    g_avg = Load_Avg(avg_obj_filepath)
else:
    g_avg = Find_Avg(folder)
    Save_Avg(avg_obj_filepath,g_avg)
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
    print(len(files))
    return files
    
#function to convert speed back to m/s
def conv(speed,i):
    return ((speed*g_avg.sound_speed_dev[i]) + g_avg.sound_speed[i])

def get_dev():
    std_dev = g_avg.sound_speed_dev
    return (std_dev)

g_files = get_files(folder,0,10) #global files so all have access to same shuffled directory
# g_files = get_files(folder,0,8700) #global files so all have access to same shuffled directory

#def data_generator(mode,batch_size):
#    if mode=='train':
        
#        #set up the file system for unpickling training data
#        i=0
#        # files = g_files[0:4744] 
#        files = g_files[0:6675] # %75 of data is training %80 would be 7120
#        # files = g_files[0:6525] # %75 of data is training %80 would be 7120
#        batch_num = 0
#        #begin data generation
#        while True:
#            # tot_elapsed = 0
#            feat_batch = [] #extra data to be used in NN
#            spect_batch = [] #spectrograms
#            label_batch = [] #data to be predicted

#            # speeds_0_batch = []
#            # speeds_50_batch = []
#            # speeds_100_batch = []
#            # speeds_150_batch = []
#            # speeds_200_batch = []
#            all_speeds = []
#            num_speeds = 5
#            for s in range(num_speeds):
#                all_speeds.append([])
            
#            for b in range(batch_size):
                

#                spect = []
#                feats = []
                
#                # speed_0 = []
#                # speed_50 = []
#                # speed_100 = []
#                # speed_150 = []
#                # speed_200 = []
                
#                if i==len(files):
#                    i=0
#                    random.shuffle(files) #shuffle files again when all have been used
                
#                #unpickle one ship
#                #print('train step 1 {}: about to open file'.format(i))
#                file = files[i]
#                file_handler = open(file,'rb')
#                # start = time.time()
#                ship = pickle.load(file_handler)
#                # stop = time.time()
#                i+=1
#                #print('train step 2 {}: file opened'.format(i))
                
#                ship.cpa = np.min(ship.distance)
                
#                #standardize and add data using formula (val - avg)/std_dev 
#                # print('g_max.cpa '+str(g_max.cpa))
#                # print('draught ' + str(g_max.draught))
#                # special_append(feats,((ship.length-g_avg.length)/g_avg.length_dev),'length')
#                special_append(feats,((ship.month-6.5)/3.4520525295347),'month')
#                special_append(feats,((ship.cpa-g_avg.cpa)/g_avg.cpa_dev),'cpa')
#                special_append(feats,((Average(ship.SOG)-g_avg.SOG)/g_avg.SOG_dev),'avg_SOG')
#                special_append(feats,((ship.draught-g_avg.draught)/g_avg.draught_dev),'draught')
                
#                special_append(feats,((ship.encoded-g_avg.wspd)/g_avg.wspd_dev),'wind_speed')
#                # special_append(feats,ship.type,'type')
#                # feats.append((ship.cpa/g_max.cpa))
#                # feats.append(float(ship.sound_speed/g_max.sound_speed))
#                # feats.append(float(ship.temp[0]/g_max.temp))
#                # feats.append(float((ship.sal[0]/g_max.sal)))
#                # feats.append(float(ship.speed))
#                # print("ship cpa " + str(ship.cpa))
                
#                feats = np.array(feats)
#                # print('feats' + str(feats))
#                feat_batch.append(feats)
#                #print('train step 3 {}: feats added'.format(i))
                
#                # print('soundspeed' + str(ship.sound_speed/g_max.sound_speed))
                
#                # for i in range(len(ship.sound_speed)):
#                    # speeds.append((ship.sound_speed[i]-g_avg.sound_speed[i])/g_avg.sound_speed_dev[i])#/1500) #normalize and add soundspeed
#                # label_batch.append(np.array(speeds))
#                # speed_0 = (ship.sound_speed[0]-g_avg.sound_speed[0])/(g_avg.sound_speed_dev[0])
#                # speeds_0_batch.append(speed_0)
                
#                # speed_0 = (ship.sound_speed[1]-g_avg.sound_speed[1])/(g_avg.sound_speed_dev[1])
#                # speeds_0_batch.append(speed_0)

#                # speed_100 = (ship.sound_speed[1]-g_avg.sound_speed[1])/(g_avg.sound_speed_dev[1])
#                # speeds_100_batch.append(speed_100)
                
#                # speed_200 = (ship.sound_speed[2]-g_avg.sound_speed[2])/(g_avg.sound_speed_dev[2])

#                # speeds_200_batch.append(speed_200)

#                for j in range(num_speeds):
#                    all_speeds[j].append((ship.sound_speed[j]-g_avg.sound_speed[j])/g_avg.sound_speed_dev[j])#/1500) #normalize and add soundspeed
#                #print('train step 4 {}: speeds added'.format(i))

#                spect = np.array((ship.spect[:255,:255]).astype(float)) #PREPARE spect DATA
#                #print('train step 5 {}: spect formatted'.format(i))

#                # spect = np.array((ship.spect[:508,:508]).astype(float)) #PREPARE spect DATA
#                # print(spect.shape)
#                # spect = (spect - g_avg.avg_spect) / (g_avg.spect_dev) #standardize spects based on the average values from each one
#                spect = spect / g_avg.max_spect
#                #print('train step 6 {}: spect standardized'.format(i))

#                # spect = g_avg.max_spect #use max value for spectrogram so technically normalizing because I haven't figured out how I want to standardize it yet
#                # print(spect)
#                spect = np.reshape(spect, (-1,255,255,1))
#                # spect = np.reshape(spect, (-1,508, 508,1))
#                spect_batch.append(spect)
#                #print('train step 7 {}: spect reshaped and appended'.format(i))

#                file_handler.close()
                
#                # elapsed = stop - start
#                # tot_elapsed = tot_elapsed + elapsed
 
            
#            #prepare batches
            
#            feat_batch = np.array(feat_batch)
#            spect_batch = np.array(spect_batch)
#            # speeds_0_batch = np.array(speeds_0_batch)
#            # speeds_100_batch = np.array(speeds_100_batch)
#            # speeds_200_batch = np.array(speeds_200_batch)
#            for n in range(num_speeds):
#                np.array(all_speeds[n])
#            # Y_train = [speeds_0_batch,speeds_100_batch,speeds_200_batch]
#            Y_train = all_speeds
#            # print(Y_train)
#            # Y_train = np.array(label_batch)
#            # print(feat_batch[0].shape)
#            spect_batch = np.reshape(spect_batch, (-1,255,255,1))
#            # spect_batch = np.reshape(spect_batch, (-1,508,508,1))
#            # stop = time.time()
#            # elapsed = stop - start
#            # print("Train Batch Number: {} Time Elapsed: {} Average Sample Time: {}".format(batch_num,tot_elapsed,tot_elapsed/batch_size))

#            batch_num = batch_num + 1

#            yield [feat_batch,spect_batch],Y_train #RETURN BATCH DATA    
          
#    if mode == 'test':
#        # set up the file system for unpickling testing data
#        i=0
#        files = g_files[6675:8900] # %25 of data is testing %20 would be 7120
#        # files = g_files[6525:8900] # %25 of data is testing %20 would be 7120
#        # files = g_files[4744:5930] 
#        batch_num = 0
        
#        while True:
#            tot_elapsed = 0
#            label_batch = []
#            feat_batch = []
#            spect_batch = []
            
#            # speeds_0_batch = []
#            # speeds_100_batch = []
#            # speeds_200_batch = []
#            all_speeds = []
#            num_speeds = 5
#            for s in range(num_speeds):
#                all_speeds.append([])

#            for b in range(batch_size):
#                # start = time.time()
                
#                spect = []
#                feats = []
                
#                # speed_0 = []
#                # speed_100 = []
#                # speed_200 = []
                
#                if i==len(files):
#                    i=0
#                    random.shuffle(files) #shuffle files again when all have been used
                
#                #unpickle one ship
#                #print('test step 1 {}'.format(i))
#                file = files[i]
                
#                file_handler = open(file,'rb')
                
#                ship = pickle.load(file_handler)
                
#                i+=1
#                #print('test step 2 {}'.format(i))
                
#                ship.cpa = np.min(ship.distance)
#                #add extra data 
#                # feats.append((ship.length-g_avg.length)/g_avg.length_dev)
#                feats.append((ship.month-6.5)/3.4520525295347)
#                feats.append((ship.cpa-g_avg.cpa)/g_avg.cpa_dev)
#                feats.append((Average(ship.SOG)-g_avg.SOG)/g_avg.SOG_dev)
#                feats.append((ship.draught-g_avg.draught)/g_avg.draught_dev)
#                feats.append((ship.encoded-g_avg.wspd)/g_avg.wspd_dev)
#                # feats.append(ship.type)
#                # feats.append(np.min(ship.distance))
                
#                # feats.append(float(ship.temp[-1]))
#                # feats.append(float((ship.sal[-1])[:-2]))
#                # feats.append(float(ship.sound_speed/g_max.sound_speed))
#                feats = np.array(feats)
#                feat_batch.append(feats)

                
#                # label_batch.append((float(ship.temp[0])/g_max.temp))
#                # for i in range(len(ship.sound_speed)):
#                    # speeds.append((ship.sound_speed[i]-g_avg.sound_speed[i])/g_avg.sound_speed_dev[i])#/1500) #normalize and add soundspeed
#                # label_batch.append(np.array(speeds))
#                # speed_0 = (ship.sound_speed[0]-g_avg.sound_speed[0])/(g_avg.sound_speed_dev[0])
#                # speeds_0_batch.append(speed_0)
                
#                # speed_100 = (ship.sound_speed[1]-g_avg.sound_speed[1])/(g_avg.sound_speed_dev[1])
#                # speeds_100_batch.append(speed_100)
                
#                # speed_200 = (ship.sound_speed[2]-g_avg.sound_speed[2])/(g_avg.sound_speed_dev[2])
#                # speeds_200_batch.append(speed_200) 

#                for j in range(num_speeds):
#                    all_speeds[j].append((ship.sound_speed[j]-g_avg.sound_speed[j])/g_avg.sound_speed_dev[j])#/1500) #normalize and add soundspeed
                
#                #print('test step 3 {}'.format(i))

#                spect = np.asarray((ship.spect[:255,:255]).astype(float)) #PREPARE BATCH DATA
                
#                #print('test step 4 {}'.format(i))

#                # spect = np.asarray((ship.spect[:508,:508]).astype(float)) #PREPARE BATCH DATA
#                # spect = (spect - g_avg.avg_spect) / (g_avg.spect_dev) #standardize spects based on the average values from each one
#                spect = spect / g_avg.max_spect
#                #print('test step 5 {}'.format(i))

#                spect = np.reshape(spect, (-1,255,255,1))
                
#                #print('test step 6 {}'.format(i))

#                # spect = np.reshape(spect, (-1,508, 508,1))
#                spect_batch.append(spect)
#                file_handler.close()

#                # stop = time.time()
#                # elapsed = stop - start
#                # tot_elapsed = tot_elapsed + elapsed

#            feat_batch = np.array(feat_batch)
#            spect_batch = np.array(spect_batch)
            
#            # speeds_0_batch = np.array(speeds_0_batch)
#            # speeds_100_batch = np.array(speeds_100_batch)
#            # speeds_200_batch = np.array(speeds_200_batch)
#            for n in range(num_speeds):
#                np.array(all_speeds[n])
#            Y_test = all_speeds

#            spect_batch = np.reshape(spect_batch, (-1,255,255,1))
#            # spect_batch = np.reshape(spect_batch, (-1,508,508,1))
#            # print("Test Batch Number: {} Time Elapsed: {} Average Sample Time: {}".format(batch_num,tot_elapsed,tot_elapsed/batch_size))
#            batch_num = batch_num + 1

#            yield [feat_batch,spect_batch],Y_test #RETURN BATCH DATA    

def eval_batch(batch_size):
    i=0
    # files = files = g_files[8000:8000+batch_size] 
    files = g_files[:9]

    
    label_batch = []
    feat_batch = []
    spect_batch = []
    date_batch = []
    
    # speeds_0_batch = []
    # speeds_100_batch = []
    # speeds_200_batch = []
    all_speeds = [] 
    num_speeds = 5
    for i in range(num_speeds):
        all_speeds.append([])

    for b in range(batch_size):
        
        spect = []
        feats = []
        
        # speed_0 = []
        # speed_100 = []
        # speed_200 = []
        
        if i==len(files):
            i=0
            random.shuffle(files) #shuffle files again when all have been used
        
        #unpickle one ship
        print(len(files))
        file = files[i]
        file_handler = open(file,'rb')
        ship = pickle.load(file_handler)
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
        print('feats type {}'.format(type(feats)))

        feat_batch.append(feats)
        print('feat batch type: {}'.format(type(feat_batch)))

        
        # label_batch.append((float(ship.temp[0])/g_max.temp))
        # for i in range(len(ship.sound_speed)):
            # speeds.append((ship.sound_speed[i]-g_avg.sound_speed[i])/g_avg.sound_speed_dev[i])#/1500) #normalize and add soundspeed
        # label_batch.append(np.array(speeds))
        for j in range(num_speeds):
            all_speeds[j].append((ship.sound_speed[j]-g_avg.sound_speed[j])/g_avg.sound_speed_dev[j])#/1500) #normalize and add soundspeed
        # speed_0 = (ship.sound_speed[0]-g_avg.sound_speed[0])/(g_avg.sound_speed_dev[0])
        # speeds_0_batch.append(speed_0)
        print('all_speeds type: {}'.format(type(all_speeds)))

        # speed_100 = (ship.sound_speed[1]-g_avg.sound_speed[1])/(g_avg.sound_speed_dev[1])
        # speeds_100_batch.append(speed_100)
        
        # speed_200 = (ship.sound_speed[2]-g_avg.sound_speed[2])/(g_avg.sound_speed_dev[2])
        # speeds_200_batch.append(speed_200)
        
        spect = np.asarray((ship.spect[:255,:255]).astype(float)) #PREPARE BATCH DATA
        # spect = np.asarray((ship.spect[:508,:508]).astype(float)) #PREPARE BATCH DATA
        # spect = (spect - g_avg.avg_spect) / (g_avg.spect_dev) #standardize spects based on the average values from each one
        spect = spect / g_avg.max_spect
        spect = np.reshape(spect, (-1,255,255,1))
        # spect = np.reshape(spect, (-1,508, 508,1))
        spect_batch.append(spect)
        
        date_batch.append(ship.file_time)
        file_handler.close()
        
    feat_batch = np.array(feat_batch)
    spect_batch = np.array(spect_batch)
    # Y_test = np.array(label_batch)
    # speeds_0_batch = np.array(speeds_0_batch)
    # speeds_100_batch = np.array(speeds_100_batch)
    # speeds_200_batch = np.array(speeds_200_batch)
    for n in range(num_speeds):
        np.array(all_speeds[n])
    # Y_test = [speeds_0_batch,speeds_100_batch,speeds_200_batch]
    Y_test = all_speeds
    
    
    spect_batch = np.reshape(spect_batch, (-1,255,255,1))
    # spect_batch = np.reshape(spect_batch, (-1,508,508,1))
        
    print('feat_batch shape is: {}'.format(feat_batch.shape))
    print('feat_batch type is: {}'.format(type(feat_batch)))

    print('spect_batch type is: {}'.format(type(spect_batch)))
    print('Y_train type is: {}'.format(type(Y_test)))    
    print(Y_test)
    return [feat_batch,spect_batch],Y_test,date_batch #RETURN BATCH DATA 

eval_batch(2)
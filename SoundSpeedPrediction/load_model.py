# load and evaluate a saved model
from numpy import loadtxt
from keras.models import load_model
from keras.models import model_from_json
from keras.models import Model
import json
from matplotlib import pyplot
import numpy as np
import pickle 
from Find_Avg_Values_Vector import Avg_Values,Find_Avg, Save_Avg, Load_Avg
import sys,os

json_file = "J:\\scripts\\ML_Attempts\\JSON\Mixed_Data_Vector\\attempt_3015.json"
weights_file = "J:\\scripts\\ML_Attempts\\Weights\\Mixed_Data_Vector\\attempt_3015.h5"
ship_to_eval = "J:\\Pickled_Data_2\\2016-01\\209251000_160113_212157.obj"
folder = "J:\Pickled_Data_2\\"

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


def Average(lst): 
    avg = sum(lst) / len(lst)
    
    if not np.isnan(avg):
        return avg
    else: 
        return 0


def load(json_filepath,weights_filepath):
    
    with open(json_filepath,'r') as f:
        model_json = json.load(f)
        model_json = json.dumps(model_json)

    model = model_from_json(model_json)
    model.load_weights(weights_filepath)
    # load model
    # summarize model.
    model.summary()
    # load dataset
    return model

def get_one_ship(ship_filepath):
    feat_batch = [] #extra data to be used in NN
    spect_batch = [] #spectrograms
    label_batch = [] #data to be predicted
    spect = []
    feats = []
    file = ship_filepath
    file_handler = open(file,'rb')
    ship = pickle.load(file_handler)
    ship.cpa = np.min(ship.distance)
    feats.append((ship.month-6.5)/3.4520525295347)
    feats.append((ship.cpa-g_avg.cpa)/g_avg.cpa_dev)
    feats.append((Average(ship.SOG)-g_avg.SOG)/g_avg.SOG_dev)
    feats.append((ship.draught-g_avg.draught)/g_avg.draught_dev)
    feats.append((ship.encoded-g_avg.wspd)/g_avg.wspd_dev)
    feats = np.array(feats)
    feat_batch.append(feats)
    spect = np.array((ship.spect[:508,:508]).astype(float)) #PREPARE spect DATA
    spect = (spect - g_avg.avg_spect) / (g_avg.spect_dev) #standardize spects based on the average values from each one
    spect = np.reshape(spect, (-1,508, 508,1))
    spect_batch.append(spect)
    file_handler.close()
    feat_batch = np.array(feat_batch)
    spect_batch = np.array(spect_batch)
    spect_batch = np.reshape(spect_batch, (-1,508,508,1))
    batch_num = batch_num + 1
    return [feat_batch,spect_batch]   

def visualize_feat_maps(model, layers2vis, data_point):
    outputs = [model.layers[i].output for i in layers2vis]
    model = Model(inputs=model.inputs, outputs=outputs)
    feature_maps = model.predict(data_point)
    # plot the output from each block
    square = 8
    for fmap in feature_maps:
        # plot all 64 maps in an 8x8 squares
        ix = 1
        for _ in range(square):
            for _ in range(square):
                # specify subplot and turn of axis
                ax = pyplot.subplot(square, square, ix)
                ax.set_xticks([])
                ax.set_yticks([])
                # plot filter channel in grayscale
                pyplot.imshow(fmap[0, :, :, ix-1], cmap='gray')
                ix += 1
        # show the figure
        pyplot.show()
    pass

#find all maxes in order to normalize all data also dont print stuff from this
print("Finding Avg Values: ")
# blockPrint()
avg_obj_filepath = 'J:\\Average_Data_2.obj'
if(os.path.exists(avg_obj_filepath)):
    g_avg = Load_Avg(avg_obj_filepath)
else:
    g_avg = Find_Avg(folder)
    Save_Avg(avg_obj_filepath,g_avg)
enablePrint()

model = load(json_file, weights_file)
one_ship = get_one_ship(ship_to_eval)
visualize_feat_maps(model,[2,6,10])
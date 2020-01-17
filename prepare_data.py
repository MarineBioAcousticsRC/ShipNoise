
import unpickle as up
import numpy as np
from keras.utils import np_utils
from dat_extract.extract.Ship_Variable_Extraction import Ship
import random

def get_data(folder):
    ships = up.unpickle_ships(folder)
    random.shuffle(ships)
    train_data_size = 5*(len(ships)/6)
    test_data_size = len(ships)/6
    train_spect = []
    test_spect = []
    
    train_speeds = []
    test_speeds = []
    speeds_categories = []
    
    i = 0
    while len(train_spect)<train_data_size:
        train_spect.append(ships[i].spect)
        i+=1
    while len(test_spect)<test_data_size and i<len(ships):
        test_spect.append(ships[i].spect)
        i+=1
    i = 0
    while len(train_speeds)<train_data_size:
        train_speeds.append(ships[i].speed) #for this run only cpa will refer to soundspeed profile
        i+=1
    while len(test_speeds)<test_data_size and i<len(ships):
        test_speeds.append(ships[i].speed)
        i+=1
    min_speed = min(train_speeds)
    max_speed = max(train_speeds)
    even_speeds = np.arange(min_speed,max_speed,.25)
    speed_bins_train = np.digitize(train_speeds,even_speeds)
    speed_bins_test = np.digitize(test_speeds,even_speeds)
    y_train = []
    y_test = []
    for a in range(len(train_speeds)):
        y_train.append(speed_bins_train[a]-1)
    for b in range(len(test_speeds)):
        y_test.append(speed_bins_test[b]-1)
    
    Y_train = np_utils.to_categorical(y_train,len(even_speeds))
    Y_test = np_utils.to_categorical(y_test,len(even_speeds))
    return train_spect, test_spect, Y_train, Y_test,len(even_speeds)  
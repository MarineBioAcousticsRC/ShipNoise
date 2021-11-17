
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

    return train_spect, test_spect, Y_train, Y_test  

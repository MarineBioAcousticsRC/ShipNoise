import unpickle as up
import numpy as np
from keras.utils import np_utils
from dat_extract.extract.Ship_Variable_Extraction import Ship
import random
import sys, os


def get_data(folder):
    ships = up.unpickle_ships(folder)
    random.shuffle(ships)
    train_data_size = 5*(len(ships)/6)
    test_data_size = len(ships)/6
    train_spect = []
    test_spect = []
    
    train_months = []
    test_months = []
    
    i = 0
    while len(train_spect)<train_data_size:
        train_spect.append(ships[i].spect)
        i+=1
    while len(test_spect)<test_data_size and i<len(ships):
        test_spect.append(ships[i].spect)
        i+=1
    i = 0
    while len(train_months)<train_data_size:
        train_months.append(ships[i].month) #for this run only cpa will refer to soundspeed profile
        i+=1
    while len(test_months)<test_data_size and i<len(ships):
        test_months.append(ships[i].month)
        i+=1

    Y_train = np_utils.to_categorical(train_months,12)
    Y_test = np_utils.to_categorical(test_months,12)
    return train_spect, test_spect, Y_train, Y_test,12  

def data_generator(folder,mode):
    if mode=='train':
        while True:
            for ships in up.unpickle_batch(folder,50,0,6000): #the first 6000 ships in batches of 50
                random.shuffle(ships)
                train_spect = []
                train_months = []
                for ship in ships:
                    train_spect.append(ship.spect)
                    
                    x_train = np.asarray(train_spect)
                    x_train =  x_train.astype('float32')
                    x_train /= np.amax(x_train) #- 0.5
                    X_train = np.reshape(x_train, (-1,501, 501,1))
                    
                    train_months.append(ship.month)
                    Y_train = np_utils.to_categorical(train_months,12)
                    
                yield X_train,Y_train
    if mode == 'test':
        while True:
            for ships in up.unpickle_batch(folder,50,6000,7200): #The last 1200 ships in batches of 50
                random.shuffle(ships)
                test_spect = []
                test_months = []
                for ship in ships:
                    test_spect.append(ship.spect)
                    
                    x_test = np.asarray(test_spect)
                    x_test =  x_test.astype('float32')
                    x_test /= np.amax(x_test) #- 0.5
                    X_test = np.reshape(x_test, (-1,501, 501,1))
                    
                    test_months.append(ship.month)
                    Y_test = np_utils.to_categorical(test_months,12)
                    
                yield X_test,Y_test
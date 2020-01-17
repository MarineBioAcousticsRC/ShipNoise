# from scipy import signal
# import matplotlib.pyplot as plt
# import numpy as np
# import os
# from pydub import AudioSegment
# #print(np.hanning(10e3))
# #228348900_140821_081045.txt
# D:\ShippingCINMS_data\COP\2014-08\228348900_140821_081045.txt
# import pickle
# #file = open("D:\PickledData\\2014-08\\566483000_140816_074210.obj",'rb')
# #ship = pickle.load(file)
# #print(ship.temp)
# a=["%02d" % x for x in range(1,13)]
# print(a)
# b = ['2014-','2015-','2016-','2017-','2018-']
# for j in range(len(b)): 
    # for i in range(len(a)):
        # str = b[j] + a[i]
        # path = os.path.join('D:','Pickled_Data_2',str)
        # os.makedirs(path)
# txt1 = "D:\ShippingCINMS_data\COP\2014-08\316001870_140817_000933.txt"
# txt2 = "D:\ShippingCINMS_data\COP\2014-08\316001870_140817_001547.txt"
# wav1 = "D:\ShippingCINMS_data\COP\2014-08\316001870_140817_000933.wav"
# wav2 = "D:\ShippingCINMS_data\COP\2014-08\316001870_140817_001547.wav"
# def merge_wav(f1,f2): #function to actually merge wav files
    
    # sound1 = AudioSegment.from_wav(f1)
    # sound2 = AudioSegment.from_wav(f2)

    # new_wav = sound1 + sound2
    # #new_wav.export(f1,format="wav")
# def merge_txt(f1,f2):
    # copy_lines = []
    # with open(f2, encoding="utf8",errors = 'ignore') as fp: #extract specific lines
        # for x, line in enumerate(fp): #copy all distance lines from later crossing 
            # if x > 18:                #and append them to the earlier crossing file
                # copy_lines.append(line[:])
    # fp.close()
    # file = open(f1,"a")
    # for line in copy_lines:    
        # file.write("%s" % line)
    # file.close()
# merge_wav(wav1,wav2)
# merge_txt(txt1,txt2)

# rootdir = 'D:\PickledData\2014-08\\'
# for subdir, dirs, files in os.walk(rootdir):
        # print('here')
        # for file in files:
            # print os.path.join(subdir, file)
            # filepath = subdir + os.sep + file #create filepath to each text file
            # print(filepath)
            # if filepath.endswith(".obj"):
                # print(filepath)
#736_140311_invSensit.tf
#D:\ShippingCINMS_data\COP\2016-09\311003300_160907_232819.txt
# [8, 0, 8, 2, 3, 9, 4, 9, 9, 8, 6, 8, 3, 9, 6, 8, 10, 5, 3, 4, 2, 6, 6, 5, 5, 5, 4, 8, 4, 7, 10, 3, 6, 11, 7, 8, 6, 4, 7, 9, 9, 9, 7, 10, 6, 4, 6, 3, 6, 1]
#tensorboard --logdir=D:\ML_Attempts\logs\mixed_data_1 --host localhost --port 8088
#score = model.evaluate(X_test, Y_test, verbose=2)
# test_spect = []
# test_months = []
# for ships in up.unpickle_batch(folder,50,6000,6050):
    # for ship in ships:
        # test_spect.append(ship.spect) #GET BATCH DATA
        # test_months.append(ship.month-1)    
    # x_test = np.asarray(test_spect) #PREPARE BATCH DATA
    # x_test =  x_test.astype('float32')
    # x_test /= np.amax(x_test) #- 0.5
    # X_test = np.reshape(x_test, (-1,501, 501,1))
# print(test_months)
# y_prob = model.predict(X_test) 
# y_classes = y_prob.argmax(axis=-1)
# print(y_classes)
# model.save_weights('D:\\scripts\\ML_Attempts\\Weights\\Categorical_Month\\second_try.h5')
# Y_test  = np_utils.to_categorical(test_months,12)
# score = model.evaluate(X_test,Y_test,batch_size=50)
# print('Test loss:', score[0])
# print('Test accuracy:', score[1])
#hightest: 1512.6522621294907
# lowest: 1484.9804990390573
# average: 1492.5601871620586
# std dev: 4.408748491127072
#  all unique:    [1484.98049904 1485.05163652 1485.18206907 1485.26413924 1485.4363708
                 # 1485.47368077 1485.50784988 1485.56840798 1485.60515254 1485.657778
                 # 1491.19411159 1491.58060687 1491.86975052 1492.06512814 1492.16330524
                 # 1492.81609296 1493.15934379 1493.37198494 1493.45568925 1493.90780692
                 # 1494.1228541  1494.14146779 1494.55375251 1494.586932   1494.93164657
                 # 1495.31740315 1495.74143649 1495.99605586 1496.48519825 1496.60589113
                 # 1497.52965117 1498.06907103 1498.21178309 1512.65226213]
# len unique: 34
# import unpickle as up
# import numpy as mat
# folder = 'D:\\Pickled_Data_2\\'
# from dat_extract.extract.Ship_Variable_Extraction import Ship
# ships = up.unpickle_ships(folder)
# for ship in ships:
    # ship.depth = mat.array([float(i) for i in ship.depth])
    # print(ship.depth)
    # ii = mat.where(ship.depth == 400)[0]
    # print(ii)
    # index = ii[0]
    # if len(ii) > 1:
        # index = ii[1]
        # ship.depth = ship.depth[index:]
        # ship.temp = ship.temp[index:]
        # ship.sal = ship.sal[index:]
        # up.one_jar(folder,ship,False)
        
    # print(float(ship.temp[index]))
# print('hello world')
# from statistics import mean
# filename = "D:\\Plumes_and_Blumes_CTD_Fixed.csv"
# import pandas as pd
# from datetime import datetime, timedelta
# data = pd.read_csv(filename,parse_dates=['date'])  
# df_4 = data.loc[(data['station'] == 4)]  
# ships = up.unpickle_a_batch(folder,0,10)
# unique = df_4['date'].unique().tolist()
# dates = []
# for i in unique:
    # date = datetime.fromtimestamp(i / 1e9)
    # dates.append(date)

# for ship in ships:
    # min = timedelta(99999999)
    # for i in range(len(unique)):
        # sub = abs(dates[i] - ship.cpa_datetime)
        # if sub < min:
            # min = sub
        
    # print(min)
# print(unique)
# print(len(unique))
# ships = up.unpickle_ships(folder)
# all_dates = []
# diffs = []
# for ship in ships:
    # if len(ship.distance) < 5:
        # up.one_jar(folder,ship,True)
    
# unique_dates = mat.unique(all_dates)
# print(unique_dates)
# print(len(unique_dates))
# print(timedelta(seconds=mean(diffs)))
# file = open("D:\\Test_Ships.txt","r")
# ships = file.readlines()
# set = set(ships)
# ship_list = list(set)
# print(len(ship_list))
# result = []
# for ship in ships:
    # result.append(len(ship.distance))
# result = mat.array(result)
# print(result.min())
# ii = mat.where(result == result.min())[0]
# print(ii)
# for index in ii:
    # print(ships[index].id)
# print(7//2)
# mid = 3
# length = 6
# print((mid - (length/2)))
# print(list(range(mid - length//2,6)))
# print((mid + (length/2)))
line = "aasdasd1234/1234/1234"
print(line[0].isdigit())
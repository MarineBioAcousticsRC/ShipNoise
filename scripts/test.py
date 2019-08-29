# from scipy import signal
# import matplotlib.pyplot as plt
# import numpy as np
# #import os
# from pydub import AudioSegment
# #print(np.hanning(10e3))
# #228348900_140821_081045.txt
D:\ShippingCINMS_data\COP\2014-08\228348900_140821_081045.txt
# import pickle
# #file = open("D:\PickledData\\2014-08\\566483000_140816_074210.obj",'rb')
# #ship = pickle.load(file)
# #print(ship.temp)
# # a=["%02d" % x for x in range(1,13)]
# # print(a)
# # b = ['2014-','2015-','2016-','2017-','2018-']
# # for j in range(len(b)): 
    # # for i in range(len(a)):
        # # str = b[j] + a[i]
        # # path = os.path.join('D:','PickledData',str)
        # # os.makedirs(path)
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
import sys
print(sys.path)
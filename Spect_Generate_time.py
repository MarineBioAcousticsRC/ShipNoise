import matplotlib.pyplot as plt
import matplotlib 
from scipy import signal
from scipy.io import wavfile
from dat_extract.extract.Ship_Variable_Extraction import Ship
from scipy import interpolate
import numpy as np
import numpy.matlib as npmb
import dat_extract.get_tf as tf
import math
import unpickle as up
import sys
import os


rootdir = 'D:\Pickled_Data_2\\' #set dir for the extraction
destination_folder = 'D:\Generated Spectrograms'

    
def generate(rootdir):
    print('here')
    ships = up.unpickle_ships(rootdir)
    i = len(ships)-1
    j = 0
    while i > 0:
        ship = ships[i]
        try:
                wavfilepath = os.path.join(ship.filepath , ship.id + '.wav') #the original wav file
                print(wavfilepath)
                #destination =  destination_folder + ship.month +'\\' + ship.id + '.png' #the destination for the spectrogram
                
                sample_rate, samples = wavfile.read(wavfilepath) #get original wav file samples at the original sample rate
                
                
                frequencies, times, spectrogram = signal.spectrogram(samples,sample_rate, window = np.hanning(1024), noverlap = 0, nfft = 1024, mode='psd') #generate spectrogram 
                uppc = tf.get_tf(ship.harp,frequencies) #get the transfer function results
                
                spectrogram = 10*np.log10(spectrogram) #convert to/from decibels ?
                
                uppc = npmb.repmat(uppc,np.size(spectrogram,1),1) #copy tf results several times to make it same size as spect results
                ship.spect = spectrogram + np.transpose(uppc) #add tf results to spect results
        
        except:
                j+=1
                print("bad ship " + str(j)) 
                print(sys.exc_info()[0])
                up.one_jar(rootdir,ship,True)
                pass
        up.one_jar(rootdir,ship,False)
        ships.pop(i)
        print(i)
        i-=1
generate(rootdir)
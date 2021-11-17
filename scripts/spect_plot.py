import unpickle as up
import matplotlib.pyplot as plt
import matplotlib 
from scipy import signal
from scipy.io import wavfile
from scipy import interpolate
import numpy as np
import numpy.matlib as npmb
import dat_extract.get_tf as tf
import unpickle as up
from dat_extract.extract.Ship_Variable_Extraction import Ship
import time

folder = 'J:\Pickled_Data\\'
destination_folder = 'J:\Generated Spectrograms\\'

def calc_pad(des_size,size):
    
    sub = des_size - size
    if (sub % 2) == 0:
        pre_pad = sub//2
        post_pad = sub//2
    else:
        pre_pad = sub//2
        post_pad = ((sub//2) + 1)
        
    return pre_pad, post_pad
    
def get_sizes(ships):
    #result = [np.size(ship.spect,1) for ship in ships]
    result = []
    for ship in ships:
        result.append(np.size(ship.spect,1))
    return result
    
def normalize(spect):
    x=0
    y=0
    #print(np.size(ships))

    #avg_size = int(np.mean(sizes))
    square_size = 512
    size = np.size(spect,1)

    pad_length = (square_size - size)
    beg_pad,end_pad = calc_pad(square_size,size)
    if pad_length>=0:
        spect = np.pad(spect,[(0,0),(beg_pad,end_pad)],mode='constant')
    else:
        spect = spect[:,abs(beg_pad):size+end_pad]

    return spect


def plot(folder):
    ships = up.unpickle_a_batch(folder,0,1)
    for ship in ships:
        wavfilepath = ship.filepath + ship.id + '.wav' #the original wav file
        sample_rate, samples = wavfile.read(wavfilepath) #get original wav file samples at the original sample rate
        destination =  destination_folder + ship.year_month +'\\' + ship.id + '.png' #the destination for the spectrogram
        print(ship.id)
        
        
        frequencies, times, spectrogram = signal.spectrogram(samples,sample_rate, window = np.hanning(1024), noverlap = 0, nfft = 1024, mode='psd') #generate spectrogram 
        uppc = tf.get_tf(ship.harp,frequencies) #get the transfer function results
        spectrogram = 10*np.log10(spectrogram) #convert to/from decibels ?
        uppc = npmb.repmat(uppc,np.size(spectrogram,1),1) #copy tf results several times to make it same size as spect results
        spectrogram = spectrogram + np.transpose(uppc) #add tf results to spect results
        spectrogram = normalize(spectrogram)
        times = times[:512]
        plt.yscale('log') #make y scale log to match the new decibel units
        axes = plt.gca() #get axes object
        axes.set_ylim([10,1000]) #set upper limit of data on axes to be 1000
        plt.pcolormesh(times,frequencies,spectrogram,vmin=60,vmax=110 ) #plot the data and add color
        plt.set_cmap('jet')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Distance [km]')

        plt.colorbar()
        #plt.xticks(locs, new_ticks)  # Set locations and labels to the distance 
        #plt.savefig(destination) #save spectrogram at destination
        #plt.imshow(spectrogram)
        plt.show() #show plot
        plt.close()
plot(folder)
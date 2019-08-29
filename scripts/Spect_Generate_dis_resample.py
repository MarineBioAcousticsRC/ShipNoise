import matplotlib.pyplot as plt
import matplotlib 
from scipy import signal
from scipy.io import wavfile
import extract.Ship_Variable_Extraction as dat
from scipy import interpolate
import numpy as np
import numpy.matlib as npmb
import extract.get_tf as tf
import math

rootdir = "D:\ShippingCINMS_copy\COP" #set dir for the extraction
destination_folder = 'D:\Generated Spectrograms\\'

def convert_time(ship):
    time_array = []
    result_array = []
    for time in ship.sampletimes:
        (h, m, s) = time.split(':')
        result = int(h) * 3600 + int(m) * 60 + int(s)
        time_array.append(result)
    for time in time_array:
        result_array.append(time - time_array[0])
    return result_array


def get_ticks(distances,times):
    result = []
    for time in times:
        if (time % 100) ==0:
            result.append(round(distances[time],2))
        
    return result


    
def generate(rootdir):
    ships = dat.extract(rootdir)
    ships = ships[3:9]
    for ship in ships:
        
        
        wavfilepath = ship.filepath + ship.id + '.wav' #the original wav file
        destination =  destination_folder + ship.month +'\\' + ship.id + '.png' #the destination for the spectrogram
        
        converted_times = convert_time(ship)
        inter = interpolate.interp1d(converted_times,ship.distance, axis=0, fill_value="extrapolate")
        
        sample_rate, samples = wavfile.read(wavfilepath) #get original wav file samples at the original sample rate
        
        sample_secs =  np.arange(0,len(samples))/sample_rate
        new_distances = inter(sample_secs)
        # sound_length = len(samples)//sample_rate
        # new_times = np.arange(0,sound_length+100)
        # new_distances = inter(new_times)
        # new_ticks =  get_ticks(new_distances,new_times)
        range_step = 1e-6 # step size of 1mm
        closest_range = np.min(np.abs(ship.distance)) # find closest point of approach (cpa)
        range_approach = np.arange(ship.distance[0], closest_range, range_step) # make a vector of distances between first range and cpa 
        range_depart  = np.arange(closest_range, ship.distance[len(ship.distance)-1], range_step) # make a vector of distances between cpa and last range
        range_desired = np.append(range_approach,range_depart)# stick them together
        number_range_samples = len(range_desired)# total length is the number of samples we expect. 
        signal_resampled= signal.resample(samples, number_range_samples)#, new_distances)
        
        
        frequencies, times, spectrogram = signal.spectrogram(signal_resampled,1e3, window = np.hanning(10e3), noverlap = 0, nfft = 10e3, mode='psd') #generate spectrogram 
        uppc = tf.get_tf(ship.harp,frequencies) #get the transfer function results
        
        spectrogram = 10*np.log10(spectrogram) #convert to/from decibels ?

     
        uppc = npmb.repmat(uppc,np.size(spectrogram,1),1) #copy tf results several times to make it same size as spect results
        spectrogram = spectrogram + np.transpose(uppc) #add tf results to spect results
        fig = plt.figure()

        plt.yscale('log') #make y scale log to match the new decibel units
        axes = plt.gca() #get axes object
        axes.set_ylim([10,1000]) #set upper limit of data on axes to be 1000
        plt.pcolormesh(times,frequencies, spectrogram,vmin=60,vmax=110 ) #plot the data and add color
        plt.set_cmap('jet')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Distance [km]')
        #locs, ticks = plt.xticks() #get current time ticks

        
        
        plt.colorbar()
        #plt.xticks(locs, new_ticks)  # Set locations and labels to the distance 
        plt.savefig(destination) #save spectrogram at destination
        plt.imshow(spectrogram)
        plt.show() #show plot
        plt.close()
        
generate(rootdir)
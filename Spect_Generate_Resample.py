import matplotlib.pyplot as plt
import matplotlib 
from scipy import signal
from scipy.io import wavfile
#import extract.Glider_Extraction as dat
import extract.Ship_Variable_Extraction as dat
from scipy import interpolate
import numpy as np
import numpy.matlib as npmb
import extract.get_tf as tf
import math

rootdir = "D:\ShippingCINMS_copy\COP" #set dir for the extraction
destination_folder = 'D:\Generated Spectrograms\\'
f_80 = 'D:\CUGN_line_80.nc'
f_90 = 'D:\CUGN_line_90.nc'

def convert_time(ship):
    time_array = []
    result_array = []
    for time in ship.sampletimes:
        (h, m, s) = time.split(':')
        result = int(h) * 3600 + int(m) * 60 + int(s)
        time_array.append(result)
    for time in time_array:
        result_array.append(time - time_array[0])
    (h, m, s) = ship.time.split(':')
    cpa_time = ((int(h) * 3600 + int(m) * 60 + int(s)) - time_array[0])
    return result_array ,cpa_time


def get_ticks(distances,times):
    result = []
    for time in times:
        if (time % 100) ==0:
            result.append(round(distances[time],2))
        
    return result

def range_spect(bins,spectrogram):
    u_bins = np.unique(bins)
    range_spectrogram = np.empty_like(spectrogram)
    for i in range(0,len(u_bins)):
            searchval = u_bins[i]
            ii = np.where(bins == searchval)[0]
            print(ii)
            for x in range(0,np.size(spectrogram,0)-1):
                counter = 0
                for j in range(0,len(ii)):
                    counter+=spectrogram[x,(ii[j])]
                range_spectrogram[x,i] = counter/len(ii)  
       
    return range_spectrogram
    
def generate(rootdir):
    #ships = dat.glider_data(rootdir,f_80,f_90)
    ships = dat.extract(rootdir)
    ships = ships[3:9]
    for ship in ships:
        
        
        wavfilepath = ship.filepath + ship.id + '.wav' #the original wav file
        destination =  destination_folder + ship.month +'\\' + ship.id + '.png' #the destination for the spectrogram
        
        
        converted_times,cpa_time = convert_time(ship)
        print(len(converted_times))
        print(cpa_time)
        cpa_index = converted_times.index(cpa_time)
        print(cpa_index)
        pre_cpa = ship.distance[:cpa_index]
        post_cpa = ship.distance[cpa_index:]
        pre_times = converted_times[:cpa_index]
        post_times = converted_times[cpa_index:]
        print(post_times)
        print(pre_cpa)
        print(post_cpa)
        approach_inter = interpolate.interp1d(pre_times,pre_cpa, axis=0, fill_value="extrapolate")
        depart_inter = interpolate.interp1d(post_times,post_cpa, axis=0, fill_value="extrapolate")
        
        
        sample_rate, samples = wavfile.read(wavfilepath) #get original wav file samples at the original sample rate
        
       
        sound_length = len(samples)//sample_rate
        print(sound_length)
        approach_times = np.arange(0,cpa_time)
        depart_times = np.arange(cpa_time,sound_length)
        
        
        frequencies, times, spectrogram = signal.spectrogram(samples,sample_rate, window = np.hanning(10e3), noverlap = 0, nfft = 10e3, mode='psd') #generate spectrogram 
        
        uppc = tf.get_tf(ship.harp,frequencies) #get the transfer function results
        spectrogram = 10*np.log10(spectrogram) #convert to/from decibels ?
        uppc = npmb.repmat(uppc,np.size(spectrogram,1),1) #copy tf results several times to make it same size as spect results
        spectrogram = spectrogram + np.transpose(uppc) #add tf results to spect results

        range_step = .01 # step size of 1m
        closest_range = np.min(np.abs(ship.distance)) # find closest point of approach (cpa)

        
        range_approach = ((np.arange(ship.distance[0], closest_range, -range_step))) # make a vector of distances between first range and cpa 
        range_depart  = np.arange(closest_range, ship.distance[len(ship.distance)-1], range_step) # make a vector of distances between cpa and last range
        range_desired = np.append(range_approach,range_depart)# stick them together
        number_range_samples = len(range_desired)# total length is the number of samples we expect. 
        
        

        print(spectrogram.shape)


        
        spect_dis_approach = approach_inter(approach_times)
        spect_dis_depart = depart_inter(depart_times)

        approach_bins = np.digitize(spect_dis_approach,range_approach)

        depart_bins = np.digitize(spect_dis_depart,range_depart)


        approach_spect = range_spect(approach_bins,spectrogram)
        depart_spect = range_spect(depart_bins,spectrogram)
        print(approach_spect)
        print(spectrogram)

        
        range_spectrogram = np.concatenate(approach_spect,depart_spect)
        plt.yscale('log') #make y scale log to match the new decibel units
        axes = plt.gca() #get axes object
        axes.set_ylim([10,1000]) #set upper limit of data on axes to be 1000
        plt.pcolormesh(times,frequencies, range_spectrogram,vmin=60,vmax=110 ) #plot the data and add color
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
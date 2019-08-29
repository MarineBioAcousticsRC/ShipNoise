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

folder = 'D:\PickledData\\'
destination_folder = 'D:\Generated Spectrograms\\'
np.set_printoptions(threshold=np.inf)

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def better_seconds(t):
    new_time = time.mktime(t.timetuple())
    return new_time


    
def convert_time(ship):
   
    start_time = find_nearest(ship.sampletimes,ship.file_time) #get the start index and cut array to fit it
    start_index = ship.sampletimes.index(start_time)
    times = ship.sampletimes[start_index:]
    cpa_index = ship.sampletimes.index(find_nearest(ship.sampletimes,ship.cpa_datetime))
    if(start_time>=ship.cpa_datetime):
        normal = False
    else:
        normal = True
    result_array = []
    for time in times:
        result_array.append(better_seconds(time) - better_seconds(times[0])) #subtract start time
    cpa_time = better_seconds(ship.cpa_datetime) - better_seconds(times[0]) #get new cpa_time in relation to file time
    
    return result_array, start_index, cpa_index,cpa_time,normal


def get_ticks(ranges,locs):
    result = []
    num_ticks = len(locs)
    tick_step = len(ranges)//num_ticks
    result.append(round(ranges[0]))
    for x in range(num_ticks-1):
        result.append(round((ranges[0+(tick_step*x)]),2))
    return result

def range_spect(bins,spectrogram): #function to convert normal spectrogram into range baste
    u_bins = np.unique(bins)
    range_spectrogram = np.zeros((np.size(spectrogram,0),len(u_bins)))
    for i in range(0,len(u_bins)):
        searchval = u_bins[i]
        ii = np.where(bins == searchval)[0]
        #print(ii[len(ii)-1])
        #print(spectrogram.shape)
        for x in range(0,np.size(spectrogram,0)):
            counter = 0
            for j in range(0,len(ii)):
                counter+=spectrogram[x,(ii[j])]
            range_spectrogram[x,i] = counter/len(ii)  
   
    return range_spectrogram
    
def get_ranges(app_bins,dep_bins,app_ranges,dep_ranges):
    app_u_bins = np.unique(app_bins)
    dep_u_bins = np.unique(dep_bins)
    ranges = []
    for bin in range(len(app_u_bins)):
        ranges.append(app_ranges[bin])
    for bin in range(len(dep_u_bins)):
        ranges.append(dep_ranges[bin])
    return(ranges)

def generate(folder):
    ships = up.unpickle_ships(folder)
    bad_apples = []
    i = 0
    for ship in ships:
        try:
        
            wavfilepath = ship.filepath + ship.id + '.wav' #the original wav file
            txtfilepath = ship.filepath + ship.id + '.txt' #the original txt file
            destination =  destination_folder + ship.year_month +'\\' + ship.id + '.png' #the destination for the spectrogram
            print(txtfilepath)
            
            converted_times,start,cpa_index,cpa_time,normal = convert_time(ship) #convert all times and find the file start time and cpa time
            print(normal)
            after_start = ship.distance[start:] #find all distances after file_time 
            closest_range = np.min(np.abs(after_start)) # find closest point of approach (cpa)
            cpa_index = after_start.index(closest_range)
            if len(after_start) < 20:
                normal = False
                raise NameError('Too Few Distances')
            if normal: #for now only do the ones that are normal
                print('here 1')
                pre_cpa = after_start[:cpa_index]
                pre_times = converted_times[:cpa_index]
                approach_inter = interpolate.interp1d(pre_times,pre_cpa, axis=0, fill_value="extrapolate")
            
            post_cpa = after_start[cpa_index:] #find all distances after cpa time
            post_times = converted_times[cpa_index:]
            depart_inter = interpolate.interp1d(post_times,post_cpa, axis=0, fill_value="extrapolate")
            print('here 2')
            
            sample_rate, samples = wavfile.read(wavfilepath) #get original wav file samples at the original sample rate
            sound_length = len(samples)//sample_rate
           
            frequencies, times, spectrogram = signal.spectrogram(samples,sample_rate, window = np.hanning(10e3), noverlap = 0, nfft = 10e3, mode='psd') #generate spectrogram 
            
            uppc = tf.get_tf(ship.harp,frequencies) #get the transfer function results
            spectrogram = 10*np.log10(spectrogram) #convert to/from decibels ?
            uppc = npmb.repmat(uppc,np.size(spectrogram,1),1) #copy tf results several times to make it same size as spect results
            spectrogram = spectrogram + np.transpose(uppc) #add tf results to spect results

            range_step = .01 # step size of 1m
            if normal:
                approach_times = np.arange(0,cpa_time)
                range_approach = ((np.arange(pre_cpa[0], closest_range, -range_step))) # make a vector of distances between first range and cpa 
                depart_times = np.arange(cpa_time,sound_length)
            else:
                depart_times = np.arange(,sound_length)
            range_depart  = (np.arange(closest_range, post_cpa[len(post_cpa)-1], range_step)) # make a vector of distances between cpa and last range
            #range_desired = np.append(range_approach,range_depart)# stick them together
            #number_range_samples = len(range_desired)# total length is the number of samples we expect. 

            if normal:
                print('here 3')
                spect_dis_approach = approach_inter(approach_times)
                approach_bins = np.digitize(spect_dis_approach,range_approach)
                approach_spect = range_spect(approach_bins,spectrogram)
                
            print('here 4')
            spect_dis_depart = depart_inter(depart_times)
            depart_bins = np.digitize(spect_dis_depart,range_depart)
            
            #depart_bins = depart_bins + last_bin
            depart_spect = range_spect(depart_bins,spectrogram)
            if normal:
                print('here 5')
                range_spectrogram = np.concatenate((approach_spect,depart_spect),axis=1)
            else:
                print('here 6')
                range_spectrogram = depart_spect
            ship.spect = range_spectrogram
            normal = True
            #plt.savefig(destination) #save spectrogram at destination
         
            #plt.close()
        except:
                i+=1
                print("bad ship" + str(i))
                up.one_jar(folder,ship,True)
                normal = False
                pass
        if normal:
                up.one_jar(folder,ship,False)
        
generate(folder)
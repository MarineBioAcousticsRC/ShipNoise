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

#converts date times into seconds and then subtracts them so they increment up from zero
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

#function to convert time ticks into distance ticks
# def get_ticks(distances,times): 
    # result = []
    # for time in times:
        # if (time % 100) ==0: #every 100 seconds find the distance
            # result.append(round(distances[time],2))
        
    # return result


    
def generate(rootdir):
    ships = dat.extract(rootdir)

    for ship in ships:
        
        print(ship.filepath)
        wavfilepath = ship.filepath + ship.id + '.wav' #the original wav file
        destination =  destination_folder + ship.month +'\\' + ship.id + '.png' #the destination for the spectrogram
        
        converted_times = convert_time(ship) #convert times to seconds
        # KF comment: I think by setting the start time of the ship transit and of the time series to 0, we are making the assumption 
        # that the sound file and ship transit start at the same time, which is probably not true. Do you agree? 
        # I'm wondering if we actually need to set them to zero, or if we can leave the times as some sort of datenumber.
        # Generally times can be stored as a number of time units since some arbitrary start date. Matlab uses days elapsed since Jan 1, 1980, for example. 
        # It looks like Python has a datetime type that can be converted to an ordinal date: https://stackoverflow.com/questions/39846918/convert-date-to-ordinal-python
        # Maybe this is worth a try in place of the  time.split approach above? Then we would theoretically have an interpolate-able type that could account 
        # for offset between the two different sets of times (AIS and acoustic) that we're trying to match up for each ship.
        
        inter = interpolate.interp1d(converted_times,ship.distance, axis=0, fill_value="extrapolate") #gets function to find distances from times
        
        sample_rate, samples = wavfile.read(wavfilepath) #get original wav file samples at the original sample rate
        sample_times_sec = np.arange(0,len(samples),1)/sample_rate # create vector of times to go with this time series (KF suggested, but doesn't address the comment above)
        
        sound_length = len(samples)//sample_rate #find number of seconds in clip
        new_times = np.arange(0,sound_length+100) #create an array that has all times included on the spectrogram
        new_distances = inter(new_times) #find all the new distances relating to every second of the clip
        # KF comment: A good sanity check on the distances would be to make sure that there are cases where the distance starts high, decreases, 
        # and then increases again, as expected when a ship passes by the sensor.
        #new_ticks =  get_ticks(new_distances,new_times) #find the specific distances that will be listed on spectrogram
        
        frequencies, times, spectrogram = signal.spectrogram(samples,sample_rate, window = np.hanning(10e3), noverlap = 0, nfft = 10e3, mode='psd') #generate spectrogram 
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
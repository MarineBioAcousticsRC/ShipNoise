import numpy as np
from dat_extract.extract.Ship_Variable_Extraction import Ship
import pickle
import unpickle as up
import math
import collections
import matplotlib.pyplot as plt
class Avg_Values:
    def __init__(self,cpa,temp,sal,depth,avg_spect,max_spect, sound_speed,
                length, SOG, draught, wspd, cpa_dev,temp_dev,sal_dev,
                depth_dev,spect_dev,sound_speed_dev,
                length_dev, SOG_dev, draught_dev,wspd_dev):
        self.cpa = cpa
        self.temp = temp
        self.sal = sal
        self.depth = depth
        self.avg_spect = avg_spect
        self.max_spect = max_spect
        self.sound_speed = sound_speed
        self.length = length
        self.SOG = SOG
        self.draught = draught
        self.wspd = wspd

        self.cpa_dev = cpa_dev
        self.temp_dev = temp_dev
        self.sal_dev = sal_dev
        self.depth_dev = depth_dev
        self.spect_dev = spect_dev
        self.sound_speed_dev = sound_speed_dev
        self.length_dev = length_dev
        self.SOG_dev = SOG_dev
        self.draught_dev = draught_dev
        self.wspd_dev = wspd_dev

def Average(list):
    list = np.array(list)
    return sum(list)/len(list)

def std_dev(list):
    list = np.array(list)
    mean = Average(list)
    diff_list = (np.array(list)-mean)**2
    std_dev = math.sqrt(sum(diff_list)/len(diff_list))
    return mean,std_dev

def apply_transform(list,avg,dev):
    return (np.array(list)-avg)/dev

#because each spect is the same size we can take the average of the averages and its equal to doing the average over the whole list
def Spect_Average(avg_list):
    spect_Average = np.mean(np.array(avg_list))

def Find_Avg(file):
    #ships = up.unpickle_ships(file)
    avg = Avg_Values(1,1,1,1,1,1,[],1,1,1,1,1,1,1,1,1,[],1,1,1,1,)
    cpa_list = []
    temp_list = []
    sal_list = []
    # depth_list = []
    spect_avg_list = []
    all_soundspeeds = []
    num_speeds = 5
    for i in range(num_speeds):
        all_soundspeeds.append([])
    length_list = []
    SOG_list = []
    draught_list = []
    wspd_list = []
    
    for ships in up.unpickle_batch(file,100,0,8900): #amass all the variables into lists to calc the avg and std_dev
        for ship in ships:
            if np.amax(ship.spect) > avg.max_spect:
                avg.max_spect = np.amax(ship.spect)
            
            #because each spect is the same size we can take the average of the averages and its equal to doing the average over the whole list
            spect_avg_list.append(np.mean(ship.spect))
            ship.cpa = np.min(ship.distance)
            cpa_list.append(ship.cpa)
            temp_list.append(float(ship.temp[1])) 
            sal_list.append(float(ship.sal[1]))
            # depth_list.append(ship.depth)
            # np.mean(ship.spect)
            # spect_list.append(np.mean(ship.spect))
            # sound_speed_list_0.append(ship.sound_speed[0]) 
            # sound_speed_list_100.append(ship.sound_speed[1]) 
            # sound_speed_list_200.append(ship.sound_speed[2]) 
            for i in range(num_speeds):
                all_soundspeeds[i].append(ship.sound_speed[i])
            length_list.append(ship.length)
            
            
            if not np.isnan(Average(ship.SOG)): #sometimes there are no samples and this makes SOG a nan
                SOG_list.append(Average(ship.SOG)) 
            else:
                SOG_list.append(0) #keeps the lists the same length
                
            draught_list.append(ship.draught)
            wspd_list.append(ship.encoded)
        

        

   #Calc all standard deviations and averages
    # print(spect_list)
    avg.cpa, avg.cpa_dev = std_dev(cpa_list)
    avg.temp, avg.temp_dev = std_dev(temp_list)
    avg.sal, avg.sal_dev = std_dev(sal_list)
    avg.avg_spect, avg.spect_dev = std_dev(spect_avg_list) #technically calculated std_dev for spectrograms based on the average of the whole spectrogram we will see if this is bad later 12/2/2020
    # avg.depth_dev = std_dev(depth_list)
    # avg.spect = np.mean(spect_list)
    # avg.spect_dev = np.std(spect_list)
    # avg.spect, avg.spect_dev = std_dev(spect_list)
    # avg.sound_speed[0], avg.sound_speed_dev[0] = std_dev(sound_speed_list_0)
    # avg.sound_speed[1], avg.sound_speed_dev[1] = std_dev(sound_speed_list_100)
    # avg.sound_speed[2], avg.sound_speed_dev[2] = std_dev(sound_speed_list_200)
    for i in range(num_speeds):
        sound_speed, sound_speed_dev = std_dev(all_soundspeeds[i])
        avg.sound_speed.append(sound_speed) 
        avg.sound_speed_dev.append(sound_speed_dev)

    avg.length, avg.length_dev = std_dev(length_list)
    avg.SOG, avg.SOG_dev = std_dev(SOG_list)
    avg.draught, avg.draught_dev = std_dev(draught_list)
    avg.wspd, avg.wspd_dev = std_dev(wspd_list)
    
    
    
    
    #TESTING__________________________________________________________________________________________
    # stand_cpa = apply_transform(cpa_list,avg.cpa, avg.cpa_dev)
    # stand_temp = apply_transform(temp_list,avg.temp, avg.temp_dev)
    # stand_sal = apply_transform(sal_list,avg.sal, avg.sal_dev)
    # stand_sound_speed = apply_transform(sound_speed_list,avg.sound_speed, avg.sound_speed_dev)
    # stand_length = apply_transform(length_list,avg.length, avg.length_dev)
    # stand_SOG = apply_transform(SOG_list,avg.SOG, avg.SOG_dev)
    # stand_draught = apply_transform(draught_list,avg.draught, avg.draught_dev)
    # stand_spect = apply_transform(spect_list,avg.spect, avg.spect_dev)
    # stand_sound_speed_0 = apply_transform(sound_speed_list_0,avg.sound_speed[0], avg.sound_speed_dev[0])
    # stand_sound_speed_100 = apply_transform(sound_speed_list_100,avg.sound_speed[1], avg.sound_speed_dev[1])
    # stand_sound_speed_200 = apply_transform(sound_speed_list_200,avg.sound_speed[2], avg.sound_speed_dev[2])
    
    
    # stand_avg_cpa, stand_dev_cpa = std_dev(stand_cpa)
    # print("cpa: " + str(stand_avg_cpa) + ' ,' + str(stand_dev_cpa))
    
    # stand_avg_temp, stand_dev_temp = std_dev(stand_temp)
    # print("temp: " + str(stand_avg_temp) + ' ,' + str(stand_dev_temp))
    
    # stand_avg_sal, stand_dev_sal = std_dev(stand_sal)
    # print("sal: " + str(stand_avg_sal) + ' ,' + str(stand_dev_sal))
    
    # stand_avg_sound_speed, stand_dev_sound_speed = std_dev(stand_sound_speed)
    # print("sound_speed: " + str(stand_avg_sound_speed) + ' ,' + str(stand_dev_sound_speed))
    
    # stand_avg_length, stand_dev_length = std_dev(stand_length)
    # print("length: " + str(stand_avg_length) + ' ,' + str(stand_dev_length))
    
    # stand_avg_SOG, stand_dev_SOG = std_dev(stand_SOG)
    # print("SOG: " + str(stand_avg_SOG) + ' ,' + str(stand_dev_SOG))
    
    # stand_avg_draught, stand_dev_draught = std_dev(stand_draught)
    # print("draught: " + str(stand_avg_draught) + ' ,' + str(stand_dev_draught))
    
    # stand_avg_spect, stand_dev_spect = std_dev(stand_spect)
    # print("spect: " + str(stand_avg_spect) + ' ,' + str(stand_dev_spect))
    
    # stand_avg_sound_speed_0, stand_dev_sound_speed_0 = std_dev(stand_sound_speed_0)
    # print("sound_speed 0: " + str(avg.sound_speed[0]) + ' ,' + str(avg.sound_speed_dev[0]))
    
    # stand_avg_sound_speed_100, stand_dev_sound_speed_100 = std_dev(stand_sound_speed_100)
    # print("sound_speed 100: " + str(avg.sound_speed[1]) + ' ,' + str(avg.sound_speed_dev[1]))
  
    # stand_avg_sound_speed_200, stand_dev_sound_speed_200 = std_dev(stand_sound_speed_200)
    # print("sound_speed 200: " + str(avg.sound_speed[2]) + ' ,' + str(avg.sound_speed_dev[2]))

    # count = collections.Counter(stand_sound_speed_0)
    
    # print(count)
    # print(len(list(count.keys())))
    # plt.hist(list(count.keys()),count.values(),edgecolor="black",width=0.5)
    
    # plt.hist(stand_sound_speed_0,50)
    # plt.xlabel("Sound Speed at Depth: {}".format(0))
    # plt.ylabel("Count")
    
    # plt.savefig("J:\\Histograms\\Standardized_Speed_Histogram_{}.png".format(0))
    # plt.close()

    # plt.hist(stand_sound_speed_100,50)
    # plt.xlabel("Sound Speed at Depth: {}".format(0))
    # plt.ylabel("Count")
    
    # plt.savefig("J:\\Histograms\\Standardized_Speed_Histogram_{}.png".format(100))
    # plt.close()
    # plt.hist(stand_sound_speed_200,50)
    # plt.xlabel("Sound Speed at Depth: {}".format(0))
    # plt.ylabel("Count")
    
    # plt.savefig("J:\\Histograms\\Standardized_Speed_Histogram_{}.png".format(200))
    # plt.close()
    return avg
    
def Save_Avg(filepath, avg):
    filehandler = open(filepath, 'wb+')
    pickle.dump(avg,filehandler)

def Load_Avg(filepath):
    file_handler = open(filepath, 'rb')
    avg = pickle.load(file_handler)
    print("Unpickled Average Values")
    return avg

# anAvg = Find_Avg("J:\Pickled_Data_2\\")
# Save_Avg('J:\\Average_Data.obj',anAvg)
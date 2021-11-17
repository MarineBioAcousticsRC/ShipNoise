import numpy as np
from dat_extract.extract.Ship_Variable_Extraction import Ship
import unpickle as up
import math

class Avg_Values:
    def __init__(self,cpa,temp,sal,depth,max_spect,spect, sound_speed,
                length, SOG, draught, cpa_dev,temp_dev,sal_dev,
                depth_dev,spect_dev,sound_speed_dev,
                length_dev, SOG_dev, draught_dev):
        self.cpa = cpa
        self.temp = temp
        self.sal = sal
        self.depth = depth
        self.max_spect = max_spect
        self.spect = spect
        self.sound_speed = sound_speed
        self.length = length
        self.SOG = SOG
        self.draught = draught
        
        self.cpa_dev = cpa_dev
        self.temp_dev = temp_dev
        self.sal_dev = sal_dev
        self.depth_dev = depth_dev
        self.spect_dev = spect_dev
        self.sound_speed_dev = sound_speed_dev
        self.length_dev = length_dev
        self.SOG_dev = SOG_dev
        self.draught_dev = draught_dev
        
def Average(list):
    list = np.array(list)
    return sum(list)/len(list)

def std_dev(list):
    list = np.array(list)
    mean = sum(list)/len(list)
    diff_list = (np.array(list)-mean)**2
    std_dev = math.sqrt(sum(diff_list)/len(diff_list))
    return mean,std_dev

def apply_transform(list,avg,dev):
    return (np.array(list)-avg)/dev
    
def Find_Avg(file):
    ships = up.unpickle_ships(file)
    avg = Avg_Values(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)
    cpa_list = []
    temp_list = []
    sal_list = []
    # depth_list = []
    # spect_list = []
    sound_speed_list = []
    length_list = []
    SOG_list = []
    draught_list = []
    
    for ship in ships: #amass all the variables into lists to calc the avg and std_dev
        
        if np.amax(ship.spect) > avg.max_spect:
            avg.max_spect = np.amax(ship.spect)
        
        ship.cpa = np.min(ship.distance)
        cpa_list.append(ship.cpa)
        temp_list.append(float(ship.temp[1])) 
        sal_list.append(float(ship.sal[1]))
        # depth_list.append(ship.depth)
        # np.mean(ship.spect)
        # spect_list.append(np.mean(ship.spect))
        sound_speed_list.append(ship.sound_speed) 
        length_list.append(ship.length)
        
        if not np.isnan(Average(ship.SOG)): #sometimes there are no samples and this makes SOG a nan
            SOG_list.append(Average(ship.SOG)) 
        else:
            SOG_list.append(0) #keeps the lists the same length
            
        draught_list.append(ship.draught) 
        

   #Calc all standard deviations and averages
    # print(spect_list)
    avg.cpa, avg.cpa_dev = std_dev(cpa_list)
    avg.temp, avg.temp_dev = std_dev(temp_list)
    avg.sal, avg.sal_dev = std_dev(sal_list)
    # avg.depth_dev = std_dev(depth_list)
    # avg.spect = np.mean(spect_list)
    # avg.spect_dev = np.std(spect_list)
    # avg.spect, avg.spect_dev = std_dev(spect_list)
    avg.sound_speed, avg.sound_speed_dev = std_dev(sound_speed_list)
    avg.length, avg.length_dev = std_dev(length_list)
    avg.SOG, avg.SOG_dev = std_dev(SOG_list)
    avg.draught, avg.draught_dev = std_dev(draught_list)
    
    
    
    
    #TESTING__________________________________________________________________________________________
    # stand_cpa = apply_transform(cpa_list,avg.cpa, avg.cpa_dev)
    # stand_temp = apply_transform(temp_list,avg.temp, avg.temp_dev)
    # stand_sal = apply_transform(sal_list,avg.sal, avg.sal_dev)
    # stand_sound_speed = apply_transform(sound_speed_list,avg.sound_speed, avg.sound_speed_dev)
    # stand_length = apply_transform(length_list,avg.length, avg.length_dev)
    # stand_SOG = apply_transform(SOG_list,avg.SOG, avg.SOG_dev)
    # stand_draught = apply_transform(draught_list,avg.draught, avg.draught_dev)
    # stand_spect = apply_transform(spect_list,avg.spect, avg.spect_dev)
    
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
    
    print("sound_speed: " + str(avg.sound_speed) + ' ,' + str(avg.sound_speed_dev))
    
    
    
    return avg
# Find_Avg("D:\Pickled_Data_2\\")
import unpickle as up
from dat_extract.extract.Ship_Variable_Extraction import Ship
import numpy as np
import math
folder = "D:\Pickled_Data_2\\"

def std_dev(list):
    mean = sum(list)/len(list)
    diff_list = (np.array(list)-mean)**2
    std_dev = math.sqrt(sum(diff_list)/len(diff_list))
    return mean,std_dev

def calc_speed(z,s,t):
    a1 = 1448.96
    a2 = 4.591
    a3 = (-5.304 * (10**(-2)))
    a4 = (2.374 * (10**(-4)))
    a5 = 1.340
    a6 = (1.630 * (10**(-2)))
    a7 = (1.675 * (10**(-7)))
    a8 = (-1.025 * (10**(-2)))
    a9 = (-7.139 * (10**(-13)))
    
    speed = a1 + a2*t + a3*(t**2) + a4*(t**3) + a5*(s-35) + a6*z + a7*(z**2) + a8*t*(s-35) + a9*t*(z**3)
    
    return speed

def all_speeds(folder):
    highest = 0
    lowest = 99999 #temps to check validity of data
    speed_list = []
    for ships in up.unpickle_batch(folder,100,0,9000):
        for ship in ships:
            ship.depth = np.array([float(i) for i in ship.depth])
            ii = np.where(ship.depth == 1)[0]
            if len(ii) > 0:
            
                index = ii[0]
                depth_400 = float(ship.depth[index])
                temp_400 = float(ship.temp[index])
                sal_400 = float(ship.sal[index])
                # print(depth_400)
                # print(temp_400)
                # print("sal" + str(sal_400))
                
                ship.sound_speed = calc_speed(depth_400,sal_400,temp_400) #for this run only cpa refers to sound speed
                
                s = ship.sound_speed
                if s > highest:
                    highest = s
                if s < lowest:
                    lowest = s
                speed_list.append(s)
            else:
                print(ship.id)


            
            up.one_jar(folder,ship,False)
    
    print(highest)
    print(lowest)
    mean, dev = std_dev(speed_list)
    print(mean)
    print(dev)
    u_speeds = np.unique(np.array(speed_list))
    print(u_speeds)
    print(len(u_speeds))
   
all_speeds(folder)

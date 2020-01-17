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

def find_closest_depth(ship,depth):
    sub = [abs(x - depth) for x in ship.depth]
    idx = sub.index(min(sub))
    return ship.depth[idx]

def specific_depth(ships,des_depth):
    highest = 0
    lowest = 99999 #temp vars to check validity of data
    speed_list = []
    all_depths=[]
    x = 0
    for ship in ships:
        ship.depth = np.array([float(i) for i in ship.depth])
        ii = np.where(ship.depth == find_closest_depth(ship,des_depth))[0]
        if len(ii) > 0:
        
            index = ii[0]
            act_depth = float(ship.depth[index])
            all_depths.append(act_depth)
            temp = float(ship.temp[index])
            sal = float(ship.sal[index])
            # print(depth_400)
            # print(temp_400)
            # print("sal" + str(sal_400))
            
            ship.sound_speed.append(calc_speed(act_depth,sal,temp))
            
            s = ship.sound_speed[-1]
            if s > highest:
                highest = s
            if s < lowest:
                lowest = s
            speed_list.append(s)
        else:
            print(ship.id)
            x+=1
    # print(x)        
    print("depth: " + str(des_depth))
    print("highest: " + str(highest))
    print("lowest: " +str(lowest))
    mean, dev = std_dev(speed_list)
    print("mean: " + str(mean))
    print("std_dev: " + str(dev))
    u_speeds = np.unique(np.array(speed_list))
    print("unique speeds: " + str(u_speeds))
    print("num unique speeds:  " + str(len(u_speeds)))
    u_depths = np.unique(np.array(all_depths))
    print("unique depths: " + str(u_depths))
    print("num unique depths:  " + str(len(u_depths)))
    print("------------------------------------------------------------------------------------")
    return ships
    
def all_speeds(folder):
    depths = [0,100,200]
    ships = up.unpickle_ships(folder)
    for ship in ships:
        ship.sound_speed = []
        up.one_jar(folder,ship,False)
    for depth in depths:
        ships = up.unpickle_ships(folder)
        new_ships = specific_depth(ships,depth)
        up.store(new_ships,folder)
    
all_speeds(folder)

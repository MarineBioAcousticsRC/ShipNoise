import unpickle as up
import matplotlib.pyplot as plt
import numpy as np
import collections

folder1 = "J:\Pickled_Data_2\\"
folder2 = "J:\Shipping_Validation\\New_Val\\"
    
def collect_months(ships):
    result = []
    for ship in ships:
        result.append(ship.month)
    return result
    
def collect_speeds(ships,depth):
    result = []
    for ship in ships:
        result.append(ship.sound_speed[depth])
    return result
    
def month_histogram(ships):
    months = collect_months(ships)
    count = collections.Counter(months)
    print(count)
    
    plt.bar(list(count.keys()),count.values(),edgecolor="black")
    plt.xlabel("Month")
    plt.ylabel("Count")
    
    plt.savefig("J:\\Histograms\\New_Month_Histogram.png")
    #plt.show()
    plt.close()
    
def speed_histogram(ships):
    
    for depth in range(0,3):
        speeds = collect_speeds(ships,depth)
        count = collections.Counter(speeds)
        
        print(count)
        print(len(list(count.keys())))
        plt.hist(speeds,50,edgecolor="black",width=0.5)
        
        plt.xlabel("Sound Speed at Depth: {}".format(depth*100))
        plt.ylabel("Count")
        
        plt.savefig("J:\\Histograms\\With_CASE-STSE_Speed_Histogram_{}.png".format(depth*100))
        plt.close()
    
def histograms():
    ships = up.unpickle_ships(folder1)
    
    month_histogram(ships)
    speed_histogram(ships)
    
histograms()    
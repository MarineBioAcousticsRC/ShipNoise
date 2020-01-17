import unpickle as up
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
import datetime
folder = "D:\Pickled_Data_2\\"

def collect(ships):
    result1 = []
    result2 = []
    for ship in ships:
        result1.append(ship.cpa_datetime.timestamp())
        result2.append(ship.spect.mean())
        # result2.append()
    return (result1,result2)
    
def Average(list):
    list = np.array(list)
    return sum(list)/len(list)    
    
def correlations():
    ships = up.unpickle_ships(folder)    
    feats, means = collect(ships)
    nans = np.logical_or(np.isnan(feats), np.isnan(means))
    infs = np.logical_or(np.isinf(feats), np.isinf(means))
    nans_infs = np.logical_or(nans,infs)
    for i in range(len(nans_infs)):
        if nans_infs[i]:
            print(ships[i].id)
            feats.pop(i)
            means.pop(i)
            
    corr = pearsonr(means, feats)
    print("Correlation between datetime and mean spect: "+str(corr))
correlations()
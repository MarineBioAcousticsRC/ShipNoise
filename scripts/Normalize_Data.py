import unpickle as up
#import Spect_Generate_Resample_File_Time as gen
import numpy as np
from dat_extract.extract.Ship_Variable_Extraction import Ship


rootdir = "D:\ShippingCINMS_copy\COP" #set dir for the extraction
destination_folder = 'D:\PickledData\\'
f_80 = 'D:\CUGN_line_80.nc'
f_90 = 'D:\CUGN_line_90.nc'

def get_sizes(ships):
    #result = [np.size(ship.spect,1) for ship in ships]
    result = []
    for ship in ships:
        result.append(np.size(ship.spect,1))
    return result
    
def normalize(folder):
    folder = 'D:\PickledData\\'
    ships = up.unpickle_ships(folder)
    sizes = get_sizes(ships)
    max_size = max(sizes)
    for i in range(len(ships)):
        pad_length = max_size - sizes[i]
        ships[i].spect = np.pad(ships[i].spect,[(0,0),(0,pad_length)],mode='constant')
        print(ships[i].spect.shape)
        print(i)
        up.one_jar(folder,ships[i],False)
normalize(destination_folder)

import unpickle as up
#import Spect_Generate_Resample_File_Time as gen
import numpy as np
from dat_extract.extract.Ship_Variable_Extraction import Ship
from tqdm import tqdm
from colorama import init, Fore

init()

rootdir = "D:\ShippingCINMS_data\COP" #set dir for the extraction
destination_folder = 'D:\Pickled_Data_2\\'
f_80 = 'D:\CUGN_line_80.nc'
f_90 = 'D:\CUGN_line_90.nc'

def get_sizes(ships):
    #result = [np.size(ship.spect,1) for ship in ships]
    result = []
    for ship in ships:
        result.append(np.size(ship.spect,1))
    return result

def find_done(folder):
    i=0
    for ships in up.unpickle_batch(folder,100,6500,9000):
        for ship in ships:
            if ship.spect is None:
                i+=1
                up.one_jar(folder,ship,True)
                tqdm.write(str(i))
                pass

def calc_pad(des_size,size):
    
    sub = des_size - size
    if (sub % 2) == 0:
        pre_pad = sub//2
        post_pad = sub//2
    else:
        pre_pad = sub//2
        post_pad = ((sub//2) + 1)
        
    return pre_pad, post_pad
    
def normalize(folder):
    x=0
    y=0
    for ships in up.unpickle_batch(folder,50,4200,9000):
        
        #print(np.size(ships))
        #print(ships[0].spect.shape)
        sizes = get_sizes(ships)
        #avg_size = int(np.mean(sizes))
        square_size = np.size(ships[0].spect,0)
        for i in tqdm(range(len(ships)),"This Batch: ",bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.YELLOW, Fore.RESET)):
            try:
                pad_length = (square_size - sizes[i])
                beg_pad,end_pad = calc_pad(square_size,sizes[i])
                if(pad_length>=0):
                    ships[i].spect = np.pad(ships[i].spect,[(0,0),(beg_pad,end_pad)],mode='constant')
                else:
                    ships[i].spect = ships[i].spect[:,abs(beg_pad):sizes[i]+end_pad]
                # print(ships[i].spect.shape)
                # print(x)
                x+=1
                up.one_jar(folder,ships[i],False)
            except:
                y+=1
                up.one_jar(folder,ships[i],True)
                tqdm.write(str(y))
                pass
# find_done(destination_folder)
normalize(destination_folder)

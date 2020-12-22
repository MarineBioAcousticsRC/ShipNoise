import pickle 
import Spect_Generate_Resample_File_Time as gen
import numpy as np

rootdir = "D:\ShippingCINMS_copy\COP" #set dir for the extraction
destination_folder = 'D:\Pickled_Data\\'
f_80 = 'D:\CUGN_line_80.nc'
f_90 = 'D:\CUGN_line_90.nc'

def store(ships):
    destination =  destination_folder + ship.year_month +'\\' + ship.id + '.obj'
    for ship in ships:
        if ship.temp != 0:
            filehandler = open(destination, 'w')
            pickle.dump(ship,filehandler)
            
def normalize(rootdir,f_80,f_90)
    ships = gen.generate(rootdir,f_80,f_90)
    store(ships)
normalize(rootdir,f_80,f_90)
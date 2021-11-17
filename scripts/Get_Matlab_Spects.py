import unpickle as up
from dat_extract.extract.Ship_Variable_Extraction import Ship
from scipy.io import loadmat
import os.path
import h5py
folder = 'J:\Pickled_Data_Range\\'
folder2 = "J:\\Pickled_Data_2\\"
ships = up.unpickle_ships(folder2)
i = 0
for ship in ships:
    spectFilePath = ship.filepath + ship.id + "_rangeFreq.mat"
    if(os.path.exists(spectFilePath)):
        with h5py.File(spectFilePath, 'r') as f:
            ship.spect = f['finalDistSpec_floored'].value
            print(spectFilePath + ' ' + str(i))
            i+=1
            up.one_jar(folder,ship,False)
    # else:
        #up.one_jar(folder,ship,True)

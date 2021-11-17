import numpy as np
import os
from scipy import interpolate
transfer_folder = 'E:\TFs'


def get_tf_file(harp):
    for subdir, dirs, files in os.walk(transfer_folder): #goes through each file not only in root but each subdirectory
        for file in files:
            trans_file = subdir + os.sep + file #create filepath to each tf file
            #print(trans_file)
            if harp == '731' or harp == '736' or harp == '738' or harp == '780':
                if trans_file.startswith(harp,30) and trans_file.endswith(".tf"):
                    return trans_file
            elif trans_file.startswith(harp,18) and trans_file.endswith(".tf"): #only looking for tf files
                return trans_file
                
def get_tf(harp,f_desired):
   filepath = get_tf_file(harp)
   print(filepath)
   measured = []
   actual = []
   with open(filepath, encoding="utf8",errors = 'ignore') as fp: #extract specific lines
        for x, line in enumerate(fp):
            actual.append(float(line[:8].strip()))
            measured.append(float(line[9:].strip()))
   tf = interpolate.interp1d(actual,measured, axis=0, fill_value="extrapolate")
   uppc = tf(f_desired)
   return uppc


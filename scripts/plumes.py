import pandas as pd
from datetime import datetime,timedelta
import numpy as np
from dat_extract.extract.Ship_Variable_Extraction import Ship
import unpickle as up


csv_file = "J:\\Plumes_and_Blumes_CTD_Fixed.csv"
folder = "J:\\Pickled_Data_2\\"

class Sample:
    def __init__(self,date,depths,temps,sals):
        self.date = date
        self.depths = depths
        self.temps = temps
        self.sals = sals

        
def get_data(filename):
    data = pd.read_csv(filename,parse_dates=['date']) 
    return data

def find_best_sample(df,des_date):
    found = True
    df_4 = df.loc[(df['station'] == 4)]
    
    diff = abs(df_4.date - des_date)
    index = (diff.idxmin())
    
    near_date = df_4.ix[[index]].date.item()
    print(abs(datetime.fromtimestamp(near_date / 1e9) - des_date))
    day_after = near_date + 86400000000000
    near_date = pd.Timestamp(near_date,unit='ns')
    day_after = pd.Timestamp(day_after,unit='ns')
    
    df_4 = df_4.set_index('date')
    df_sel = df_4[near_date:day_after]
    print(df_sel.head())
    
    depths = df_sel['depth'].to_numpy()
    temps = df_sel['wt'].to_numpy()
    sals = df_sel['salinity'].to_numpy()
    
    best_sample = Sample(near_date,depths,temps,sals)

    return found,best_sample

def fix_sample(sample):
    searchval = 1
    ii = np.where(sample.depths == searchval)[0]

    if len(ii) > 1:
        index = ii[1]
        sample.depths = sample.depths[index:]
        sample.temps = sample.temps[index:]
        sample.sals = sample.sals[index:]

    return sample
    
def match_ships(rootdir,csv):
    i=0
    data_frame = get_data(csv)
    for ships in up.unpickle_batch(rootdir,100,9000,9100):
        for ship in ships:
            # if isinstance(ship.sal, int):
            print(ship.id + ': ' + str(i))
            found,sample = find_best_sample(data_frame,ship.cpa_datetime)
            sample = fix_sample(sample)
           
            if found:
                ship.depth = sample.depths
                ship.temp = sample.temps
                ship.sal = sample.sals
                ship.IMO = sample.date
                
                up.one_jar(rootdir,ship,False)
                print('pickled: ' + str(i))
                i+=1
            
match_ships(folder,csv_file)
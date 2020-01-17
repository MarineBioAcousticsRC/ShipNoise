#import unpickle as up
from datetime import datetime,timedelta
import numpy as np
from dat_extract.extract.Ship_Variable_Extraction import Ship
from importlib import reload


class Sample:
    def __init__(self,provider,date,depths,temps,sals,lat,lon):
        self.provider = provider
        self.date = date
        self.depths = depths
        self.temps = temps
        self.sals = sals
        self.lat = lat
        self.lon = lon




def get_samples(filepath):
    samples = []
    result = []
    with open(filepath, encoding="utf8",errors = 'ignore') as fp: #extract specific lines
        for x, line in enumerate(fp):
            (num,provider,date,time,station,depth,temp,sal) = line.split(',')
            # print(line)
            if str(provider) == 'CalCOFI':
                lat = 34.44444444
                lon = -120.23027778
                date = str(date)
                con_date = datetime.strptime(date.strip(), '%d-%b-%y')
                
            else:
                lat = 34.25027778
                lon = -119.91055556
                date = str(date)
                con_date = datetime.strptime(date.strip(), '%Y%m%d')
                
            new_sample = Sample(provider,con_date,depth,temp,sal,lat,lon)
            samples.append(new_sample)
    result = same_sample(samples)
    return result
def all_dates(samples):
    result = []
    for sample in samples:
        result.append(sample.date)
    return result
def same_sample(samples):
    result = []
    dates = all_dates(samples)
    unique_dates = np.unique(dates)
    for date in unique_dates:
        depths = []
        temps = []
        sals = []
        ii = [x for x,val in enumerate(dates) if val==date]
        s = samples[ii[0]]
        for j in range(len(ii)):
            index = ii[j]
            depths.append(samples[index].depths)
            temps.append(samples[index].temps)
            sals.append(samples[index].sals)
        result.append(Sample(s.provider,date,depths,temps,sals,s.lat,s.lon))
    return(result)

def match_ships(filepath):
    import unpickle as up
    samples = get_samples(filepath)
    print(samples[30].provider)
    print(samples[30].depths)
    for i in range(len(samples)):
        if '300' not in samples[i].depths:
            print("Not In: " + str(samples[i].date))
        else:
            print(samples[i].date)
    # for ships in up.unpickle_batch("D:\Pickled_Data_2\\",100,0,9000):
        # for ship in ships:
            # if ship.temp == 0:
            # closest = timedelta(days=300)
            # i = 0 
            # for sample in samples:
                # this = abs(sample.date - ship.cpa_datetime)
                # if this < closest:
                    # closest = this
                    # index = i
                # i+=1
            # ship.depth = samples[index].depths
            # ship.IMO = samples[index].date
            # ship.temp = samples[index].temps
            # ship.sal = samples[index].sals
            # print(ship.temp)
            # up.one_jar("D:\Pickled_Data_2\\",ship,False)
match_ships('D:\CALCOFI.csv')
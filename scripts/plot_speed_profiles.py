from datetime import datetime,timedelta
import numpy as np
from dat_extract.extract.Ship_Variable_Extraction import Ship
import matplotlib.pyplot as plt
from importlib import reload
import collections
folder1 = "J:\Pickled_Data_2\\"
folder2 = "J:\Shipping_Validation\\New_Val\\"

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
                
            elif str(provider) == 'UCSB':
                lat = 34.25027778
                lon = -119.91055556
                date = str(date)
                con_date = datetime.strptime(date.strip(), '%Y%m%d')
            elif str(provider) == 'SPRAY':
                lat = 34.25
                lon = -119.9 
                date = str(date)
                con_date = datetime.strptime(date.strip(), '%d-%b-%y')
            elif str(provider) == 'CASE':
                lat = 34.29
                lon = -120 
                date = str(date)
                con_date = datetime.strptime(date.strip(), '%d-%b-%y')
                
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
            if (str(samples[index].temps) == 'NaN'):
                # print('NAN')
                continue
            else:
                depths.append(samples[index].depths)
                temps.append(samples[index].temps)
                sals.append(samples[index].sals)
        result.append(Sample(s.provider,date,depths,temps,sals,s.lat,s.lon))
    return(result)
def find_closest_depth(sample,depth):
    sub = [abs(x - depth) for x in sample.depths]
    idx = sub.index(min(sub))
    return sample.depths[idx]

def plot_same_day(filepath):
    samples = get_samples(filepath)
    days = [datetime(2015,7,15),datetime(2015,7,18),datetime(2015,7,19)]
    depths = range(0,500,10)

    spray_speeds = []
    case_speeds = []
    calcofi_speeds = []

    for sample in samples:
        if sample.date == days[0]:
            spray_sample = sample
        if sample.date == days[1]:
            case_sample = sample
        if sample.date == days[2]:
            calcofi_sample = sample

    samples = [spray_sample,case_sample,calcofi_sample]

    for sample in samples:
        sample.lat = []
        sample.depths = np.array([float(i) for i in sample.depths])
        for depth in depths:
            ii = np.where(sample.depths == find_closest_depth(sample,depth))[0]
            if len(ii) > 0:
            
                index = ii[0]
                act_depth = float(sample.depths[index])
                temp = float(sample.temps[index])
                sal = float(sample.sals[index])
                # print(depth_400)
                # print(temp_400)
                # print("sal" + str(sal_400))
                sample.lat.append(calc_speed(act_depth,sal,temp))

    spray_speeds = spray_sample.lat
    case_speeds = case_sample.lat
    calcofi_speeds = calcofi_sample.lat

    plt.plot(spray_speeds,depths,'r',label='SPRAY 07/15/2015')
    plt.plot(case_speeds,depths,'g',label='CASE-STSE: 07/18/2015')
    plt.plot(calcofi_speeds,depths,'b',label='CALCOFI: 07/19/2015')
    plt.title('Sound Speed Profile July 2015')
    plt.gca().invert_yaxis()
    plt.legend()
    plt.show()
plot_same_day('J:\\CALCOFI_SPRAY_CASE.csv')
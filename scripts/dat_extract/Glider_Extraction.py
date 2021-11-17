import pandas as pd
import netCDF4 as nc
import numpy as np
from datetime import datetime,timedelta
import Ship_Variable_Extraction as dat
import xarray as xr 
from geopy.distance import geodesic
import unpickle as up
from extract.Ship_Variable_Extraction import Ship



folder = "J:\PickledData\\"
rootdir = "J:\ShippingCINMS_data\COP"
f_80 = 'J:\CUGN_line_80.nc'
f_90 = 'J:\CUGN_line_90.nc'

# a function to find the index of the point closest pt
# (in squared distance) to give lat/lon value.
def get_closest_coord(ds_80,ds_90,latpt,lonpt):
    idx_80 = (((ds_80.lat-latpt)**2 + (ds_80.lon-lonpt)**2)).argmin()
    idx_90 = (((ds_90.lat-latpt)**2 + (ds_90.lon-lonpt)**2)).argmin()
    coords_80 = ds_80.isel(profile=idx_80)
    coords_90 = ds_90.isel(profile=idx_90)
    if (((coords_80.lat-latpt)**2) + ((coords_80.lon-lonpt)**2)).argmin() <= (((coords_90.lat-latpt)**2) + ((ds_90.lon-lonpt)**2)).argmin():
        coords = coords_80
    else:
        coords = coords_90
    coords_1 = (coords.lat,coords.lon)
    coords_2 = (latpt,lonpt)
    if (geodesic(coords_1, coords_2).km < 15):
        return coords
    else:
        return 0
        
# a function to get the profiles closest to the time of ship travel
def get_closest_time(ds_80,ds_90,des_time):
    des_time = (des_time - datetime(1970, 1, 1)) / timedelta(seconds=1)
    minus_time = pd.Timestamp((des_time - (604800)),unit = 's')
    plus_time = pd.Timestamp((des_time + 604800),unit = 's')
    conv_time_80 = []
    conv_time_90 =[]
    for time in ds_80.time.data:
        conv_time_80.append(pd.Timestamp(time))
    for time in ds_90.time.data:
        conv_time_90.append(pd.Timestamp(time))
    idx_80 = []
    idx_90 = []
    i = 0
    for time in conv_time_80:
        if(time >= minus_time) and (time <= plus_time):
            idx_80.append(i)
        i+=1
    i = 0
    for time in conv_time_90:
        if(time >= minus_time) and (time <= plus_time):
            idx_90.append(i)
        i+=1
    sbst_80 = ds_80.isel(profile=idx_80)
    sbst_90 = ds_90.isel(profile=idx_90)
    #ds_90.sel(profile=idx_90)
    if (np.size(idx_80) > 0) or (np.size(idx_90) > 0):
        if(np.size(sbst_80.profile) > 0) and (np.size(sbst_90.profile)):
            return sbst_80,sbst_90
        else:
            return 0,0
    else:
        return 0,0

def glider_data(f_80,f_90,folder):
    
    ships = up.unpickle_ships(folder)
    ds_80 = xr.open_dataset(f_80)
    ds_90 = xr.open_dataset(f_90)
    no_data = []
    for ship in ships:
        filepath = ship.filepath + ship.id
        print(filepath)
        sbst_80, sbst_90 = get_closest_time(ds_80,ds_90,ship.cpa_datetime)
        if(sbst_80 != 0) or (sbst_90 != 0):
            best_profile = get_closest_coord(sbst_80,sbst_90,ship.harplat, ship.harplon)
            if(best_profile != 0):
                lat = best_profile.lat
                lon = best_profile.lon
                ship.temp = best_profile.temperature
                ship.sal = best_profile.salinity
            else:
                no_data.append((ship.mmsi,ship.month))
        else:
                no_data.append((ship.mmsi,ship.month))
        
        
        #print(ship.temp)
        #print(ship.sal)
    print(no_data)
    print(len(no_data))
    print(len(ships))
    print(len(no_data)/len(ships))
    up.store(ships,folder)
    
glider_data(rootdir,f_80,f_90,folder)
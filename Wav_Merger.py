import Ship_Variable_Extraction as dat
from pydub import AudioSegment
import numpy as np
from datetime import datetime, timedelta 
import os 
import shutil

filepath = "D:\ShippingCINMS_data\COP"

def merge_wav(f1,f2): #function to actually merge wav files
    
    sound1 = AudioSegment.from_wav(f1)
    sound2 = AudioSegment.from_wav(f2)

    new_wav = sound1 + sound2
    #new_wav.export(f1,format="wav")
    
def get_all_mmsi(ships): #function to get all the mmsi of ships
    result = []
    for ship in ships:
        result.append(ship.mmsi)
    print('here')
    print(result)
    return result

def merge_txt(f1,f2):
    copy_lines = []
    with open(f2, encoding="utf8",errors = 'ignore') as fp: #extract specific lines
        for x, line in enumerate(fp): #copy all distance lines from later crossing 
            if x > 18:                #and append them to the earlier crossing file
                copy_lines.append(line[:])
    fp.close()
    file = open(f1,"a")
    for line in copy_lines:    
        file.write("%s" % line)
    file.close()
    
def move_files(ship):
    wavfile = ship.filepath + ship.id + '.wav'
    txtfile = ship.filepath + ship.id + '.txt'
    picfile = ship.filepath + ship.id + '.jpg'
    new_wavfile =  'D:\Merged_Later_Files\\' + ship.year_month + '\\' + ship.id + '.wav'
    new_txtfile = 'D:\Merged_Later_Files\\' + ship.year_month + '\\' + ship.id + '.txt'
    new_picfile = 'D:\Merged_Later_Files\\' + ship.year_month + '\\' + ship.id + '.jpg'
    shutil.move(wavfile, new_wavfile)
    shutil.move(txtfile, new_txtfile)
    shutil.move(picfile, new_picfile)
    
def same_crossing(file): #function to decide what wav files to merge
    ships = dat.extract(file)
    all_mmsi = get_all_mmsi(ships)
    i=0
    while i < len(ships):
        searchval = ships[i].mmsi
        print(searchval)
        ii = [x for x,val in enumerate(all_mmsi) if val==searchval and x > i] #find all occurences of same mmsi
        print(ii)
        for j in range(len(ii)): # go through all occurances and see if they are actually same crossing
            index = ii[j]
            delta = abs(ships[i].cpa_datetime - ships[index].cpa_datetime) #find the time difference
            print(delta)
            if delta < timedelta(hours=1): #only merge if crossing is within an hour of eachother 
                wav1 = ships[i].filepath + ships[i].id + '.wav' #construct filepaths to wav and txt files
                txt1 = ships[i].filepath + ships[i].id + '.txt'
                wav2 = ships[index].filepath + ships[index].id + '.wav'
                txt2 = ships[index].filepath + ships[index].id + '.txt'
                
                if(ships[i].cpa_datetime < ships[index].cpa_datetime): 
                    merge_wav(wav1,wav2)#merge the two files with earlier first
                    merge_txt(txt1,txt2)
                    move_files(ships[index])
                    print("merged:")
                    print(wav1)
                    print(wav2)
                    
                    
                if(ships[i].cpa_datetime > ships[index].cpa_datetime):
                    merge_wav(wav2,wav1) #merge the two files with earlier first
                    merge_txt(txt2,txt1)
                    move_files(ships[i])
                    print("merged:")
                    print(wav2)
                    print(wav1)   
        i+=1
        
        
same_crossing(filepath)
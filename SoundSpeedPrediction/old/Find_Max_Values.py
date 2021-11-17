import numpy as np
from dat_extract.extract.Ship_Variable_Extraction import Ship
import unpickle as up

class Max_Values:
    def __init__(self,cpa,temp,sal,depth,spect,sound_speed,
                length, SOG, draught):
        self.cpa = cpa
        self.temp = temp
        self.sal = sal
        self.depth = depth
        self.spect = spect
        self.sound_speed = sound_speed
        self.length = length
        self.SOG = SOG
        self.draught = draught
        
        
def Average(lst): 
    return sum(lst) / len(lst)


    
def Find_Max(file):
    ships = up.unpickle_ships(file)
    max = Max_Values(0,0,0,0,0,0,0,0,0.1)
    
    
    for ship in ships:
        ship.cpa = np.min(ship.distance)
        if ship.cpa > max.cpa:
            max.cpa = ship.cpa
            
        if float(ship.temp[1]) > max.temp:
            max.temp = float(ship.temp[1])
            
        if float(ship.sal[1]) > max.sal:
            max.sal = float(ship.sal[1])
            
        # if float(ship.depth[0]) > max.depth:
            # max.depth = float(ship.depth[0])
            
        if np.amax(ship.spect) > max.spect:
            max.spect = np.amax(ship.spect)
            
        if ship.sound_speed > max.sound_speed:
            max.sound_speed = ship.sound_speed
            
        if ship.length > max.length:
            max.length = ship.length
        
        if Average(ship.SOG) > max.SOG:
            max.SOG = Average(ship.SOG)
            
        if ship.draught > max.draught:
            max.draught = ship.draught
    return max
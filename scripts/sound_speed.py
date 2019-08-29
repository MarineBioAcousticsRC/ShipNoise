import unpickle as up
from dat_extract.extract.Ship_Variable_Extraction import Ship

folder = "D:\PickledData\\"

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


ships = up.unpickle_ships(folder)
for ship in ships:
    deepest_temp = float(ship.temp[len(ship.temp)-1])
    print(deepest_temp)
    deepest_sal = float(ship.sal[len(ship.sal)-1])
    print(deepest_sal)
    deepest_depth = float(ship.depth[len(ship.depth)-1])
    print(deepest_depth)
    ship.cpa = calc_speed(deepest_depth,deepest_sal,deepest_temp) #for this run only cpa refers to sound speed
up.store(ships,folder)
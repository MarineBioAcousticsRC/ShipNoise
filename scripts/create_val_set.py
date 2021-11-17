import os 
import unpickle as up
import random

folder1 = "J:\Pickled_Data_2\\"
folder2 = "J:\Shipping_Validation\\Random_Val\\"

def choose_and_move(root,destination,batch):
    ships = up.unpickle_ships(destination)
    rand_ships = random.sample(ships,batch)
    up.store(rand_ships,root)
    for ship in rand_ships:
        up.one_jar(destination,ship,True)
    
choose_and_move(folder1,folder2,1000)    
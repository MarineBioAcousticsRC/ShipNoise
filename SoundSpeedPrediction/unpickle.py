import os
import pickle as pickle
#from dat_extract.extract.Ship_Variable_Extraction_Validation import Ship
# from dat_extract.extract.MARCAD_Ship_Variable_Extraction import Ship
import random
from tqdm import tqdm, trange
from colorama import init, Fore

import json, codecs
import numpy as np
init()

#folder = "J:\Pickled_Data_5\\"
#print(folder)
def pickle_2_json(pickle_dir, json_dir):
    ships = unpickle_ships(pickle_dir)
    store_as_json(json_dir,ships)

def store_as_json(rootdir, ships):
    i = 0
    for ship in ships:
        #destination = rootdir + ship.year_month + '\\' + ship.id + '.json'
        destination = rootdir + ship.id + '.json'

        ship.spect = ship.spect.tolist()
        ship.depth = ship.depth.tolist()
        ship.sal = list(map(float,ship.sal))
        json.dump(ship.__dict__, open(destination, 'w+', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4, default=str) ### this saves the array in .json format
        i += 1
        print("pickled: " + str(destination))

def unpickle_json(rootdir):
    ships = []
    i = 0
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            # print os.path.join(subdir, file)
            filepath = subdir + os.sep + file  # create filepath to each text file
            if filepath.endswith(".json"):
                obj_text = open(filepath, 'r', encoding='utf-8').read()
                ship = json.loads(obj_text)
                # ship["spect"] = np.asarray(ship.spect)
                ships.append(ship)
                # f = rootdir + ships[i].year_month + '\\' + ships[i].id + '.json'
                # print(f)
                i += 1
                print("JSON Unpickled! " + str(i))
    return ships

def unpickle_ships(rootdir):
    ships = []
    i = 0
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            # print os.path.join(subdir, file)
            filepath = subdir + os.sep + file  # create filepath to each text file
            if filepath.endswith(".obj"):
                file = open(filepath, 'rb')
                ships.append(pickle.load(file))
                f = rootdir + ships[i].year_month + '\\' + ships[i].id + '.obj'
                print(f)
                i += 1
                print("unpickled! " + str(i))
    return ships


def unpickle_a_batch(rootdir, start, stop):
    ships = []
    i = 0
    for subdir, dirs, files in os.walk(rootdir):
        new_files = files[start:stop]
        for file in new_files:
            # print os.path.join(subdir, file)
            filepath = subdir + os.sep + file  # create filepath to each text file
            if filepath.endswith(".obj"):
                file = open(filepath, 'rb')
                ships.append(pickle.load(file))
                f = rootdir + ships[i].year_month + '\\' + ships[i].id + '.obj'
                print(f)
                i += 1
                print("unpickled! " + str(i))
    return ships


def store(Ship, rootdir):
    destination = rootdir + Ship['filepath'] + '.obj'
        # if isinstance(ship.temp, int):
        # print("no data")
        # else:
    filehandler = open(destination, 'wb+')
    pickle.dump(Ship, filehandler)
    print("pickled: " + str(destination))


def clear_shelf(rootdir):
    i = 0
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".obj"):
                os.remove(filepath)
                i += 1
    print("cleared shelf: " + str(i))


def one_jar(rootdir, ship, smash):
    destination = rootdir + ship.year_month + '\\' + ship.id + '.obj'
    if smash:
        filehandler = open(destination, 'wb+')
        filehandler.close()
        os.remove(destination)
        tqdm.write("smashed!")
    else:
        tqdm.write(destination)
        filehandler = open(destination, 'wb+')
        pickle.dump(ship, filehandler)


def store_encodings(encodings, rootdir):
    i = 0
    for encoding in encodings:
        destination = rootdir + "encoding_" + str(i) + '.pickle'
        # if isinstance(ship.temp, int):
        # print("no data")
        # else:
        # print(ship.spect.shape)
        filehandler = open(destination, 'wb+')
        pickle.dump(encoding, filehandler)
        i += 1
        print("pickled! " + str(i))


def unpickle_encodings(rootdir):
    encodings = []
    i = 0
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            # print os.path.join(subdir, file)
            filepath = subdir + os.sep + file  # create filepath to each text file
            if filepath.endswith(".pickle"):
                file = open(filepath, 'rb')
                encodings.append(pickle.load(file))
                print(filepath)
                i += 1
                print("unpickled! " + str(i))
    return encodings


def unpickle_batch(rootdir, batch_size, start, stop):
    x = 0
    j = 0
    num_batches = (stop - start)//batch_size

    files = []
    for r, d, f in os.walk(rootdir):
        for file in f:
            if file.endswith('.obj'):
                files.append(os.path.join(r, file))
    # files = files[:9000]
    # random.shuffle(files)
    files = files[start:stop]
    # random.shuffle(files)
    for j in range(num_batches):
        ships = []
        i = 0
        # print(j)
        #batch_size = len(files)//num_batches
        batch = files[j*batch_size:(j+1)*batch_size]

        # print(len(batch))
        for file in batch:
            # os.path.join(subdir, file)
            # print(filepath)
            # print(file)
            file_handler = open(file, 'rb')
            ships.append(pickle.load(file_handler))
            i += 1
            x += 1
            tqdm.write("unpickled! " + file)
        j += 1
        yield ships
# clear_shelf(folder)
# store(ships,folder)
# for ship in ships:
    # print(ship.mmsi)
#if __name__ == '__main__':
#    pickle_2_json("J:\\Test_Pickles\\","J:\\Test_JSON")

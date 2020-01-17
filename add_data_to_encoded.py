import unpickle as up

folder = "D:\PickledData\\"

def add_data(folder):
    ships = up.unpickle_ships(folder)
    #add month or whatever info you wanna give it
    ship.encoded.append(ship.month)
    up.store(ships,folder)
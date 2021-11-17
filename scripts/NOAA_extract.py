import datetime

import unpickle as up
from dat_extract.extract.Ship_Variable_Extraction import Ship


class noaa_sample:
    def __init__(self, date, wdir, wspd, gst, wvht, dpd, apd, mwd, pres, atmp, wtmp, dewp, vis, tide):
        self.date = date
        self.wdir = wdir
        self.wspd = wspd
        self.gst = gst
        self.wvht = wvht
        self.dpd = dpd
        self.apd = apd
        self.mwd = pres
        self.atmp = atmp
        self.wtmp = wtmp
        self.dewp = dewp
        self.vis = vis
        self.tide = tide


def noaa_extract(file):
    samples = []
    with open(file, encoding="utf8", errors='ignore') as fp:  # extract specific lines
        for x, line in enumerate(fp):
            # print(line)
            (yr, mon, day, hour, min, wdir, wspd, gst, wvht, dpd, apd,
             mwd, pres, atmp, wtmp, dewp, vis, tide) = line.split(',')
            date = datetime.datetime(int(yr), int(
                mon), int(day), int(hour), int(min))
            new_sample = noaa_sample(date, float(wdir), float(wspd), float(gst), float(wvht), float(dpd), float(
                apd), float(mwd), float(pres), float(atmp), float(wtmp), float(dewp), float(vis), float(tide))
            samples.append(new_sample)
    return samples


def samples_to_ships(file):
    samples = noaa_extract(file)
    for ships in up.unpickle_batch("J:\Pickled_Data_3\\", 100, 0, 9000):
        for ship in ships:
            closest = datetime.timedelta(days=800)
            i = 0
            for sample in samples:
                this = abs(sample.date - ship.cpa_datetime)
                if this < closest and sample.wspd != 99.0 and sample.wspd != 9.0 and sample.wspd != 999.0:
                    closest = this
                    index = i
                i += 1
            if samples[index].wspd == 99.0 or samples[index].wspd == 9.0:
                print('something went wrong')
            else:
                # as a test to see if this is worth it putting variables into encoded
                ship.encoded = float(samples[index].wspd)
            print(ship.encoded)
            up.one_jar("J:\Pickled_Data_3\\", ship, False)


samples_to_ships("J:\\NOAA_ALL.csv")

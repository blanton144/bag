import ephem
import numpy as np
from astropy.time import Time


def apo_observer():
    apo = ephem.Observer()
    apo.lat = '32:46:49'
    apo.lon = '254:10:47'
    apo.elevation = 2788.
    apo.temp = 5.
    apo.pressure = 1.01325 * np.exp(- apo.elevation / (29.3 * apo.temp))
    return apo


def lco_observer():
    lco = ephem.Observer()
    lco.lat = '-29:00:53'
    lco.lon = '289:18:27'
    lco.elevation = 2380.
    lco.temp = 12.
    lco.pressure = 1.01325 * np.exp(- lco.elevation / (29.3 * lco.temp))
    return lco


def to_time(ephem_time):
    return Time(ephem_time.datetime(), scale='utc')


class Schedule():
    def __init__(self, observer=None):
        self.observer = observer
        if(self.observer is None):
            self.observer = apo_observer()
        self.sun = ephem.Sun()
        self.moon = ephem.Moon()

    def calculate(self, date=None, twilight='-15'):
        self.observer.date = ephem.Date(date) + 1. + 7. / 24.
        self.observer.horizon = twilight
        self.sun.compute(self.observer)
        self.moon.compute(self.observer)
        evening = self.observer.previous_setting(self.sun, use_center=True)
        morning = self.observer.next_rising(self.sun, use_center=True)
        if(self.moon.phase < 35.):
            self.dark_time_start = to_time(evening).mjd
            self.dark_time_end = to_time(morning).mjd
            self.bright_time_start = 0.
            self.bright_time_end = 0.
        elif(self.moon.phase > 95.):
            self.bright_time_start = to_time(evening).mjd
            self.bright_time_end = to_time(morning).mjd
            self.dark_time_start = 0.
            self.dark_time_end = 0.
        else:
            self.observer.horizon = '0'
            self.observer.date = evening
            self.moon.compute(self.observer)
            if(self.moon.alt > 0.):  # if moon is up at beginning of night
                self.bright_time_start = to_time(evening).mjd
                moonset = self.observer.next_setting(self.moon)
                if(moonset < morning):  # bright time til it sets
                    self.bright_time_end = to_time(moonset).mjd
                    self.dark_time_start = to_time(moonset).mjd
                    self.dark_time_end = to_time(morning).mjd
                else:  # which might be after morning
                    self.bright_time_end = to_time(morning).mjd
                    self.dark_time_start = 0.
                    self.dark_time_end = 0.
            else:  # if moon is down at beginning of night
                self.dark_time_start = to_time(evening).mjd
                moonrise = self.observer.next_rising(self.moon)
                if(moonrise > morning):  # if it doesn't rise tonight
                    self.dark_time_end = to_time(morning).mjd
                    self.bright_time_start = 0.
                    self.bright_time_end = 0.
                else:  # if it does rise tonight
                    self.dark_time_end = to_time(moonrise).mjd
                    self.bright_time_start = to_time(moonrise).mjd
                    self.bright_time_end = to_time(morning).mjd

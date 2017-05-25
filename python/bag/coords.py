from astropy.utils.iers import IERS_A, IERS_A_URL
from astropy.utils.data import download_file
from astropy.utils import iers
import astropy.time as time

iers_a_file = download_file(IERS_A_URL, cache=True)
iers_a = IERS_A.open(iers_a_file)
iers.IERS.iers_table = iers.IERS_A.open(download_file(iers.IERS_A_URL,
                                                      cache=True))


def mjd2lst(mjd=None, longitude=None):
    """
    Returns LST in hours, given Modified Julian Day in days
    """
    timeobs = time.Time(mjd, format='mjd', scale='utc')
    timeobs.delta_ut1_utc = 0.  # this correction is less than 1 sec
    longitude = longitude * 1.
    lst = timeobs.sidereal_time('mean', longitude=longitude)
    return lst

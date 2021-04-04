#!/usr/bin/env python

from astropy import units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astroplan import Observer

# For option
from argparse import ArgumentParser

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO)


def get_option():

    """ get options
    """
    argparser = ArgumentParser(fromfile_prefix_chars='@')
    argparser.add_argument('ra', type=str, help='R.A. of the target')
    argparser.add_argument('dec', type=str, help='Dec. of the target')
    argparser.add_argument('time', type=str, help='observation time in UTC')
    argparser.add_argument('-hx', '--hexagonal', type=bool, default=False,
                           help='Ra-Dec is in hexagonal hh:mm:ss.sss dd:mm:ss')
    argparser.add_argument('-s', '--site', type=str, default='subaru',
                           help='Observation site')
#    argparser.add_argument('-e', '--end', type=str, default='2020-01-01 15:00:00',
#                           help='End time. Format is yyyy-mm-dd HH:MM:SS')
#    argparser.add_argument('-dlc', '--drawLearningCurve', type=bool, default=False,
#                           help='Whether to draw learning curve after learning')
    return argparser.parse_args()


def calc_az_el(ra, dec, time, inr=0, pa=0):

    """ Calcurate alt-azimuth from ra-dec
        Atmospheric dispersion is not taken into account

    Parameters
    ----------
    ra : `float`
       R.A. in degree
    dec : `float`
       Dec. in degree
    """

    # Set Observation Site (Subaru)
    tel = EarthLocation.of_site('Subaru')
    tel2 = Observer.at_site("Subaru", timezone="US/Hawaii")
    obs_time = Time(time)

    # Ra-Dec to Az-El (Center)
    coord_cent = SkyCoord(ra, dec, unit=u.deg)
    altaz_cent = coord_cent.transform_to(AltAz(obstime=obs_time,
                                               location=tel))

    # Instrument rotator angle
    paa = tel2.parallactic_angle(obs_time, coord_cent).deg
    lat = tel2.location.lat.deg
    dc = coord_cent.dec.deg
    logging.debug("Subaru Latitude: %s", lat)
    if dc > lat:
        inr = paa + pa
    else:
        inr = paa - pa

    az = altaz_cent.az.deg
    el = altaz_cent.alt.deg

    return az, el, inr


# default
# Usage
# python3 ./LookForStars_mod.py posdata.txt ra_deg dec_deg "yyyy-mm-dd hh:mm:ss" inr_s inr_e 
# date/time is in UTC
# set inr 999 if it needs to calc.
if __name__ == '__main__':

    args = get_option()

    if args.hexagonal:
        ra_s = args.ra.split(":")
        ra = 15. * (float(ra_s[0]) + float(ra_s[1])/60. + float(ra_s[2])/3600.)
        dec_s = args.dec.split(":")
        if float(dec_s[0]) < 0:
            dec = float(dec_s[0]) - float(dec_s[1])/60. - float(dec_s[2])/3600.
        else:
            dec = float(dec_s[0]) + float(dec_s[1])/60. + float(dec_s[2])/3600.
    else:
        ra = float(args.ra)
        dec = float(args.dec)

    """
    iers.IERS_A_URL="ftp://cddis.gsfc.nasa.gov/pub/products/iers/finals2000A.all"
    download_IERS_A()
    """

    # time in UTC
    # format: 2018-01-09 12:12:13'
    az, el, inr = calc_az_el(ra, dec, args.time)

    print(az, el, inr)

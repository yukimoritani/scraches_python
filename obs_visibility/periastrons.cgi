#!/usr/bin/env python

import cgi,cgitb
import datetime,time,os,sys
import math

cgitb.enable()

class Phase:
    def __init__(self, period, t0, p0):
        self.p = period
        self.t = t0
        self.o = p0
    #current phase
    def phase(self, mjd):
        ph = (mjd - self.t) / self.p -self.o
        return ph
    def periastron(self, starti):
        print "Recent Periastrons<br>"
        for i in range(starti, starti+10):
#            print i
            peri = self.t + (i + self.o) * self.p
            print "   %f (%s)<br>"% (peri, calcdate(peri))


def html_head():
    print "Content-type: text/html"
    print
    print """
    <html>
    <head>
    <title>Periastrons</title>
    </head>
    <body>
    """

def html_tail():
    print"""
    </body>
    </html>
    """

def currentmjd():
    now = datetime.datetime.utcnow()
    print "Current time<br>"
    print "%s<br>"% now
    offsety = 0
    offsetm = 0
    if(int(now.month) == 1 or int(now.month) == 2):
         offsety = -1
         offsetm = 12
    mjd = int(365.25 * (float(now.year)+offsety))
    mjd += int((float(now.year)+offsety) / 400.)
    mjd -= int((float(now.year)+offsety) / 100.)
    mjd += int(30.59 * ((float(now.month)+offsetm) - 2.))
    mjd += float(now.day) - 678912
    mjd += (float(now.hour) + float(now.minute) / 60. + float(now.second) / 3600.) /24.
    print "MJD: %f<br>"% mjd
    return mjd


def calcdate(mjd):
    mjd0 = 2400000.5
    c0 = 68569.5
    c1 =36524.25
    c2 =365.25025
    c3 =365.25
    c4 =31
    c5 =30.59
    c6 =11
    a = math.floor(mjd + mjd0 + c0)
    b = math.floor(a/c1)
    c = a - math.floor(b*c1+0.75)
    d = math.floor((c+1)/c2)
    e = c - math.floor(d*c3)+c4
    f = math.floor(e/c5)
    g = mjd + mjd0 + 0.5
    h = e - math.floor(f*c5) + g - math.floor(g);
    i = math.floor(f/c6)
    year = 100.*(b-49)+d+i
    month = f - i*12 + 2
    day= math.floor(h)
    j  = (h-day)*24
    hour = math.floor(j)
    k = (j-hour)*60.
    minute = math.floor(k)
    second = (k-minute)*60
    date = "%04d-%02d-%02d %02d:%02d:%05.2f" % (year, month, day, hour, minute, second)
    return date

def html_phase(object,mjd):
    target = Phase(*object)
    phs = float(target.phase(mjd))
    print "phase = %f  after periastron<br>"% (phs - math.floor(phs))
    start = int(math.floor(phs))
#    print start
    target.periastron(start)
    print "<p>"



def main():
    #ephemeris:period, t0, periastron phase
    a0535 = [110.24, 53398.43, 0.0]
    u0115  = [24.3, 43540.951, 0.0]
    gro1008 = [249.48, 54424.71, 0.0]
    gx304 = [132.5, 55934.5, 0.0]
    hess0632 = [315, 54857.5, 0.967]
    lsi61 = [26.4960, 51057.89, 0.0]
    agl2241 = [60.37, 53243, 0.0]
    mxb0656 = [101.2, 54408, 0.0]
    u1036  = [61,54841.199, 0.0]
    gx0834 = [132.5, 55934.5, 0.0]
    h1145 = [186.5, 42536, 0.0]
    gx302 = [41.182, 55531.63, 0.0]
    s1417 = [42.12, 49713.62, 0.0]
    u0728 = [34.5446, 50365.5, 0.0]
    html_head()
    mjd = currentmjd()
    print "<p>"
    print  "<h4>4U0115+634</h4>"
    html_phase(u0115,mjd)
    print  "<h4>LS I +61 303</h4>"
    html_phase(lsi61,mjd)
    print  "<h4>A0535+262</h4>"
    html_phase(a0535,mjd)
    print  "<h4>HESS J0632+057</h4>"
    html_phase(hess0632,mjd)
    print  "<h4>MXB 0656-072</h4>"
    html_phase(mxb0656,mjd)
    print  "<h4>4U 0728-25 (outburst phase) </h4>"
    html_phase(u0728,mjd)
    print  "<h4>GRO J1008-57</h4>"
    html_phase(gro1008,mjd)
    print  "<h4>4U1036-61</h4>"
    html_phase(u1036,mjd)
    print  "<h4>H1145-619</h4>"
    html_phase(h1145,mjd)
    print  "<h4>GX301-2</h4>"
    html_phase(gx302,mjd)
    print  "<h4>GX304-1</h4>"
    html_phase(gx304,mjd)
    print  "<h4>2S 1417-624</h4>"
    html_phase(s1417,mjd)
    print  "<h4>AGL J2241+4454</h4>"
    html_phase(agl2241,mjd)
    html_tail()

if __name__=='__main__':
    main()

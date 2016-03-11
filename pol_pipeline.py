#!/usr/bin/env python

import os
import sys
import numpy

sirphot="../../reduction/pyIRSF-1.3beta2/sirphot.py"
#pyirsf="../../reduction/pyIRSF-1.3beta2/"
#sys.path.append(pyirsf)
#import sirphot

#listfile="fitslist"
listfile="fitslist.4"
#outj="2sirphot.txt"
#outh="2sirphot.txt"
#outk="2sirphot.txt"
out="2sirphot.txt"

f=open(listfile)
line = f.readlines()
f.close

for l in line:
    #print l
    #sirphot(l)
    os.system("%s %s" % (sirphot, l))
    l2=l.replace(".fits", "_sirphot.txt")
    os.system("mv %s %s" % (out, l2))
    #print l2
    #if l2.find("ja")!=-1:
       #os.rename(outj, l2)
    #   os.system("mv %s %s" % (outj, l2))
    #elif l2.find("ha")!=-1:
       #os.rename(outh, l)
    #   os.system("mv %s %s" % (outh, l2))
    #elif l2.find("ka")!=-1:
    #   #os.rename(outk, l2)
    #   os.system("mv %s %s" % (outk, l2))
    #else:
    #   print("Invalid band.")


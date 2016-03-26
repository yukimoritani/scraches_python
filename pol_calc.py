#!/usr/bin/env python

import os
import sys
import math
import numpy
import re

ERROR=-999.

def PolCalc(inname,posx,posy,expt):
    # zero magnitude: sirphot.py
    zeroj=21.
    zeroh=21.2
    zerok=20.3
    if inname[0]=="j":
        zmag=zeroj
    elif inname[0]=="h":
        zmag=zeroh
    elif inname[0]=="k":
        zmag=zerok
    else:
        zmag=zeroj

    #rotangle
    ang=["00", "22", "45", "67"]
    Iins=[]
    #ret=re.split('[jhk]a','ajabhab',1)
    #print ret
    #print inname
    for a in ang:
        str1=re.findall('[jhk]a',inname)
        str2=re.split('[jhk]a',inname)
        #print str2
        tinname=str2[0] + str1[0] + a + str2[1]
        Iins.extend(CalcCount(tinname,posx,posy,zmag,expt))
    #print Iins
    Stok=Stokes=CalcStokes(Iins)
    return Stok

def CalcCount(inname,posx,poxy,zmag,expt):
    f=open(inname)
    line=f.readlines()
    f.close

    for l in line:
        ll=l.split()
        # x,y,flux,mag,magerr 
        flag=0
        if math.fabs(float(ll[0])-posx)<5 and math.fabs(float(ll[1])-posy)<5 :
            I = pow(10., (zmag-float(ll[3]))/2.5) * expt
            Ierr = float(ll[4]) * I / 1.0857
            #print inname
            flag=1
            break
    #print I,Ierr
    if flag==0 :
            I=ERROR
            Ierr=ERROR
    return I,Ierr

def CalcStokes(Iins):
# Ins: I00 Ie00 I22 Ie22 I45 Ie45 I67 Ie67
    if ERROR in Iins :
        sI=ERROR
        sIerr=ERROR
        sQ=ERROR
        sQerr=ERROR
        sU=ERROR
        sUerr=ERROR
    else:
        sI = sum(Iins[0::2])/2
        tmp=[pow(x,2.) for x in Iins[1::2]]
        #print tmp
        sIerr = math.sqrt(sum(tmp)) /2
        #sIerr = math.sqrt(sum(pow(Iins[1::2],2.))) /2
        sQ = Iins[4]-Iins[0]
        sQerr = math.sqrt(pow(Iins[5],2.)+pow(Iins[1],2.))
        sU = Iins[6]-Iins[2]
        sUerr = math.sqrt(pow(Iins[7],2.)+pow(Iins[3],2.))
    print "%lf %lf %lf %lf %lf %lf" % (sI,sIerr,sQ,sQerr,sU,sUerr),
    return  sI,sIerr,sQ,sQerr,sU,sUerr


if __name__ == '__main__':
    posx=float(sys.argv[3])
    posy=float(sys.argv[4])
    expt=float(sys.argv[2])
    #fin=open(sys.argv[1])
    #fline=fin.readlines()
    #fin.close
    #for inname in fline:
    Sins=[] 
    Sins.extend(PolCalc(sys.argv[1],posx,posy,expt))
    #Sins.extend(PolCalc(inname.rstrip("\n"),posx,posy,expt))
    # sI,sIerr,sQ,sQerr,sU,sUerr
    if ERROR in Sins : 
        P=ERROR
        Perr=ERROR
    else :
        PI=math.sqrt(pow(Sins[2],2.)+pow(Sins[4],2.))
        PIerr=math.sqrt(pow(Sins[2],2.)*pow(Sins[3],2.)+pow(Sins[4],2.)*pow(Sins[5],2.))/PI
        P=PI/Sins[0]
        Perr=math.sqrt(pow(PIerr/Sins[0],2.)+pow(P*Sins[1]/Sins[0],2.))
    print "%lf %lf" % (P,Perr)

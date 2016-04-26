#!/usr/bin/env python

import os
import sys
import math as mt
import numpy as np
import Gnuplot

## angle: radian
def MakeData(ecc,inc,arg,node,major):
    minor=major*mt.sqrt(1-ecc*ecc);

    ### make matrix to tranxfer rot_co. to iner_co.
    rotp=np.array([[mt.cos(arg),-1.*mt.sin(arg),0.],[mt.sin(arg),mt.cos(arg),0.],[0.,0.,1.]])
    roti=np.array([[1.,0.,0.],[0.,mt.cos(inc),-1*mt.sin(inc)],[0.,mt.sin(inc),mt.cos(inc)]])
    rota=np.array([[mt.cos(node),-1.*mt.sin(node),0],[mt.sin(node),mt.cos(node),0],[0,0,1]])

    trans=np.matmul(rota,np.matmul(roti,rotp))
    #trans=np.matmul(rota,rotp)

    f=open("data.dat","w")
    for t in np.arange(0.,1.,0.005):
        phase=t*2*mt.pi
        obj=np.array([[major*(mt.cos(phase)-ecc)], [minor*mt.sin(phase)],[0.]])
        objrot=np.matmul(trans,obj)

        #print objrot[0][0],objrot[1][0],objrot[2][0],t
        f.write("%e %e %e %lf\n" % (objrot[0][0],objrot[1][0],objrot[2][0],t))

def PlotEllipse(arg,inc,ecc,mang,node):
    g=Gnuplot.Gnuplot()
    g('set term postscript eps enhanced 20"')
    cmd="set output \"out_"+ ecc + "_" + mang + "_" + node + ".eps\""
    g(cmd)
    cmd="set view " + inc + "," + arg
    g(cmd)
    g('unset border')
    g('unset tics')
    g('set key off')
    g('set parametric')
    g('set xrange [-1.5:1.5]')
    g('set yrange [-1.5:1.5]')
    g('set zrange [-1.5:1.5]')
    g('sp "data.dat" w l lc rgb "red", 0.01*cos(u)*cos(v),0.01*sin(u)*cos(v),0.01*sin(v)')
    g('unset parametric')
    g('set term x11')
    g('q')


if __name__ == '__main__':
    d2r=mt.pi/180.
    ## observer: argument:+90
    o_i="60."
    ### argument: 45 deg
    o_a="130"

    f=open(sys.argv[1],"r")
    line=f.readlines()
    f.close
    for l in line:
        ll=l.split()
        #### file: ecc,i,node
        major=1.
        arg=0.
        MakeData(float(ll[0]),float(ll[1])*d2r,arg*d2r,float(ll[2])*d2r,major)
        PlotEllipse(o_a,o_i,ll[0],ll[1],ll[2])

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 05 14:47:23 2014

@author: soutobias
"""

import numpy as np
from numpy import *
import argosqc as qc

def arredondar(num):
    return float( '%.0f' % ( num ) )

def tempos(boias):

    lines = open('anemometros.txt', 'rb')
    
    boia2,epocaini,epocafim,anemo=[],[],[],[]
    for line in lines:
        dataline = line.strip()
        columns = dataline.split()
        if columns[0].decode('ascii')==boias:
            epocaini.append(columns[1].decode('ascii'))
            epocafim.append(columns[2].decode('ascii'))
            anemo.append(columns[3].decode('ascii'))
    
    anemomet=[epocaini,epocafim,anemo]

    return anemomet

def qualitycontrol(Epoch,data,Wdir1,Wspd1,Gust1,Wdir2,Wspd2,Gust2,Wvht,Wmax,Dpd,Mwd,Pres,Humi,Atmp,Wtmp,Dewp,Cvel1,Cdir1,Cvel2,Cdir2,Cvel3,Cdir3,Battery,Lat,boias):

    Wdir1flag,Wspd1flag,Gust1flag,Wdir2flag,Wspd2flag=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    Gust2flag,Wvhtflag,Wmaxflag,Dpdflag,Mwdflag=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    Presflag,Humiflag,Atmpflag,Wtmpflag,Dewpflag=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    Cvel1flag,Cdir1flag,Cvel2flag,Cdir2flag,Cvel3flag=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    Cdir3flag=[0]*len(Epoch)

    Wdir1flagid,Wspd1flagid,Gust1flagid,Wdir2flagid,Wspd2flagid=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    Gust2flagid,Wvhtflagid,Wmaxflagid,Dpdflagid,Mwdflagid=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    Presflagid,Humiflagid,Atmpflagid,Wtmpflagid,Dewpflagid=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    Cvel1flagid,Cdir1flagid,Cvel2flagid,Cdir2flagid,Cvel3flagid=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    Cdir3flagid=[0]*len(Epoch)


    (rWvht,rDpd,rMwd,rWspd,rWdir,rGust,rAtmp,rPres,rDewp,rWtmp,rApd,rHumi,rCvel,rCdir, sigmaWvht,sigmaPres,sigmaAtmp,sigmaWspd,sigmaWtmp,sigmaHumi,misHumi1,misHumi2,misCvel,misCvel1,misCdir,misDewp,misAtmp,misWtmp,rWmax)=qc.valoresargos()

    (r1Wvht,r1Dpd,r1Wspd,r1Gust,r1Atmp,r1Pres,r1Dewp,r1Wtmp,r1Apd,r1Cvel,r1Wmax,r2Atmp,r3Atmp)=qc.valoresclima()
    ##############################################
    #RUN THE QC CHECKS
    ##############################################
    
    #time check
    (timeflag) = qc.timecheck(Epoch)

    #Missing value check
    (Wdir1flag,Wdir1flagid)=qc.misvaluecheck(Epoch,Wdir1,Wdir1flag,-9999,Wdir1flagid)
    (Wspd1flag,Wspd1flagid)=qc.misvaluecheck(Epoch,Wspd1,Wspd1flag,-9999,Wspd1flagid)
    (Gust1flag,Gust1flagid)=qc.misvaluecheck(Epoch,Gust1,Gust1flag,-9999,Gust1flagid)
    (Wdir2flag,Wdir2flagid)=qc.misvaluecheck(Epoch,Wdir2,Wdir2flag,-9999,Wdir2flagid)
    (Wspd2flag,Wspd2flagid)=qc.misvaluecheck(Epoch,Wspd2,Wspd2flag,-9999,Wspd2flagid)
    (Gust2flag,Gust2flagid)=qc.misvaluecheck(Epoch,Gust2,Gust2flag,-9999,Gust2flagid)
    (Mwdflag,Mwdflagid)=qc.misvaluecheck(Epoch,Mwd,Mwdflag,-9999,Mwdflagid)
    (Wvhtflag,Wvhtflagid)=qc.misvaluecheck(Epoch,Wvht,Wvhtflag,-9999,Wvhtflagid)
    (Wmaxflag,Wmaxflagid)=qc.misvaluecheck(Epoch,Wmax,Wmaxflag,-9999,Wmaxflagid)
    (Dpdflag,Dpdflagid)=qc.misvaluecheck(Epoch,Dpd,Dpdflag,-9999,Dpdflagid)
    (Presflag,Presflagid)=qc.misvaluecheck(Epoch,Pres,Presflag,-9999,Presflagid)
    (Dewpflag,Dewpflagid)=qc.misvaluecheck(Epoch,Dewp,Dewpflag,misDewp,Dewpflagid)
    (Atmpflag,Atmpflagid)=qc.misvaluecheck(Epoch,Atmp,Atmpflag,misAtmp,Atmpflagid)
    (Wtmpflag,Wtmpflagid)=qc.misvaluecheck(Epoch,Wtmp,Wtmpflag,misWtmp,Wtmpflagid)
    (Cvel1flag,Cvel1flagid)=qc.misvaluecheck(Epoch,Cvel1,Cvel1flag,misCvel,Cvel1flagid)
    (Cvel1flag,Cvel1flagid)=qc.misvaluecheck(Epoch,Cvel1,Cvel1flag,misCvel1,Cvel1flagid)
    (Cdir1flag,Cdir1flagid)=qc.misvaluecheck(Epoch,Cdir1,Cdir1flag,misCdir,Cdir1flagid)
    (Cvel2flag,Cvel2flagid)=qc.misvaluecheck(Epoch,Cvel2,Cvel2flag,misCvel,Cvel2flagid)
    (Cvel2flag,Cvel2flagid)=qc.misvaluecheck(Epoch,Cvel2,Cvel2flag,misCvel1,Cvel2flagid)
    (Cdir2flag,Cdir2flagid)=qc.misvaluecheck(Epoch,Cdir2,Cdir2flag,misCdir,Cdir2flagid)
    (Cvel3flag,Cvel3flagid)=qc.misvaluecheck(Epoch,Cvel3,Cvel3flag,misCvel,Cvel3flagid)
    (Cvel3flag,Cvel3flagid)=qc.misvaluecheck(Epoch,Cvel3,Cvel3flag,misCvel1,Cvel3flagid)
    (Cdir3flag,Cdir3flagid)=qc.misvaluecheck(Epoch,Cdir3,Cdir3flag,misCdir,Cdir3flagid)
    (Humiflag,Humiflagid)=qc.misvaluecheck(Epoch,Humi,Humiflag,misHumi1,Humiflagid)
    (Humiflag,Humiflagid)=qc.misvaluecheck(Epoch,Humi,Humiflag,misHumi2,Humiflagid)

    (Dewpflag,Dewpflagid)=qc.misvaluecheck(Epoch,Dewp,Dewpflag,-9999,Dewpflagid)
    (Atmpflag,Atmpflagid)=qc.misvaluecheck(Epoch,Atmp,Atmpflag,-9999,Atmpflagid)
    (Wtmpflag,Wtmpflagid)=qc.misvaluecheck(Epoch,Wtmp,Wtmpflag,-9999,Wtmpflagid)
    (Cvel1flag,Cvel1flagid)=qc.misvaluecheck(Epoch,Cvel1,Cvel1flag,-9999,Cvel1flagid)
    (Cdir1flag,Cdir1flagid)=qc.misvaluecheck(Epoch,Cdir1,Cdir1flag,-9999,Cdir1flagid)
    (Cvel2flag,Cvel2flagid)=qc.misvaluecheck(Epoch,Cvel2,Cvel2flag,-9999,Cvel2flagid)
    (Cdir2flag,Cdir2flagid)=qc.misvaluecheck(Epoch,Cdir2,Cdir2flag,-9999,Cdir2flagid)
    (Cvel3flag,Cvel3flagid)=qc.misvaluecheck(Epoch,Cvel3,Cvel3flag,-9999,Cvel3flagid)
    (Cdir3flag,Cdir3flagid)=qc.misvaluecheck(Epoch,Cdir3,Cdir3flag,-9999,Cdir3flagid)
    (Humiflag,Humiflagid)=qc.misvaluecheck(Epoch,Humi,Humiflag,-9999,Humiflagid)
    
    #Coarse Range check
    (Wvhtflag,Wvhtflagid) = qc.rangecheck(Epoch, Wvht,rWvht,Wvhtflag,Wvhtflagid)
    (Wmaxflag,Wmaxflagid) = qc.rangecheck(Epoch, Wmax,rWmax,Wmaxflag,Wmaxflagid)
    (Dpdflag,Dpdflagid) = qc.rangecheck(Epoch, Dpd,rDpd,Dpdflag,Dpdflagid)
    (Mwdflag,Mwdflagid) = qc.rangecheck(Epoch,Mwd,rMwd,Mwdflag,Mwdflagid)
    
    (Humiflag,Humiflagid) = qc.rangecheck(Epoch, Humi,rHumi,Humiflag,Humiflagid)
    (Presflag,Presflagid) = qc.rangecheck(Epoch, Pres,rPres,Presflag,Presflagid)
    (Dewpflag,Dewpflagid) = qc.rangecheck(Epoch, Dewp,rDewp,Dewpflag,Dewpflagid)
    (Atmpflag,Atmpflagid) = qc.rangecheck(Epoch,Atmp,rAtmp,Atmpflag,Atmpflagid)
    
    (Wspd1flag,Wspd1flagid) = qc.rangecheck(Epoch, Wspd1,rWspd,Wspd1flag,Wspd1flagid)
    (Wdir1flag,Wdir1flagid) = qc.rangecheck(Epoch, Wdir1,rWdir,Wdir1flag,Wdir1flagid)
    (Gust1flag,Gust1flagid) = qc.rangecheck(Epoch, Gust1,rGust,Gust1flag,Gust1flagid)
    (Wspd2flag,Wspd2flagid) = qc.rangecheck(Epoch, Wspd2,rWspd,Wspd2flag,Wspd2flagid)
    (Wdir2flag,Wdir2flagid) = qc.rangecheck(Epoch, Wdir2,rWdir,Wdir2flag,Wdir2flagid)
    (Gust2flag,Gust2flagid) = qc.rangecheck(Epoch, Gust2,rGust,Gust2flag,Gust2flagid)
    
    (Wtmpflag,Wtmpflagid) = qc.rangecheck(Epoch,Wtmp,rWtmp,Wtmpflag,Wtmpflagid)
    (Cvel1flag,Cvel1flagid) = qc.rangecheck(Epoch, Cvel1,rCvel,Cvel1flag,Cvel1flagid)
    (Cdir1flag,Cdir1flagid) = qc.rangecheck(Epoch, Cdir1,rCdir,Cdir1flag,Cdir1flagid)
    (Cvel2flag,Cvel2flagid) = qc.rangecheck(Epoch, Cvel2,rCvel,Cvel2flag,Cvel2flagid)
    (Cdir2flag,Cdir2flagid) = qc.rangecheck(Epoch, Cdir2,rCdir,Cdir2flag,Cdir2flagid)
    (Cvel3flag,Cvel3flagid) = qc.rangecheck(Epoch, Cvel3,rCvel,Cvel3flag,Cvel3flagid)
    (Cdir3flag,Cdir3flagid) = qc.rangecheck(Epoch, Cdir3,rCdir,Cdir3flag,Cdir3flagid)

    #Soft Range check

    (Wvhtflag,Wvhtflagid) = qc.rangecheckclima(Epoch, Wvht,r1Wvht,Wvhtflag,Wvhtflagid)
    (Wmaxflag,Wmaxflagid) = qc.rangecheckclima(Epoch, Wmax,r1Wmax,Wmaxflag,Wmaxflagid)
    (Dpdflag,Dpdflagid) = qc.rangecheckclima(Epoch, Dpd,r1Dpd,Dpdflag,Dpdflagid)

    (Presflag,Presflagid) = qc.rangecheckclima(Epoch, Pres,r1Pres,Presflag,Presflagid)
    (Dewpflag,Dewpflagid) = qc.rangecheckclima(Epoch, Dewp,r1Dewp,Dewpflag,Dewpflagid)

    if mean(Lat)<=-27:
        (Atmpflag,Atmpflagid) = qc.rangecheckclima(Epoch,Atmp,r1Atmp,Atmpflag,Atmpflagid)
    elif mean(Lat)>-27 and mean(Lat)<=-18: 
        (Atmpflag,Atmpflagid) = qc.rangecheckclima(Epoch,Atmp,r2Atmp,Atmpflag,Atmpflagid)
    else:
        (Atmpflag,Atmpflagid) = qc.rangecheckclima(Epoch,Atmp,r3Atmp,Atmpflag,Atmpflagid)
    
    (Wspd1flag,Wspd1flagid) = qc.rangecheckclima(Epoch, Wspd1,r1Wspd,Wspd1flag,Wspd1flagid)
    (Gust1flag,Gust1flagid) = qc.rangecheckclima(Epoch, Gust1,r1Gust,Gust1flag,Gust1flagid)
    (Wspd2flag,Wspd2flagid) = qc.rangecheckclima(Epoch, Wspd2,r1Wspd,Wspd2flag,Wspd2flagid)
    (Gust2flag,Gust2flagid) = qc.rangecheckclima(Epoch, Gust2,r1Gust,Gust2flag,Gust2flagid)
    
    (Wtmpflag,Wtmpflagid) = qc.rangecheckclima(Epoch,Wtmp,r1Wtmp,Wtmpflag,Wtmpflagid)
    (Cvel1flag,Cvel1flagid) = qc.rangecheckclima(Epoch, Cvel1,r1Cvel,Cvel1flag,Cvel1flagid)
    (Cvel2flag,Cvel2flagid) = qc.rangecheckclima(Epoch, Cvel2,r1Cvel,Cvel2flag,Cvel2flagid)
    (Cvel3flag,Cvel3flagid) = qc.rangecheckclima(Epoch, Cvel3,r1Cvel,Cvel3flag,Cvel3flagid)

    #Significance wave height vs Max wave height
    (Wvhtflag,Wmaxflag,Wvhtflagid,Wmaxflagid) = qc.wvhtwmaxcheck(Epoch,Wvht,Wmax,Wvhtflag,Wmaxflag,Wvhtflagid,Wmaxflagid)
    
    #Wind speed vs Gust speed
    (Wspd1flag,Gust1flag,Wspd1flagid,Gust1flagid) = qc.windspeedgustcheck(Epoch,Wspd1,Gust1,Wspd1flag,Gust1flag,Wspd1flagid,Gust1flagid)
    (Wspd2flag,Gust2flag,Wspd2flagid,Gust2flagid) = qc.windspeedgustcheck(Epoch,Wspd2,Gust2,Wspd2flag,Gust2flag,Wspd2flagid,Gust2flagid)
   
    #Dew point and Air temperature check
    (Dewpflag,Dewpflagid) = qc.dewpatmpcheck(Epoch,Dewp,Atmp,Dewpflag,Atmpflag,Dewpflagid)
    
    #Check of effects of battery voltage in sensors    
    (Presflag,Presflagid) = qc.batsensorcheck(Epoch,Battery,Pres,Presflag,Presflagid)    
    
    #Stucksensorcheck
    (Wvhtflag,Wvhtflagid) = qc.stucksensorcheck(Epoch, Wvht,Wvhtflag,7,Wvhtflagid)
    (Wmaxflag,Wmaxflagid) = qc.stucksensorcheck(Epoch, Wmax,Wmaxflag,7,Wmaxflagid)
    
    (Humiflag,Humiflagid) = qc.stucksensorcheck(Epoch, Humi,Humiflag,7,Humiflagid)
    (Presflag,Presflagid) = qc.stucksensorcheck(Epoch, Pres,Presflag,7,Presflagid)
    (Dewpflag,Dewpflagid) = qc.stucksensorcheck(Epoch, Dewp,Dewpflag,7,Dewpflagid)
    (Atmpflag,Atmpflagid) = qc.stucksensorcheck(Epoch,Atmp,Atmpflag,7,Atmpflagid)
    
    (Wspd1flag,Wspd1flagid) = qc.stucksensorcheck(Epoch, Wspd1,Wspd1flag,7,Wspd1flagid)
    (Wdir1flag,Wdir1flagid) = qc.stucksensorcheck(Epoch, Wdir1,Wdir1flag,7,Wdir1flagid)
    (Gust1flag,Gust1flagid) = qc.stucksensorcheck(Epoch, Gust1,Gust1flag,7,Gust1flagid)
    (Wspd2flag,Wspd2flagid) = qc.stucksensorcheck(Epoch, Wspd2,Wspd2flag,7,Wspd2flagid)
    (Wdir2flag,Wdir2flagid) = qc.stucksensorcheck(Epoch, Wdir2,Wdir2flag,7,Wdir2flagid)
    (Gust2flag,Gust2flagid) = qc.stucksensorcheck(Epoch, Gust2,Gust2flag,7,Gust2flagid)
    
    (Wtmpflag,Wtmpflagid) = qc.stucksensorcheck(Epoch,Wtmp,Wtmpflag,7,Wtmpflagid)
    (Cvel1flag,Cvel1flagid) = qc.stucksensorcheck(Epoch, Cvel1,Cvel1flag,7,Cvel1flagid)
    (Cdir1flag,Cdir1flagid) = qc.stucksensorcheck(Epoch, Cdir1,Cdir1flag,7,Cdir1flagid)
    (Cvel2flag,Cvel2flagid) = qc.stucksensorcheck(Epoch, Cvel2,Cvel2flag,7,Cvel2flagid)
    (Cdir2flag,Cdir2flagid) = qc.stucksensorcheck(Epoch, Cdir2,Cdir2flag,7,Cdir2flagid)
    (Cvel3flag,Cvel3flagid) = qc.stucksensorcheck(Epoch, Cvel3,Cvel3flag,7,Cvel3flagid)
    (Cdir3flag,Cdir3flagid) = qc.stucksensorcheck(Epoch, Cdir3,Cdir3flag,7,Cdir3flagid)

    anemomet=tempos(boias)

    #related measurement check
    (Wdirflag,Wspdflag,Gustflag,Wdir,Wspd,Gust,Wdirflagid,Wspdflagid,Gustflagid) = qc.relatedmeascheck4(Epoch,Wdir1,Wspd1,Gust1,Wdir2,Wspd2,Gust2,Wspd1flag, Wdir1flag,Gust1flag,Wspd2flag, Wdir2flag,Gust2flag,Wdir1flagid,Wspd1flagid,Gust1flagid,Wdir2flagid,Wspd2flagid,Gust2flagid,anemomet)
    #Time continuity check
    (Wvhtflag,Wvhtflagid) = qc.tcontinuitycheck(Epoch, Wvht,Wvhtflag,sigmaWvht,Wvhtflagid,1)
    (Humiflag,Humiflagid) = qc.tcontinuitycheck(Epoch, Humi,Humiflag,sigmaHumi,Humiflagid,1)
    (Presflag,Presflagid) = qc.tcontinuitycheck(Epoch, Pres,Presflag,sigmaPres,Presflagid,1)
    (Atmpflag,Atmpflagid) = qc.tcontinuitycheck(Epoch,Atmp,Atmpflag,sigmaAtmp,Atmpflagid,1)
    (Wspdflag,Wspdflagid) = qc.tcontinuitycheck(Epoch, Wspd,Wspdflag,sigmaWspd,Wspdflagid,1)    
    (Wtmpflag,Wtmpflagid) = qc.tcontinuitycheck(Epoch,Wtmp,Wtmpflag,sigmaWtmp,Wtmpflagid,1)


    #Frontal passage exception for time continuity
    (Atmpflag,Atmpflagid)=qc.frontexcepcheck1(Epoch,Wdir,Wdirflag,Atmpflag,Atmpflagid)
#    (Wdirflag,Wdirflagid)=qc.frontexcepcheck2(Epoch,Wdir,Wdirflag,Atmpflag,Atmpflagid)

    (Atmpflag,Atmpflagid)=qc.frontexcepcheck3(Epoch,Wspd,Atmp,Wspdflag,Atmpflag,Atmpflagid)
    (Wspdflag,Wspdflagid)=qc.frontexcepcheck4(Epoch,Pres,Presflag,Wdirflag,Wdirflagid)
    
    (Presflag,Presflagid)=qc.frontexcepcheck5(Epoch,Pres,Presflag,Presflagid)
    (Wvhtflag,Wvhtflagid)=qc.frontexcepcheck6(Epoch,Wspd,Wspdflag,Wvhtflagid,Wvhtflag)

    for i in range(len(Cvel1)):
        if Cvel1flag[i]==4 and Cdir1flag[i]!=4:
            Cdir1flag[i]=4
            Cdir1flagid[i]='12'

        if Cvel1flag[i]!=4 and Cdir1flag[i]==4:
            Cvel1flag[i]=4
            Cvel1flagid[i]='12'

        if Cvel2flag[i]==4 and Cdir2flag[i]!=4:
            Cdir2flag[i]=4
            Cdir2flagid[i]='12'

        if Cvel2flag[i]!=4 and Cdir2flag[i]==4:
            Cvel2flag[i]=4
            Cvel2flagid[i]='12'

        if Cvel3flag[i]==4 and Cdir3flag[i]!=4:
            Cdir3flag[i]=4
            Cdir3flagid[i]='12'

        if Cvel3flag[i]!=4 and Cdir3flag[i]==4:
            Cvel3flag[i]=4
            Cvel3flagid[i]='12'

        if Gustflag[i]!=4 and Wspdflag[i]==4 and Wdirflag[i]!=4:
            Gustflag[i]=4
            Wdirflag[i]=4
            Gustflagid[i]='12'
            Wdirflagid[i]='12'
            
        if Gustflag[i]==4 and Wspdflag[i]!=4 and Wdirflag[i]!=4:
            Wspdflag[i]=4
            Wdirflag[i]=4
            Wspdflagid[i]='12'
            Wdirflagid[i]='12'

        if Gustflag[i]!=4 and Wspdflag[i]!=4 and Wdirflag[i]==4:
            Gustflag[i]=4
            Wspdflag[i]=4
            Gustflagid[i]='12'
            Wspdflagid[i]='12'

        if Gustflag[i]==4 and Wspdflag[i]==4 and Wdirflag[i]!=4:
            Wdirflag[i]=4
            Wdirflagid[i]='12'

        if Gustflag[i]!=4 and Wspdflag[i]==4 and Wdirflag[i]==4:
            Gustflag[i]=4
            Gustflagid[i]='12'

        if Gustflag[i]==4 and Wspdflag[i]!=4 and Wdirflag[i]==4:
            Wspdflag[i]=4
            Wspdflagid[i]='12'



    flag=np.array([Wdirflag,Wspdflag,Gustflag,Wvhtflag,Wmaxflag,Dpdflag,Mwdflag,Presflag,Humiflag,Atmpflag,Wtmpflag,Dewpflag,Cvel1flag,Cdir1flag,Cvel2flag,Cdir2flag,Cvel3flag,Cdir3flag])
    flagid=np.array([Wdirflagid,Wspdflagid,Gustflagid,Wvhtflagid,Wmaxflagid,Dpdflagid,Mwdflagid,Presflagid,Humiflagid,Atmpflagid,Wtmpflagid,Dewpflagid,Cvel1flagid,Cdir1flagid,Cvel2flagid,Cdir2flagid,Cvel3flagid,Cdir3flagid])

    return Wspd,Wdir,Gust,flag,flagid


def qualitycontrol_adcp(Epoch,cvel1,cdir1,cvel2,cdir2,cvel3,cdir3,cvel4,cdir4,cvel5,cdir5,cvel6,cdir6,cvel7,cdir7,cvel8,cdir8,cvel9,cdir9,cvel10,cdir10,cvel11,cdir11,cvel12,cdir12,cvel13,cdir13,cvel14,cdir14,cvel15,cdir15,cvel16,cdir16,cvel17,cdir17,cvel18,cdir18,cvel19,cdir19,cvel20,cdir20):

    cvel1flag,cdir1flag,cvel2flag,cdir2flag,cvel3flag,cdir3flag,cvel4flag,cdir4flag=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    cvel5flag,cdir5flag,cvel6flag,cdir6flag,cvel7flag,cdir7flag,cvel8flag,cdir8flag=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    cvel9flag,cdir9flag,cvel10flag,cdir10flag,cvel11flag,cdir11flag,cvel12flag,cdir12flag=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    cvel13flag,cdir13flag,cvel14flag,cdir14flag,cvel15flag,cdir15flag,cvel16flag,cdir16flag=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    cvel17flag,cdir17flag,cvel18flag,cdir18flag,cvel19flag,cdir19flag,cvel20flag,cdir20flag=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)

    cvel1flagid,cdir1flagid,cvel2flagid,cdir2flagid,cvel3flagid,cdir3flagid,cvel4flagid,cdir4flagid=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    cvel5flagid,cdir5flagid,cvel6flagid,cdir6flagid,cvel7flagid,cdir7flagid,cvel8flagid,cdir8flagid=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    cvel9flagid,cdir9flagid,cvel10flagid,cdir10flagid,cvel11flagid,cdir11flagid,cvel12flagid,cdir12flagid=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    cvel13flagid,cdir13flagid,cvel14flagid,cdir14flagid,cvel15flagid,cdir15flagid,cvel16flagid,cdir16flagid=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)
    cvel17flagid,cdir17flagid,cvel18flagid,cdir18flagid,cvel19flagid,cdir19flagid,cvel20flagid,cdir20flagid=[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch),[0]*len(Epoch)

    
    (rWvht,rDpd,rMwd,rWspd,rWdir,rGust,rAtmp,rPres,rDewp,rWtmp,rApd,rHumi,rCvel,rcdir, sigmaWvht,sigmaPres,sigmaAtmp,sigmaWspd,sigmaWtmp,sigmaHumi,misHumi1,misHumi2,misCvel,misCvel1,miscdir,misDewp,misAtmp,misWtmp,rWmax)=qc.valoresargos()

    (r1Wvht,r1Dpd,r1Wspd,r1Gust,r1Atmp,r1Pres,r1Dewp,r1Wtmp,r1Apd,r1Cvel,r1Wmax,r2Atmp,r3Atmp)=qc.valoresclima()
    ##############################################
    #RUN THE QC CHECKS
    ##############################################
    print('inicio testes')
    #Missing value check

    (cvel1flag,cvel1flagid)=qc.misvaluecheck(Epoch,cvel1,cvel1flag,-9999,cvel1flagid)
    (cdir1flag,cdir1flagid)=qc.misvaluecheck(Epoch,cdir1,cdir1flag,-9999,cdir1flagid)

    (cvel2flag,cvel2flagid)=qc.misvaluecheck(Epoch,cvel2,cvel2flag,-9999,cvel2flagid)
    (cdir2flag,cdir2flagid)=qc.misvaluecheck(Epoch,cdir2,cdir2flag,-9999,cdir2flagid)

    (cvel3flag,cvel3flagid)=qc.misvaluecheck(Epoch,cvel3,cvel3flag,-9999,cvel3flagid)
    (cdir3flag,cdir3flagid)=qc.misvaluecheck(Epoch,cdir3,cdir3flag,-9999,cdir3flagid)

    (cvel4flag,cvel4flagid)=qc.misvaluecheck(Epoch,cvel4,cvel4flag,-9999,cvel4flagid)
    (cdir4flag,cdir4flagid)=qc.misvaluecheck(Epoch,cdir4,cdir4flag,-9999,cdir4flagid)

    (cvel5flag,cvel5flagid)=qc.misvaluecheck(Epoch,cvel5,cvel5flag,-9999,cvel5flagid)
    (cdir5flag,cdir5flagid)=qc.misvaluecheck(Epoch,cdir5,cdir5flag,-9999,cdir5flagid)
    
    (cvel6flag,cvel6flagid)=qc.misvaluecheck(Epoch,cvel6,cvel6flag,-9999,cvel6flagid)
    (cdir6flag,cdir6flagid)=qc.misvaluecheck(Epoch,cdir6,cdir6flag,-9999,cdir6flagid)

    (cvel7flag,cvel7flagid)=qc.misvaluecheck(Epoch,cvel7,cvel7flag,-9999,cvel7flagid)
    (cdir7flag,cdir7flagid)=qc.misvaluecheck(Epoch,cdir7,cdir7flag,-9999,cdir7flagid)

    (cvel8flag,cvel8flagid)=qc.misvaluecheck(Epoch,cvel8,cvel8flag,-9999,cvel8flagid)
    (cdir8flag,cdir8flagid)=qc.misvaluecheck(Epoch,cdir8,cdir8flag,-9999,cdir8flagid)

    (cvel9flag,cvel9flagid)=qc.misvaluecheck(Epoch,cvel9,cvel9flag,-9999,cvel9flagid)
    (cdir9flag,cdir9flagid)=qc.misvaluecheck(Epoch,cdir9,cdir9flag,-9999,cdir9flagid)

    (cvel10flag,cvel10flagid)=qc.misvaluecheck(Epoch,cvel10,cvel10flag,-9999,cvel10flagid)
    (cdir10flag,cdir10flagid)=qc.misvaluecheck(Epoch,cdir10,cdir10flag,-9999,cdir10flagid)

    (cvel11flag,cvel11flagid)=qc.misvaluecheck(Epoch,cvel11,cvel11flag,-9999,cvel11flagid)
    (cdir11flag,cdir11flagid)=qc.misvaluecheck(Epoch,cdir11,cdir11flag,-9999,cdir11flagid)

    (cvel12flag,cvel12flagid)=qc.misvaluecheck(Epoch,cvel12,cvel12flag,-9999,cvel12flagid)
    (cdir12flag,cdir12flagid)=qc.misvaluecheck(Epoch,cdir12,cdir12flag,-9999,cdir12flagid)

    (cvel13flag,cvel13flagid)=qc.misvaluecheck(Epoch,cvel13,cvel13flag,-9999,cvel13flagid)
    (cdir13flag,cdir13flagid)=qc.misvaluecheck(Epoch,cdir13,cdir13flag,-9999,cdir13flagid)

    (cvel14flag,cvel14flagid)=qc.misvaluecheck(Epoch,cvel14,cvel14flag,-9999,cvel14flagid)
    (cdir14flag,cdir14flagid)=qc.misvaluecheck(Epoch,cdir14,cdir14flag,-9999,cdir14flagid)

    (cvel15flag,cvel15flagid)=qc.misvaluecheck(Epoch,cvel15,cvel15flag,-9999,cvel15flagid)
    (cdir15flag,cdir15flagid)=qc.misvaluecheck(Epoch,cdir15,cdir15flag,-9999,cdir15flagid)

    (cvel16flag,cvel16flagid)=qc.misvaluecheck(Epoch,cvel16,cvel16flag,-9999,cvel16flagid)
    (cdir16flag,cdir16flagid)=qc.misvaluecheck(Epoch,cdir16,cdir16flag,-9999,cdir16flagid)

    (cvel17flag,cvel17flagid)=qc.misvaluecheck(Epoch,cvel17,cvel17flag,-9999,cvel17flagid)
    (cdir17flag,cdir17flagid)=qc.misvaluecheck(Epoch,cdir17,cdir17flag,-9999,cdir17flagid)

    (cvel18flag,cvel18flagid)=qc.misvaluecheck(Epoch,cvel18,cvel18flag,-9999,cvel18flagid)
    (cdir18flag,cdir18flagid)=qc.misvaluecheck(Epoch,cdir18,cdir18flag,-9999,cdir18flagid)

    (cvel19flag,cvel19flagid)=qc.misvaluecheck(Epoch,cvel19,cvel19flag,-9999,cvel19flagid)
    (cdir19flag,cdir19flagid)=qc.misvaluecheck(Epoch,cdir19,cdir19flag,-9999,cdir19flagid)

    (cvel20flag,cvel20flagid)=qc.misvaluecheck(Epoch,cvel20,cvel20flag,-9999,cvel20flagid)
    (cdir20flag,cdir20flagid)=qc.misvaluecheck(Epoch,cdir20,cdir20flag,-9999,cdir20flagid)

    #Coarse Range check
    (cvel1flag,cvel1flagid) = qc.rangecheck(Epoch, cvel1,[-5000,5000],cvel1flag,cvel1flagid)
    (cdir1flag,cdir1flagid) = qc.rangecheck(Epoch, cdir1,[0,360],cdir1flag,cdir1flagid)

    (cvel2flag,cvel2flagid) = qc.rangecheck(Epoch, cvel2,[-5000,5000],cvel2flag,cvel2flagid)
    (cdir2flag,cdir2flagid) = qc.rangecheck(Epoch, cdir2,[0,360],cdir2flag,cdir2flagid)

    (cvel3flag,cvel3flagid) = qc.rangecheck(Epoch, cvel3,[-5000,5000],cvel3flag,cvel3flagid)
    (cdir3flag,cdir3flagid) = qc.rangecheck(Epoch, cdir3,[0,360],cdir3flag,cdir3flagid)

    (cvel4flag,cvel4flagid) = qc.rangecheck(Epoch, cvel4,[-5000,5000],cvel4flag,cvel4flagid)
    (cdir4flag,cdir4flagid) = qc.rangecheck(Epoch, cdir4,[0,360],cdir4flag,cdir4flagid)

    (cvel5flag,cvel5flagid) = qc.rangecheck(Epoch, cvel5,[-5000,5000],cvel5flag,cvel5flagid)
    (cdir5flag,cdir5flagid) = qc.rangecheck(Epoch, cdir5,[0,360],cdir5flag,cdir5flagid)

    (cvel6flag,cvel6flagid) = qc.rangecheck(Epoch, cvel6,[-5000,5000],cvel6flag,cvel6flagid)
    (cdir6flag,cdir6flagid) = qc.rangecheck(Epoch, cdir6,[0,360],cdir6flag,cdir6flagid)

    (cvel7flag,cvel7flagid) = qc.rangecheck(Epoch, cvel7,[-5000,5000],cvel7flag,cvel7flagid)
    (cdir7flag,cdir7flagid) = qc.rangecheck(Epoch, cdir7,[0,360],cdir7flag,cdir7flagid)

    (cvel8flag,cvel8flagid) = qc.rangecheck(Epoch, cvel8,[-5000,5000],cvel8flag,cvel8flagid)
    (cdir8flag,cdir8flagid) = qc.rangecheck(Epoch, cdir8,[0,360],cdir8flag,cdir8flagid)

    (cvel9flag,cvel9flagid) = qc.rangecheck(Epoch, cvel9,[-5000,5000],cvel9flag,cvel9flagid)
    (cdir9flag,cdir9flagid) = qc.rangecheck(Epoch, cdir9,[0,360],cdir9flag,cdir9flagid)

    (cvel10flag,cvel10flagid) = qc.rangecheck(Epoch, cvel10,[-5000,5000],cvel10flag,cvel10flagid)
    (cdir10flag,cdir10flagid) = qc.rangecheck(Epoch, cdir10,[0,360],cdir10flag,cdir10flagid)

    (cvel11flag,cvel11flagid) = qc.rangecheck(Epoch, cvel11,[-5000,5000],cvel11flag,cvel11flagid)
    (cdir11flag,cdir11flagid) = qc.rangecheck(Epoch, cdir11,[0,360],cdir11flag,cdir11flagid)

    (cvel12flag,cvel12flagid) = qc.rangecheck(Epoch, cvel12,[-5000,5000],cvel12flag,cvel12flagid)
    (cdir12flag,cdir12flagid) = qc.rangecheck(Epoch, cdir12,[0,360],cdir12flag,cdir12flagid)

    (cvel13flag,cvel13flagid) = qc.rangecheck(Epoch, cvel13,[-5000,5000],cvel13flag,cvel13flagid)
    (cdir13flag,cdir13flagid) = qc.rangecheck(Epoch, cdir13,[0,360],cdir13flag,cdir13flagid)

    (cvel14flag,cvel14flagid) = qc.rangecheck(Epoch, cvel14,[-5000,5000],cvel14flag,cvel14flagid)
    (cdir14flag,cdir14flagid) = qc.rangecheck(Epoch, cdir14,[0,360],cdir14flag,cdir14flagid)

    (cvel15flag,cvel15flagid) = qc.rangecheck(Epoch, cvel15,[-5000,5000],cvel15flag,cvel15flagid)
    (cdir15flag,cdir15flagid) = qc.rangecheck(Epoch, cdir15,[0,360],cdir15flag,cdir15flagid)

    (cvel16flag,cvel16flagid) = qc.rangecheck(Epoch, cvel16,[-5000,5000],cvel16flag,cvel16flagid)
    (cdir16flag,cdir16flagid) = qc.rangecheck(Epoch, cdir16,[0,360],cdir16flag,cdir16flagid)

    (cvel17flag,cvel17flagid) = qc.rangecheck(Epoch, cvel17,[-5000,5000],cvel17flag,cvel17flagid)
    (cdir17flag,cdir17flagid) = qc.rangecheck(Epoch, cdir17,[0,360],cdir17flag,cdir17flagid)

    (cvel18flag,cvel18flagid) = qc.rangecheck(Epoch, cvel18,[-5000,5000],cvel18flag,cvel18flagid)
    (cdir18flag,cdir18flagid) = qc.rangecheck(Epoch, cdir18,[0,360],cdir18flag,cdir18flagid)

    (cvel19flag,cvel19flagid) = qc.rangecheck(Epoch, cvel19,[-5000,5000],cvel19flag,cvel19flagid)
    (cdir19flag,cdir19flagid) = qc.rangecheck(Epoch, cdir19,[0,360],cdir19flag,cdir19flagid)

    (cvel20flag,cvel20flagid) = qc.rangecheck(Epoch, cvel20,[-5000,5000],cvel20flag,cvel20flagid)
    (cdir20flag,cdir20flagid) = qc.rangecheck(Epoch, cdir20,[0,360],cdir20flag,cdir20flagid)




    #Soft Range check
    (cvel1flag,cvel1flagid) = qc.rangecheckclima(Epoch, cvel1,[-1500,1500],cvel1flag,cvel1flagid)

    (cvel2flag,cvel2flagid) = qc.rangecheckclima(Epoch, cvel2,[-1500,1500],cvel2flag,cvel2flagid)

    (cvel3flag,cvel3flagid) = qc.rangecheckclima(Epoch, cvel3,[-1500,1500],cvel3flag,cvel3flagid)

    (cvel4flag,cvel4flagid) = qc.rangecheckclima(Epoch, cvel4,[-1500,1500],cvel4flag,cvel4flagid)

    (cvel5flag,cvel5flagid) = qc.rangecheckclima(Epoch, cvel5,[-1500,1500],cvel5flag,cvel5flagid)

    (cvel6flag,cvel6flagid) = qc.rangecheckclima(Epoch, cvel6,[-1500,1500],cvel6flag,cvel6flagid)

    (cvel7flag,cvel7flagid) = qc.rangecheckclima(Epoch, cvel7,[-1500,1500],cvel7flag,cvel7flagid)

    (cvel8flag,cvel8flagid) = qc.rangecheckclima(Epoch, cvel8,[-1500,1500],cvel8flag,cvel8flagid)

    (cvel9flag,cvel9flagid) = qc.rangecheckclima(Epoch, cvel9,[-1500,1500],cvel9flag,cvel9flagid)

    (cvel10flag,cvel10flagid) = qc.rangecheckclima(Epoch, cvel10,[-1500,1500],cvel10flag,cvel10flagid)

    (cvel11flag,cvel11flagid) = qc.rangecheckclima(Epoch, cvel11,[-1500,1500],cvel11flag,cvel11flagid)

    (cvel12flag,cvel12flagid) = qc.rangecheckclima(Epoch, cvel12,[-1500,1500],cvel12flag,cvel12flagid)

    (cvel13flag,cvel13flagid) = qc.rangecheckclima(Epoch, cvel13,[-1500,1500],cvel13flag,cvel13flagid)

    (cvel14flag,cvel14flagid) = qc.rangecheckclima(Epoch, cvel14,[-1500,1500],cvel14flag,cvel14flagid)

    (cvel15flag,cvel15flagid) = qc.rangecheckclima(Epoch, cvel15,[-1500,1500],cvel15flag,cvel15flagid)

    (cvel16flag,cvel16flagid) = qc.rangecheckclima(Epoch, cvel16,[-1500,1500],cvel16flag,cvel16flagid)

    (cvel17flag,cvel17flagid) = qc.rangecheckclima(Epoch, cvel17,[-1500,1500],cvel17flag,cvel17flagid)

    (cvel18flag,cvel18flagid) = qc.rangecheckclima(Epoch, cvel18,[-1500,1500],cvel18flag,cvel18flagid)

    (cvel19flag,cvel19flagid) = qc.rangecheckclima(Epoch, cvel19,[-1500,1500],cvel19flag,cvel19flagid)

    (cvel20flag,cvel20flagid) = qc.rangecheckclima(Epoch, cvel20,[-1500,1500],cvel20flag,cvel20flagid)

    #Stucksensorcheck

    (cvel1flag,cvel1flagid) = qc.stucksensorcheck(Epoch, cvel1,cvel1flag,12,cvel1flagid)

    (cvel2flag,cvel2flagid) = qc.stucksensorcheck(Epoch, cvel2,cvel2flag,12,cvel2flagid)

    (cvel3flag,cvel3flagid) = qc.stucksensorcheck(Epoch, cvel3,cvel3flag,12,cvel3flagid)

    (cvel4flag,cvel4flagid) = qc.stucksensorcheck(Epoch, cvel4,cvel4flag,12,cvel4flagid)

    (cvel5flag,cvel5flagid) = qc.stucksensorcheck(Epoch, cvel5,cvel5flag,12,cvel5flagid)

    (cvel6flag,cvel6flagid) = qc.stucksensorcheck(Epoch, cvel6,cvel6flag,12,cvel6flagid)

    (cvel7flag,cvel7flagid) = qc.stucksensorcheck(Epoch, cvel7,cvel7flag,12,cvel7flagid)

    (cvel8flag,cvel8flagid) = qc.stucksensorcheck(Epoch, cvel8,cvel8flag,12,cvel8flagid)

    (cvel9flag,cvel9flagid) = qc.stucksensorcheck(Epoch, cvel9,cvel9flag,12,cvel9flagid)

    (cvel10flag,cvel10flagid) = qc.stucksensorcheck(Epoch, cvel10,cvel10flag,12,cvel10flagid)

    (cvel11flag,cvel11flagid) = qc.stucksensorcheck(Epoch, cvel11,cvel11flag,12,cvel11flagid)

    (cvel12flag,cvel12flagid) = qc.stucksensorcheck(Epoch, cvel12,cvel12flag,12,cvel12flagid)

    (cvel13flag,cvel13flagid) = qc.stucksensorcheck(Epoch, cvel13,cvel13flag,12,cvel13flagid)

    (cvel14flag,cvel14flagid) = qc.stucksensorcheck(Epoch, cvel14,cvel14flag,12,cvel14flagid)

    (cvel15flag,cvel15flagid) = qc.stucksensorcheck(Epoch, cvel15,cvel15flag,12,cvel15flagid)

    (cvel16flag,cvel16flagid) = qc.stucksensorcheck(Epoch, cvel16,cvel16flag,12,cvel16flagid)

    (cvel17flag,cvel17flagid) = qc.stucksensorcheck(Epoch, cvel17,cvel17flag,12,cvel17flagid)

    (cvel18flag,cvel18flagid) = qc.stucksensorcheck(Epoch, cvel18,cvel18flag,12,cvel18flagid)

    (cvel19flag,cvel19flagid) = qc.stucksensorcheck(Epoch, cvel19,cvel19flag,12,cvel19flagid)

    (cvel20flag,cvel20flagid) = qc.stucksensorcheck(Epoch, cvel20,cvel20flag,12,cvel20flagid)

    u1,v1=[],[]
    u2,v2=[],[]
    u3,v3=[],[]
    u4,v4=[],[]
    u5,v5=[],[]
    u6,v6=[],[]
    u7,v7=[],[]
    u8,v8=[],[]
    u9,v9=[],[]
    u10,v10=[],[]
    u11,v11=[],[]
    u12,v12=[],[]
    u13,v13=[],[]
    u14,v14=[],[]
    u15,v15=[],[]
    u16,v16=[],[]
    u17,v17=[],[]
    u18,v18=[],[]
    u19,v19=[],[]
    u20,v20=[],[]
    
    for i in range(len(cvel1)):
        (uu,vv)=intdir2uv(cvel1[i], cdir1[i])
        u1.append(uu)
        v1.append(vv)

        (uu,vv)=intdir2uv(cvel2[i], cdir2[i])
        u2.append(uu)
        v2.append(vv)

        (uu,vv)=intdir2uv(cvel3[i], cdir3[i])
        u3.append(uu)
        v3.append(vv)

        (uu,vv)=intdir2uv(cvel4[i], cdir4[i])
        u4.append(uu)
        v4.append(vv)

        (uu,vv)=intdir2uv(cvel5[i], cdir5[i])
        u5.append(uu)
        v5.append(vv)

        (uu,vv)=intdir2uv(cvel6[i], cdir6[i])
        u6.append(uu)
        v6.append(vv)

        (uu,vv)=intdir2uv(cvel7[i], cdir7[i])
        u7.append(uu)
        v7.append(vv)

        (uu,vv)=intdir2uv(cvel8[i], cdir8[i])
        u8.append(uu)
        v8.append(vv)

        (uu,vv)=intdir2uv(cvel9[i], cdir9[i])
        u9.append(uu)
        v9.append(vv)

        (uu,vv)=intdir2uv(cvel10[i], cdir10[i])
        u10.append(uu)
        v10.append(vv)

        (uu,vv)=intdir2uv(cvel11[i], cdir11[i])
        u11.append(uu)
        v11.append(vv)

        (uu,vv)=intdir2uv(cvel12[i], cdir12[i])
        u12.append(uu)
        v12.append(vv)

        (uu,vv)=intdir2uv(cvel13[i], cdir13[i])
        u13.append(uu)
        v13.append(vv)

        (uu,vv)=intdir2uv(cvel14[i], cdir14[i])
        u14.append(uu)
        v14.append(vv)

        (uu,vv)=intdir2uv(cvel15[i], cdir15[i])
        u15.append(uu)
        v15.append(vv)

        (uu,vv)=intdir2uv(cvel16[i], cdir16[i])
        u16.append(uu)
        v16.append(vv)

        (uu,vv)=intdir2uv(cvel17[i], cdir17[i])
        u17.append(uu)
        v17.append(vv)

        (uu,vv)=intdir2uv(cvel18[i], cdir18[i])
        u18.append(uu)
        v18.append(vv)

        (uu,vv)=intdir2uv(cvel19[i], cdir19[i])
        u19.append(uu)
        v19.append(vv)

        (uu,vv)=intdir2uv(cvel20[i], cdir20[i])
        u20.append(uu)
        v20.append(vv)


    #Time continuity check

    (cvel1flag,cvel1flagid,cdir1flag,cdir1flagid) = qc.tcontinuityadcpcheck(Epoch, u1,cvel1flag,cvel1flagid,cdir1flag,cdir1flagid)
    (cvel1flag,cvel1flagid,cdir1flag,cdir1flagid) = qc.tcontinuityadcpcheck(Epoch, v1,cvel1flag,cvel1flagid,cdir1flag,cdir1flagid)

    (cvel2flag,cvel2flagid,cdir2flag,cdir2flagid) = qc.tcontinuityadcpcheck(Epoch, u2,cvel2flag,cvel2flagid,cdir2flag,cdir2flagid)
    (cvel2flag,cvel2flagid,cdir2flag,cdir2flagid) = qc.tcontinuityadcpcheck(Epoch, v2,cvel2flag,cvel2flagid,cdir2flag,cdir2flagid)

    (cvel3flag,cvel3flagid,cdir3flag,cdir3flagid) = qc.tcontinuityadcpcheck(Epoch, u3,cvel3flag,cvel3flagid,cdir3flag,cdir3flagid)
    (cvel3flag,cvel3flagid,cdir3flag,cdir3flagid) = qc.tcontinuityadcpcheck(Epoch, v3,cvel3flag,cvel3flagid,cdir3flag,cdir3flagid)

    (cvel4flag,cvel4flagid,cdir4flag,cdir4flagid) = qc.tcontinuityadcpcheck(Epoch, u4,cvel4flag,cvel4flagid,cdir4flag,cdir4flagid)
    (cvel4flag,cvel4flagid,cdir4flag,cdir4flagid) = qc.tcontinuityadcpcheck(Epoch, v4,cvel4flag,cvel4flagid,cdir4flag,cdir4flagid)

    (cvel5flag,cvel5flagid,cdir5flag,cdir5flagid) = qc.tcontinuityadcpcheck(Epoch, u5,cvel5flag,cvel5flagid,cdir5flag,cdir5flagid)
    (cvel5flag,cvel5flagid,cdir5flag,cdir5flagid) = qc.tcontinuityadcpcheck(Epoch, v5,cvel5flag,cvel5flagid,cdir5flag,cdir5flagid)

    (cvel6flag,cvel6flagid,cdir6flag,cdir6flagid) = qc.tcontinuityadcpcheck(Epoch, u6,cvel6flag,cvel6flagid,cdir6flag,cdir6flagid)
    (cvel6flag,cvel6flagid,cdir6flag,cdir6flagid) = qc.tcontinuityadcpcheck(Epoch, v6,cvel6flag,cvel6flagid,cdir6flag,cdir6flagid)

    (cvel7flag,cvel7flagid,cdir7flag,cdir7flagid) = qc.tcontinuityadcpcheck(Epoch, u7,cvel7flag,cvel7flagid,cdir7flag,cdir7flagid)
    (cvel7flag,cvel7flagid,cdir7flag,cdir7flagid) = qc.tcontinuityadcpcheck(Epoch, v7,cvel7flag,cvel7flagid,cdir7flag,cdir7flagid)

    (cvel8flag,cvel8flagid,cdir8flag,cdir8flagid) = qc.tcontinuityadcpcheck(Epoch, u8,cvel8flag,cvel8flagid,cdir8flag,cdir8flagid)
    (cvel8flag,cvel8flagid,cdir8flag,cdir8flagid) = qc.tcontinuityadcpcheck(Epoch, v8,cvel8flag,cvel8flagid,cdir8flag,cdir8flagid)

    (cvel9flag,cvel9flagid,cdir9flag,cdir9flagid) = qc.tcontinuityadcpcheck(Epoch, u9,cvel9flag,cvel9flagid,cdir9flag,cdir9flagid)
    (cvel9flag,cvel9flagid,cdir9flag,cdir9flagid) = qc.tcontinuityadcpcheck(Epoch, v9,cvel9flag,cvel9flagid,cdir9flag,cdir9flagid)

    (cvel10flag,cvel10flagid,cdir10flag,cdir10flagid) = qc.tcontinuityadcpcheck(Epoch, u10,cvel10flag,cvel10flagid,cdir10flag,cdir10flagid)
    (cvel10flag,cvel10flagid,cdir10flag,cdir10flagid) = qc.tcontinuityadcpcheck(Epoch, v10,cvel10flag,cvel10flagid,cdir10flag,cdir10flagid)

    (cvel11flag,cvel11flagid,cdir11flag,cdir11flagid) = qc.tcontinuityadcpcheck(Epoch, u11,cvel11flag,cvel11flagid,cdir11flag,cdir11flagid)
    (cvel11flag,cvel11flagid,cdir11flag,cdir11flagid) = qc.tcontinuityadcpcheck(Epoch, v11,cvel11flag,cvel11flagid,cdir11flag,cdir11flagid)

    (cvel12flag,cvel12flagid,cdir12flag,cdir12flagid) = qc.tcontinuityadcpcheck(Epoch, u12,cvel12flag,cvel12flagid,cdir12flag,cdir12flagid)
    (cvel12flag,cvel12flagid,cdir12flag,cdir12flagid) = qc.tcontinuityadcpcheck(Epoch, v12,cvel12flag,cvel12flagid,cdir12flag,cdir12flagid)

    (cvel13flag,cvel13flagid,cdir13flag,cdir13flagid) = qc.tcontinuityadcpcheck(Epoch, u13,cvel13flag,cvel13flagid,cdir13flag,cdir13flagid)
    (cvel13flag,cvel13flagid,cdir13flag,cdir13flagid) = qc.tcontinuityadcpcheck(Epoch, v13,cvel13flag,cvel13flagid,cdir13flag,cdir13flagid)

    (cvel14flag,cvel14flagid,cdir14flag,cdir14flagid) = qc.tcontinuityadcpcheck(Epoch, u14,cvel14flag,cvel14flagid,cdir14flag,cdir14flagid)
    (cvel14flag,cvel14flagid,cdir14flag,cdir14flagid) = qc.tcontinuityadcpcheck(Epoch, v14,cvel14flag,cvel14flagid,cdir14flag,cdir14flagid)

    (cvel15flag,cvel15flagid,cdir15flag,cdir15flagid) = qc.tcontinuityadcpcheck(Epoch, u15,cvel15flag,cvel15flagid,cdir15flag,cdir15flagid)
    (cvel15flag,cvel15flagid,cdir15flag,cdir15flagid) = qc.tcontinuityadcpcheck(Epoch, v15,cvel15flag,cvel15flagid,cdir15flag,cdir15flagid)

    (cvel16flag,cvel16flagid,cdir16flag,cdir16flagid) = qc.tcontinuityadcpcheck(Epoch, u16,cvel16flag,cvel16flagid,cdir16flag,cdir16flagid)
    (cvel16flag,cvel16flagid,cdir16flag,cdir16flagid) = qc.tcontinuityadcpcheck(Epoch, v16,cvel16flag,cvel16flagid,cdir16flag,cdir16flagid)

    (cvel17flag,cvel17flagid,cdir17flag,cdir17flagid) = qc.tcontinuityadcpcheck(Epoch, u17,cvel17flag,cvel17flagid,cdir17flag,cdir17flagid)
    (cvel17flag,cvel17flagid,cdir17flag,cdir17flagid) = qc.tcontinuityadcpcheck(Epoch, v17,cvel17flag,cvel17flagid,cdir17flag,cdir17flagid)

    (cvel18flag,cvel18flagid,cdir18flag,cdir18flagid) = qc.tcontinuityadcpcheck(Epoch, u18,cvel18flag,cvel18flagid,cdir18flag,cdir18flagid)
    (cvel18flag,cvel18flagid,cdir18flag,cdir18flagid) = qc.tcontinuityadcpcheck(Epoch, v18,cvel18flag,cvel18flagid,cdir18flag,cdir18flagid)

    (cvel19flag,cvel19flagid,cdir19flag,cdir19flagid) = qc.tcontinuityadcpcheck(Epoch, u19,cvel19flag,cvel19flagid,cdir19flag,cdir19flagid)
    (cvel19flag,cvel19flagid,cdir19flag,cdir19flagid) = qc.tcontinuityadcpcheck(Epoch, v19,cvel19flag,cvel19flagid,cdir19flag,cdir19flagid)

    (cvel20flag,cvel20flagid,cdir20flag,cdir20flagid) = qc.tcontinuityadcpcheck(Epoch, u20,cvel20flag,cvel20flagid,cdir20flag,cdir20flagid)
    (cvel20flag,cvel20flagid,cdir20flag,cdir20flagid) = qc.tcontinuityadcpcheck(Epoch, v20,cvel20flag,cvel20flagid,cdir20flag,cdir20flagid)

    flag=np.array([cvel1flag,cdir1flag,cvel2flag,cdir2flag,cvel3flag,cdir3flag,cvel4flag,cdir4flag,cvel5flag,cdir5flag,cvel6flag,cdir6flag,cvel7flag,cdir7flag,cvel8flag,cdir8flag,cvel9flag,cdir9flag,cvel10flag,cdir10flag,cvel11flag,cdir11flag,cvel12flag,cdir12flag,cvel13flag,cdir13flag,cvel14flag,cdir14flag,cvel15flag,cdir15flag,cvel16flag,cdir16flag,cvel17flag,cdir17flag,cvel18flag,cdir18flag,cvel19flag,cdir19flag,cvel20flag,cdir20flag])
    flagid=np.array([cvel1flagid,cdir1flagid,cvel2flagid,cdir2flagid,cvel3flagid,cdir3flagid,cvel4flagid,cdir4flagid,cvel5flagid,cdir5flagid,cvel6flagid,cdir6flagid,cvel7flagid,cdir7flagid,cvel8flagid,cdir8flagid,cvel9flagid,cdir9flagid,cvel10flagid,cdir10flagid,cvel11flagid,cdir11flagid,cvel12flagid,cdir12flagid,cvel13flagid,cdir13flagid,cvel14flagid,cdir14flagid,cvel15flagid,cdir15flagid,cvel16flagid,cdir16flagid,cvel17flagid,cdir17flagid,cvel18flagid,cdir18flagid,cvel19flagid,cdir19flagid,cvel20flagid,cdir20flagid])

    return flag,flagid, u1,v1
    
#    for i in range(len(cvel1)):
#        if cvel1flag[i]==4 or cdir1flag[i]==4 or cvel2flag[i]==4 or cdir2flag[i]==4 or cvel3flag[i]==4 or cdir3flag[i]==4 or cvel4flag[i]==4 or cdir4flag[i]==4 or cvel5flag[i]==4 or cdir5flag[i]==4 or cvel6flag[i]==4 or cdir6flag[i]==4 or cvel7flag[i]==4 or cdir7flag[i]==4 or cvel8flag[i]==4 or cdir8flag[i]==4 or cvel9flag[i]==4 or cdir9flag[i]==4 or cvel10flag[i]==4 or cdir10flag[i]==4 or cvel11flag[i]==4 or cdir11flag[i]==4 or cvel12flag[i]==4 or cdir12flag[i]==4 or cvel13flag[i]==4 or cdir13flag[i]==4 or cvel14flag[i]==4 or cdir14flag[i]==4 or cvel15flag[i]==4 or cdir15flag[i]==4 or cvel16flag[i]==4 or cdir16flag[i]==4 or cvel17flag[i]==4 or cdir17flag[i]==4 or cvel18flag[i]==4 or cdir18flag[i]==4 or cvel19flag[i]==4 or cdir19flag[i]==4 or cvel20flag[i]==4 or cdir20flag[i]==4:
#            if cdir1flag[i]!=4:
#                cdir1flagid[i]='60'
#            if cvel1flag[i]!=4:
#                cvel1flagid[i]='60'
#            if cvel2flag[i]!=4:
#                cvel2flagid[i]='60'
#            if cdir2flag[i]!=4:
#                cdir2flagid[i]='60'
#            if cvel3flag[i]!=4:
#                cvel3flagid[i]='60'
#            if cdir3flag[i]!=4:
#                cdir3flagid[i]='60'
#            if cvel4flag[i]!=4:
#                cvel4flagid[i]='60'
#            if cdir4flag[i]!=4:
#                cdir4flagid[i]='60'
#            if cvel5flag[i]!=4:
#                cvel5flagid[i]='60'
#            if cdir5flag[i]!=4:
#                cdir5flagid[i]='60'
#            if cvel6flag[i]!=4:
#                cvel6flagid[i]='60'
#            if cdir6flag[i]!=4:
#                cdir6flagid[i]='60'
#            if cvel7flag[i]!=4:
#                cvel7flagid[i]='60'
#            if cdir7flag[i]!=4:
#                cdir7flagid[i]='60'
#            if cvel8flag[i]!=4:
#                cvel8flagid[i]='60'
#            if cdir8flag[i]!=4:
#                cdir8flagid[i]='60'
#            if cvel9flag[i]!=4:
#                cvel9flagid[i]='60'
#            if cdir9flag[i]!=4:
#                cdir9flagid[i]='60'
#            if cvel10flag[i]!=4:
#                cvel10flagid[i]='60'
#            if cdir10flag[i]!=4:
#                cdir10flagid[i]='60'
#            if cvel11flag[i]!=4:
#                cvel11flagid[i]='60'
#            if cdir11flag[i]!=4:
#                cdir11flagid[i]='60'
#            if cvel12flag[i]!=4:
#                cvel12flagid[i]='60'
#            if cdir12flag[i]!=4:
#                cdir12flagid[i]='60'
#            if cvel13flag[i]!=4:
#                cvel13flagid[i]='60'
#            if cdir13flag[i]!=4:
#                cdir13flagid[i]='60'
#            if cvel14flag[i]!=4:
#                cvel14flagid[i]='60'
#            if cdir14flag[i]!=4:
#                cdir14flagid[i]='60'
#            if cvel15flag[i]!=4:
#                cvel15flagid[i]='60'
#            if cdir15flag[i]!=4:
#                cdir15flagid[i]='60'
#            if cvel16flag[i]!=4:
#                cvel16flagid[i]='60'
#            if cdir16flag[i]!=4:
#                cdir16flagid[i]='60'
#            if cvel17flag[i]!=4:
#                cvel17flagid[i]='60'
#            if cdir17flag[i]!=4:
#                cdir17flagid[i]='60'
#            if cvel18flag[i]!=4:
#                cvel18flagid[i]='60'
#            if cdir18flag[i]!=4:
#                cdir18flagid[i]='60'
#            if cvel19flag[i]!=4:
#                cvel19flagid[i]='60'
#            if cdir19flag[i]!=4:
#                cdir19flagid[i]='60'
#            if cvel20flag[i]!=4:
#                cvel20flagid[i]='60'
#            if cdir20flag[i]!=4:
#                cdir20flagid[i]='60'


def qualitycontrol_rt(epoch,buoy,Lat,lon,sensor00,year,month,day,hour,minute,wspd1,gust1,wdir1,wspd2,gust2,wdir2,battery,flood,atmp,humi,dewp,pres,arad,wtmp,cloro,turb,cvel1,cdir1,cvel2,cdir2,cvel3,cdir3,wvht,wmax,dpd,mwd,spred,bhead,sensoresbons):
#    (wspd,wdir,gust,flag,flagid)=qualitycontrol3(epoca,data,variables1,variables2,lat,sensoresbons)


    wdir1flag,wspd1flag,gust1flag,wdir2flag,wspd2flag=[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch)
    gust2flag,wvhtflag,wmaxflag,dpdflag,mwdflag=[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch)
    presflag,humiflag,atmpflag,wtmpflag,dewpflag=[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch)
    cvel1flag,cdir1flag,cvel2flag,cdir2flag,cvel3flag,cdir3flag=[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch),[0]*len(epoch)

    wdir1flagid,wspd1flagid,gust1flagid,wdir2flagid,wspd2flagid=['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch)
    gust2flagid,wvhtflagid,wmaxflagid,dpdflagid,mwdflagid=['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch)
    presflagid,humiflagid,atmpflagid,wtmpflagid,dewpflagid=['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch)
    cvel1flagid,cdir1flagid,cvel2flagid,cdir2flagid,cvel3flagid,cdir3flagid=['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch),['0']*len(epoch)



    (rwvht,rdpd,rmwd,rwspd,rwdir,rgust,ratmp,rpres,rdewp,rwtmp,rapd,rhumi,rcvel,rcdir, sigmawvht,sigmapres,sigmaatmp,sigmawspd,sigmawtmp,sigmahumi,mishumi1,mishumi2,miscvel,miscvel1,miscdir,misdewp,misatmp,miswtmp,rwmax)=qc.valoresargos()

    (r1wvht,r1dpd,r1wspd,r1gust,r1atmp,r1pres,r1dewp,r1wtmp,r1apd,r1cvel,r1wmax,r2atmp,r3atmp)=qc.valoresclima()
    ##############################################
    #RUN The Qc checKs
    ##############################################
    
    #time check
    (timeflag) = qc.timecheck(epoch)

    #missing value check
    (wdir1flag,wdir1flagid)=qc.misvaluecheck(epoch,wdir1,wdir1flag,-9999,wdir1flagid)
    (wspd1flag,wspd1flagid)=qc.misvaluecheck(epoch,wspd1,wspd1flag,-9999,wspd1flagid)
    (gust1flag,gust1flagid)=qc.misvaluecheck(epoch,gust1,gust1flag,-9999,gust1flagid)
    (wdir2flag,wdir2flagid)=qc.misvaluecheck(epoch,wdir2,wdir2flag,-9999,wdir2flagid)
    (wspd2flag,wspd2flagid)=qc.misvaluecheck(epoch,wspd2,wspd2flag,-9999,wspd2flagid)
    (gust2flag,gust2flagid)=qc.misvaluecheck(epoch,gust2,gust2flag,-9999,gust2flagid)
    (mwdflag,mwdflagid)=qc.misvaluecheck(epoch,mwd,mwdflag,-9999,mwdflagid)
    (wvhtflag,wvhtflagid)=qc.misvaluecheck(epoch,wvht,wvhtflag,-9999,wvhtflagid)
    (wmaxflag,wmaxflagid)=qc.misvaluecheck(epoch,wmax,wmaxflag,-9999,wmaxflagid)
    (dpdflag,dpdflagid)=qc.misvaluecheck(epoch,dpd,dpdflag,-9999,dpdflagid)
    (presflag,presflagid)=qc.misvaluecheck(epoch,pres,presflag,-9999,presflagid)
    (dewpflag,dewpflagid)=qc.misvaluecheck(epoch,dewp,dewpflag,misdewp,dewpflagid)
    (atmpflag,atmpflagid)=qc.misvaluecheck(epoch,atmp,atmpflag,misatmp,atmpflagid)
    (wtmpflag,wtmpflagid)=qc.misvaluecheck(epoch,wtmp,wtmpflag,miswtmp,wtmpflagid)
    (cvel1flag,cvel1flagid)=qc.misvaluecheck(epoch,cvel1,cvel1flag,miscvel,cvel1flagid)
    (cvel1flag,cvel1flagid)=qc.misvaluecheck(epoch,cvel1,cvel1flag,miscvel1,cvel1flagid)
    (cdir1flag,cdir1flagid)=qc.misvaluecheck(epoch,cdir1,cdir1flag,miscdir,cdir1flagid)
    (cvel2flag,cvel2flagid)=qc.misvaluecheck(epoch,cvel2,cvel2flag,miscvel,cvel2flagid)
    (cvel2flag,cvel2flagid)=qc.misvaluecheck(epoch,cvel2,cvel2flag,miscvel1,cvel2flagid)
    (cdir2flag,cdir2flagid)=qc.misvaluecheck(epoch,cdir2,cdir2flag,miscdir,cdir2flagid)
    (cvel3flag,cvel3flagid)=qc.misvaluecheck(epoch,cvel3,cvel3flag,miscvel,cvel3flagid)
    (cvel3flag,cvel3flagid)=qc.misvaluecheck(epoch,cvel3,cvel3flag,miscvel1,cvel3flagid)
    (cdir3flag,cdir3flagid)=qc.misvaluecheck(epoch,cdir3,cdir3flag,miscdir,cdir3flagid)
    (humiflag,humiflagid)=qc.misvaluecheck(epoch,humi,humiflag,mishumi1,humiflagid)
    (humiflag,humiflagid)=qc.misvaluecheck(epoch,humi,humiflag,mishumi2,humiflagid)

    (dewpflag,dewpflagid)=qc.misvaluecheck(epoch,dewp,dewpflag,-9999,dewpflagid)
    (atmpflag,atmpflagid)=qc.misvaluecheck(epoch,atmp,atmpflag,-9999,atmpflagid)
    (wtmpflag,wtmpflagid)=qc.misvaluecheck(epoch,wtmp,wtmpflag,-9999,wtmpflagid)
    (cvel1flag,cvel1flagid)=qc.misvaluecheck(epoch,cvel1,cvel1flag,-9999,cvel1flagid)
    (cdir1flag,cdir1flagid)=qc.misvaluecheck(epoch,cdir1,cdir1flag,-9999,cdir1flagid)
    (cvel2flag,cvel2flagid)=qc.misvaluecheck(epoch,cvel2,cvel2flag,-9999,cvel2flagid)
    (cdir2flag,cdir2flagid)=qc.misvaluecheck(epoch,cdir2,cdir2flag,-9999,cdir2flagid)
    (cvel3flag,cvel3flagid)=qc.misvaluecheck(epoch,cvel3,cvel3flag,-9999,cvel3flagid)
    (cdir3flag,cdir3flagid)=qc.misvaluecheck(epoch,cdir3,cdir3flag,-9999,cdir3flagid)
    (humiflag,humiflagid)=qc.misvaluecheck(epoch,humi,humiflag,-9999,humiflagid)

    #checagem de sensores ruins
    (wdir1flag,wdir1flagid)=qc.sensorruimcheck(epoch,wdir1,wdir1flag,sensoresbons[0],wdir1flagid)
    (wspd1flag,wspd1flagid)=qc.sensorruimcheck(epoch,wspd1,wspd1flag,sensoresbons[1],wspd1flagid)
    (gust1flag,gust1flagid)=qc.sensorruimcheck(epoch,gust1,gust1flag,sensoresbons[2],gust1flagid)

    (wdir2flag,wdir2flagid)=qc.sensorruimcheck(epoch,wdir2,wdir2flag,sensoresbons[3],wdir2flagid)
    (wspd2flag,wspd2flagid)=qc.sensorruimcheck(epoch,wspd2,wspd2flag,sensoresbons[4],wspd2flagid)
    (gust2flag,gust2flagid)=qc.sensorruimcheck(epoch,gust2,gust2flag,sensoresbons[5],gust2flagid)

    (wvhtflag,wvhtflagid)=qc.sensorruimcheck(epoch,wvht,wvhtflag,sensoresbons[6],wvhtflagid)
    (wmaxflag,wmaxflagid)=qc.sensorruimcheck(epoch,wmax,wmaxflag,sensoresbons[7],wmaxflagid)
    (dpdflag,dpdflagid)=qc.sensorruimcheck(epoch,dpd,dpdflag,sensoresbons[8],dpdflagid)
    (mwdflag,mwdflagid)=qc.sensorruimcheck(epoch,mwd,mwdflag,sensoresbons[9],mwdflagid)

    (presflag,presflagid)=qc.sensorruimcheck(epoch,pres,presflag,sensoresbons[10],presflagid)
    (humiflag,humiflagid)=qc.sensorruimcheck(epoch,humi,humiflag,sensoresbons[11],humiflagid)
    (atmpflag,atmpflagid)=qc.sensorruimcheck(epoch,atmp,atmpflag,sensoresbons[12],atmpflagid)
    (wtmpflag,wtmpflagid)=qc.sensorruimcheck(epoch,wtmp,wtmpflag,sensoresbons[13],wtmpflagid)
    (dewpflag,dewpflagid)=qc.sensorruimcheck(epoch,dewp,dewpflag,sensoresbons[14],dewpflagid)

    (cvel1flag,cvel1flagid)=qc.sensorruimcheck(epoch,cvel1,cvel1flag,sensoresbons[15],cvel1flagid)
    (cdir1flag,cdir1flagid)=qc.sensorruimcheck(epoch,cdir1,cdir1flag,sensoresbons[16],cdir1flagid)
    (cvel2flag,cvel2flagid)=qc.sensorruimcheck(epoch,cvel2,cvel2flag,sensoresbons[17],cvel2flagid)
    (cdir2flag,cdir2flagid)=qc.sensorruimcheck(epoch,cdir2,cdir2flag,sensoresbons[18],cdir2flagid)
    (cvel3flag,cvel3flagid)=qc.sensorruimcheck(epoch,cvel3,cvel3flag,sensoresbons[19],cvel3flagid)
    (cdir3flag,cdir3flagid)=qc.sensorruimcheck(epoch,cdir3,cdir3flag,sensoresbons[20],cdir3flagid)


    #coarse Range check
    (wvhtflag,wvhtflagid) = qc.rangecheck(epoch, wvht,rwvht,wvhtflag,wvhtflagid)
    (wmaxflag,wmaxflagid) = qc.rangecheck(epoch, wmax,rwmax,wmaxflag,wmaxflagid)
    (dpdflag,dpdflagid) = qc.rangecheck(epoch, dpd,rdpd,dpdflag,dpdflagid)
    (mwdflag,mwdflagid) = qc.rangecheck(epoch,mwd,rmwd,mwdflag,mwdflagid)
    
    (humiflag,humiflagid) = qc.rangecheck(epoch, humi,rhumi,humiflag,humiflagid)
    (presflag,presflagid) = qc.rangecheck(epoch, pres,rpres,presflag,presflagid)
    (dewpflag,dewpflagid) = qc.rangecheck(epoch, dewp,rdewp,dewpflag,dewpflagid)
    (atmpflag,atmpflagid) = qc.rangecheck(epoch,atmp,ratmp,atmpflag,atmpflagid)
    
    (wspd1flag,wspd1flagid) = qc.rangecheck(epoch, wspd1,rwspd,wspd1flag,wspd1flagid)
    (wdir1flag,wdir1flagid) = qc.rangecheck(epoch, wdir1,rwdir,wdir1flag,wdir1flagid)
    (gust1flag,gust1flagid) = qc.rangecheck(epoch, gust1,rgust,gust1flag,gust1flagid)
    (wspd2flag,wspd2flagid) = qc.rangecheck(epoch, wspd2,rwspd,wspd2flag,wspd2flagid)
    (wdir2flag,wdir2flagid) = qc.rangecheck(epoch, wdir2,rwdir,wdir2flag,wdir2flagid)
    (gust2flag,gust2flagid) = qc.rangecheck(epoch, gust2,rgust,gust2flag,gust2flagid)
    
    (wtmpflag,wtmpflagid) = qc.rangecheck(epoch,wtmp,rwtmp,wtmpflag,wtmpflagid)
    (cvel1flag,cvel1flagid) = qc.rangecheck(epoch, cvel1,rcvel,cvel1flag,cvel1flagid)
    (cdir1flag,cdir1flagid) = qc.rangecheck(epoch, cdir1,rcdir,cdir1flag,cdir1flagid)
    (cvel2flag,cvel2flagid) = qc.rangecheck(epoch, cvel2,rcvel,cvel2flag,cvel2flagid)
    (cdir2flag,cdir2flagid) = qc.rangecheck(epoch, cdir2,rcdir,cdir2flag,cdir2flagid)
    (cvel3flag,cvel3flagid) = qc.rangecheck(epoch, cvel3,rcvel,cvel3flag,cvel3flagid)
    (cdir3flag,cdir3flagid) = qc.rangecheck(epoch, cdir3,rcdir,cdir3flag,cdir3flagid)

    #soft Range check

    (wvhtflag,wvhtflagid) = qc.rangecheckclima(epoch, wvht,r1wvht,wvhtflag,wvhtflagid)
    (wmaxflag,wmaxflagid) = qc.rangecheckclima(epoch, wmax,r1wmax,wmaxflag,wmaxflagid)
    (dpdflag,dpdflagid) = qc.rangecheckclima(epoch, dpd,r1dpd,dpdflag,dpdflagid)

    (presflag,presflagid) = qc.rangecheckclima(epoch, pres,r1pres,presflag,presflagid)
    (dewpflag,dewpflagid) = qc.rangecheckclima(epoch, dewp,r1dewp,dewpflag,dewpflagid)

    try:
        if mean(Lat)<=-27:
            (atmpflag,atmpflagid) = qc.rangecheckclima(epoch,atmp,r1atmp,atmpflag,atmpflagid)
        elif mean(Lat)>-27 and mean(Lat)<=-18: 
            (atmpflag,atmpflagid) = qc.rangecheckclima(epoch,atmp,r2atmp,atmpflag,atmpflagid)
        else:
            (atmpflag,atmpflagid) = qc.rangecheckclima(epoch,atmp,r3atmp,atmpflag,atmpflagid)
    except:
        (atmpflag,atmpflagid) = qc.rangecheckclima(epoch,atmp,r1atmp,atmpflag,atmpflagid)
        
    
    (wspd1flag,wspd1flagid) = qc.rangecheckclima(epoch, wspd1,r1wspd,wspd1flag,wspd1flagid)
    (gust1flag,gust1flagid) = qc.rangecheckclima(epoch, gust1,r1gust,gust1flag,gust1flagid)
    (wspd2flag,wspd2flagid) = qc.rangecheckclima(epoch, wspd2,r1wspd,wspd2flag,wspd2flagid)
    (gust2flag,gust2flagid) = qc.rangecheckclima(epoch, gust2,r1gust,gust2flag,gust2flagid)
    
    (wtmpflag,wtmpflagid) = qc.rangecheckclima(epoch,wtmp,r1wtmp,wtmpflag,wtmpflagid)
    (cvel1flag,cvel1flagid) = qc.rangecheckclima(epoch, cvel1,r1cvel,cvel1flag,cvel1flagid)
    (cvel2flag,cvel2flagid) = qc.rangecheckclima(epoch, cvel2,r1cvel,cvel2flag,cvel2flagid)
    (cvel3flag,cvel3flagid) = qc.rangecheckclima(epoch, cvel3,r1cvel,cvel3flag,cvel3flagid)

    #significance wave height vs max wave height
    (wvhtflag,wmaxflag,wvhtflagid,wmaxflagid) = qc.wvhtwmaxcheck(epoch,wvht,wmax,wvhtflag,wmaxflag,wvhtflagid,wmaxflagid)
    
    #wind speed vs gust speed
    (wspd1flag,gust1flag,wspd1flagid,gust1flagid) = qc.windspeedgustcheck(epoch,wspd1,gust1,wspd1flag,gust1flag,wspd1flagid,gust1flagid)
    (wspd2flag,gust2flag,wspd2flagid,gust2flagid) = qc.windspeedgustcheck(epoch,wspd2,gust2,wspd2flag,gust2flag,wspd2flagid,gust2flagid)
   
    #dew point and air temperature check
    (dewpflag,dewpflagid) = qc.dewpatmpcheck(epoch,dewp,atmp,dewpflag,atmpflag,dewpflagid)
    
    #check of effects of battery voltage in sensors    
    (presflag,presflagid) = qc.batsensorcheck(epoch,battery,pres,presflag,presflagid)    
    
    #stucksensorcheck
    (wvhtflag,wvhtflagid) = qc.stucksensorcheck(epoch, wvht,wvhtflag,12,wvhtflagid)
    (wmaxflag,wmaxflagid) = qc.stucksensorcheck(epoch, wmax,wmaxflag,12,wmaxflagid)
    
    (humiflag,humiflagid) = qc.stucksensorcheck(epoch, humi,humiflag,12,humiflagid)
    (presflag,presflagid) = qc.stucksensorcheck(epoch, pres,presflag,12,presflagid)
    (dewpflag,dewpflagid) = qc.stucksensorcheck(epoch, dewp,dewpflag,12,dewpflagid)
    (atmpflag,atmpflagid) = qc.stucksensorcheck(epoch,atmp,atmpflag,12,atmpflagid)
    
    (wspd1flag,wspd1flagid) = qc.stucksensorcheck(epoch, wspd1,wspd1flag,12,wspd1flagid)
    (wdir1flag,wdir1flagid) = qc.stucksensorcheck(epoch, wdir1,wdir1flag,12,wdir1flagid)
    (gust1flag,gust1flagid) = qc.stucksensorcheck(epoch, gust1,gust1flag,12,gust1flagid)
    (wspd2flag,wspd2flagid) = qc.stucksensorcheck(epoch, wspd2,wspd2flag,12,wspd2flagid)
    (wdir2flag,wdir2flagid) = qc.stucksensorcheck(epoch, wdir2,wdir2flag,12,wdir2flagid)
    (gust2flag,gust2flagid) = qc.stucksensorcheck(epoch, gust2,gust2flag,12,gust2flagid)
    
    (wtmpflag,wtmpflagid) = qc.stucksensorcheck(epoch,wtmp,wtmpflag,12,wtmpflagid)
    (cvel1flag,cvel1flagid) = qc.stucksensorcheck(epoch, cvel1,cvel1flag,12,cvel1flagid)
    (cdir1flag,cdir1flagid) = qc.stucksensorcheck(epoch, cdir1,cdir1flag,12,cdir1flagid)
    (cvel2flag,cvel2flagid) = qc.stucksensorcheck(epoch, cvel2,cvel2flag,12,cvel2flagid)
    (cdir2flag,cdir2flagid) = qc.stucksensorcheck(epoch, cdir2,cdir2flag,12,cdir2flagid)
    (cvel3flag,cvel3flagid) = qc.stucksensorcheck(epoch, cvel3,cvel3flag,12,cvel3flagid)
    (cdir3flag,cdir3flagid) = qc.stucksensorcheck(epoch, cdir3,cdir3flag,12,cdir3flagid)


    #related measurement check
    (wdirflag,wspdflag,gustflag,wdir,wspd,gust,wdirflagid,wspdflagid,gustflagid) = qc.relatedmeascheck3(epoch,wdir1,wspd1,gust1,wdir2,wspd2,gust2,wspd1flag, wdir1flag,gust1flag,wspd2flag, wdir2flag,gust2flag,wdir1flagid,wspd1flagid,gust1flagid,wdir2flagid,wspd2flagid,gust2flagid)

    
    #Time continuity check
    (wvhtflag,wvhtflagid) = qc.tcontinuitycheck(epoch, wvht,wvhtflag,sigmawvht,wvhtflagid,1)
    (wmaxflag,wmaxflagid) = qc.tcontinuitycheck(epoch, wmax,wmaxflag,sigmawvht,wmaxflagid,1)
    (humiflag,humiflagid) = qc.tcontinuitycheck(epoch, humi,humiflag,sigmahumi,humiflagid,1)
    (presflag,presflagid) = qc.tcontinuitycheck(epoch, pres,presflag,sigmapres,presflagid,1)
    (atmpflag,atmpflagid) = qc.tcontinuitycheck(epoch,atmp,atmpflag,sigmaatmp,atmpflagid,1)
    (wspdflag,wspdflagid) = qc.tcontinuitycheck(epoch, wspd,wspdflag,sigmawspd,wspdflagid,1)    
    (wtmpflag,wtmpflagid) = qc.tcontinuitycheck(epoch,wtmp,wtmpflag,sigmawtmp,wtmpflagid,1)


    #Frontal passage exception for time continuity
    (atmpflag,atmpflagid)=qc.frontexcepcheck1(epoch,wdir,wdirflag,atmpflag,atmpflagid)
#    (wdirflag,wdirflagid)=qc.frontexcepcheck2(epoch,wdir,wdirflag,atmpflag,atmpflagid)

    (atmpflag,atmpflagid)=qc.frontexcepcheck3(epoch,wspd,atmp,wspdflag,atmpflag,atmpflagid)
    (wspdflag,wspdflagid)=qc.frontexcepcheck4(epoch,pres,presflag,wdirflag,wdirflagid)
    
    (presflag,presflagid)=qc.frontexcepcheck5(epoch,pres,presflag,presflagid)
    (wvhtflag,wvhtflagid)=qc.frontexcepcheck6(epoch,wspd,wspdflag,wvhtflagid,wvhtflag)

    for i in range(len(cvel1)):
        if buoy==157599 and wdirflag!=4:
            direc_vento=wdir[i]+180
            if direc_vento>=360:
                wdir[i]=direc_vento-360
            else:
                wdir[i]=direc_vento
        if cvel1flag[i]==4 or cdir1flag[i]==4 or cvel2flag[i]==4 or cdir2flag[i]==4 or cvel3flag[i]==4 or cdir3flag[i]==4:
            if cdir1flag[i]!=4:
                cdir1flagid[i]='60'
            if cvel1flag[i]!=4:
                cvel1flagid[i]='60'
            if cvel2flag[i]!=4:
                cvel2flagid[i]='60'
            if cdir2flag[i]!=4:
                cdir2flagid[i]='60'
            if cvel3flag[i]!=4:
                cvel3flagid[i]='60'
            if cdir3flag[i]!=4:
                cdir3flagid[i]='60'

        if mwdflag[i]==4 or wvhtflag[i]==4 or wmaxflag[i]==4 or dpdflag[i]==4:
            if wvhtflag[i]!=4:
                wvhtflagid[i]='60'
            if wmaxflag[i]!=4:
                wmaxflagid[i]='60'
            if dpdflag[i]!=4:
                dpdflagid[i]='60'
            if mwdflag[i]!=4:
                mwdflagid[i]='60'

        if wdirflag[i]==4 or gustflag[i]==4 or wspdflag[i]==4:
            if wdirflag[i]!=4:
                wdirflagid[i]='60'                
            if gustflag[i]!=4:
                gustflagid[i]='60'  
            if wspdflag[i]!=4:
                wspdflagid[i]='60'  

    return wspd,wdir,gust,wdirflag,wspdflag,gustflag,wvhtflag,wmaxflag,dpdflag,mwdflag,presflag,humiflag,atmpflag,wtmpflag,dewpflag,cvel1flag,cdir1flag,cvel2flag,cdir2flag,cvel3flag,cdir3flag,wdirflagid,wspdflagid,gustflagid,wvhtflagid,wmaxflagid,dpdflagid,mwdflagid,presflagid,humiflagid,atmpflagid,wtmpflagid,dewpflagid,cvel1flagid,cdir1flagid,cvel2flagid,cdir2flagid,cvel3flagid,cdir3flagid



def intdir2uv(intensidade, direcao):

	import numpy as np

	direcao = np.mod(direcao,360)
	direcao = direcao*np.pi/180

	u=intensidade*np.sin(direcao)
	v=intensidade*np.cos(direcao)

	return u, v

def uv2intdir(u, v):

    import numpy as np
    if u>=0 and v>=0:
        intensidade=np.sqrt((u*u)+(v*v))
        direcao=rad2deg(np.arcsin(v/u))
    elif u<0 and v>=0:
        intensidade=np.sqrt((u*u)+(v*v))
        direcao=rad2deg(np.arcsin(v/(-u)))+90    
    elif u<0 and v<0:
        intensidade=np.sqrt((u*u)+(v*v))
        direcao=rad2deg(np.arcsin((-v)/(-u)))+180 
    elif u>=0 and v<0:
        intensidade=np.sqrt((u*u)+(v*v))
        direcao=rad2deg(np.arcsin((-v)/u))+270

    return intensidade,direcao    
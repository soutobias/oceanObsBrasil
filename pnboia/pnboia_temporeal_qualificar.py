# -*- coding: utf-8 -*-
"""
created on Tue may 03 10:08:32 2016

@author: Tobias
"""
from qualitycontrol import *
import mysql.connector as MySQLdb
import re
import time
import csv
from telnetlib import Telnet
import datetime
import numpy as np
import operator
import argosqc as qc
import smtplib

import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )


def consulta_banco(boia):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    argosbruto=[]
    [anoq,mesq,diaq,horaq,minq,secq,wdayq,ydayq,isdstq]=time.gmtime(time.time())
    if mesq==1:
        anoq=anoq-1
        mesq=12
    else:
        mesq=mesq-1
    epoch_25=time.strftime('%y-%m-%d',time.gmtime((datetime.datetime(anoq,mesq,25,horaq,0) - datetime.datetime(1970,1,1)).total_seconds()))
    epoch_25=datetime.datetime.strptime(epoch_25, '%y-%m-%d')
    print(str(epoch_25))
    cur.execute("SELECT * FROm argos_bruto wheRe argos_id=%s and data>='%s'\
    ORdeR by data" %(boia , epoch_25))
    for row in cur.fetchall():
        argosbruto.append(row[:])

    cur.close()
    db.close()
    return argosbruto


def alimentarbd(Data1,boia):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    cur.execute("SELECT datahora FROM pnboia WHERE esta_id='%s'\
    ORDER BY datahora DESC limit 20" % boia)
    for row in cur.fetchall():
        c1.append(row)
    if c1!=[]:
        for i in range(len(Data1)):
            if Data1[i][2]>max(c1)[0]:
                sql = "INSERT INTO pnboia (esta_id,lat,lon,datahora,bateria,heading,wspd,\
                wspdflagid,wdir,wdirflagid,gust,gustflagid,atmp,atmpflagid,pres,presflagid,dewp,\
                dewpflagid,humi,humiflagid,wtmp,wtmpflagid,cvel1,cvel1flagid,cdir1,cdir1flagid,\
                cvel2,cvel2flagid,cdir2,cdir2flagid,cvel3,cvel3flagid,cdir3,cdir3flagid,wvht,\
                wvhtflagid,wmax,wmaxflagid,dpd,dpdflagid,mwd,mwdflagid,spred)\
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s',\
                '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',\
                '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',\
                '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                (int(boia),float(Data1[i][0]),float(Data1[i][1]),(Data1[i][2]),float(Data1[i][3]),\
                float(Data1[i][4]),float(Data1[i][5]),int(Data1[i][6]),float(Data1[i][7]),\
                int(Data1[i][8]),float(Data1[i][9]),\
                int(Data1[i][10]),float(Data1[i][11]),int(Data1[i][12]),float(Data1[i][13]),\
                int(Data1[i][14]),float(Data1[i][15]),int(Data1[i][16]),float(Data1[i][17]),\
                int(Data1[i][18]),float(Data1[i][19]),int(Data1[i][20]),float(Data1[i][21]),\
                int(Data1[i][22]),float(Data1[i][23]),int(Data1[i][24]),\
                float(Data1[i][25]),int(Data1[i][26]),int(Data1[i][27]),int(Data1[i][28]),\
                float(Data1[i][29]),int(Data1[i][30]),int(Data1[i][31]),int(Data1[i][32]),\
                float(Data1[i][33]),int(Data1[i][34]),float(Data1[i][35]),int(Data1[i][36]),\
                float(Data1[i][37]),int(Data1[i][38]),float(Data1[i][39]),int(Data1[i][40]),\
                int(Data1[i][41]))
                cur.execute(sql)
                db.commit()
            else: #inserir update
                sql = "UPDATE pnboia SET esta_id=%s,lat=%s,lon=%s,datahora='%s',bateria=%s,heading=%s,wspd=%s,\
                wspdflagid=%s,wdir=%s,wdirflagid=%s,gust=%s,gustflagid=%s,atmp=%s,atmpflagid=%s,pres=%s,presflagid=%s,dewp=%s,\
                dewpflagid=%s,humi=%s,humiflagid=%s,wtmp=%s,wtmpflagid=%s,cvel1=%s,cvel1flagid=%s,cdir1=%s,cdir1flagid=%s,\
                cvel2=%s,cvel2flagid=%s,cdir2=%s,cdir2flagid=%s,cvel3=%s,cvel3flagid=%s,cdir3=%s,cdir3flagid=%s,wvht=%s,\
                wvhtflagid=%s,wmax=%s,wmaxflagid=%s,dpd=%s,dpdflagid=%s,mwd=%s,mwdflagid=%s,spred=%s \
                WHERE esta_id=%s and datahora='%s'" % \
                (int(boia),float(Data1[i][0]),float(Data1[i][1]),(Data1[i][2]),float(Data1[i][3]),\
                float(Data1[i][4]),float(Data1[i][5]),int(Data1[i][6]),float(Data1[i][7]),\
                int(Data1[i][8]),float(Data1[i][9]),\
                int(Data1[i][10]),float(Data1[i][11]),int(Data1[i][12]),float(Data1[i][13]),\
                int(Data1[i][14]),float(Data1[i][15]),int(Data1[i][16]),float(Data1[i][17]),\
                int(Data1[i][18]),float(Data1[i][19]),int(Data1[i][20]),float(Data1[i][21]),\
                int(Data1[i][22]),float(Data1[i][23]),int(Data1[i][24]),\
                float(Data1[i][25]),int(Data1[i][26]),int(Data1[i][27]),int(Data1[i][28]),\
                float(Data1[i][29]),int(Data1[i][30]),int(Data1[i][31]),int(Data1[i][32]),\
                float(Data1[i][33]),int(Data1[i][34]),float(Data1[i][35]),int(Data1[i][36]),\
                float(Data1[i][37]),int(Data1[i][38]),float(Data1[i][39]),int(Data1[i][40]),\
                int(Data1[i][41]),int(boia),(Data1[i][2]))
                cur.execute(sql)
                db.commit()
    else:
        for i in range(len(Data1)):
            sql = "INSERT INTO pnboia (esta_id,lat,lon,datahora,bateria,heading,wspd,\
            wspdflagid,wdir,wdirflagid,gust,gustflagid,atmp,atmpflagid,pres,presflagid,dewp,\
            dewpflagid,humi,humiflagid,wtmp,wtmpflagid,cvel1,cvel1flagid,cdir1,cdir1flagid,\
            cvel2,cvel2flagid,cdir2,cdir2flagid,cvel3,cvel3flagid,cdir3,cdir3flagid,wvht,\
            wvhtflagid,wmax,wmaxflagid,dpd,dpdflagid,mwd,mwdflagid,spred)\
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s',\
            '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',\
            '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',\
            '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
            (int(boia),float(Data1[i][0]),float(Data1[i][1]),(Data1[i][2]),float(Data1[i][3]),\
            float(Data1[i][4]),float(Data1[i][5]),int(Data1[i][6]),float(Data1[i][7]),\
            int(Data1[i][8]),float(Data1[i][9]),\
            int(Data1[i][10]),float(Data1[i][11]),int(Data1[i][12]),float(Data1[i][13]),\
            int(Data1[i][14]),float(Data1[i][15]),int(Data1[i][16]),float(Data1[i][17]),\
            int(Data1[i][18]),float(Data1[i][19]),int(Data1[i][20]),float(Data1[i][21]),\
            int(Data1[i][22]),float(Data1[i][23]),int(Data1[i][24]),\
            float(Data1[i][25]),int(Data1[i][26]),int(Data1[i][27]),int(Data1[i][28]),\
            float(Data1[i][29]),int(Data1[i][30]),int(Data1[i][31]),int(Data1[i][32]),\
            float(Data1[i][33]),int(Data1[i][34]),float(Data1[i][35]),int(Data1[i][36]),\
            float(Data1[i][37]),int(Data1[i][38]),float(Data1[i][39]),int(Data1[i][40]),\
            int(Data1[i][41]))
            cur.execute(sql)
            db.commit()
    cur.close()
    db.close()
    print('dados inseridos')


def boiasfuncionando():

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    boias=[]
    cur.execute("SELECT estacao_id, argos_id,nome, argos_id, argos_id FROM pnboia_estacao WHERE sit=1")
    for row in cur.fetchall():
        boias.append(row)
    return boias
    cur.close()
    db.close()

boias=boiasfuncionando()

for s in range(len(boias)):
    print(boias[s][2])
    bat=consulta_banco(int(boias[s][1]))

    variables=['argos_id,lat,lon,data,sensor00,sensor01,sensor02,sensor03,sensor04,sensor05,sensor06,sensor07,sensor08,sensor09,sensor10,sensor11,sensor12,sensor13,sensor14,sensor15,sensor16,sensor17,sensor18,sensor19,sensor20,sensor21,sensor22,sensor23,sensor24,sensor25']

    anodia,horamin=[],[]
    anodia1,horamin1=[],[]
    year0,month0,day0,hour0=[],[],[],[]
    sensor00,lat,lon=[],[],[]
    year,month,day,hour,minute,battery,flood,wspd1,gust1,wdir1,wspd2,gust2,wdir2=[],[],[],[],[],[],[],[],[],[],[],[],[]
    atmp,humi,dewp,pres,wtmp,bhead,cloro,turb,arad=[],[],[],[],[],[],[],[],[]
    cvel1,cdir1,cvel2,cdir2,cvel3,cdir3,wvht,wmax,dpd,mwd,spred=[],[],[],[],[],[],[],[],[],[],[]
    xxx=[]
    epoca=[]
    print(bat)
    for i in range(len(bat)):
        if int(float(bat[i][5]))==1 and float(bat[i][7])<=12 and float(bat[i][8])<=23:
            year0.append(int(bat[i][4].year))
            month0.append(int(bat[i][4].month))
            day0.append(int(bat[i][4].day))
            hour0.append(int(bat[i][4].hour))
            sensor00.append(int(float(bat[i][5])))
            if bat[i][2]!="-9999":
                lat.append(float(bat[i][2]))
                lon.append(float(bat[i][3])-360)
            else:
                lat.append((bat[i][2]))
                lon.append((bat[i][3]))

            year.append(int(float(bat[i][6])))
            month.append(int(float(bat[i][7])))
            day.append(int(float(bat[i][8])))
            hour.append(int(float(bat[i][9])))
            minute.append(20)
            battery.append(float(bat[i][16]))
            flood.append(int(float(bat[i][19])))
            wspd1.append(float(bat[i][20]))
            gust1.append(float(bat[i][21]))
            wdir1.append(float(bat[i][22]))
            wspd2.append(float(bat[i][23]))
            gust2.append(float(bat[i][24]))
            wdir2.append(float(bat[i][25]))

            atmp.append("-9999")
            humi.append("-9999")
            dewp.append("-9999")
            pres.append("-9999")
            wtmp.append("-9999")
            bhead.append("-9999")
            cloro.append("-9999")
            turb.append("-9999")
            arad.append("-9999")
            cvel1.append("-9999")
            cdir1.append("-9999")
            cvel2.append("-9999")
            cdir2.append("-9999")
            cvel3.append("-9999")
            cdir3.append("-9999")
            wvht.append("-9999")
            wmax.append("-9999")
            dpd.append("-9999")
            mwd.append("-9999")
            spred.append("-9999")

            #print(bat[i], float(bat[i][7]))
            epoca.append((datetime.datetime(int(float(bat[i][6])),int(float(bat[i][7])),int(float(bat[i][8])),int(float(bat[i][9])),0) - datetime.datetime(1970,1,1)).total_seconds())

        elif int(float(bat[i][5]))==2:
            year0.append(int(bat[i][4].year))
            month0.append(int(bat[i][4].month))
            day0.append(int(bat[i][4].day))
            hour0.append(int(bat[i][4].hour))

            sensor00.append(int(float(bat[i][5])))
            if bat[i][2]!="-9999":
                lat.append(float(bat[i][2]))
                lon.append(float(bat[i][3])-360)
            else:
                lat.append((bat[i][2]))
                lon.append((bat[i][3]))
            #print(i, len(year0))
            year.append(int(float(year0[-1])))
            month.append(int(float(month0[-1])))
            day.append(int(float(day0[-1])))
            hour.append(int(float(bat[i][6])))
            minute.append(20)
            wspd1.append(float(bat[i][7]))
            gust1.append(float(bat[i][8]))
            wdir1.append(float(bat[i][9]))
            atmp.append(float(bat[i][10]))
            humi.append(float(bat[i][11]))
            dewp.append(float(bat[i][12]))
            pres.append(float(bat[i][13]))
            wtmp.append(float(bat[i][14]))
            if boias[s][0]==69007:
                bhead.append(float(bat[i][15]))
                cloro.append(float(bat[i][16]))
                turb.append(float(bat[i][17]))
                arad.append(float(bat[i][18]))
                cvel1.append(float(bat[i][19]))
                cdir1.append(float(bat[i][20]))
                cvel2.append(float(bat[i][21]))
                cdir2.append(float(bat[i][22]))
                cvel3.append(float(bat[i][23]))
                cdir3.append(float(bat[i][24]))
                wvht.append(float(bat[i][25]))
                wmax.append(float(bat[i][26]))
                dpd.append(float(bat[i][27]))
                mwd.append(float(bat[i][28]))
                spred.append(float(bat[i][29]))

            else:
                bhead.append(float(bat[i][16]))
                cloro.append(float(bat[i][17]))
                turb.append(float(bat[i][18]))
                arad.append(float(bat[i][19]))
                cvel1.append(float(bat[i][20]))
                cdir1.append(float(bat[i][21]))
                cvel2.append(float(bat[i][22]))
                cdir2.append(float(bat[i][23]))
                cvel3.append(float(bat[i][24]))
                cdir3.append(float(bat[i][25]))
                wvht.append(float(bat[i][26]))
                wmax.append(float(bat[i][27]))
                dpd.append(float(bat[i][28]))
                mwd.append(float(bat[i][29]))
                spred.append(float(bat[i][30]))


            battery.append("-9999")
            flood.append("-9999")
            wspd2.append("-9999")
            gust2.append("-9999")
            wdir2.append("-9999")

            if hour[-1]==23 and int(hour0[-1])==0:
                if day0[-1]!=1:
                    day[-1]=day0[-1]-1
                else:
                    if month[-1]==1:
                        year[-1]=year[-1]-1
                        month[-1]=12
                        day[-1]=31
                    elif month[-1]==3:
                        month[-1]=month[-1]-1
                        day[-1]=28
                    elif month[-1]==5 or month[-1]==7 or month[-1]==10 or month[-1]==12:
                        day[-1]=30
                        month[-1]=month[-1]-1
                    else:
                        day[-1]=31
                        month[-1]=month[-1]-1
                        continue
                    continue
            elif int(hour[-1])==22 and int(hour0[-1])==0:
                if int(day0[-1])!=1:
                    day[-1]=day0[-1]-1
                else:
                    if int(month[-1])==1:
                        year[-1]=year[-1]-1
                        month[-1]=12
                        day[-1]=31
                    elif int(month[-1])==3:
                        month[-1]=month[-1]-1
                        day[-1]=28
                    elif int(month[-1])==5 or int(month[-1])==7 or int(month[-1])==10 or int(month[-1])==12:
                        day[-1]=30
                        month[-1]=month[-1]-1
                    else:
                        day[-1]=31
                        month[-1]=month[-1]-1
                        continue
                    continue
            elif int(hour[-1])==22 and int(hour0[-1])==1:
                if int(day0[-1])!=1:
                    day[-1]=day0[-1]-1
                else:
                    if int(month[-1])==1:
                        year[-1]=year[-1]-1
                        month[-1]=12
                        day[-1]=31
                    elif int(month[-1])==3:
                        month[-1]=month[-1]-1
                        day[-1]=28
                    elif int(month[-1])==5 or int(month[-1])==7 or int(month[-1])==10 or int(month[-1])==12:
                        day[-1]=30
                        month[-1]=month[-1]-1
                    else:
                        day[-1]=31
                        month[-1]=month[-1]-1
                        continue
                    continue
            elif int(hour[-1])==23 and int(hour0[-1])==1:
                if int(day0[-1])!=1:
                    day[-1]=day0[-1]-1
                else:
                    if int(month[-1])==1:
                        year[-1]=year[-1]-1
                        month[-1]=12
                        day[-1]=31
                    elif int(month[-1])==3:
                        month[-1]=month[-1]-1
                        day[-1]=28
                    elif int(month[-1])==5 or int(month[-1])==7 or int(month[-1])==10 or int(month[-1])==12:
                        day[-1]=30
                        month[-1]=month[-1]-1
                    else:
                        day[-1]=31
                        month[-1]=month[-1]-1
                        continue
                    continue
            else:
                day[-1]=day0[-1]



    [anoq,mesq,diaq,horaq,minq,secq,wdayq,ydayq,isdstq]=time.gmtime(time.time())
    epoch_26=(datetime.datetime(anoq,mesq,diaq,horaq,0) - datetime.datetime(1970,1,1)).total_seconds()+3600*3
    [anoq,mesq,diaq,horaq,minq,secq,wdayq,ydayq,isdstq]=time.gmtime(time.time()-3600*24*31)
    epoch_27=(datetime.datetime(anoq,mesq,25,0,0) - datetime.datetime(1970,1,1)).total_seconds()-3600*3

    variables50=['lat','lon','sensor00','year','month','day','hour','minute','wspd1','gust1','wdir1','wspd2','gust2','wdir2','battery','flood','atmp','humi','dewp','pres','arad','wtmp','cloro','turb','cvel1','cdir1','cvel2','cdir2','cvel3','cdir3','wvht','wmax','dpd','mwd','spred','bhead']

    epoca=[]
    c,i=0,0
    for w in range(len(year)):
        print(year[w],month[w],day[w],hour[w])
        try:
            kkkk=(datetime.datetime(int(year[i]),int(month[i]),int(day[i]),int(hour[i]),0) - datetime.datetime(1970,1,1)).total_seconds()
            if kkkk<epoch_26 and kkkk>epoch_27 and i<len(year):
                for ii in range(len(variables50)):
                    exec("%s[c]=%s[i]"% (variables50[ii],variables50[ii]))
                epoca.append((datetime.datetime(int(year[i]),int(month[i]),int(day[i]),int(hour[i]),0) - datetime.datetime(1970,1,1)).total_seconds())
                c=c+1
                i=i+1
            else:
                i=i+1
        except Exception as e:
            i=i+1
    for ii in range(len(variables50)):
        exec("%s=%s[0:c]"% (variables50[ii],variables50[ii]))

    variables=['buoy','epoca','lat','lon','sensor00','year','month','day','hour','minute','wspd1','gust1','wdir1','wspd2','gust2','wdir2','battery','flood','atmp','humi','dewp','pres','arad','wtmp','cloro','turb','cvel1','cdir1','cvel2','cdir2','cvel3','cdir3','wvht','wmax','dpd','mwd','spred','bhead']
    varfinal1=['buoy','epoca','lat','lon','sensor00','year','month','day','hour','minute','atmp','humi','dewp','pres','arad','wtmp','cloro','turb','cvel1','cdir1','cvel2','cdir2','cvel3','cdir3','wvht','wmax','dpd','mwd','spred','bhead']
    varfinal2=['wspd1','gust1','wdir1','wspd2','gust2','wdir2','battery','flood']


    buoy=[]
    for i in range(len(epoca)):
        buoy.append(boias[s][0])

    data=[]
    data = np.array([buoy,epoca,lat,lon,sensor00,year,month,day,hour,minute,wspd1,gust1,wdir1,wspd2,gust2,wdir2,battery,flood,atmp,humi,dewp,pres,arad,wtmp,cloro,turb,cvel1,cdir1,cvel2,cdir2,cvel3,cdir3,wvht,wmax,dpd,mwd,spred,bhead])
    data = data.transpose()

#    stop
    data1=sorted(data, key=operator.itemgetter(1,4))

    header = "epoca,lat,lon,sensor00,year,month,day,hour,minute,wspd1,gust1,wdir1,wspd2,gust2,wdir2,battery,flood,atmp,humi,dewp,pres,arad,wtmp,cloro,turb,cvel1,cdir1,cvel2,cdir2,cvel3,cdir3,wvht,wmax,dpd,mwd,spred,bhead"

    n=0
    kk=0
    while n==0:
        kk+=1
        n=1
        c,i=0,0
        for w in range(len(epoca)):
            if i<=(len(epoca)-2):
                if epoca[i]==epoca[i+1]:
                    n=0
                    if sensor00[i]==sensor00[i+1]:
                        for ii in range(len(variables)):
                            exec("%s[c]=%s[i]"% (variables[ii],variables[ii]))
                        c=c+1
                        i=i+2
                    else:
                        for ii in range(len(varfinal1)):
                            exec("%s[c]=%s[i]"% (varfinal1[ii],varfinal1[ii]))
                        for ii in range(len(varfinal2)):
                            exec("%s[c]=%s[i+1]"% (varfinal2[ii],varfinal2[ii]))
                        c=c+1
                        i=i+2
                        continue
                else:
                    for ii in range(len(variables)):
                        exec("%s[c]=%s[i]"% (variables[ii],variables[ii]))
                    c=c+1
                    i=i+1
                    continue
            elif i==(len(epoca)-1):
                for ii in range(len(variables)):
                    exec("%s[c]=%s[i]"% (variables[ii],variables[ii]))
                c=c+1
                i=i+1
            else:
                continue
        for ii in range(len(variables)):
            exec("%s=%s[0:c]"% (variables[ii],variables[ii]))
    for ii in range(len(variables)):
        exec("%s=%s[0:c]"% (variables[ii],variables[ii]))

    for i in range(len(epoca)):
        if wdir1[i]!=None or wdir1!=-9999:
            wdir1[i]=float(wdir1[i])
        if wspd1[i]!=None or wspd1!=-9999:
            wspd1[i]=float(wspd1[i])
        if gust1[i]!=None or gust1!=-9999:
            gust1[i]=float(gust1[i])
        if wdir2[i]!=None or wdir2!=-9999:
            wdir2[i]=float(wdir2[i])
        if wspd2[i]!=None or wspd2!=-9999:
            wspd2[i]=float(wspd2[i])
        if gust2[i]!=None or gust2!=-9999:
            gust2[i]=float(gust2[i])
        if wvht[i]!=None or wvht!=-9999:
            wvht[i]=float(wvht[i])
        if wmax[i]!=None or wmax!=-9999:
            wmax[i]=float(wmax[i])
        if dpd[i]!=None or dpd!=-9999:
            dpd[i]=float(dpd[i])
        if mwd[i]!=None or mwd!=-9999:
            mwd[i]=float(mwd[i])
        if pres[i]!=None or pres!=-9999:
            pres[i]=float(pres[i])
        if humi[i]!=None or humi!=-9999:
            humi[i]=float(humi[i])
        if atmp[i]!=None or atmp!=-9999:
            atmp[i]=float(atmp[i])
        if wtmp[i]!=None or wtmp!=-9999:
            wtmp[i]=float(wtmp[i])
        if dewp[i]!=None or dewp!=-9999:
            dewp[i]=float(dewp[i])
        if cvel1[i]!=None or cvel1!=-9999:
            cvel1[i]=float(cvel1[i])
        if cvel2[i]!=None or cvel2!=-9999:
            cvel2[i]=float(cvel2[i])
        if cvel3[i]!=None or cvel3!=-9999:
            cvel3[i]=float(cvel3[i])
        if cdir1[i]!=None or cdir1!=-9999:
            cdir1[i]=float(cdir1[i])
        if cdir2[i]!=None or cdir2!=-9999:
            cdir2[i]=float(cdir2[i])
        if cdir3[i]!=None or cdir3!=-9999:
            cdir3[i]=float(cdir3[i])

    data=[]
    data = np.array([buoy,epoca,lat,lon,sensor00,year,month,day,hour,minute,wspd1,gust1,wdir1,wspd2,gust2,wdir2,battery,flood,atmp,humi,dewp,pres,arad,wtmp,cloro,turb,cvel1,cdir1,cvel2,cdir2,cvel3,cdir3,wvht,wmax,dpd,mwd,spred,bhead])
    data1 = data.transpose()
    data1=sorted(data1, key=operator.itemgetter(0,1))

    header = "epoca,lat,lon,sensor00,year,month,day,hour,minute,wspd1,gust1,wdir1,wspd2,gust2,wdir2,battery,flood,atmp,humi,dewp,pres,arad,wtmp,cloro,turb,cvel1,cdir1,cvel2,cdir2,cvel3,cdir3,wvht,wmax,dpd,mwd,spred,bhead"

    variables1=['buoy','epoca','lat','lon','sensor00','year','month','day','hour','minute','wspd1','gust1','wdir1','wspd2','gust2','wdir2','battery','flood','atmp','humi','dewp','pres','arad','wtmp','cloro','turb','cvel1','cdir1','cvel2','cdir2','cvel3','cdir3','wvht','wmax','dpd','mwd','spred','bhead']
    variables2=['wdir1','wspd1','gust1','wdir2','wspd2','gust2','wvht','wmax','dpd','mwd','pres','humi','atmp','wtmp','dewp','cvel1','cdir1','cvel2','cdir2','cvel3','cdir3']
    variables3=['wdir','wspd','gust','wvht','wmax','dpd','mwd','pres','humi','atmp','wtmp','dewp','cvel1','cdir1','cvel2','cdir2','cvel3','cdir3']


    if int(boias[s][1])==157599:
        sensoresbons=[0,0,0, 1,1,1, 0,0,0,0, 0,0,0,0,0, 0,0,0,0,0,0,0]

    elif int(boias[s][1])==69152:
        sensoresbons=[0,0,0, 0,0,0, 0,0,0,0, 0,0,0,0,0, 0,0,0,0,0,0,0]
#
#    elif int(boias[s][1])==69007:
#        sensoresbons=[0,0,0, 1,1,1, 0,0,0,0, 0,0,0,0,0, 0,0,0,0,0,0,0]
    if len(epoca)>=3:
        (wspd,wdir,gust,wdirflag,wspdflag,gustflag,wvhtflag,wmaxflag,dpdflag,mwdflag,presflag,humiflag,atmpflag,wtmpflag,dewpflag,cvel1flag,cdir1flag,cvel2flag,cdir2flag,cvel3flag,cdir3flag,wdirflagid,wspdflagid,gustflagid,wvhtflagid,wmaxflagid,dpdflagid,mwdflagid,presflagid,humiflagid,atmpflagid,wtmpflagid,dewpflagid,cvel1flagid,cdir1flagid,cvel2flagid,cdir2flagid,cvel3flagid,cdir3flagid)=qualitycontrol_rt(epoca,buoy,lat,lon,sensor00,year,month,day,hour,minute,wspd1,gust1,wdir1,wspd2,gust2,wdir2,battery,flood,atmp,humi,dewp,pres,arad,wtmp,cloro,turb,cvel1,cdir1,cvel2,cdir2,cvel3,cdir3,wvht,wmax,dpd,mwd,spred,bhead,sensoresbons)

        datahora=[]
        for i in range(len(wdir)):
            wspd[i]=float( '%.1f' % ( wspd[i] ) )
            gust[i]=float( '%.1f' % ( gust[i] ) )
            datahora.append(datetime.datetime(int(year[i]),int(month[i]),int(day[i]),int(hour[i])))
            aw=int(year[i])-2002
            if int(boias[s][1])==157599:
                decmag=17.59
                decvar=0.13
            elif int(boias[s][1])==69152:
                decmag=21.08
                decvar=0.09
            elif int(boias[s][1])==69007:
                decmag=21.31
                decvar=0.08
            var=cdir1flag[i]
            if var!=4:
                cdir1[i]=int(arredondar(float(cdir1[i])-(decmag+(decvar*aw))))
                if float(cdir1[i])>360:
                    cdir1[i]=float(cdir1[i])-360
                elif float(cdir1[i])<0:
                    cdir1[i]=float(cdir1[i])+360
            var=cdir2flag[i]
            if var!=4:
                cdir2[i]=int(arredondar(float(cdir2[i])-(decmag+(decvar*aw))))
                if float(cdir2[i])>360:
                    cdir2[i]=float(cdir2[i])-360
                elif float(cdir2[i])<0:
                    cdir2[i]=float(cdir2[i])+360
            var=cdir3flag[i]
            if var!=4:
                cdir3[i]=int(arredondar(float(cdir3[i])-(decmag+(decvar*aw))))
                if float(cdir3[i])>360:
                    cdir3[i]=float(cdir3[i])-360
                elif float(cdir3[i])<0:
                    cdir3[i]=float(cdir3[i])+360
            var=wdirflag[i]
            if var!=4:
                wdir[i]=int(arredondar(float(wdir[i])-(decmag+(decvar*aw))))
                if float(wdir[i])>360:
                    wdir[i]=float(wdir[i])-360
                elif float(wdir[i])<0:
                    wdir[i]=float(wdir[i])+360
            var=mwdflag[i]
            if var!=4:
                mwd[i]=int(arredondar(float(mwd[i])-(decmag+(decvar*aw))))
                if float(mwd[i])>360:
                    mwd[i]=float(mwd[i])-360
                elif float(mwd[i])<0:
                    mwd[i]=float(mwd[i])+360



        header1="id_boia","lat","lon","year","month","day","hour","battery","bhead","wspd","wspdflagid","wdir","wdirflagid","gust","gustflagid","atmp","atmpflagid","pres","presflagid","dewp","dewpflagid","humi","humiflagid","wtmp","wtmpflagid","cvel1","cvel1flagid","cdir1","cdir1flagid","cvel2","cvel2flagid","cdir2","cdir2flagid","cvel3","cvel3flagid","cdir3","cdir3flagid","wvht","wvhtflagid","wmax","wmaxflagid","dpd","dpdflagid","mwd","mwdflagid","spred"
        cabecalho="Longitude,Latitude,Ano,Mes,Dia,Hora,Nivel de bateria da boia (V),Alinhamento da Boia (graus),Velocidade do Vento a 10 metros (m/s),IDENTIFICADOR DO FLAG,Direcao do Vento a 4.7 metros,IDENTIFICADOR DO FLAG,Rajada do Vento a 10 metros (m/s),IDENTIFICADOR DO FLAG,Temperatura do Ar (C),IDENTIFICADOR DO FLAG,Pressao Atmosferica (mb),IDENTIFICADOR DO FLAG,Ponto de Orvalho (C),IDENTIFICADOR DO FLAG,Humidade Relativa,IDENTIFICADOR DO FLAG,Temperatura da Superficie do Mar (C),IDENTIFICADOR DO FLAG,Velocidade da Corrente na profundidade de 6 a 8.5m (mm/s),IDENTIFICADOR DO FLAG,Direcao da Corrente na profundidade de 6 a 8.5m (graus),IDENTIFICADOR DO FLAG,Velocidade da Corrente na profundidade de 8.5 a 11m (mm/s),IDENTIFICADOR DO FLAG,Direcao da Corrente na profundidade de 8.5 a 11m (graus),IDENTIFICADOR DO FLAG,Velocidade da Corrente na profundidade de 11 a 13.5m (mm/s),IDENTIFICADOR DO FLAG,Direcao da Corrente na profundidade de 11 a 13.5m (graus),IDENTIFICADOR DO FLAG,Altura Significativa de Ondas (m),IDENTIFICADOR DO FLAG,Altura Maxima de Ondas (m),IDENTIFICADOR DO FLAG,Periodo de Pico (s),IDENTIFICADOR DO FLAG,Direcao de Ondas media (graus),IDENTIFICADOR DO FLAG,Espalhamento (graus)"
        data = np.array([lat,lon,datahora,battery,bhead,wspd,wspdflagid,wdir,wdirflagid,gust,gustflagid,atmp,atmpflagid,pres,presflagid,dewp,dewpflagid,humi,humiflagid,wtmp,wtmpflagid,cvel1,cvel1flagid,cdir1,cdir1flagid,cvel2,cvel2flagid,cdir2,cdir2flagid,cvel3,cvel3flagid,cdir3,cdir3flagid,wvht,wvhtflagid,wmax,wmaxflagid,dpd,dpdflagid,mwd,mwdflagid,spred])
        data = data.transpose()
        data3=sorted(data, key=operator.itemgetter(2))
        print('inserindo dados no BD')
        alimentarbd(data3,boias[s][0])


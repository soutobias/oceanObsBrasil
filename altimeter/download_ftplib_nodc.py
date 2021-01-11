#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 19:01:11 2019

@author: tobias
"""


import ftplib
import time

# Connection information

def download_ftplib_nodc(datahora1):
    username = ''
    password = ''

    print("teste")
    print(datahora1)
    # Directory and matching information
    directory = 'pub/data.nodc/jason3/ogdr/ogdr/'

    datahora=time.gmtime()
    ano=datahora.tm_year
    dia=datahora.tm_mday
    mes=datahora.tm_mon
    hora=datahora.tm_hour
    ano1=datahora1.tm_year
    dia1=datahora1.tm_mday
    mes1=datahora1.tm_mon
    hora1=datahora1.tm_hour

    if dia<10:
        dia="0"+str(dia)
    if dia1<10:
        dia1="0"+str(dia1)
    if mes<10:
        mes="0"+str(mes)
    if mes1<10:
        mes1="0"+str(mes1)

    dia=str(dia)
    mes=str(mes)
    dia1=str(dia1)
    mes1=str(mes1)

    ftp = ftplib.FTP('ftp.nodc.noaa.gov')
    ftp.login(username, password)
    ftp.cwd(directory)

    dir_list = []
    ftp.dir(dir_list.append)
    directory2 = dir_list[-1].split(' ')[-1]
    print(directory)
    ftp.cwd(directory2)

    if dia1!=dia:
        hour=0
        while hour<=hora:
            if hour<10:
                valor="0"+str(hour)
            else:
                valor=str(hour)
            filematch = "JA3_OPN_*"+str(ano)+mes+dia+"_"+valor+"*.nc"
            for filename in ftp.nlst(filematch):
                fhandle = open(filename, 'wb')
                print ('Getting ' + filename)
                ftp.retrbinary('RETR ' + filename, fhandle.write)
                fhandle.close()
                print(filename)
            hour=hour+1

        while hora1<=23:
            if hora1<10:
                valor="0"+str(hora1)
            else:
                valor=str(hora1)
            filematch = "JA3_OPN_*_*_"+str(ano)+mes1+dia1+"_"+valor+"*_*_*.nc"
            print(ftp.nlst(filematch))
            for filename in ftp.nlst(filematch):
                fhandle = open(filename, 'wb')
                print ('Getting ' + filename)
                ftp.retrbinary('RETR ' + filename, fhandle.write)
                fhandle.close()
                print(filename)
            hora1=hora1+1

    else:
        hour1=hora1
        while hour1<=hora:
            if hour1<10:
                valor="0"+str(hour1)
            else:
                valor=str(hour1)
            filematch = "JA3_OPN_*_*_"+str(ano)+mes+dia+"_"+valor+"*_*_*.nc"
            for filename in ftp.nlst(filematch):
                fhandle = open(filename, 'wb')
                print ('Getting ' + filename)
                ftp.retrbinary('RETR ' + filename, fhandle.write)
                fhandle.close()
                print(filename)
            hour1=hour1+1
    return


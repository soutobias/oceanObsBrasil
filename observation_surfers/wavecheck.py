#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 13:22:52 2019

@author: producao
"""

from bs4 import BeautifulSoup
import requests
import numpy as np
import time
import datetime
import operator

import mysql.connector as MySQLdb

import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def alimentarbd(Data1,boia):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    cur.execute("SELECT datahora FROM wavecheck WHERE esta_wave=%s\
    ORDER BY datahora DESC limit 20" % Data1[0][0])
    for row in cur.fetchall():
        c1.append(row)
    if c1!=[]:
        for i in range(len(Data1)):
            if Data1[i][1]>max(c1)[0]:
                sql = "INSERT INTO wavecheck (esta_wave,datahora,altura,formacao,\
                direcao,observacao)\
                VALUES (%s, '%s', %s, '%s','%s', '%s')" % \
                ((Data1[i][0]),(Data1[i][1]),(Data1[i][2]),(Data1[i][3]),\
                (Data1[i][4]),(Data1[i][5]))
                cur.execute(sql)
                db.commit()
            else: #inserir update
                sql = "UPDATE wavecheck SET esta_wave=%s,datahora='%s',altura=%s,\
                formacao='%s',direcao='%s',observacao='%s'\
                WHERE esta_wave=%s and datahora='%s'" % \
                ((Data1[i][0]),(Data1[i][1]),(Data1[i][2]),(Data1[i][3]),\
                (Data1[i][4]),(Data1[i][5]),(Data1[i][0]),(Data1[i][1]))
                cur.execute(sql)
                db.commit()
    else:
        for i in range(len(Data1)):
            sql = "INSERT INTO wavecheck (esta_wave,datahora,altura,formacao,\
            direcao,observacao)\
            VALUES (%s, '%s', %s, '%s','%s', '%s')" % \
            ((Data1[i][0]),(Data1[i][1]),(Data1[i][2]),(Data1[i][3]),\
            (Data1[i][4]),(Data1[i][5]))
            cur.execute(sql)
            db.commit()

    cur.close()
    db.close()


def buscabd():

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    rico=[]
    cur.execute("SELECT id, nome, site FROM wavecheck_estacao")
    for row in cur.fetchall():
        rico.append(row)

    cur.close()
    db.close()

    return rico


wave=buscabd()

datahora=time.gmtime(time.time())
ano2=(datahora.tm_year)
mes2=(datahora.tm_mon)
dia2=(datahora.tm_mday)
dia=datetime.date(ano2, mes2, dia2)


for i in range(len(wave)):
    esta_id=[]
    altura=[]
    direcao=[]
    observacao=[]
    formacao=[]
    datahora=[]

    resp=requests.get(wave[i][2])


    soup=BeautifulSoup(resp.text,'html.parser')
    l=soup.find("p", {"class": "alerta-pico-desatualizado"})
    if l==None:
        print(wave[i][1])
        print("Tem dados para esse pico")
        # l is the list which contains all the text i.e news
        l=soup.find("td", {"id": "forecast_wave_size"}).get_text(strip=True)
        try:
            [k1,k2]=l.split("m")
            altura.append(float(k1))
        except:
            altura.append(0)
        l=soup.find("div", {"style": "line-height: 14px;"}).get_text(strip=True)
        formacao.append(str(l))

        l=soup.find("td", {"id": "forecast_wave_direction"}).get_text(strip=True)
        direcao.append(str(l))

        l=soup.find("img", {"class": "avatar avatar-50 wp-user-avatar-50wp-user-avatar wp-user-avatar-50px alignnone photo avatar-default"}).get_text(strip=True)
        l=str(l)
        l=l.replace("\n","")
        observacao.append(deEmojify(str(l)))

        esta_id.append(wave[i][0])
        datahora.append(dia)
        data = np.array([esta_id,datahora,altura,formacao,direcao,observacao])
        data3 = data.transpose()
        alimentarbd(data3,wave[i][0])


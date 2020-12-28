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

import pandas as pd
from pandas.io import sql
import sqlalchemy

import sys
import os

sys.path.append(os.environ['HOME'])
import user_config

sys.path.append(user_config.path )
sys.path.append(user_config.path + "/database" )

import db_function as db

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')


wave = db.select_station(["institution"], ["wavecheck"])

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

    resp=requests.get(wave["url"][i])


    soup=BeautifulSoup(resp.text,'html.parser')
    l=soup.find("p", {"class": "alerta-pico-desatualizado"})
    if l==None:
        print([1])
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

        datahora.append(dia)
        data = np.array([datahora, altura, direcao])
        data3 = data.transpose()

        df = pd.DataFrame(data3)

        df.columns = ['date_time', 'swvht', 'wvdir']

        df = df.replace(to_replace =['None', 'NULL', ' ', ''], value =np.nan)

        station = wave["id"][i]
        df['station_id'] = station

        db.delete_old_data(df, station)
        db.insert_new_data(df)

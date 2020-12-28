# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 21:14:07 2019

@author: tobia
"""
from bs4 import BeautifulSoup
import requests
import time
import datetime
import numpy as np
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


site='https://ricosurf.com.br/boletim-das-ondas/rio-janeiro'

resp=requests.get(site)

soup=BeautifulSoup(resp.text,'html.parser')

#text_file = open('Output.txt', "w")
#text_file.write(str(soup))
#text_file.close()
picosatuais=[]
l=soup.find_all('a', attrs={'class': 'beach-peak col-xxs-12 col-xs-6 col-md-4'})
for i in l:
    l1=i.find('div', attrs={'class': 'place'}).get_text(strip=True)
    picosatuais.append(l1)

#l=soup.find_all('a', attrs={'class': 'beach-peak disabled col-xxs-12 col-xs-6 col-md-4'})
#for i in l:
#    l1=i.find('div', attrs={'class': 'place'}).get_text(strip=True)
#    nome.append(l1)



datahora=time.gmtime(time.time())
ano2=(datahora.tm_year)
mes2=(datahora.tm_mon)
dia2=(datahora.tm_mday)
dia=datetime.date(ano2, mes2, dia2)

rico = db.select_station(["institution"], ["ricosurf"])

wvht,periodo,tsm,direcao,datahora=[],[],[],[],[]

for i in range(len(rico)):
    wvht,periodo,tsm,direcao,datahora=[],[],[],[],[]
    for ii in range(len(picosatuais)):
        if rico.name[i]==picosatuais[ii]:
            print(rico.name[i])
            resp=requests.get(rico.url[i])
            soup=BeautifulSoup(resp.text,'html.parser')
            l=soup.find("div", {"class": "h5 text-primary margin-xxs-bottom"}).get_text(strip=True)
            kk=l
            kk=kk.replace(",", ".")
            wvht.append(float(kk[0:-1]))
            l=soup.find_all('div', attrs={'class': 'h5 no-margin text-primary'})
            kk=l[0].get_text(strip=True)
            kk=kk.replace(",", ".")
            periodo.append(float(kk[0:-1]))
            kk=l[1].get_text(strip=True)
            tsm.append(float(kk[0:-2]))

            l=soup.find("div", {"class": "small line-height-xs"}).get_text(strip=True)
            direcao.append(l)
            datahora.append(dia)
            data = np.array([datahora,wvht,periodo,tsm,direcao])
            data3 = data.transpose()

            df = pd.DataFrame(data3)

            df.columns = ['date_time', 'swvht', 'tp', 'sst', 'wvdir']

            df = df.replace(to_replace =['None', 'NULL', ' ', ''], value =np.nan)

            station = rico["id"][i]
            df['station_id'] = station

            db.delete_old_data(df, station)
            db.insert_new_data(df)

            continue


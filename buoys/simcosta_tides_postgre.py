"""
Created on Tue Feb 12 23:34:44 2019
@author: tobia
"""

import psutil
import time
import datetime
import operator
import urllib.request, json
import pandas as pd

import numpy as np

from pandas.io import sql
import sqlalchemy

import sys
import os

sys.path.append(os.environ['HOME'])
import user_config

sys.path.append(user_config.path )
sys.path.append(user_config.path + "/database" )

import db_function as db

def remove_dup_columns(frame):
     keep_names = set()
     keep_icols = list()
     for icol, name in enumerate(frame.columns):
          if name not in keep_names:
               keep_names.add(name)
               keep_icols.append(icol)
     return frame.iloc[:, keep_icols]


boias_simcosta = db.select_station(["institution", "data_type"], ["simcosta", "tide"])
tempoini=str(int(np.ceil(time.time()-3600*24)))
tempofim=str(int(np.ceil(time.time())))

for i in range(len(boias_simcosta['url'])):
    print(i)
    with urllib.request.urlopen("http://simcosta.furg.br/api/maregrafo_data?boiaID="+str(boias_simcosta['url'][i])+"&type=json&time1="+tempoini+"&time2="+tempofim+"&params=water_l1") as url:
        data = json.loads(url.read().decode())
        data = pd.DataFrame(data)
    with urllib.request.urlopen("http://simcosta.furg.br/api/maregrafo_data?boiaID="+str(boias_simcosta['url'][i])+"&type=json&time1="+tempoini+"&time2="+tempofim+"&params=relative_humidity,wind_direction,wind_speed,dew_point,atm_pressure,air_temp") as url:
        data1 = json.loads(url.read().decode())
        data1 = pd.DataFrame(data1)

    result = pd.concat([data,  data1], axis=1, join='inner')

    result = remove_dup_columns(result)

    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    if len(result) == 0:
        print ("Nao ha dados para essa boia")
    else:
        result['datahora'] = pd.to_datetime(result.iloc[:,0:6])

        del result['YEAR']
        del result['MONTH']
        del result['DAY']
        del result['HOUR']
        del result['MINUTE']
        del result['SECOND']

        result.columns = ['water_level', 'wspd', 'wdir', 'atmp', 'rh', 'dewpt', 'pres', 'date_time']

        result = result.replace(to_replace =['None', 'NULL', ' ', ''],
                                value =np.nan)

        # for key in result.keys():
        #   result[key] = result[key].astype(float)

        station = boias_simcosta['id'][i]
        result['station_id'] = station

        db.delete_old_data(result, station)
        db.insert_new_data(result)

        print('dados da boia simcosta '+ boias_simcosta['name'][i]+' inseridos no banco')

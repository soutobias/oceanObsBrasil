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


boias_simcosta = db.select_station(["institution", "type"], ["simcosta", "buoy"])
tempoini=str(int(np.ceil(time.time()-3600*24)))
tempofim=str(int(np.ceil(time.time())))

for i in range(len(boias_simcosta['url'])):
    print(i)
    with urllib.request.urlopen("http://simcosta.furg.br/api/metereo_data?boiaID="+str(boias_simcosta['url'][i])+"&type=json&time1="+tempoini+"&time2="+tempofim+"&params=Average_wind_direction_N,Last_sampling_interval_gust_speed,Average_Dew_Point,Average_Pressure,Solar_Radiation_Average_Reading,Average_Air_Temperature,Instantaneous_Humidity,Average_Humidity,Average_wind_speed") as url:
        data = json.loads(url.read().decode())
        data = pd.DataFrame(data)
    with urllib.request.urlopen("http://simcosta.furg.br/api/oceanic_data?boiaID="+str(boias_simcosta['url'][i])+"&type=json&time1="+tempoini+"&time2="+tempofim+"&params=H10,HAvg,Hsig_Significant_Wave_Height_m,HM0,Mean_Wave_Direction_deg,Hmax_Maximum_Wave_Height_m,ZCN,Tp5,TAvg,T10,Tsig,Mean_Spread_deg,TP_Peak_Period_seconds,Average_Salinity,Average_Temperature_deg_C,Average_Temperature_C,Average_CDOM_QSDE,Average_Chlorophyll_Fluorescence,Average_Dissolved_Oxygen,Average_Nephelometric_Turbidity_Unit_NTU,Cell_Average_Direction_N,Cell_Average_Magnitude_mm_s") as url:
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
        del result['Hmt']
        del result['Avg_Wnd_Dir']
        del result['M_Decl']
        del result['Avg_W_Tmp1']
        del result['Avg_Sal']
        del result['Avg_Spre_N']
        del result['Avg_Wv_Dir']
        del result['Avg_Cel1_Mag']
        del result['Avg_Cel1_Dir']
        del result['Avg_Cel1_Dir_N']
        del result['Avg_Turb']
        del result['Avg_Chl']
        del result['Avg_DO']
        del result['ZCN']
        del result['HM0']
        del result['TAvg']
        del result['Tp5']
        del result['T10']
        del result['HAvg']
        del result['Tsig']
        del result['CDOM']
        del result['H10']
        del result['Avg_Sol_Rad']

        result.columns = ['pres', 'atmp', 'rh', 'dewpt', 'wspd', 'wdir', 'gust', 'swvht', 'mxwvht', 'tp', 'sst', 'wvspread', 'wvdir', 'date_time']

        result = result.replace(to_replace =['None', 'NULL', ' ', ''],
                                value =np.nan)

        # for key in result.keys():
        #   result[key] = result[key].astype(float)

        station = boias_simcosta['id'][i]
        result['station_id'] = station

        db.delete_old_data(result, station)
        db.insert_new_data(result)

        print('dados da boia simcosta '+ boias_simcosta['name'][i]+' inseridos no banco')

"""
Created on Tue Feb 12 23:34:44 2019
@author: tobia
"""

import psutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import os
import time
import datetime
import operator
import numpy as np
import urllib.request, json
import pandas as pd

import mysql.connector as MySQLdb
import numpy as np

from pandas.io import sql
import sqlalchemy

import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )

def boiasfuncionando():

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    cur.execute("SELECT id, estacao FROM simcosta_estacao \
    ORDER BY id")
    for row in cur.fetchall():
        c1.append(row)

    return c1

def remove_dup_columns(frame):
     keep_names = set()
     keep_icols = list()
     for icol, name in enumerate(frame.columns):
          if name not in keep_names:
               keep_names.add(name)
               keep_icols.append(icol)
     return frame.iloc[:, keep_icols]

boias_simcosta = boiasfuncionando()

# x = pd.read_csv('simcosta_estacao.csv')

# x.index = x.id
# del x['id']

# con = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
#                                         format(user_config.username,
#                                             user_config.password,
#                                             user_config.host,
#                                             user_config.database))

# x.to_sql(con=con, name='simcosta_estacao', if_exists='replace')


tempoini=str(int(np.ceil(time.time()-3600*24*365*2)))
tempofim=str(int(np.ceil(time.time())))

data01,data02,data03=[],[],[]
for i in boias_simcosta:
    print(i)
    with urllib.request.urlopen("http://simcosta.furg.br/api/metereo_data?boiaID="+str(i[0])+"&type=json&time1="+tempoini+"&time2="+tempofim+"&params=Average_wind_direction_N,Last_sampling_interval_gust_speed,Average_Dew_Point,Average_Pressure,Solar_Radiation_Average_Reading,Average_Air_Temperature,Instantaneous_Humidity,Average_Humidity,Average_wind_speed") as url:
        data = json.loads(url.read().decode())
        data = pd.DataFrame(data)
    with urllib.request.urlopen("http://simcosta.furg.br/api/oceanic_data?boiaID="+str(i[0])+"&type=json&time1="+tempoini+"&time2="+tempofim+"&params=H10,HAvg,Hsig_Significant_Wave_Height_m,HM0,Mean_Wave_Direction_deg,Hmax_Maximum_Wave_Height_m,ZCN,Tp5,TAvg,T10,Tsig,Mean_Spread_deg,TP_Peak_Period_seconds,Average_Salinity,Average_Temperature_deg_C,Average_Temperature_C,Average_CDOM_QSDE,Average_Chlorophyll_Fluorescence,Average_Dissolved_Oxygen,Average_Nephelometric_Turbidity_Unit_NTU,Cell_Average_Direction_N,Cell_Average_Magnitude_mm_s") as url:
        data1 = json.loads(url.read().decode())
        data1 = pd.DataFrame(data1)

    result = pd.concat([data,  data1], axis=1, join='inner')

    result = remove_dup_columns(result)

    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    result['datahora'] = pd.to_datetime(result.iloc[:,0:6])
    result.index = result['datahora']



    del result['datahora']
    del result['YEAR']
    del result['MONTH']
    del result['DAY']
    del result['HOUR']
    del result['MINUTE']
    del result['SECOND']

    result = result.replace(to_replace =['None', 'NULL', ' ', ''],
                            value =np.nan)

    for key in result.keys():
      result[key] = result[key].astype(float)

    result['id'] = i[0]

    con = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                            format(user_config.username,
                                                user_config.password,
                                                user_config.host,
                                                user_config.database))

    result.to_sql(con=con, name='simcosta', if_exists='append')
    print('dados da boia simcosta '+i[1]+' inseridos no banco')

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

def deleta_dado(tempoini,boia):

    x=time.gmtime(int(tempoini))
    tempo1=str(x.tm_year)+'-'+str(x.tm_mon).zfill(2)+'-'+str(x.tm_mday).zfill(2)+' 00:00:00'

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    cur.execute("DELETE FROm maregrafos WHERE datahora>='%s' AND id = '%s'"% (tempo1,boia))
    # cur.execute("SELECT wmo FROm deriva_estacao")
    db.commit()
    cur.close()
    db.close()

    return

def boiasfuncionando():

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    cur.execute("SELECT id, estacao FROM mare_estacao WHERE instituicao = 'simcosta'\
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


tempoini=str(int(np.ceil(time.time()-3600*24)))
tempofim=str(int(np.ceil(time.time())))

for i in boias_simcosta:
    print(i)
    with urllib.request.urlopen("http://simcosta.furg.br/api/maregrafo_data?boiaID="+str(i[0])+"&type=json&time1="+tempoini+"&time2="+tempofim+"&params=water_l1") as url:
        data = json.loads(url.read().decode())
        data = pd.DataFrame(data)
    with urllib.request.urlopen("http://simcosta.furg.br/api/maregrafo_data?boiaID="+str(i[0])+"&type=json&time1="+tempoini+"&time2="+tempofim+"&params=relative_humidity,wind_direction,wind_speed,dew_point,atm_pressure,air_temp") as url:
        data1 = json.loads(url.read().decode())
        data1 = pd.DataFrame(data1)

    result = pd.concat([data,  data1], axis=1, join='inner')

    result = remove_dup_columns(result)

    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    if len(result) == 0:
        print ("Nao ha dados para essa boia")
    else:
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


        deleta_dado(tempoini,i[0])

        con = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                format(user_config.username,
                                                    user_config.password,
                                                    user_config.host,
                                                    user_config.database))

        result.to_sql(con=con, name='maregrafos', if_exists='append')
        print('dados do maregrafo '+i[1]+' inseridos no banco')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 22:14:53 2020

@author: tobias
"""

from erddapy import ERDDAP
import time
import pandas as pd
from pandas.io import sql
import sqlalchemy
from pathlib import Path
from sqlalchemy import create_engine
import user_config
import mysql.connector as MySQLdb

import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )


def consulta_estacao():

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    wmo_mb,satelite=[],[]
    cur.execute("SELECT wmo,satelite FROm deriva_estacao")
    # cur.execute("SELECT wmo FROm deriva_estacao")

    for row in cur.fetchall():
        if row[0]!=None:
            wmo_mb.append(str(row[0]))
            satelite.append(row[1])

    cur.close()
    db.close()

    return wmo_mb,satelite

def consulta_dado():

    x=time.gmtime(time.time()-3600*48)
    tempo1=str(x.tm_year)+'-'+str(x.tm_mon).zfill(2)+'-'+str(x.tm_mday).zfill(2)+' 00:00:00'

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    tempo,id1,lat,lon,sst,pres=[],[],[],[],[],[]

    cur.execute("SELECT * FROm deriva WHERE tempo>='%s' ORDER BY tempo"% tempo1)
    # cur.execute("SELECT wmo FROm deriva_estacao")

    for row in cur.fetchall():
        tempo.append(row[0])
        id1.append(row[1])
        lat.append(row[2])
        lon.append(row[3])
        sst.append(row[4])
        pres.append(row[5])

    cur.close()
    db.close()

    return tempo,id1,lat,lon,sst,pres

def deleta_dado():

    x=time.gmtime(time.time()-3600*48)
    tempo1=str(x.tm_year)+'-'+str(x.tm_mon).zfill(2)+'-'+str(x.tm_mday).zfill(2)+' 00:00:00'

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    cur.execute("DELETE FROm deriva WHERE tempo>='%s'"% tempo1)
    # cur.execute("SELECT wmo FROm deriva_estacao")
    db.commit()
    cur.close()
    db.close()

    return

#baixar dados das boias de deriva já lançadas pela marinha
[wmo_mb,sat]=consulta_estacao()

x=time.gmtime(time.time()-3600*24)



#descrição das variáveis para baixar dados do erddap
e = ERDDAP(
  server='http://osmc.noaa.gov/erddap',
  protocol='tabledap',
)

e.response = 'csv'
e.dataset_id = 'OSMC_30day'
e.constraints = {
    'time>=': str(x.tm_year)+"-"+str(x.tm_mon).zfill(2)+"-"+str(x.tm_mday).zfill(2)+"T"+str(x.tm_hour).zfill(2)+":00:00Z",
    'longitude>=': -80.0,
    'longitude<=': 80.0,
    'platform_type=': "DRIFTING BUOYS (GENERIC)"
}
e.variables = [
    'platform_code',
    'time',
    'latitude',
    'longitude',
    'sst',
    'slp',
]

df = e.to_pandas()



#trabalhando com os dados baixados do erddap
df.columns = ['id', 'tempo','lat','lon','sst','pres']

df.id=df.id.apply(str)
k=df[df.id.str.contains('|'.join(wmo_mb))]

dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ')

k['tempo'] = pd.to_datetime(k['tempo'])

k = k.set_index('tempo')

k.index = k.index.strftime('%Y-%m-%d %H:%M:%S')

for i in range(len(wmo_mb)):
    k.id[k.id==(wmo_mb[i])]=sat[i]

k.id=k.id.apply(str)

k['lat']=k.lat.round(4)
k['lon']=k.lon.round(4)
k['sst']=k.sst.round(3)
k['pres']=k.pres.round(1)


#baixando dados do banco de dados já exixtente para concatenar com os dados baixados do erddap
[tempo,id1,lat,lon,sst,pres]=consulta_dado()

df1 = pd.DataFrame({'tempo': tempo, 'id': id1, 'lat': lat, 'lon': lon, 'sst': sst, 'pres': pres})
df1 = df1.set_index('tempo')

if len(df1)!=0:
    df1.index = df1.index.strftime('%Y-%m-%d %H:%M:%S')

    df1.id=df1.id.apply(str)

    df1['lat']=df1.lat.round(4)
    df1['lon']=df1.lon.round(4)
    df1['sst']=df1.sst.round(3)
    df1['pres']=df1.pres.round(1)


    #concatenando dataframes
    frames = [k, df1]
    result = pd.concat(frames)

else:
    result=k

print('dados baixados do ERDDAP')
#classificando os dados
result.sort_values("tempo", inplace = True)

# result.to_csv('arquivo1.csv')
# dropping ALL duplicate values
result=result.drop_duplicates(subset=['id','lat','lon','sst','pres'],keep='first')

deleta_dado()

con = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                format(user_config.username, user_config.password,
                                                      user_config.host, user_config.database))

result.to_sql(con=con, name='deriva', if_exists='append')


print('dados copiados para BD')
print('ok')

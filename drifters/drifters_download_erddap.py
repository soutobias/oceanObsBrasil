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
import MySQLdb


def bancodedados():

    local="pnboia-uol.mysql.uhserver.com"
    usr="pnboia"
    password="Ch@tasenha1"
    data_base="pnboia_uol"

    return local,usr,password,data_base

def consulta_estacao():

    x=time.gmtime(time.time()-3600*24*100)
    
    (local,usr,password,data_base)=bancodedados()
    
    db = MySQLdb.connect(local,usr,password,data_base)
    
    cur=db.cursor()
    
    tempo=str(x.tm_year-5)+'-06-01 00:00:00'
    wmo_mb,satelite=[],[]
    cur.execute("SELECT wmo,satelite FROm deriva_estacao where data >'%s'"% tempo)
    # cur.execute("SELECT wmo FROm deriva_estacao")

    for row in cur.fetchall():
        if row[0]!=None:
            wmo_mb.append(row[0])
            satelite.append(row[1])
    
    cur.close()
    db.close()

    return wmo_mb,satelite

[wmo_mb,sat]=consulta_estacao()

x=time.gmtime(time.time()-3600*24*100)

for i in range(len(wmo_mb)):

    print(wmo_mb[i])

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
        'platform_type=': "DRIFTING BUOYS (GENERIC)",
        'platform_code=': str(wmo_mb[i]),
    }        
    e.variables = [
        'platform_code',
        'time',
        'latitude',
        'longitude',
        'sst',
        'slp',
    ]
    try:
        df = e.to_pandas()
    except:
        print("Não há dados para o WMO "+str(wmo_mb[i]))

    try:       
        df.columns = ['id', 'tempo','lat','lon','sst','pres']

        df.id=sat[i]
        
        dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ')
        
        df['tempo'] = pd.to_datetime(df['tempo'])
        
        df = df.set_index('tempo')
        
        df['lat']=df.lat.round(4)
        df['lon']=df.lon.round(4)
        df['sst']=df.sst.round(3)
        df['pres']=df.pres.round(1)
        df.index = df.index.strftime('%Y-%m-%d %H:%M:%S')

        df.sort_values("tempo", inplace = True)
        df=df.drop_duplicates(subset=['id','lat','lon','sst','pres'],keep='first')

        
        (local,usr,password,data_base)=bancodedados()
        
        #    con = MySQLdb.connect(local,usr,password,data_base)
        
        con = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                       format(usr, password, 
                                                              local, data_base))
        
        df.to_sql(con=con, name='deriva', if_exists='append')
    except:
        print("Outro erro")
    

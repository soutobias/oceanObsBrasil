# -*- coding: utf-8 -*-

from netCDF4 import Dataset
import numpy as np
import re
import time
import glob
import datetime
from math import radians, cos, sin, asin, sqrt
import mysql.connector as MySQLdb
from download_ftplib_nodc import *

import pandas as pd
import sys
import os

sys.path.append(os.environ['HOME'])
import user_config

sys.path.append(user_config.path )
sys.path.append(user_config.path + "/database" )
sys.path.append(user_config.path + "/altimeter" )


import db_function as db

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # 6367 km is the radius of the Earth
    km = 6367 * c
    return km


# ABRINDO ARQUIVO COM A POSICAO DAS BOIAS DO PNBOIA
datahora1=time.gmtime(time.time()-3600*12)
download_ftplib_nodc(datahora1)

lat01=-35.8333
lat02=7
lon01=-55.20
lon02=-20

#VARIAVEL DOS ARQUIVOS NETCDF. CRIADO PARA FACILITAR OS LOOPS POSTERIORES
variables=['tempo','lat','lon','swh_ku','swh_ku_mle3','wind_speed_alt','wind_speed_alt_mle3']

#CRIANDO MATRIZES VAZIAS PARA CADA ESTACAO PARA SEREM COMPLETADAS POSTERIORMENTE
for i in range(len(variables)):
    exec("%s_99=[]"% (variables[i]))


#ABRINDO CONJUNTO DE ARQUIVOS NETCDF BAIXADO DO FTP. OS QUATRO ULTIMOS NUMEROS
#REPRESENTADOS ABAIXO (0701, POR EXEMPLO), REPRESENTAM O MES E O DIA DOS DADOS

#glob_pattern = "GW_L2P_ALT_JAS2_NRT_20161024*.nc"

file_list=[]
glob_pattern = "*JA3*.nc"
if glob.glob(glob_pattern)!=[]:
    file_list.append(glob.glob(glob_pattern))

for i6 in range(len(file_list)):
    for f in  file_list[i6]:
        print(f)
        NC = Dataset(f,'r')
        tempo = NC.groups['data_01'].variables['time']
        lat = NC.groups['data_01'].variables['latitude']
        lon = NC.groups['data_01'].variables['longitude']
        wind_speed_alt = NC.groups['data_01'].variables['wind_speed_alt']
        wind_speed_alt_mle3 = NC.groups['data_01'].variables['wind_speed_alt_mle3']
        swh_ku = NC.groups['data_01'].groups["ku"].variables['swh_ocean']
        swh_ku_mle3 = NC.groups['data_01'].groups["ku"].variables['swh_ocean_mle3']

        #ARTIMANHAS PARA ACELERAR A ROTINA. LIMITES ESCOLHIDOS DE MODO QUE NAO SE BUSQUE ARQUIVOS QUE NAO TENHA DADOS PARA AS BOIAS
        f1=np.where((np.array([lat])<lat02) & (np.array([lat])>lat01))
        print(f1[1])
        lon00=[]
        for we in f1[1]:
            lon00.append(lon[we])
        #OUTRAS ARTIMANHAS PARA ACELERAR A ROTINA
        if lon00!=[]:
            print(min(lon00))
            if max(lon00)<lon01+360 and min(lon00)>lon02+360:
                qr=1
            else:
                for i in range(len(lat)):
                    if lat[i]>=lat01 and lat[i]<=lat02 and lon[i]>=lon01+360 and lon[i]<=lon02+360:
                        print("ok")
                        if np.ma.is_masked(swh_ku[i])==False:
                            for i2 in range(len(variables)):
                                if variables[i2]=="lat" or variables[i2]=="tempo":
                                    exec("%s_99.append(float(%s[i]))"% (variables[i2],variables[i2]))
                                elif variables[i2]=="lon":
                                    if lon[i]>180:
                                        exec("%s_99.append(float(%s[i])-360)"% (variables[i2],variables[i2]))
                                    else:
                                        exec("%s_99.append(float(%s[i]))"% (variables[i2],variables[i2]))
                                else:
                                    exec("%s_99.append(%s[i])"% (variables[i2],variables[i2]))
        NC.close()


#CONVERTENDO O TEMPO DOS DADOS DE SATELITE PARA ANO, MES. DIA, HORA, MIN
x=(datetime.datetime(2000,1,1) - datetime.datetime(1970,1,1)).total_seconds()

year=[0]*len(lat_99)
month=[0]*len(lat_99)
day=[0]*len(lat_99)
hour=[0]*len(lat_99)
minute=[0]*len(lat_99)
for i in range(len(lat_99)):
    [year[i],month[i],day[i],hour[i],minute[i],s,dd,ddd,dddd]=time.gmtime(int(tempo_99[i])+x)

lon_med,lat_med,swh_med,swh_mle3_med,tempo_med,year_med,month_med,day_med,hour_med,minute_med=[],[],[],[],[],[],[],[],[],[]

c=0
for i in range(len(lon_99)-12):
    if c+12<len(lon_99) and tempo_99[c+12]-tempo_99[c]<60:
        lon_med.append(lon_99[c])
        lat_med.append(lat_99[c])
        swh_med.append(swh_ku_99[c])
        swh_mle3_med.append(swh_ku_mle3_99[c])
        tempo_med.append(tempo_99[c])
        year_med.append(year[c])
        month_med.append(month[c])
        day_med.append(day[c])
        hour_med.append(hour[c])
        minute_med.append(minute[c])
        c+=13
    elif c+11<len(lon_99) and tempo_99[c+11]-tempo_99[c]<60:
        lon_med.append(lon_99[c])
        lat_med.append(lat_99[c])
        swh_med.append(swh_ku_99[c])
        swh_mle3_med.append(swh_ku_mle3_99[c])
        tempo_med.append(tempo_99[c])
        year_med.append(year[c])
        month_med.append(month[c])
        day_med.append(day[c])
        hour_med.append(hour[c])
        minute_med.append(minute[c])
        c+=12
    elif c+10<len(lon_99) and tempo_99[c+10]-tempo_99[c]<60:
        lon_med.append(lon_99[c])
        lat_med.append(lat_99[c])
        swh_med.append(swh_ku_99[c])
        swh_mle3_med.append(swh_ku_mle3_99[c])
        tempo_med.append(tempo_99[c])
        year_med.append(year[c])
        month_med.append(month[c])
        day_med.append(day[c])
        hour_med.append(hour[c])
        minute_med.append(minute[c])
        c+=11
    elif c+9<len(lon_99) and tempo_99[c+9]-tempo_99[c]<60:
        lon_med.append(lon_99[c])
        lat_med.append(lat_99[c])
        swh_med.append(swh_ku_99[c])
        swh_mle3_med.append(swh_ku_mle3_99[c])
        tempo_med.append(tempo_99[c])
        year_med.append(year[c])
        month_med.append(month[c])
        day_med.append(day[c])
        hour_med.append(hour[c])
        minute_med.append(minute[c])
        c+=10
    elif c+8<len(lon_99) and tempo_99[c+8]-tempo_99[c]<60:
        lon_med.append(lon_99[c])
        lat_med.append(lat_99[c])
        swh_med.append(swh_ku_99[c])
        swh_mle3_med.append(swh_ku_mle3_99[c])
        tempo_med.append(tempo_99[c])
        year_med.append(year[c])
        month_med.append(month[c])
        day_med.append(day[c])
        hour_med.append(hour[c])
        minute_med.append(minute[c])
        c+=9
    elif c+7<len(lon_99) and tempo_99[c+7]-tempo_99[c]<60:
        lon_med.append(lon_99[c])
        lat_med.append(lat_99[c])
        swh_med.append(swh_ku_99[c])
        swh_mle3_med.append(swh_ku_mle3_99[c])
        tempo_med.append(tempo_99[c])
        year_med.append(year[c])
        month_med.append(month[c])
        day_med.append(day[c])
        hour_med.append(hour[c])
        minute_med.append(minute[c])
        c+=8
    elif c+6<len(lon_99) and tempo_99[c+6]-tempo_99[c]<60:
        lon_med.append(lon_99[c])
        lat_med.append(lat_99[c])
        swh_med.append(swh_ku_99[c])
        swh_mle3_med.append(swh_ku_mle3_99[c])
        tempo_med.append(tempo_99[c])
        year_med.append(year[c])
        month_med.append(month[c])
        day_med.append(day[c])
        hour_med.append(hour[c])
        minute_med.append(minute[c])
        c+=7
    elif c+5<len(lon_99) and tempo_99[c+5]-tempo_99[c]<60:
        lon_med.append(lon_99[c])
        lat_med.append(lat_99[c])
        swh_med.append(swh_ku_99[c])
        swh_mle3_med.append(swh_ku_mle3_99[c])
        tempo_med.append(tempo_99[c])
        year_med.append(year[c])
        month_med.append(month[c])
        day_med.append(day[c])
        hour_med.append(hour[c])
        minute_med.append(minute[c])
        c+=6
    elif c+4<len(lon_99) and tempo_99[c+4]-tempo_99[c]<60:
        lon_med.append(lon_99[c])
        lat_med.append(lat_99[c])
        swh_med.append(swh_ku_99[c])
        swh_mle3_med.append(swh_ku_mle3_99[c])
        tempo_med.append(tempo_99[c])
        year_med.append(year[c])
        month_med.append(month[c])
        day_med.append(day[c])
        hour_med.append(hour[c])
        minute_med.append(minute[c])
        c+=5
    elif c+3<len(lon_99) and tempo_99[c+3]-tempo_99[c]<60:
        lon_med.append(lon_99[c])
        lat_med.append(lat_99[c])
        swh_med.append(swh_ku_99[c])
        swh_mle3_med.append(swh_ku_mle3_99[c])
        tempo_med.append(tempo_99[c])
        year_med.append(year[c])
        month_med.append(month[c])
        day_med.append(day[c])
        hour_med.append(hour[c])
        minute_med.append(minute[c])
        c+=4
    elif c+2<len(lon_99) and tempo_99[c+2]-tempo_99[c]<60:
        lon_med.append(lon_99[c])
        lat_med.append(lat_99[c])
        swh_med.append(swh_ku_99[c])
        swh_mle3_med.append(swh_ku_mle3_99[c])
        tempo_med.append(tempo_99[c])
        year_med.append(year[c])
        month_med.append(month[c])
        day_med.append(day[c])
        hour_med.append(hour[c])
        minute_med.append(minute[c])
        c+=3
    elif c+1<len(lon_99) and tempo_99[c+1]-tempo_99[c]<60:
        lon_med.append(lon_99[c])
        lat_med.append(lat_99[c])
        swh_med.append(swh_ku_99[c])
        swh_mle3_med.append(swh_ku_mle3_99[c])
        tempo_med.append(tempo_99[c])
        year_med.append(year[c])
        month_med.append(month[c])
        day_med.append(day[c])
        hour_med.append(hour[c])
        minute_med.append(minute[c])
        c+=2
    else:
        lon_med.append(lon_99[c])
        lat_med.append(lat_99[c])
        swh_med.append(swh_ku_99[c])
        swh_mle3_med.append(swh_ku_mle3_99[c])
        tempo_med.append(tempo_99[c])
        year_med.append(year[c])
        month_med.append(month[c])
        day_med.append(day[c])
        hour_med.append(hour[c])
        minute_med.append(minute[c])
        c+=1
    if c>=len(lon_99):
        break

datahora_med=[]
origem=[]
for i in range(len(day_med)):
    datahora_med.append(datetime.datetime.strptime(str(day_med[i])+"/"+str(month_med[i])+"/"+str(year_med[i])+" "+str(hour_med[i])+":"+str(minute_med[i])+":00", '%d/%m/%Y %H:%M:%S'))

Data = np.array([datahora_med, lat_med, lon_med, swh_med])
Data3 = Data.transpose()

df = pd.DataFrame(Data3)

df.columns = ['date_time', 'lat', 'lon', 'swvht']

df = df.replace(to_replace =['None', 'NULL', ' ', ''], value =np.nan)

df["institution"] = 'jason3'
df["type"] = 'altimeter'

print(df)
try:
    # Deleting existing data // avoid duplicate
    db.delete_old_data_no_station(df)
    # Insert new data
    db.insert_new_data_no_station(df)
except:
    print("No data to insert")

print('Programa finalizado.')


dir_name = "./"
test = os.listdir(dir_name)

for item in test:
    if item.endswith(".nc"):
        os.remove(os.path.join(dir_name, item))


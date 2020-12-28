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

import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )


def alimentarbd(Data1):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    if len(Data1)>0:
        cur.execute("SELECT datahora FROM altimetro WHERE satelite='%s' \
        ORDER BY datahora DESC limit 20"%Data1[0][0])
        for row in cur.fetchall():
            c1.append(row)
        if c1!=[]:
            for i in range(len(Data1)):
                if Data1[i][1]>max(c1)[0]:
                    sql = "INSERT INTO altimetro (satelite,datahora,lat,lon,swh)\
                    VALUES ('%s', '%s', %s, %s, %s)" % \
                    ((Data1[i][0]),(Data1[i][1]),(Data1[i][2]),(Data1[i][3]),\
                    (Data1[i][4]))
                    cur.execute(sql)
                    db.commit()
                else: #inserir update
                    sql = "UPDATE altimetro SET satelite='%s',datahora='%s',lat=%s,lon=%s,swh=%s\
                    WHERE datahora='%s' and satelite='%s'  and swh=%s" % \
                    ((Data1[i][0]),(Data1[i][1]),(Data1[i][2]),(Data1[i][3]),\
                    (Data1[i][4]),(Data1[i][1]),(Data1[0][0]),(Data1[i][4]))
                    cur.execute(sql)
                    db.commit()
        else:
            for i in range(len(Data1)):
                sql = "INSERT INTO altimetro (satelite,datahora,lat,lon,swh)\
                VALUES ('%s', '%s', %s, %s, %s)" % \
                ((Data1[i][0]),(Data1[i][1]),(Data1[i][2]),(Data1[i][3]),\
                (Data1[i][4]))
                cur.execute(sql)
                db.commit()

        cur.close()
        db.close()
        print('Dados inseridos no banco')
    else:
        print('nao há dados para serem inseridos')


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
datahora1=time.gmtime(time.time()-3600*10)
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

datahora=time.gmtime()
ano=datahora.tm_year
dia=datahora.tm_mday
mes=datahora.tm_mon
hora=datahora.tm_hour
datahora=time.gmtime(time.time()-3600*10)
ano1=datahora.tm_year
dia1=datahora.tm_mday
mes1=datahora.tm_mon
hora1=datahora.tm_hour
if dia<10:
    dia="0"+str(dia)
if dia1<10:
    dia1="0"+str(dia1)
if mes<10:
    mes="0"+str(mes)
if mes1<10:
    mes1="0"+str(mes1)

dia=str(dia)
mes=str(mes)
dia1=str(dia1)
mes1=str(mes1)
file_list=[]
if dia1!=dia:
    hour=0
    while hour<=hora:
        if hour<10:
            valor="0"+str(hour)
        else:
            valor=str(hour)
        glob_pattern = "*JA3_OPR_*_*_"+str(ano)+mes+dia+"_"+valor+"*_*_*.nc"
        if glob.glob(glob_pattern)!=[]:
            file_list.append(glob.glob(glob_pattern))
        hour=hour+1
    while hora1<=23:
        if hora1<10:
            valor="0"+str(hora1)
        else:
            valor=str(hora1)
        glob_pattern = "*JA3_OPR_*_*_"+str(ano)+mes1+dia1+"_"+valor+"*_*_*.nc"
        if glob.glob(glob_pattern)!=[]:
            file_list.append(glob.glob(glob_pattern))
        hora1=hora1+1
else:
    hour1=hora1
    while hour1<=hora:
        if hour1<10:
            valor="0"+str(hour1)
        else:
            valor=str(hour1)
        glob_pattern = "*JA3_OPR_*_*_"+str(ano)+mes1+dia1+"_"+valor+"*_*_*.nc"
        if glob.glob(glob_pattern)!=[]:
            file_list.append(glob.glob(glob_pattern))
        hour1=hour1+1
#ABRINDO CADA NETCDF POR VEZ
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
        breakpoint()

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
                        if np.ma.is_masked(swh_ku[i])==False:
                            print(i)
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

breakpoint()


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
    origem.append('jason3')
    datahora_med.append(datetime.datetime.strptime(str(day_med[i])+"/"+str(month_med[i])+"/"+str(year_med[i])+" "+str(hour_med[i])+":"+str(minute_med[i])+":00", '%d/%m/%Y %H:%M:%S'))

Data=np.array([origem,datahora_med,lat_med,lon_med,swh_med])
Data = Data.transpose()
# header="year,month,day,hour,minute,lat,lon,swh"
# np.savetxt("jason03.csv", Data,'%s',delimiter=" ",header=header)

# import xlsxwriter
# import math
# workbook=xlsxwriter.Workbook("jason03.xls")
# worksheet=workbook.add_worksheet()

# cabecalho=['datahora','lat','lon','wvht','wvht2']

# for ii in range(len(cabecalho)):
#     worksheet.write(0,ii,cabecalho[ii])

# for i in range(len(Data)):
#     for ii in range(len(Data[0])):
#         worksheet.write(i+1,ii,Data[i][ii])

# workbook.close()
breakpoint()

print('Alimentando o banco de dados')
alimentarbd(Data)

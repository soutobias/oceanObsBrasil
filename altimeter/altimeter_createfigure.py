# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 21:14:07 2019

@author: tobias
"""

import mysql.connector as MySQLdb
import numpy as np
import time
import datetime
import operator
import xlsxwriter
from math import sin, cos, sqrt, atan2, radians
import math
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
from cartopy import config

from shapely import geometry
from shapely.geometry.polygon import LinearRing

import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )



def ftp_pnboia(filename):

    import ftplib
#    import os

    server = user_config.ftpserver
    username = user_config.ftpusername
    password = user_config.ftppassword

    directory1 = '/ondas/dados_observacionais/'

    ftp = ftplib.FTP(server)
    ftp.login(user=username, passwd=password)
    ftp.cwd(directory1)

    #    os.chdir(r"c:\\ndbc\\sql\\")
    myfile = open(filename, 'rb')
    ftp.storbinary('STOR %s' % filename, myfile, 1024)
#    ftp.storlines('STOR ' + filename, myfile)
    myfile.close()

    print('arquivo_copiado para o FTP')

def buscabd(tempo):
    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    cur.execute("SELECT datahora,satelite,lat,lon,swh FROM altimetro \
                WHERE datahora>='%s' ORDER BY datahora"%(tempo))
    datahora,satelite,lat,lon,swh,ano,mes,dia,hora,minuto=[],[],[],[],[],[],[],[],[],[]
    for row in cur.fetchall():
        ano.append(row[0].year)
        mes.append(row[0].month)
        dia.append(row[0].day)
        hora.append(row[0].hour)
        minuto.append(row[0].minute)
        datahora.append((datetime.datetime(row[0].year,row[0].month,row[0].day,row[0].hour,0) - datetime.datetime(1970,1,1)).total_seconds())
        satelite.append(row[1])
        lat.append(row[2])
        lon.append(row[3])
        swh.append(row[4])

    data = np.array([ano,mes,dia,hora,satelite,lat,lon,swh,datahora])
    data = data.transpose()
    data=sorted(data, key=operator.itemgetter(0,1,2,3,4),reverse=True)
    # cabecalho="ano,mes,dia,hora,satelite,lat,lon,swh,datahora"

    # # np.savetxt("/root/Public/remobs/altimetro/altimetro.txt", data,'%s',delimiter=",",header=cabecalho)

    # workbook=xlsxwriter.Workbook("/root/Public/remobs/altimetro/altimetro.xls")
    # worksheet=workbook.add_worksheet()

    # cabecalho=['ano','mes','dia','hora','satelite','lat','lon','swh','datahora']

    # for ii in range(len(cabecalho)):
    #     worksheet.write(0,ii,cabecalho[ii])

    # for i in range(len(data)):
    #     for ii in range(len(data[0])):
    #         worksheet.write(i+1,ii,data[i][ii])

    # workbook.close()

    return data

def gerarfigura(data1,flag):
    dataho1=time.time()-(3600*24*flag)
    dataho2=time.time()-(3600*24*(flag-1))

    lines = open('metareav.txt', 'r')

    lat1,lat2,lat3,lat4,lat5,lat6,lat7,lat8,lat9,lat10=[],[],[],[],[],[],[],[],[],[]
    lon1,lon2,lon3,lon4,lon5,lon6,lon7,lon8,lon9,lon10=[],[],[],[],[],[],[],[],[],[]
    i=1
    for line in lines:
        dataline = line.strip()
        columns = dataline.split()
        if columns[0]!='0':
            exec("lat%s.append(float(columns[1]))"%str(i))
            exec("lon%s.append(float(columns[2]))"%str(i))
        else:
            i=i+1
#
    lat01=-35.8333
    lat02=7
    lon01=-55.20
    lon02=-20

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.COASTLINE)
    # ax.add_feature(states_provinces, edgecolor='gray')
    # ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='0.8'))
    ax.set_xlim(lon01, lon02)
    ax.set_ylim(lat01, lat02)

    # set a margin around the data
    ax.margins(0.005,0.005)
    #
    ax.plot(lon1,lat1,linewidth=0.5,color='k')
    ax.plot(lon2,lat2,linewidth=0.5,color='k')
    ax.plot(lon3,lat3,linewidth=0.5,color='k')
    ax.plot(lon4,lat4,linewidth=0.5,color='k')
    ax.plot(lon5,lat5,linewidth=0.5,color='k')
    ax.plot(lon6,lat6,linewidth=0.5,color='k')
    ax.plot(lon7,lat7,linewidth=0.5,color='k')
    ax.plot(lon8,lat8,linewidth=0.5,color='k')
    ax.plot(lon9,lat9,linewidth=0.5,color='k')
    ax.plot(lon10,lat10,linewidth=0.5,color='k')


    for i in range(len(data1)):
        if float(data1[i][7])<1.5 and float(data1[i][8])>=dataho1 and float(data1[i][8])<=dataho2:
            ax.annotate(str(round(float(data1[i][7]),1)),xy=(float(data1[i][6]),float(data1[i][5])),xycoords='data',color='black',fontsize=5)
        if float(data1[i][7])>=1.5 and float(data1[i][7])<2.5 and float(data1[i][8])>=dataho1 and float(data1[i][8])<=dataho2:
            ax.annotate(str(round(float(data1[i][7]),1)),xy=(float(data1[i][6]),float(data1[i][5])),color='green',fontsize=5)
        elif float(data1[i][7])>=2.5 and float(data1[i][7])<3.0 and float(data1[i][8])>=dataho1 and float(data1[i][8])<=dataho2:
            ax.annotate(str(round(float(data1[i][7]),1)),xy=(float(data1[i][6]),float(data1[i][5])),color='red',fontsize=5)
        elif float(data1[i][7])>=3.0 and float(data1[i][7])<3.5 and float(data1[i][8])>=dataho1 and float(data1[i][8])<=dataho2:
            ax.annotate(str(round(float(data1[i][7]),1)),xy=(float(data1[i][6]),float(data1[i][5])),color='gray',fontsize=5)
        elif float(data1[i][7])>=3.5 and float(data1[i][7])<4.0 and float(data1[i][8])>=dataho1 and float(data1[i][8])<=dataho2:
            ax.annotate(str(round(float(data1[i][7]),1)),xy=(float(data1[i][6]),float(data1[i][5])),color='purple',fontsize=5)
        elif float(data1[i][7])>=4.0 and float(data1[i][7])<8.0 and float(data1[i][8])>=dataho1 and float(data1[i][8])<=dataho2:
            ax.annotate(str(round(float(data1[i][7]),1)),xy=(float(data1[i][6]),float(data1[i][5])),color='blue',fontsize=5)
        elif float(data1[i][7])>=8.0 and float(data1[i][8])>=dataho1 and float(data1[i][8])<=dataho2:
            ax.annotate(str(round(float(data1[i][7]),1)),xy=(float(data1[i][6]),float(data1[i][5])),color='orange',fontsize=5)


    geom = geometry.box(minx=-55,maxx=-43,miny=-20.5,maxy=-11)
    ax.add_geometries([geom], crs=ccrs.PlateCarree(), facecolor='white')

    ax.annotate('LEGENDA',xy=(-54,-13),color='black',fontsize=11)
    ax.annotate('MENOR QUE 1.5 m',xy=(-54.5,-14),color='black',fontsize=6)
    ax.annotate('1.5 a 2.5 m',xy=(-54.5,-15),color='green',fontsize=6)
    ax.annotate('2.5 a 3.0 m',xy=(-54.5,-16),color='red',fontsize=6)
    ax.annotate('3.0 a 3.5 m',xy=(-54.5,-17),color='gray',fontsize=6)
    ax.annotate('3.5 a 4.0 m',xy=(-54.5,-18),color='purple',fontsize=6)
    ax.annotate('4.0 a 8.0 m',xy=(-54.5,-19),color='blue',fontsize=6)
    ax.annotate('MAIOR QUE 8.0 m',xy=(-54.5,-20),color='orange',fontsize=6)

    #
    datahora1=time.gmtime(dataho1)
    datahora2=time.gmtime(dataho2)

    plt.title('Ondas Altimetro METAREA V entre '+str(datahora1.tm_mday)+'/'+str(datahora1.tm_mon)+' '+str(datahora1.tm_hour)+':00 e '+str(datahora2.tm_mday)+'/'+str(datahora2.tm_mon)+' '+str(datahora2.tm_hour)+':00.')
    #
    if flag==3:
        plt.savefig('altimetro_mapa_18h.png', format='png',dpi=300, pad_inches = 0)
        plt.close()
    if flag==2:
        plt.savefig('altimetro_mapa_12h.png', format='png',dpi=300, pad_inches = 0)
        plt.close()
    if flag==1:
        plt.savefig('altimetro_mapa_6h.png', format='png',dpi=300, pad_inches = 0)
        plt.close()
    return 0

print('inicio')
datahora1=time.gmtime(time.time()-(3600*24))
tempo=datetime.datetime.strptime(str(datahora1[2])+"/"+str(datahora1[1])+"/"+str(datahora1[0])+" 00:00:00", '%d/%m/%Y %H:%M:%S')

(final)=buscabd(tempo)

gerarfigura(final,3)
gerarfigura(final,2)
gerarfigura(final,1)
# os.chdir("/root/Public/remobs/altimetro")
# ftp_pnboia('altimetro.xls')
# ftp_pnboia('altimetro_mapa_18h.png')
# ftp_pnboia('altimetro_mapa_12h.png')
# ftp_pnboia('altimetro_mapa_6h.png')
print('done')




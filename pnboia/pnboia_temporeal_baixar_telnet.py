# -*- coding: utf-8 -*-
"""
Created on Tue May 03 10:08:32 2016

@author: Tobias
"""

import mysql.connector as MySQLdb
import re
import time
import csv
from telnetlib import Telnet
import datetime
import numpy as np
import operator
import argosqc as qc
import smtplib

import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )


def inserir_bd(Data1,boia):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    cur.execute("SELECT data FROM argos_bruto WHERE argos_id=%s\
    ORDER BY data DESC limit 5" % boia)
    for row in cur.fetchall():
        c1.append(row)
    if c1!=[]:
        c1=c1[0]
    for i in range(len(Data1)):
        if c1!=[]:
            if Data1[i][3]>c1[0]:
                sql = "INSERT INTO argos_bruto (argos_id,lat,lon,data,sensor00,sensor01,\
                sensor02,sensor03,sensor04,sensor05,sensor06,sensor07,sensor08,sensor09,\
                sensor10,sensor11,sensor12,sensor13,sensor14,sensor15,sensor16,sensor17,\
                sensor18,sensor19,sensor20,sensor21,sensor22,sensor23,sensor24,sensor25)\
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s',\
                '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s',\
                '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                (int(Data1[i][0]),str(Data1[i][1]),str(Data1[i][2]),(Data1[i][3]),\
                str(Data1[i][5]),str(Data1[i][6]),str(Data1[i][7]),str(Data1[i][8]),\
                str(Data1[i][9]),str(Data1[i][10]),str(Data1[i][11]),str(Data1[i][12]),\
                str(Data1[i][13]),str(Data1[i][14]),str(Data1[i][15]),str(Data1[i][16]),\
                str(Data1[i][17]),str(Data1[i][18]),str(Data1[i][19]),str(Data1[i][20]),\
                str(Data1[i][21]),str(Data1[i][22]),str(Data1[i][23]),str(Data1[i][24]),\
                str(Data1[i][25]),str(Data1[i][26]),str(Data1[i][27]),str(Data1[i][28]),\
                str(Data1[i][29]),str(Data1[i][30]))
                cur.execute(sql)
                db.commit()
        else:
            print('teste')
            sql = "INSERT INTO argos_bruto (argos_id,lat,lon,data,sensor00,sensor01,\
            sensor02,sensor03,sensor04,sensor05,sensor06,sensor07,sensor08,sensor09,\
            sensor10,sensor11,sensor12,sensor13,sensor14,sensor15,sensor16,sensor17,\
            sensor18,sensor19,sensor20,sensor21,sensor22,sensor23,sensor24,sensor25)\
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s',\
            '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s',\
            '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
            (int(Data1[i][0]),str(Data1[i][1]),str(Data1[i][2]),(Data1[i][3]),\
            str(Data1[i][5]),str(Data1[i][6]),str(Data1[i][7]),str(Data1[i][8]),\
            str(Data1[i][9]),str(Data1[i][10]),str(Data1[i][11]),str(Data1[i][12]),\
            str(Data1[i][13]),str(Data1[i][14]),str(Data1[i][15]),str(Data1[i][16]),\
            str(Data1[i][17]),str(Data1[i][18]),str(Data1[i][19]),str(Data1[i][20]),\
            str(Data1[i][21]),str(Data1[i][22]),str(Data1[i][23]),str(Data1[i][24]),\
            str(Data1[i][25]),str(Data1[i][26]),str(Data1[i][27]),str(Data1[i][28]),\
            str(Data1[i][29]),str(Data1[i][30]))
            cur.execute(sql)
            db.commit()



def boiasfuncionando():

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    boias=[]
    cur.execute("SELECT estacao_id, argos_id,nome, argos_id, argos_id FROM pnboia_estacao WHERE sit=1")
    for row in cur.fetchall():
        boias.append(row)
    return boias

def baixar_dados(boia):
    programa = "05655"
    saida = []
    comando = "PRV,5655,DS,,"
    usern = user_config.pnboia_user
    passw = user_config.pnboia_psw

    try:
        tn = Telnet(user_config.pnboia_telnet)
    except :
        pass

    #---Login

    try:
        tn.read_until(b"Username: ")
        tn.write(usern.encode('ascii') + b"\n")

        tn.read_until(b"Password: ")
        tn.write(passw.encode('ascii') + b"\n")

        print ("Login com servidor de dados realizado...")# ,tn.read_until('SERVER', 5)
        print ("Realizando coleta de dados para boia " + str(boia) + "...")

    except:
        pass


    #---Comando para coleta de dados
    #print comando
    print(str(comando) + str(boia) + "\n\r")
    tn.write(passw.encode('ascii') + b"\n")
    comando1=comando+str(boia)
    tn.write(comando1.encode('ascii') + b"\n")

    dados = tn.read_until(b'SERVER',5)
    print ("Dado recebidos: \n\r")
    tn.close()
    dados=dados.decode("utf-8")
    if dados[0:7] != "No data":
        dados = dados.replace("\r\n",";")
        dados = re.sub("\s+", ",", dados.strip())
        dados = dados.replace(";,", ";");
        dados = dados.replace(";;", ";");
        dados = dados.replace("/" + programa, programa);
        dados = dados.replace(":,", ":");
        dados = dados.replace(";ARGOS,READY;/ARGOS,READY;/","")
        dados = dados.replace(",?,",",")
        dados = dados.replace(",?","")
        dados = dados + ";;"
        dadoslimpos = dados.replace(";","\n")
        print (str(dados.count(";")) + " linhas recebidas...")
    else:
        print ("Sem dados disponíveis ou sem autorização de acesso.")
    contador = 0
    checkpoint = 0
    resultado = []
    bat = []
    final= []

    #with open(str(nome_arq) + '.csv', 'w') as csvfile:
    #    #date, bat, hs, tp, dp, hmax, ws1, wg1, wd1, ws2, wg2, wd2, at, rh, dwp, pr, sst
    #     fieldnames = ['date','bat','hs','tp','dp','hmax','ws1','wg1','wd1','ws2','wg2','wd2','airt','rh','dwp','pr','sst']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore', delimiter = ',')
    #     writer.writeheader()

    while contador != dados.count(";"):
        linha = dados[checkpoint:dados.index(";",checkpoint)]
        checkpoint = dados.index(";",checkpoint) + 1
        contador = contador + 1
        if programa in linha[0:6]:
            saida = []
            saidadois = []
            saida = linha.split(",")
            linha = dados[checkpoint:dados.index(";",checkpoint)]
            checkpoint = dados.index(";",checkpoint) + 1
            contador = contador + 1
            if ":" in linha:
                saidadois = linha.split(",")
                linha = dados[checkpoint:dados.index(";",checkpoint)]
                checkpoint = dados.index(";",checkpoint) + 1
                contador = contador + 1
                while programa not in linha[0:6] and contador < dados.count(";") and ":" not in linha:
                    saidadois.extend(linha.split(","))
                    linha = dados[checkpoint:dados.index(";",checkpoint)]
                    checkpoint = dados.index(";",checkpoint) + 1
                    contador = contador + 1
                resultado = saida
                resultado.extend(saidadois)
                if len(resultado) >= 42:
                    if int(float(resultado[15])) == 1:
                        bat.append([int(resultado[1]),str(resultado[8]),str(resultado[9]),str(resultado[12]),str(resultado[13]),str(resultado[15]),str(resultado[16]),str(resultado[17]),str(resultado[18]),str(resultado[19]),str(resultado[20]),str(resultado[21]),str(resultado[22]),str(resultado[23]),str(resultado[24]),str(resultado[25]),str(resultado[26]),str(resultado[27]),str(resultado[28]),str(resultado[29]),str(resultado[30]),str(resultado[31]),str(resultado[32]),str(resultado[33]),str(resultado[34]),str(resultado[35]),str(resultado[36]),str(resultado[37]),str(resultado[38]),str(resultado[39]),str(resultado[40])])
                    if int(float(resultado[15])) == 2:
                        bat.append([int(resultado[1]),str(resultado[8]),str(resultado[9]),str(resultado[12]),str(resultado[13]),str(resultado[15]),str(resultado[16]),str(resultado[17]),str(resultado[18]),str(resultado[19]),str(resultado[20]),str(resultado[21]),str(resultado[22]),str(resultado[23]),str(resultado[24]),str(resultado[25]),str(resultado[26]),str(resultado[27]),str(resultado[28]),str(resultado[29]),str(resultado[30]),str(resultado[31]),str(resultado[32]),str(resultado[33]),str(resultado[34]),str(resultado[35]),str(resultado[36]),str(resultado[37]),str(resultado[38]),str(resultado[39]),str(resultado[40])])
                if len(resultado) == 40 or len(resultado) == 41:
                    if int(float(resultado[8])) == 1:
                        bat.append([int(resultado[1]),"-9999","-9999",str(resultado[5]),str(resultado[6]),str(resultado[8]),str(resultado[9]),str(resultado[10]),str(resultado[11]),str(resultado[12]),str(resultado[13]),str(resultado[14]),str(resultado[15]),str(resultado[16]),str(resultado[17]),str(resultado[18]),str(resultado[19]),str(resultado[20]),str(resultado[21]),str(resultado[22]),str(resultado[23]),str(resultado[24]),str(resultado[25]),str(resultado[26]),str(resultado[27]),str(resultado[28]),str(resultado[29]),str(resultado[30]),str(resultado[31]),str(resultado[32]),str(resultado[33]),str(resultado[34])])
                    if int(float(resultado[8])) == 2:
                        bat.append([int(resultado[1]),"-9999","-9999",str(resultado[5]),str(resultado[6]),str(resultado[8]),str(resultado[9]),str(resultado[10]),str(resultado[11]),str(resultado[12]),str(resultado[13]),str(resultado[14]),str(resultado[15]),str(resultado[16]),str(resultado[17]),str(resultado[18]),str(resultado[19]),str(resultado[20]),str(resultado[21]),str(resultado[22]),str(resultado[23]),str(resultado[24]),str(resultado[25]),str(resultado[26]),str(resultado[27]),str(resultado[28]),str(resultado[29]),str(resultado[30]),str(resultado[31]),str(resultado[32]),str(resultado[33]),str(resultado[34])])
                if len(resultado) == 35 or len(resultado) == 34:
                    if int(float(resultado[8])) == 1:
                        bat.append([int(resultado[1]),"-9999","-9999",str(resultado[5]),str(resultado[6]),str(resultado[8]),str(resultado[9]),str(resultado[10]),str(resultado[11]),str(resultado[12]),str(resultado[13]),str(resultado[14]),str(resultado[15]),str(resultado[16]),str(resultado[17]),str(resultado[18]),str(resultado[19]),str(resultado[20]),str(resultado[21]),str(resultado[22]),str(resultado[23]),str(resultado[24]),str(resultado[25]),str(resultado[26]),str(resultado[27]),str(resultado[28]),str(resultado[29]),str(resultado[30]),str(resultado[31]),str(resultado[32]),str(resultado[33]),0])
                    if int(float(resultado[8])) == 2:
                        bat.append([int(resultado[1]),"-9999","-9999",str(resultado[5]),str(resultado[6]),str(resultado[8]),str(resultado[9]),str(resultado[10]),str(resultado[11]),str(resultado[12]),str(resultado[13]),str(resultado[14]),str(resultado[15]),str(resultado[16]),str(resultado[17]),str(resultado[18]),str(resultado[19]),str(resultado[20]),str(resultado[21]),str(resultado[22]),str(resultado[23]),str(resultado[24]),str(resultado[25]),str(resultado[26]),str(resultado[27]),str(resultado[28]),str(resultado[29]),str(resultado[30]),str(resultado[31]),str(resultado[32]),str(resultado[33]),0])

    for i in range(len(bat)):
        bat[i][3]=datetime.datetime.strptime(bat[i][3]+" "+bat[i][4], '%Y-%m-%d %H:%M:%S')


    return bat


boias=boiasfuncionando()

for i in range(len(boias)):
    print(boias[i][2])
    dados=baixar_dados(int(boias[i][1]))
#    print(dados)
    inserir_bd(dados,int(boias[i][1]))



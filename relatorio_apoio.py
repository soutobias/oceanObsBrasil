# Test for list structures in PyLaTeX.
# More info @ http://en.wikibooks.org/wiki/LaTeX/List_Structures
from pylatex import Document, Section, Subsection, Command,Itemize, Enumerate, Description,Tabular,Figure
from pylatex.utils import italic, NoEscape
import time,datetime
import mysql.connector as MySQLdb
import math
import numpy as np
import operator

import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )


def arredondar(num):
    return float( '%.0f' % ( num ) )

def arredondar1(num):
    return float( '%.1f' % ( num ) )



def ftp_pnboia1(filename):

    import ftplib

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


def ftp_pnboia(filename):

    import ftplib
#    import os

    server = user_config.ftpserver1
    username = user_config.ftpusername1
    password = user_config.ftppassword1

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

def buscabdotherbuoys(tempo):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)


    cur=db.cursor()

    c1=[]

    cur.execute("SELECT otherbuoys_estacao.nome,otherbuoys_estacao.lat,otherbuoys_estacao.lon,\
                otherbuoys.datahora,otherbuoys.mwd,otherbuoys.hm0,otherbuoys.seapeakdir,\
                otherbuoys.seahm0,otherbuoys.swellpeakdir,otherbuoys.swellhm0,otherbuoys.wspd,otherbuoys.gust \
                FROM otherbuoys INNER JOIN otherbuoys_estacao WHERE otherbuoys.datahora>='%s' \
                AND otherbuoys_estacao.id=otherbuoys.esta_id \
                ORDER BY datahora DESC" % (tempo))


    nome,lat,lon,datahora,mwd,hm0,seapeakdir,seahm0=[],[],[],[],[],[],[],[]
    swellpeakdir,swellhm0=[],[]
    ano,mes,dia,hora,minuto=[],[],[],[],[]
    wspd,gust=[],[]
    for row in cur.fetchall():
        nome.append(row[0])
        lat.append(row[1])
        lon.append(row[2])
        datahora.append(row[3])
        ano.append(row[3].year)
        mes.append(row[3].month)
        dia.append(row[3].day)
        hora.append(row[3].hour)
        minuto.append(row[3].minute)
        mwd.append(row[4])
        hm0.append(row[5])
        seapeakdir.append(row[6])
        seahm0.append(row[7])
        swellpeakdir.append(row[8])
        swellhm0.append(row[9])
        wspd.append(row[10])
        gust.append(row[11])

    data = np.array([ano,mes,dia,hora,minuto,nome,lat,lon,mwd,hm0,seapeakdir,seahm0,swellpeakdir,swellhm0,wspd,gust])
    data = data.transpose()

    return data

def buscabdsimcosta(tempo):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    cur.execute("SELECT simcosta_estacao.estacao,simcosta_estacao.lat,\
                simcosta_estacao.lon,\
                simcosta.datahora,simcosta.Avg_Wnd_Sp,simcosta.Gust_Sp,simcosta.Avg_Wnd_Dir_N,\
                simcosta.Avg_Air_Tmp,simcosta.Avg_Air_Press,simcosta.Avg_DewP,simcosta.Avg_Hmt,\
                simcosta.Avg_W_Tmp1,\
                simcosta.Hsig,\
                simcosta.Hmax,simcosta.TP,simcosta.Avg_Wv_Dir_N,simcosta.Avg_Spre\
                FROM simcosta INNER JOIN simcosta_estacao WHERE \
                simcosta.datahora>='%s' AND \
                simcosta_estacao.id=simcosta.id \
                ORDER BY datahora DESC" % (tempo))

    datahora,wspd,gust,wdir,atmp,pres,dewp=[],[],[],[],[],[],[]
    humi,wtmp1,wvht=[],[],[]
    wmax,apd,mwd,spred,nome,lat,lon=[],[],[],[],[],[],[]
    ano,mes,dia,hora,minuto=[],[],[],[],[]
    for row in cur.fetchall():
        nome.append(row[0])
        lat.append(row[1])
        lon.append(row[2])
        datahora.append(row[3])
        ano.append(row[3].year)
        mes.append(row[3].month)
        dia.append(row[3].day)
        hora.append(row[3].hour)
        minuto.append(row[3].minute)
        wspd.append(row[4])
        gust.append(row[5])
        wdir.append(row[6])
        atmp.append(row[7])
        pres.append(row[8])
        dewp.append(row[9])
        humi.append(row[10])
        wtmp1.append(row[11])
        wvht.append(row[12])
        wmax.append(row[13])
        apd.append(row[14])
        mwd.append(row[15])
        spred.append(row[16])



    data = np.array([ano,mes,dia,hora,minuto,nome,lat,lon,wspd,gust,wdir,atmp,pres,dewp,humi,wtmp1,wvht,wmax,apd,mwd,spred])
    data = data.transpose()
    data=sorted(data, key=operator.itemgetter(5,0,1,2,3,4),reverse=True)

    return data

def buscabdpnboia(tempo):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    cur.execute("SELECT pnboia_estacao.nome,pnboia.lat,\
                pnboia.lon,\
                pnboia.datahora,pnboia.bateria,pnboia.heading,pnboia.wspd,\
                pnboia.wspdflagid,pnboia.wdir,pnboia.wdirflagid,pnboia.gust,\
                pnboia.gustflagid,pnboia.atmp,pnboia.atmpflagid,pnboia.pres,pnboia.presflagid,pnboia.dewp,\
                pnboia.dewpflagid,pnboia.humi,pnboia.humiflagid,pnboia.wtmp,pnboia.wtmpflagid,\
            pnboia.cvel1,pnboia.cvel1flagid,pnboia.cdir1,pnboia.cdir1flagid,\
                pnboia.cvel2,pnboia.cvel2flagid,pnboia.cdir2,pnboia.cdir2flagid,pnboia.cvel3,\
                pnboia.cvel3flagid,pnboia.cdir3,pnboia.cdir3flagid,pnboia.wvht,\
                pnboia.wvhtflagid,pnboia.wmax,pnboia.wmaxflagid,pnboia.dpd,pnboia.dpdflagid,\
                pnboia.mwd,pnboia.mwdflagid,pnboia.spred\
                FROM pnboia INNER JOIN pnboia_estacao WHERE \
                pnboia.datahora>='%s' AND \
                pnboia_estacao.estacao_id=pnboia.esta_id \
                ORDER BY datahora DESC" % (tempo))

    datahora,bateria,heading,wspd=[],[],[],[]
    wspdflagid,wdir,wdirflagid,gust,gustflagid,atmp,atmpflagid,pres,presflagid,dewp=[],[],[],[],[],[],[],[],[],[]
    dewpflagid,humi,humiflagid,wtmp,wtmpflagid,cvel1,cvel1flagid,cdir1,cdir1flagid=[],[],[],[],[],[],[],[],[]
    cvel2,cvel2flagid,cdir2,cdir2flagid,cvel3,cvel3flagid,cdir3,cdir3flagid,wvht=[],[],[],[],[],[],[],[],[]
    wvhtflagid,wmax,wmaxflagid,dpd,dpdflagid,mwd,mwdflagid,spred=[],[],[],[],[],[],[],[]

    nome,lat,lon,ano,mes,dia,hora,minuto=[],[],[],[],[],[],[],[]
    for row in cur.fetchall():
        nome.append(row[0])
        lat.append(row[1])
        lon.append(row[2])
        datahora.append(row[3])
        ano.append(row[3].year)
        mes.append(row[3].month)
        dia.append(row[3].day)
        hora.append(row[3].hour)
        minuto.append(row[3].minute)
        bateria.append(row[4])
        heading.append(row[5])
        if int(row[7])>0 and int(row[7])<50:
            wspd.append('None')
        else:
            wspd.append(row[6])
        if int(row[9])>0 and int(row[9])<50:
            wdir.append('None')
        else:
            wdir.append(row[8])
        if int(row[11])>0 and int(row[11])<50:
            gust.append('None')
        else:
            gust.append(row[10])
        if int(row[13])>0 and int(row[13])<50:
            atmp.append('None')
        else:
            atmp.append(row[12])
        if int(row[21])>0 and int(row[21])<50:
            wtmp.append('None')
        else:
            wtmp.append(row[20])
        if int(row[35])>0 and int(row[35])<50:
            wvht.append('None')
        else:
            wvht.append(row[34])
        if int(row[37])>0 and int(row[37])<50:
            wmax.append('None')
        else:
            wmax.append(row[36])
        if int(row[39])>0 and int(row[39])<50:
            dpd.append('None')
        else:
            dpd.append(row[38])
        if int(row[41])>0 and int(row[41])<50:
            mwd.append('None')
        else:
            mwd.append(row[40])

    data = np.array([ano,mes,dia,hora,nome,wspd,wdir,gust,atmp,wtmp,wvht,wmax,dpd,mwd])

    data = data.transpose()
    data=sorted(data, key=operator.itemgetter(5,0,1,2,4),reverse=True)

    return data


def buscabdndbc(tempo):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]

    cur.execute("SELECT datahora,lat,lon,wdir,wspd,gst,\
                wvht,dpd,apd,mwd,pres,ptdy,atmp,wtmp FROM ndbc WHERE datahora>='%s'\
                ORDER BY datahora DESC" % (tempo))

    datahora,lat,lon,wdir,wspd,gst,wvht,dpd,apd,mwd,pres,ptdy,atmp,wtmp=[],[],[],[],[],[],[],[],[],[],[],[],[],[]
    ano,mes,dia,hora=[],[],[],[]
    for row in cur.fetchall():
        datahora.append(row[0])
        ano.append(row[0].year)
        mes.append(row[0].month)
        dia.append(row[0].day)
        hora.append(row[0].hour)
        lat.append(row[1])
        lon.append(row[2])
        wspd.append(row[3])
        wdir.append(row[4])
        gst.append(row[5])
        wvht.append(row[6])
        dpd.append(row[7])
        apd.append(row[8])
        mwd.append(row[9])
        pres.append(row[10])
        ptdy.append(row[11])
        atmp.append(row[12])
        wtmp.append(row[13])

    data = np.array([ano,mes,dia,hora,lat,lon,wdir,wspd,gst,wvht,dpd,apd,mwd,pres,ptdy,atmp,wtmp])
    data = data.transpose()

    return data


def buscabdrico(tempo):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    cur.execute("SELECT ricosurf_estacao.nome,ricosurf_estacao.lat,\
                ricosurf_estacao.lon,\
                ricosurf.datahora,ricosurf.wvht,ricosurf.periodo,\
                ricosurf.tsm,ricosurf.direcao \
                FROM ricosurf INNER JOIN ricosurf_estacao WHERE \
                ricosurf.datahora>='%s' AND \
                ricosurf_estacao.id=ricosurf.esta_id \
                ORDER BY datahora DESC" % (tempo))

    nome,lat,lon,ano,mes,dia,hora,minuto=[],[],[],[],[],[],[],[]
    datahora,wvht,periodo,tsm,direcao=[],[],[],[],[]

    for row in cur.fetchall():
        nome.append(row[0])
        lat.append(row[1])
        lon.append(row[2])
        datahora.append(row[3])
        ano.append(row[3].year)
        mes.append(row[3].month)
        dia.append(row[3].day)
        hora.append(row[3].day)
        minuto.append(row[3].day)
        wvht.append(row[4])
        periodo.append(row[5])
        tsm.append(row[6])
        direcao.append(row[7])

    data = np.array([ano,mes,dia,hora,minuto,nome,lat,lon,wvht,periodo,tsm,direcao])
    data = data.transpose()

    return data

def buscabdespiritosanto(tempo):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    cur.execute("SELECT buoy_espiritosanto_estacao.nome,buoy_espiritosanto_estacao.lat,\
                buoy_espiritosanto_estacao.lon,\
                buoy_espiritosanto.datahora,buoy_espiritosanto.wspd,buoy_espiritosanto.wdir,buoy_espiritosanto.wtmp,\
                buoy_espiritosanto.atmp,buoy_espiritosanto.pres,buoy_espiritosanto.humi,buoy_espiritosanto.mwd,\
                buoy_espiritosanto.spred,buoy_espiritosanto.dpd,buoy_espiritosanto.wvht \
                FROM buoy_espiritosanto INNER JOIN buoy_espiritosanto_estacao WHERE \
                buoy_espiritosanto.datahora>='%s' AND \
                buoy_espiritosanto_estacao.id=buoy_espiritosanto.esta_id \
                ORDER BY datahora DESC" % (tempo))

    datahora,wspd,wdir,wtmp,atmp,pres,humi,mwd=[],[],[],[],[],[],[],[]
    spred,dpd,wvht=[],[],[]
    nome,lat,lon,ano,mes,dia,hora,minuto=[],[],[],[],[],[],[],[]

    for row in cur.fetchall():
        nome.append(row[0])
        lat.append(row[1])
        lon.append(row[2])
        datahora.append(row[3])
        ano.append(row[3].year)
        mes.append(row[3].month)
        dia.append(row[3].day)
        hora.append(row[3].hour)
        minuto.append(row[3].minute)
        wspd.append(row[4])
        wdir.append(row[5])
        wtmp.append(row[6])
        atmp.append(row[7])
        pres.append(row[8])
        humi.append(row[9])
        mwd.append(row[10])
        spred.append(row[11])
        dpd.append(row[12])
        wvht.append(row[13])

    data = np.array([ano,mes,dia,hora,minuto,nome,lat,lon,wspd,wdir,wtmp,atmp,pres,humi,mwd,spred,dpd,wvht])
    data = data.transpose()

    return data


def buscabdwavecheck(tempo):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    cur.execute("SELECT wavecheck_estacao.id,wavecheck_estacao.estado,wavecheck_estacao.nome,wavecheck_estacao.lat,\
                wavecheck_estacao.lon,\
                wavecheck.datahora,wavecheck.altura,wavecheck.formacao,\
                wavecheck.direcao,wavecheck.observacao\
                FROM wavecheck INNER JOIN wavecheck_estacao WHERE \
                wavecheck.datahora>='%s' AND \
                wavecheck_estacao.id=wavecheck.esta_wave \
                ORDER BY datahora DESC" % (tempo))

    datahora,altura,formacao,direcao,observacao=[],[],[],[],[]
    nome,lat,lon,ano,mes,dia,hora,minuto=[],[],[],[],[],[],[],[]
    ident,estado=[],[]
    for row in cur.fetchall():
        ident.append(row[0])
        estado.append(row[1])
        nome.append(row[2])
        lat.append(row[3])
        lon.append(row[4])
        datahora.append(row[5])
        ano.append(row[5].year)
        mes.append(row[5].month)
        dia.append(row[5].day)
        hora.append(row[5].day)
        minuto.append(row[5].day)
        altura.append(row[6])
        formacao.append(row[7])
        direcao.append(row[8])
        observacao.append(row[9])

    data = np.array([ident,ano,mes,dia,hora,minuto,estado,nome,lat,lon,altura,formacao,direcao,observacao])
    data = data.transpose()
    data=sorted(data, key=operator.itemgetter(1,2,3,4,5,0),reverse=True)

    return data

def abrirmare(tempo4):

    lines = open('./mares.txt', 'r')
    ano,mes,dia,hora,situacao=[],[],[],[],[]
    lines.readline()
    for line in lines:
        dataline = line.strip()
        columns = dataline.split()
        year=tempo4.year;
        month=tempo4.month;
        year=tempo4.year;
        day=tempo4.day;
        if month==12:
            month1=1;
            year1=year+1
        else:
            month1=month+1
            year1=year

        if int(columns[0])==year and int(columns[1])==month and int(columns[2])>=day:
            ano.append(int(columns[0]))
            mes.append(int(columns[1]))
            dia.append(int(columns[2]))
            situacao.append(columns[3])
        elif int(columns[0])==year1 and int(columns[1])==month1:
            ano.append(int(columns[0]))
            mes.append(int(columns[1]))
            dia.append(int(columns[2]))
            situacao.append(columns[3])

    data = np.array([ano[0:-3],mes[0:-3],dia[0:-3],situacao[0:-3]])
    data = data.transpose()


    return data

def fill_document(doc):
    """Add a section, a subsection and some text to the document.


    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """


    datahora1=time.gmtime(time.time()-(3600*24))
    tempo=datetime.datetime.strptime(str(datahora1[2])+"/"+str(datahora1[1])+"/"+str(datahora1[0])+" 00:00:00", '%d/%m/%Y %H:%M:%S')

    datahora1=time.gmtime(time.time()-3600*2)
    tempo1=datetime.datetime.strptime(str(datahora1[2])+"/"+str(datahora1[1])+"/"+str(datahora1[0])+" "+str(datahora1[3])+":00:00", '%d/%m/%Y %H:%M:%S')

    datahora6=time.gmtime(time.time()-3600*15)
    tempo6=datetime.datetime.strptime(str(datahora1[2])+"/"+str(datahora1[1])+"/"+str(datahora1[0])+" "+str(datahora1[3])+":00:00", '%d/%m/%Y %H:%M:%S')


    wave=buscabdwavecheck(tempo)
    buoy_espiritosanto=buscabdespiritosanto(tempo)
    rico=buscabdrico(tempo)
    ndbc=buscabdndbc(tempo)
    pnboia=buscabdpnboia(tempo)
    simcosta=buscabdsimcosta(tempo)
    otherbuoys=buscabdotherbuoys(tempo)

    datahora4=time.gmtime(time.time()-(3600*24*8))
    tempo4=datetime.datetime.strptime(str(datahora4[2])+"/"+str(datahora4[1])+"/"+str(datahora4[0])+" 00:00:00", '%d/%m/%Y %H:%M:%S')



    mare=abrirmare(tempo4)

    doc.append('TODOS OS DADOS ESTAO EM HORA ZULU')
    with doc.create(Section('FASE DA LUA')):
        with doc.create(Description()) as desc:
            for i in range(len(mare)):
                desc.add_item(str(mare[i][0])+'-'+str(mare[i][1])+'-'+str(mare[i][2]),str(mare[i][3]))

    estados=('Rio Grande do Sul','Santa Catarina','Parana','Sao Paulo','Rio de Janeiro','Espirito Santo','Bahia','Sergipe','Alagoas','Pernambuco','Paraiba','Rio Grande do Norte','Ceara','Piaui','Maranhao','Belem')

    for s in range(len(estados)):
        with doc.create(Section(estados[s])):
            x=0
            y=0
            for i in range(len(wave)):
                if wave[i][6]==estados[s] and int(wave[i][3])==int(tempo1.day):
                    x=1
                    if x==1 and y==0:
                        with doc.create(Subsection('Praias WAVECHECK')):
                            with doc.create(Tabular('|c|c|c|c|c|c|c|c|c|')) as table:
                                table.add_hline()
                                table.add_row(('ano','mes','dia','estado','nome','lat','lon','altura(m)','direcao'))
                                table.add_hline()
                                table.add_row((wave[i][1],wave[i][2],wave[i][3],wave[i][6],wave[i][7],wave[i][8],wave[i][9],wave[i][10],wave[i][12]))
                                x=2
                                y=1
                    else:
                        table.add_hline()
                        table.add_row((wave[i][1],wave[i][2],wave[i][3],wave[i][6],wave[i][7],wave[i][8],wave[i][9],wave[i][10],wave[i][12]))
                    if x!=0:
                        table.add_hline()




            if estados[s]=="Rio de Janeiro":
                with doc.create(Subsection('Praias RICO SURF')):
                    with doc.create(Tabular('|c|c|c|c|c|c|c|c|c|c|')) as table:
                        x=0
                        y=0
                        for i in range(len(rico)):
                            if int(rico[i][2])==tempo1.day:
                                x=1
                                if x==1 and y==0:
                                    table.add_hline()
                                    table.add_row(('ano','mes','dia','nome','lat','lon','altura(m)','periodo(s)','tsm(°C)','direcao'))
                                    table.add_hline()
                                    table.add_row((rico[i][0],rico[i][1],rico[i][2],rico[i][5][0:30],rico[i][6],rico[i][7],rico[i][8],rico[i][9],rico[i][10],rico[i][11]))
                                    x=2
                                    y=1
                                elif  int(rico[i][2])==tempo1.day:
                                    table.add_hline()
                                    table.add_row((rico[i][0],rico[i][1],rico[i][2],rico[i][5][0:30],rico[i][6],rico[i][7],rico[i][8],rico[i][9],rico[i][10],rico[i][11]))
                                if x!=0:
                                    table.add_hline()




            if estados[s]=="Rio Grande do Sul":
                with doc.create(Subsection('Simcosta')):
                    with doc.create(Tabular('|c|c|c|c|c|c|c|c|c|c|c|c|c|c|')) as table:
                        x=0
                        y=0
                        for i in range(len(simcosta)):
                            if simcosta[i][5]=='RS2' or simcosta[i][5]=='RS3' or simcosta[i][5]=='RS4' or simcosta[i][5]=='RS5':
                                if int(simcosta[i][3])>=tempo1.hour-4 and int(simcosta[i][2])==tempo1.day:
                                    x=1
                                    if x==1 and y==0:
                                        table.add_hline()
                                        table.add_row(('mes','dia','hora','min','boia','vvel(nós)','rajada(nós)','vdir','t_ar(°C)','t_ag(°C)','Hs(m)','Hmax(m)','Tp(s)','dirmed'))
                                        table.add_hline()
                                        if simcosta[i][8]!=None:
                                            value=arredondar1(float(simcosta[i][8])*1.94384)
                                        else:
                                            value=None
                                        if simcosta[i][9]!=None:
                                            value1=arredondar1(float(simcosta[i][9])*1.94384)
                                        else:
                                            value1=None
                                        table.add_row((simcosta[i][1],simcosta[i][2],simcosta[i][3],simcosta[i][4],simcosta[i][5],value,value1,simcosta[i][10],simcosta[i][11],simcosta[i][15],simcosta[i][16],simcosta[i][17],simcosta[i][18],simcosta[i][19]))
                                        x=2
                                        y=1
                                    else:
                                        table.add_hline()
                                        if simcosta[i][8]!=None:
                                            value=arredondar1(float(simcosta[i][8])*1.94384)
                                        else:
                                            value=None
                                        if simcosta[i][9]!=None:
                                            value1=arredondar1(float(simcosta[i][9])*1.94384)
                                        else:
                                            value1=None
                                        table.add_row((simcosta[i][1],simcosta[i][2],simcosta[i][3],simcosta[i][4],simcosta[i][5],value,value1,simcosta[i][10],simcosta[i][11],simcosta[i][15],simcosta[i][16],simcosta[i][17],simcosta[i][18],simcosta[i][19]))
                                    if x!=0:
                                        table.add_hline()

            if estados[s]=="Rio de Janeiro":
                with doc.create(Subsection('Simcosta')):
                    with doc.create(Tabular('|c|c|c|c|c|c|c|c|c|c|c|c|c|c|')) as table:
                        x=0
                        y=0
                        for i in range(len(simcosta)):
                            if simcosta[i][5]=='RJ3' or simcosta[i][5]=='RJ4':
                                if int(simcosta[i][3])>=tempo1.hour-4 and int(simcosta[i][2])==tempo1.day:
                                    x=1
                                    if x==1 and y==0:
                                        table.add_hline()
                                        table.add_row(('mes','dia','hora','min','boia','vvel(nós)','rajada(nós)','vdir','t_ar(°C)','t_ag(°C)','Hs(m)','Hmax(m)','Tp(s)','dirmed'))
                                        table.add_hline()
                                        if simcosta[i][8]!=None:
                                            value=arredondar1(float(simcosta[i][8])*1.94384)
                                        else:
                                            value=None
                                        if simcosta[i][9]!=None:
                                            value1=arredondar1(float(simcosta[i][9])*1.94384)
                                        else:
                                            value1=None
                                        table.add_row((simcosta[i][1],simcosta[i][2],simcosta[i][3],simcosta[i][4],simcosta[i][5],value,value1,simcosta[i][10],simcosta[i][11],simcosta[i][15],simcosta[i][16],simcosta[i][17],simcosta[i][18],simcosta[i][19]))
                                        x=2
                                        y=1
                                    else:
                                        table.add_hline()
                                        if simcosta[i][8]!=None:
                                            value=arredondar1(float(simcosta[i][8])*1.94384)
                                        else:
                                            value=None
                                        if simcosta[i][9]!=None:
                                            value1=arredondar1(float(simcosta[i][9])*1.94384)
                                        else:
                                            value1=None
                                        table.add_row((simcosta[i][1],simcosta[i][2],simcosta[i][3],simcosta[i][4],simcosta[i][5],value,value1,simcosta[i][10],simcosta[i][11],simcosta[i][15],simcosta[i][16],simcosta[i][17],simcosta[i][18],simcosta[i][19]))
                                    if x!=0:
                                        table.add_hline()

            if estados[s]=="Bahia":
                with doc.create(Subsection('Simcosta')):
                    with doc.create(Tabular('|c|c|c|c|c|c|c|c|c|c|c|c|c|c|')) as table:
                        x=0
                        y=0
                        for i in range(len(simcosta)):
                            if simcosta[i][5]=='BA1':
                                if int(simcosta[i][3])>=tempo1.hour-4 and int(simcosta[i][2])==tempo1.day:
                                    x=1
                                    if x==1 and y==0:
                                        table.add_hline()
                                        table.add_row(('mes','dia','hora','min','boia','vvel(nós)','rajada(nós)','vdir','t_ar(°C)','t_ag(°C)','Hs(m)','Hmax(m)','Tp(s)','dirmed'))
                                        table.add_hline()
                                        if simcosta[i][8]!=None:
                                            value=arredondar1(float(simcosta[i][8])*1.94384)
                                        else:
                                            value=None
                                        if simcosta[i][9]!=None:
                                            value1=arredondar1(float(simcosta[i][9])*1.94384)
                                        else:
                                            value1=None
                                        table.add_row((simcosta[i][1],simcosta[i][2],simcosta[i][3],simcosta[i][4],simcosta[i][5],value,value1,simcosta[i][10],simcosta[i][11],simcosta[i][15],simcosta[i][16],simcosta[i][17],simcosta[i][18],simcosta[i][19]))
                                        x=2
                                        y=1
                                    else:
                                        table.add_hline()
                                        if simcosta[i][8]!=None:
                                            value=arredondar1(float(simcosta[i][8])*1.94384)
                                        else:
                                            value=None
                                        if simcosta[i][9]!=None:
                                            value1=arredondar1(float(simcosta[i][9])*1.94384)
                                        else:
                                            value1=None
                                        table.add_row((simcosta[i][1],simcosta[i][2],simcosta[i][3],simcosta[i][4],simcosta[i][5],value,value1,simcosta[i][10],simcosta[i][11],simcosta[i][15],simcosta[i][16],simcosta[i][17],simcosta[i][18],simcosta[i][19]))
                                    if x!=0:
                                        table.add_hline()


            if estados[s]=="Espirito Santo":
                with doc.create(Subsection('Boias')):
                    with doc.create(Tabular('|c|c|c|c|c|c|c|c|c|c|c|')) as table:
                        x=0
                        y=0
                        for i in range(len(buoy_espiritosanto)):
                            if int(buoy_espiritosanto[i][3])>=tempo1.hour-6 and int(buoy_espiritosanto[i][2])==tempo1.day:
                                    x=1
                                    if x==1 and y==0:
                                        table.add_hline()
                                        table.add_row(('mes','dia','hora','min','vvel(nos)','vdir','t_ag(°C)','t_ar(°C)','Hs(m)','Tp(s)','dirmed'))
                                        table.add_hline()
                                        if buoy_espiritosanto[i][8]!=None:
                                            value=arredondar1(float(buoy_espiritosanto[i][8])*1.94384)
                                        else:
                                            value=None
                                        table.add_row((buoy_espiritosanto[i][1],buoy_espiritosanto[i][2],buoy_espiritosanto[i][3],buoy_espiritosanto[i][4],value,buoy_espiritosanto[i][9],buoy_espiritosanto[i][10],buoy_espiritosanto[i][11],buoy_espiritosanto[i][17],buoy_espiritosanto[i][16],buoy_espiritosanto[i][14]))
                                        x=2
                                        y=1
                                    else:
                                        table.add_hline()
                                        if buoy_espiritosanto[i][8]!=None:
                                            value=arredondar1(float(buoy_espiritosanto[i][8])*1.94384)
                                        else:
                                            value=None
                                        table.add_row((buoy_espiritosanto[i][1],buoy_espiritosanto[i][2],buoy_espiritosanto[i][3],buoy_espiritosanto[i][4],value,buoy_espiritosanto[i][9],buoy_espiritosanto[i][10],buoy_espiritosanto[i][11],buoy_espiritosanto[i][17],buoy_espiritosanto[i][16],buoy_espiritosanto[i][14]))
                                    if x!=0:
                                        table.add_hline()

            if estados[s]=="Rio de Janeiro":
                with doc.create(Subsection('Pnboia')):
                    with doc.create(Tabular('|c|c|c|c|c|c|c|c|c|c|c|c|c|')) as table:
                        x=0
                        y=0
                        for i in range(len(pnboia)):
                            if pnboia[i][4]=='itaguai':
                                if int(pnboia[i][3])>=tempo1.hour-8 and int(pnboia[i][2])==tempo1.day:
                                    x=1
                                    if x==1 and y==0:
                                        table.add_hline()
                                        table.add_row(('mes','dia','hora','boia','vvel(nós)','vdir','rajada(nós)','t_ar(°C)','t_ag(°C)','Hs(m)','Hmax(m)','Tp(m)','dirmed'))
                                        table.add_hline()
                                        try:
                                            value=arredondar1(float(pnboia[i][5])*1.94384)
                                        except:
                                            value=None
                                        try:
                                            value1=arredondar1(float(pnboia[i][7])*1.94384)
                                        except:
                                            value1=None
                                        table.add_row((pnboia[i][1],pnboia[i][2],pnboia[i][3],pnboia[i][4],value,pnboia[i][6],value1,pnboia[i][8],pnboia[i][9],pnboia[i][10],pnboia[i][11],pnboia[i][12],pnboia[i][13]))
                                        x=2
                                        y=1
                                    else:
                                        table.add_hline()
                                        try:
                                            value=arredondar1(float(pnboia[i][5])*1.94384)
                                        except:
                                            value=None
                                        try:
                                            value1=arredondar1(float(pnboia[i][7])*1.94384)
                                        except:
                                            value1=None
                                        table.add_row((pnboia[i][1],pnboia[i][2],pnboia[i][3],pnboia[i][4],value,pnboia[i][6],value1,pnboia[i][8],pnboia[i][9],pnboia[i][10],pnboia[i][11],pnboia[i][12],pnboia[i][13]))
                                    if x!=0:
                                        table.add_hline()

            if estados[s]=="Santa Catarina":
                with doc.create(Subsection('Pnboia')):
                    with doc.create(Tabular('|c|c|c|c|c|c|c|c|c|c|c|c|c|')) as table:
                        x=0
                        y=0
                        for i in range(len(pnboia)):
                            if pnboia[i][4]=='itajai':
                                if int(pnboia[i][3])>=tempo1.hour-8 and int(pnboia[i][2])==tempo1.day:
                                    x=1
                                    if x==1 and y==0:
                                        table.add_hline()
                                        table.add_row(('mes','dia','hora','boia','vvel(nós)','vdir','rajada(nós)','t_ar(°C)','t_ag(°C)','Hs(m)','Hmax(m)','Tp(m)','dirmed'))
                                        table.add_hline()
                                        try:
                                            value=arredondar1(float(pnboia[i][5])*1.94384)
                                        except:
                                            value=None
                                        try:
                                            value1=arredondar1(float(pnboia[i][7])*1.94384)
                                        except:
                                            value1=None
                                        table.add_row((pnboia[i][1],pnboia[i][2],pnboia[i][3],pnboia[i][4],value,pnboia[i][6],value1,pnboia[i][8],pnboia[i][9],pnboia[i][10],pnboia[i][11],pnboia[i][12],pnboia[i][13]))
                                        x=2
                                        y=1
                                    else:
                                        table.add_hline()
                                        try:
                                            value=arredondar1(float(pnboia[i][5])*1.94384)
                                        except:
                                            value=None
                                        try:
                                            value1=arredondar1(float(pnboia[i][7])*1.94384)
                                        except:
                                            value1=None
                                        table.add_row((pnboia[i][1],pnboia[i][2],pnboia[i][3],pnboia[i][4],value,pnboia[i][6],value1,pnboia[i][8],pnboia[i][9],pnboia[i][10],pnboia[i][11],pnboia[i][12],pnboia[i][13]))
                                    if x!=0:
                                        table.add_hline()


            if estados[s]=="Sergipe":
                with doc.create(Subsection('Boias')):
                    with doc.create(Tabular('|c|c|c|c|c|c|c|c|')) as table:
                        x=0
                        y=0
                        for i in range(len(otherbuoys)):
                            if int(otherbuoys[i][3])>=tempo1.hour and int(otherbuoys[i][2])==tempo1.day and otherbuoys[i][5]=='celse':
                                x=1
                                if x==1 and y==0:
                                    table.add_hline()
                                    table.add_row(('mes','dia','hora','minuto','Onda_dirmed','Hs(m)','vvel(nos)','rajada(nos)'))
                                    table.add_hline()
                                    if otherbuoys[i][14]!=None:
                                        value=arredondar1(float(otherbuoys[i][14])*1.94384)
                                    else:
                                        value=None
                                    if otherbuoys[i][15]!=None:
                                        value1=arredondar1(float(otherbuoys[i][15])*1.94384)
                                    else:
                                        value1=None
                                    table.add_row((otherbuoys[i][1],otherbuoys[i][2],otherbuoys[i][3],otherbuoys[i][4],otherbuoys[i][8],otherbuoys[i][9],value,value1))
                                    x=2
                                    y=1
                                else:
                                    table.add_hline()
                                    if otherbuoys[i][14]!=None:
                                        value=arredondar1(float(otherbuoys[i][14])*1.94384)
                                    else:
                                        value=None
                                    if otherbuoys[i][15]!=None:
                                        value1=arredondar1(float(otherbuoys[i][15])*1.94384)
                                    else:
                                        value1=None
                                    table.add_row((otherbuoys[i][1],otherbuoys[i][2],otherbuoys[i][3],otherbuoys[i][4],otherbuoys[i][8],otherbuoys[i][9],value,value1))
                                if x!=0:
                                    table.add_hline()


            if estados[s]=="Pernambuco":
                with doc.create(Subsection('Boias')):
                    with doc.create(Tabular('|c|c|c|c|c|c|c|c|')) as table:
                        x=0
                        y=0
                        for i in range(len(otherbuoys)):
                            if int(otherbuoys[i][3])>=tempo1.hour and int(otherbuoys[i][2])==tempo1.day and otherbuoys[i][5]=='suape':
                                x=1
                                if x==1 and y==0:
                                    table.add_hline()
                                    table.add_row(('mes','dia','hora','minuto','Onda_dirmed','Hs(m)','vvel(nos)','rajada(nos)'))
                                    table.add_hline()
                                    if otherbuoys[i][14]!=None:
                                        value=arredondar1(float(otherbuoys[i][14])*1.94384)
                                    else:
                                        value=None
                                    if otherbuoys[i][15]!=None:
                                        value1=arredondar1(float(otherbuoys[i][15])*1.94384)
                                    else:
                                        value1=None
                                    table.add_row((otherbuoys[i][1],otherbuoys[i][2],otherbuoys[i][3],otherbuoys[i][4],otherbuoys[i][8],otherbuoys[i][9],value,value1))
                                    x=2
                                    y=1
                                else:
                                    table.add_hline()
                                    if otherbuoys[i][14]!=None:
                                        value=arredondar1(float(otherbuoys[i][14])*1.94384)
                                    else:
                                        value=None
                                    if otherbuoys[i][15]!=None:
                                        value1=arredondar1(float(otherbuoys[i][15])*1.94384)
                                    else:
                                        value1=None
                                    table.add_row((otherbuoys[i][1],otherbuoys[i][2],otherbuoys[i][3],otherbuoys[i][4],otherbuoys[i][8],otherbuoys[i][9],value,value1))
                                if x!=0:
                                    table.add_hline()

    with doc.create(Section('NDBC e ALTIMETRO')):
        with doc.create(Tabular('|c|c|c|c|c|c|c|c|')) as table:
            x=0
            y=0
            for i in range(len(ndbc)):
                if int(ndbc[i][3])>=tempo1.hour-12 and int(ndbc[i][2])==tempo1.day and ndbc[i][9]!=None:
                    if float(ndbc[i][9])>=2.5:
                        x=1
                        if x==1 and y==0:
                            table.add_hline()
                            table.add_row(('mes','dia','hora','lat','lon','Hs(m)','Tp(s)','onda_dirmed'))
                            table.add_hline()
                            if ndbc[i][7]!=None:
                                value=arredondar1(float(ndbc[i][7])*1.94384)
                            else:
                                value=None
                            if ndbc[i][8]!=None:
                                value=arredondar1(float(ndbc[i][8])*1.94384)
                            else:
                                value=None
                            table.add_row((ndbc[i][1],ndbc[i][2],ndbc[i][3],ndbc[i][4],ndbc[i][5],ndbc[i][9],ndbc[i][10],ndbc[i][12]))
                            x=2
                            y=1
                        else:
                            table.add_hline()
                            if ndbc[i][7]!=None:
                                value=arredondar1(float(ndbc[i][7])*1.94384)
                            else:
                                value=None
                            if ndbc[i][8]!=None:
                                value=arredondar1(float(ndbc[i][8])*1.94384)
                            else:
                                value=None
                            table.add_row((ndbc[i][1],ndbc[i][2],ndbc[i][3],ndbc[i][4],ndbc[i][5],ndbc[i][9],ndbc[i][10],ndbc[i][12]))
                        if x!=0:
                            table.add_hline()
        with doc.create(Figure(position='h!')) as figura1:
            figura1.add_image('ndbc_mapa_ontem.png', width='550px')
            figura1.add_caption('Altura de onda em metros')
        with doc.create(Figure(position='h!')) as figura2:
            figura2.add_image('ndbc_mapa_hoje.png', width='550px')
            figura2.add_caption('Altura de onda em metros')
        with doc.create(Figure(position='h!')) as figura3:
            figura3.add_image('altimetro_mapa_18h.png', width='550px')
            figura3.add_caption('Altura de onda em metros')
        with doc.create(Figure(position='h!')) as figura4:
            figura4.add_image('altimetro_mapa_12h.png', width='550px')
            figura4.add_caption('Altura de onda em metros')
        with doc.create(Figure(position='h!')) as figura5:
            figura3.add_image('altimetro_mapa_6h.png', width='550px')
            figura3.add_caption('Altura de onda em metros')


if __name__ == '__main__':
    # Basic document

    datahora1=time.gmtime(time.time()-(3600*24))
    tempo2=datetime.datetime.strptime(str(datahora1[2])+"/"+str(datahora1[1])+"/"+str(datahora1[0]), '%d/%m/%Y')

#    doc = Document('basic')


    geometry_options = {
        "head": "10pt",
        "margin": "0.1in",
        "bottom": "0.1in",
        "includeheadfoot": False
    }

    doc = Document(documentclass='memoir',document_options=['10pt','a4paper'],
                                geometry_options=geometry_options, lmodern = True)

    new_comm1 = NoEscape(r'\trimFrame')
    doc.append(new_comm1)
    new_comm2 = NoEscape(r'\settrimmedsize{286mm}{198mm}{*}')
    doc.append(new_comm2)

    doc.preamble.append(Command('title', 'DADOS OBSERVACIONAIS'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    doc.append(Command('fontsize', arguments = ['10', '12']))
    doc.append(Command('selectfont'))

    fill_document(doc)

    nomearquivo='./Relatorio_apoio_oceanografico'
    doc.generate_pdf(nomearquivo, compiler='pdflatex')
    import os
    # os.chdir("/root/Public/remobs")
    ftp_pnboia("Relatorio_apoio_oceanografico.pdf")
    # ftp_pnboia1("Relatorio_apoio_oceanografico.pdf")

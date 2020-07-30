# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 23:34:44 2019

@author: tobia
"""

import mysql.connector as MySQLdb

import psutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import datetime
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
import operator

import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )

def alimentarbd(Data1,boia):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    cur.execute("SELECT datahora FROM buoy_espiritosanto WHERE esta_id='%s'\
    ORDER BY datahora DESC limit 20" % boia)
    for row in cur.fetchall():
        c1.append(row)
    if c1!=[]:
        for i in range(len(Data1)):
            if Data1[i][0]>max(c1)[0]:
                sql = "INSERT INTO buoy_espiritosanto (esta_id,datahora,wspd,wdir,wtmp,atmp,pres,\
                humi,mwd,spred,dpd,wvht)\
                VALUES (%s, '%s', %s, %s, %s, %s, %s,\
                %s, %s, %s, %s, %s)" % \
                (int(boia),(Data1[i][0]),(Data1[i][1]),(Data1[i][2]),(Data1[i][3]),\
                (Data1[i][4]),(Data1[i][5]),(Data1[i][6]),(Data1[i][7]),\
                (Data1[i][8]),(Data1[i][9]),(Data1[i][10]))
                cur.execute(sql)
                db.commit()
            else: #inserir update
                sql = "UPDATE buoy_espiritosanto SET esta_id=%s,datahora='%s',wspd=%s,wdir=%s,\
                wtmp=%s,atmp=%s,pres=%s,humi=%s,mwd=%s,spred=%s,dpd=%s,wvht=%s\
                WHERE esta_id=%s and datahora='%s'" % \
                (int(boia),(Data1[i][0]),(Data1[i][1]),(Data1[i][2]),(Data1[i][3]),\
                (Data1[i][4]),(Data1[i][5]),(Data1[i][6]),(Data1[i][7]),\
                (Data1[i][8]),(Data1[i][9]),(Data1[i][10]),(boia),(Data1[i][0]))
                cur.execute(sql)
                db.commit()
    else:
        for i in range(len(Data1)):
            sql = "INSERT INTO buoy_espiritosanto (esta_id,datahora,wspd,wdir,wtmp,atmp,pres,\
            humi,mwd,spred,dpd,wvht)\
            VALUES (%s, '%s', %s, %s, %s, %s, %s,\
            %s, %s, %s, %s, %s)" % \
            (int(boia),(Data1[i][0]),(Data1[i][1]),(Data1[i][2]),(Data1[i][3]),\
            (Data1[i][4]),(Data1[i][5]),(Data1[i][6]),(Data1[i][7]),\
            (Data1[i][8]),(Data1[i][9]),(Data1[i][10]))
            cur.execute(sql)
            db.commit()

    cur.close()
    db.close()




datahora=time.gmtime(time.time()-24*3600)
ano1=str(datahora.tm_year)
mes1=datahora.tm_mon
if mes1<10:
    mes1="0"+str(mes1)
else:
    mes1=str(mes1)
dia1=datahora.tm_mday
if dia1<10:
    dia1="0"+str(dia1)
else:
    dia1=str(dia1)

datahora=time.gmtime(time.time())
ano2=str(datahora.tm_year)
mes2=datahora.tm_mon
if mes2<10:
    mes2="0"+str(mes2)
else:
    mes2=str(mes2)
dia2=datahora.tm_mday
if dia2<10:
    dia2="0"+str(dia2)
else:
    dia2=str(dia2)
hora2=datahora.tm_hour


options = webdriver.FirefoxOptions()
options.add_argument('-headless')
#options.add_argument("--no-sandbox");
options.add_argument("--disable-dev-shm-usage");
options.set_preference("dom.disable_beforeunload", True)
options.set_preference("browser.tabs.warnOnClose", False)


print("conectando ao site da buoy_espiritosanto")
driver = webdriver.Firefox(options=options)
print("conectado com sucesso")

driver.get(user_config.espiritosanto_url)


time.sleep(6)
print("digitando usuario")
driver.find_element_by_css_selector("#id_sc_field_usuario").send_keys(user_config.espiritosanto_user)
print("digitando senha")
driver.find_element_by_css_selector("#id_sc_field_senha").send_keys(user_config.espiritosanto_psw)
print("clicando em ok")
driver.find_element_by_css_selector("#id_img_sub_form_b").click()
time.sleep(3)
print("indo para a secao de dados das boias")
action = ActionChains(driver);
zeroLevelMenu = driver.find_element_by_css_selector("#item_276 > span")
action.move_to_element(zeroLevelMenu).perform();
firstLevelMenu = driver.find_element_by_css_selector("#item_311 > span")
action.move_to_element(firstLevelMenu).perform();
secondLevelMenu = driver.find_element_by_css_selector("#item_278")
action.move_to_element(secondLevelMenu).perform();
secondLevelMenu.click();
time.sleep(6)

number = 0  # first frame
driver.switch_to.frame(number)
time.sleep(10)
print("selecionando a boia e o periodo de coleta de dados")
driver.find_element_by_css_selector("#SC_datalanc_dia").send_keys(dia1)
driver.find_element_by_css_selector("#SC_datalanc_mes").send_keys(mes1)
driver.find_element_by_css_selector("#SC_datalanc_ano").send_keys(ano1)
driver.find_element_by_css_selector("#SC_datalanc_input_2_dia").send_keys(dia2)
driver.find_element_by_css_selector("#SC_datalanc_input_2_mes").send_keys(mes2)
driver.find_element_by_css_selector("#SC_datalanc_input_2_ano").send_keys(ano2)
driver.find_element_by_css_selector("#SC_meteoname").click()
driver.find_element_by_css_selector("#SC_meteoname > option:nth-child(2)").click()

print("pesquisando os dados")
driver.find_element_by_css_selector("#id_img_Bbpassfld_rightall").click()
time.sleep(1)
driver.find_element_by_css_selector("#id_img_sc_b_pesq_bot").click()
time.sleep(4)



print("gerando tabela completa")
driver.find_element_by_css_selector("#quant_linhas_f0_bot").click()
driver.find_element_by_css_selector("option:nth-child(4)").click()
time.sleep(7)
soup=BeautifulSoup(driver.page_source, 'lxml')

# k=str(soup.encode("utf-8"))
# text_file = open('Output.txt', "w")
# text_file.write(k)
# text_file.close()


l=soup.find("table", {"id": "sc-ui-grid-body-2e80ed0d"})

#l=soup.find("tbody", {"id": "tbody_RelIMAREMETEOROLOGICO_2_bot"})

#l1 = l.find_all(attrs={"class": True})


l1 = l.find_all(attrs={"class": "scGridFieldOddFont css_meteoparamname_grid_line"})
parametro,datahora,valor=[],[],[]

for i in l1:
    parametro.append(i.get_text(strip=True))

l1 = l.find_all(attrs={"class": "scGridFieldOddFont css_datalanc_grid_line"})
for i in l1:
    kk=i.get_text(strip=True)
    datahora.append(datetime.datetime.strptime(kk, '%d/%m/%Y %H:%M:%S')+ datetime.timedelta(hours=3))


l1 = l.find_all(attrs={"class": "scGridFieldOddFont css_value_grid_line"})
for i in l1:
    valor.append(i.get_text(strip=True))

variables1=['Wind Speed','Wind Direction','Water temperature','Air Temperature','Atmosferic Pressure','Relative Humidity','Mean Wave Direction','Mean Wave Spread','Peak Wave Period','Significant Wave Height']

variables=['wspd','wdir','wtmp','atmp','pres','humi','mwd','spred','dpd','wvht']


tempo=[]
for i in range(21):
    if i+3<10:
        tempo.append(datetime.datetime.strptime(dia1+"/"+mes1+"/"+ano1+" 0"+str(i+3)+":00:00", '%d/%m/%Y %H:%M:%S'))
    else:
        tempo.append(datetime.datetime.strptime(dia1+"/"+mes1+"/"+ano1+" "+str(i+3)+":00:00", '%d/%m/%Y %H:%M:%S'))

for i in range(hora2+1):
    if i<10:
        tempo.append(datetime.datetime.strptime(dia2+"/"+mes2+"/"+ano2+" 0"+str(i)+":00:00", '%d/%m/%Y %H:%M:%S'))
    else:
        tempo.append(datetime.datetime.strptime(dia2+"/"+mes2+"/"+ano2+" "+str(i)+":00:00", '%d/%m/%Y %H:%M:%S'))




for i in range(len(variables)):
    exec("%s=['NULL']*len(tempo)"%variables[i])

for i in range(len(tempo)):
    for iii in range(len(parametro)):
        if tempo[i]==datahora[iii] and parametro[iii]=='Wind Speed':
            wspd[i]= float( '%.1f' % (float(valor[iii])))
        if tempo[i]==datahora[iii] and parametro[iii]=='Wind Direction':
            wdir[i]=int(float( '%.0f' % (float(valor[iii]))))
        if tempo[i]==datahora[iii] and parametro[iii]=='Water temperature':
            wtmp[i]=float( '%.1f' % (float(valor[iii])))
        if tempo[i]==datahora[iii] and parametro[iii]=='Air Temperature':
            atmp[i]=float( '%.1f' % (float(valor[iii])))
        if tempo[i]==datahora[iii] and parametro[iii]=='Atmosferic Pressure':
            pres[i]=float( '%.1f' % (float(valor[iii])))
        if tempo[i]==datahora[iii] and parametro[iii]=='Relative Humidity':
            humi[i]=float( '%.1f' % (float(valor[iii])))
        if tempo[i]==datahora[iii] and parametro[iii]=='Mean Wave Direction':
            mwd[i]=float(valor[iii])
        if tempo[i]==datahora[iii] and parametro[iii]=='Mean Wave Spread':
            spred[i]=float(valor[iii])
        if tempo[i]==datahora[iii] and parametro[iii]=='Peak Wave Period':
            dpd[i]=float(valor[iii])
        if tempo[i]==datahora[iii] and parametro[iii]=='Significant Wave Height':
            wvht[i]=float(valor[iii])


driver_process = psutil.Process(driver.service.process.pid)
#driver.quit()

if driver_process.is_running():
    print ("driver is running")

    firefox_process = driver_process.children()
    if firefox_process:
        firefox_process = firefox_process[0]

        if firefox_process.is_running():
            print("Firefox is still running, we can quit")
            driver.quit()
        else:
            print("Firefox is dead, can't quit. Let's kill the driver")
            firefox_process.kill()
    else:
        print("driver has died")

data = np.array([tempo,wspd,wdir,wtmp,atmp,pres,humi,mwd,spred,dpd,wvht])
data = data.transpose()
data3=sorted(data, key=operator.itemgetter(0))
alimentarbd(data3,1)



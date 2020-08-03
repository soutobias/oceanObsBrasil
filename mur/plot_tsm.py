

import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )

import pandas as pd



### DataViz Packages
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
from cartopy import config
from shapely import geometry



# Builded Packages
sys.path.insert(1,'/home/oceanObsBrasil/database')
from databaseMySQL import consulta_dados


# Dataframe from database

dados_sst = consulta_dados('mur', 'SELECT * FROM mur WHERE datahora = (SELECT max(datahora) FROM mur)')



# MetaAreas :

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




lons = [lon1, lon2, lon3, lon4, lon5, lon6, lon7, lon8, lon9, lon10]
lats = [lat1, lat2, lat3, lat4, lat5, lat6, lat7, lat8, lat9, lat10]



# Limites das áreas para plot

# Area Alfa
lat_a_1=-37
lat_a_2=-27
lon_a_1=-55
lon_a_2=-42


# Area Bravo
lat_b_1=-32
lat_b_2=-22
lon_b_1=-49
lon_b_2=-37

# Area Charlie
lat_c_1=-29
lat_c_2=-22
lon_c_1=-49
lon_c_2=-42

# Area Delta
lat_d_1=-27
lat_d_2=-16
lon_d_1=-42
lon_d_2=-32

# Area ECHO
lat_e_1=-22
lat_e_2=-12
lon_e_1=-40
lon_e_2=-32


# Area FOXTROT
lat_f_1=-16
lat_f_2=-3
lon_f_1=-39
lon_f_2=-25


# Area GOLF
lat_g_1 = -6
lat_g_2= 2
lon_g_1=-45
lon_g_2=-28


# Area HOTEL
lat_h_1=-37
lat_h_2=-27
lon_h_1=-55
lon_h_2=-42


# Box Coords das Metareas
# ex: lat_x_1 = min_coord , lat_x_2 = max_coord



metareas = pd.DataFrame({'Area':['Alfa','Bravo','Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf'],
                            'Lat_1': [lat_a_1, lat_b_1, lat_c_1, lat_d_1, lat_e_1, lat_f_1,lat_g_1],
                            'Lat_2': [lat_a_2, lat_b_2, lat_c_2, lat_d_2, lat_e_2, lat_f_2,lat_g_2],
                            'Lon_1': [lon_a_1, lon_b_1, lon_c_1, lon_d_1, lon_e_1, lon_f_1,lon_g_1],
                            'Lon_2': [lon_a_2, lon_b_2, lon_c_2, lon_d_2, lon_e_2, lon_f_2,lon_g_2]})






#
#
# # PLOT TODAS ZONAS
# fig = plt.figure(figsize=(10,10))
# i = 0
# for area in range(len(metareas)):
#     if metareas['Area'][area] == 'Bravo':
#         continue
#     else:
#         i += 1
#         ax = fig.add_subplot(2,3,i,projection=ccrs.PlateCarree())
#         ax.add_feature(cfeature.LAND)
#         ax.add_feature(cfeature.COASTLINE)
#         # ax.add_feature(states_provinces, edgecolor='gray')
#         # ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='0.8'))
#         ax.set_xlim(metareas['Lon_1'][area] , metareas['Lon_2'][area])
#         ax.set_ylim(metareas['Lat_1'][area] , metareas['Lat_2'][area])
#
#
#         # Colocando a zona
#         gr = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
#                      linewidth=0.5, color='gray', alpha=0.6, linestyle='--', fontsize = 6)
#
#
#
#



######### SUBPLOTS ZONAS ################################

# String details :
# date:
data_dados = max(dados_sst['datahora'])
data_plot = data_dados.strftime("%Y-%m-%d")



fig = plt.figure(figsize=(8,6))
i = 0
for area in range(len(metareas)):
    if metareas['Area'][area] == 'Bravo':
        continue
    else:
        i += 1
        ax = fig.add_subplot(2,3,i,projection=ccrs.PlateCarree())
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.COASTLINE)
        # ax.add_feature(states_provinces, edgecolor='gray')
        # ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='0.8'))
        ax.set_xlim(metareas['Lon_1'][area] , metareas['Lon_2'][area])
        ax.set_ylim(metareas['Lat_1'][area] , metareas['Lat_2'][area])


        # Colocando a zona
        gr = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                     linewidth=0.5, color='gray', alpha=0.6, linestyle='--')

        gr.top_labels = False
        gr.right_labels = False
        gr.xlabel_style = {'size':6}
        gr.ylabel_style = {'size':6}

        # Lines zones

        for zona in range(len(lats)):
            ax.plot(lons[zona],lats[zona],linewidth=0.5,color='k')



        ax.set_title("Área %s" % metareas['Area'][area])
        ax.set_box_aspect(1)



        # Colocando os ponto
        ax.scatter(dados_sst['lon'],dados_sst['lat'], c = dados_sst['sst'], s = 1.6,cmap = 'Reds')


        # Plotando temp em cada ponto :
        ## Condicional em Golf para mudar a posição dos valores
        for pos in range(len(dados_sst)):
            if metareas['Area'][area] == 'Golf':
                if dados_sst['lat'][pos] > metareas['Lat_1'][area] and dados_sst['lat'][pos] < metareas['Lat_2'][area]:
                    ax.annotate(str(round(dados_sst['sst'][pos],1)),xy=(dados_sst['lon'][pos]+0.15,dados_sst['lat'][pos]+0.15),color='k',fontsize=4, fontweight = 'bold')
            else:
                if dados_sst['lat'][pos] > metareas['Lat_1'][area] and dados_sst['lat'][pos] < metareas['Lat_2'][area]:
                    ax.annotate(str(round(dados_sst['sst'][pos],1)),xy=(dados_sst['lon'][pos]+0.15,dados_sst['lat'][pos]),color='k',fontsize=4, fontweight = 'bold')



        # set a margin around the data


        ax.margins(0.005,0.005)



fig.subplots_adjust(top=0.9, bottom=0.08, hspace = 0.05)
fig.suptitle("TSM - %s" % data_plot, size = 16, y = 0.95)
plt.savefig("tsm_ultimo_dado.jpg", dpi = 300)

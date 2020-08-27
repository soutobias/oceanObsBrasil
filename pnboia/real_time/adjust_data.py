import pandas as pd
import time_codes
import numpy as np
from datetime import datetime
import time_codes

def adjust_data(raw_data):

    anodia, horamin = [], []
    anodia1, horamin1 = [], []
    year0, month0, day0, hour0 = [], [], [], []
    sensor00, lat, lon = [], [], []
    year, month, day, hour, minute, battery = [], [], [], [], [], []
    flood, wspd1, gust1, wdir1, wspd2, gust2, wdir2 = [], [], [], [], [], [], []
    atmp, humi, dewp, pres, wtmp, bhead, cloro, turb, arad = [], [], [], [], [], [], [], [], []
    cvel1, cdir1, cvel2, cdir2, cvel3, cdir3, wvht, wmax, dpd, mwd, spred = [], [], [], [], [], [], [], [], [], [], []
    epoca = []

    for data in raw_data:

        if int(float(data[5])) == 1 and float(data[7]) <= 12 and float(data[8]) <= 23:

            year0.append(int(data[4].year))
            month0.append(int(data[4].month))
            day0.append(int(data[4].day))
            hour0.append(int(data[4].hour))
            sensor00.append(int(float(data[5])))

            if data[2] != np.nan:
                lat.append(float(data[2]))
                lon.append(float(data[3])-360)
            else:
                lat.append((data[2]))
                lon.append((data[3]))

            year.append(int(float(data[6])))
            month.append(int(float(data[7])))
            day.append(int(float(data[8])))
            hour.append(int(float(data[9])))
            minute.append(20)
            battery.append(float(data[16]))
            flood.append(int(float(data[19])))
            wspd1.append(float(data[20]))
            gust1.append(float(data[21]))
            wdir1.append(float(data[22]))
            wspd2.append(float(data[23]))
            gust2.append(float(data[24]))
            wdir2.append(float(data[25]))

            atmp.append(np.nan)
            humi.append(np.nan)
            dewp.append(np.nan)
            pres.append(np.nan)
            wtmp.append(np.nan)
            bhead.append(np.nan)
            cloro.append(np.nan)
            turb.append(np.nan)
            arad.append(np.nan)
            cvel1.append(np.nan)
            cdir1.append(np.nan)
            cvel2.append(np.nan)
            cdir2.append(np.nan)
            cvel3.append(np.nan)
            cdir3.append(np.nan)
            wvht.append(np.nan)
            wmax.append(np.nan)
            dpd.append(np.nan)
            mwd.append(np.nan)
            spred.append(np.nan)

            epoca.append((datetime.datetime(int(float(data[6])),int(float(data[7])),int(float(data[8])),int(float(data[9])),0) - datetime.datetime(1970,1,1)).total_seconds())

        elif int(float(data[5]))==2:
            year0.append(int(data[4].year))
            month0.append(int(data[4].month))
            day0.append(int(data[4].day))
            hour0.append(int(data[4].hour))

            sensor00.append(int(float(data[5])))
            if data[2] != np.nan and data[2] != '-9999':
                lat.append(float(data[2]))
                lon.append(float(data[3])-360)
            else:
                lat.append(np.nan)
                lon.append(np.nan)

            year.append(int(float(year0[-1])))
            month.append(int(float(month0[-1])))
            day.append(int(float(day0[-1])))
            hour.append(int(float(data[6])))
            minute.append(20)
            wspd1.append(float(data[7]))
            gust1.append(float(data[8]))
            wdir1.append(float(data[9]))
            atmp.append(float(data[10]))
            humi.append(float(data[11]))
            dewp.append(float(data[12]))
            pres.append(float(data[13]))
            wtmp.append(float(data[14]))
            bhead.append(float(data[16]))
            cloro.append(float(data[17]))
            turb.append(float(data[18]))
            arad.append(float(data[19]))
            cvel1.append(float(data[20]))
            cdir1.append(float(data[21]))
            cvel2.append(float(data[22]))
            cdir2.append(float(data[23]))
            cvel3.append(float(data[24]))
            cdir3.append(float(data[25]))
            wvht.append(float(data[26]))
            wmax.append(float(data[27]))
            dpd.append(float(data[28]))
            mwd.append(float(data[29]))
            spred.append(float(data[30]))

            battery.append(np.nan)
            flood.append(np.nan)
            wspd2.append(np.nan)
            gust2.append(np.nan)
            wdir2.append(np.nan)

            if hour[-1]==23 and int(hour0[-1])==0:
                if day0[-1]!=1:
                    day[-1]=day0[-1]-1
                else:
                    if month[-1]==1:
                        year[-1]=year[-1]-1
                        month[-1]=12
                        day[-1]=31
                    elif month[-1]==3:
                        month[-1]=month[-1]-1
                        day[-1]=28
                    elif month[-1]==5 or month[-1]==7 or month[-1]==10 or month[-1]==12:
                        day[-1]=30
                        month[-1]=month[-1]-1
                    else:
                        day[-1]=31
                        month[-1]=month[-1]-1
                        continue
                    continue

            elif int(hour[-1])==22 and int(hour0[-1])==0:
                if int(day0[-1])!=1:
                    day[-1]=day0[-1]-1
                else:
                    if int(month[-1])==1:
                        year[-1]=year[-1]-1
                        month[-1]=12
                        day[-1]=31
                    elif int(month[-1])==3:
                        month[-1]=month[-1]-1
                        day[-1]=28
                    elif int(month[-1])==5 or int(month[-1])==7 or int(month[-1])==10 or int(month[-1])==12:
                        day[-1]=30
                        month[-1]=month[-1]-1
                    else:
                        day[-1]=31
                        month[-1]=month[-1]-1
                        continue
                    continue

            elif int(hour[-1])==22 and int(hour0[-1])==1:
                if int(day0[-1])!=1:
                    day[-1]=day0[-1]-1
                else:
                    if int(month[-1])==1:
                        year[-1]=year[-1]-1
                        month[-1]=12
                        day[-1]=31
                    elif int(month[-1])==3:
                        month[-1]=month[-1]-1
                        day[-1]=28
                    elif int(month[-1])==5 or int(month[-1])==7 or int(month[-1])==10 or int(month[-1])==12:
                        day[-1]=30
                        month[-1]=month[-1]-1
                    else:
                        day[-1]=31
                        month[-1]=month[-1]-1
                        continue
                    continue

            elif int(hour[-1])==23 and int(hour0[-1])==1:
                if int(day0[-1])!=1:
                    day[-1]=day0[-1]-1
                else:
                    if int(month[-1])==1:
                        year[-1]=year[-1]-1
                        month[-1]=12
                        day[-1]=31
                    elif int(month[-1])==3:
                        month[-1]=month[-1]-1
                        day[-1]=28
                    elif int(month[-1])==5 or int(month[-1])==7 or int(month[-1])==10 or int(month[-1])==12:
                        day[-1]=30
                        month[-1]=month[-1]-1
                    else:
                        day[-1]=31
                        month[-1]=month[-1]-1
                        continue
                    continue
            else:
                day[-1]=day0[-1]

    df = pd.DataFrame({
        'lat': lat,
        'lon': lon,
        'sensor00': sensor00,
        'year': year,
        'month': month,
        'day': day,
        'hour': hour,
        'minute': minute,
        'wspd1': wspd1,
        'gust1': gust1,
        'wdir1': wdir1,
        'wspd2': wspd2,
        'gust2': gust2,
        'wdir2': wdir2,
        'battery': battery,
        'flood': flood,
        'atmp': atmp,
        'humi': humi,
        'dewp': dewp,
        'pres': pres,
        'arad': arad,
        'wtmp': wtmp,
        'cloro': cloro,
        'turb': turb,
        'cvel1': cvel1,
        'cdir1': cdir1,
        'cvel2': cvel2,
        'cdir2': cdir2,
        'cvel3': cvel3,
        'cdir3': cdir3,
        'wvht': wvht,
        'wmax': wmax,
        'dpd': dpd,
        'mwd': mwd,
        'spred': spred,
        'bhead': bhead,
        })


    df['data'] = [datetime.strptime(str(int(df.year[i])) +  \
        str(int(df.month[i])).zfill(2) + str(int(df.day[i])).zfill(2) + \
        str(int(df.hour[i])).zfill(2),'%Y%m%d%H') for i in range(len(df))]

    df = df.set_index('data')

    gmtime = time_codes.gmtime()

    last_month = time_codes.last_month()

    df = df.loc[last_month: gmtime]

    del df['year']
    del df['month']
    del df['day']
    del df['hour']
    del df['minute']

    return df.reset_index().sort_values(by=['data', 'sensor00']).set_index('data')

def adjust_different_message_data(df):

    df = df.reset_index().drop_duplicates(subset=['data', 'sensor00'], keep='first').sort_values(by=['data', 'sensor00']).set_index('data')

    for i in range(len(df) - 1):
        if df.index[i] == df.index[i + 1]:
            df['lat'][i] = df['lat'][i+1]
            df['lon'][i] = df['lon'][i+1]
            df['sensor00'][i] = df['sensor00'][i+1]
            df['year'][i] = df['year'][i+1]
            df['month'][i] = df['month'][i+1]
            df['day'][i] = df['day'][i+1]
            df['hour'][i] = df['hour'][i+1]
            df['minute'][i] = df['minute'][i+1]
            df['atmp'][i] = df['atmp'][i+1]
            df['humi'][i] = df['humi'][i+1]
            df['dewp'][i] = df['dewp'][i+1]
            df['pres'][i] = df['pres'][i+1]
            df['arad'][i] = df['arad'][i+1]
            df['wtmp'][i] = df['wtmp'][i+1]
            df['cloro'][i] = df['cloro'][i+1]
            df['turb'][i] = df['turb'][i+1]
            df['cvel1'][i] = df['cvel1'][i+1]
            df['cdir1'][i] = df['cdir1'][i+1]
            df['cvel2'][i] = df['cvel2'][i+1]
            df['cdir2'][i] = df['cdir2'][i+1]
            df['cvel3'][i] = df['cvel3'][i+1]
            df['cdir3'][i] = df['cdir3'][i+1]
            df['wvht'][i] = df['wvht'][i+1]
            df['wmax'][i] = df['wmax'][i+1]
            df['dpd'][i] = df['dpd'][i+1]
            df['mwd'][i] = df['mwd'][i+1]
            df['spred'][i] = df['spred'][i+1]
            df['bhead'][i] = df['bhead'][i+1]

    df = df.reset_index().drop_duplicates(subset=['data', 'sensor00'], keep='first').sort_values(by=['data', 'sensor00']).set_index('data')

    return df

def rotate_data(df, flag, buoy):

    df['tmp_dec'] = (df.index.year - 2002) * float(buoy["vardeclinacao"]) + float(buoy["declinacao"])

    df.loc[flag['cdir1'] == 0, "cdir1"] = df['cdir1'] - df['tmp_dec']
    df.loc[df["cdir1"] < 0, "cdir1"] = df["cdir1"] + 360

    df.loc[flag['cdir2'] == 0, "cdir2"] = df['cdir2'] - df['tmp_dec']
    df.loc[df["cdir2"] < 0, "cdir2"] = df["cdir2"] + 360

    df.loc[flag['cdir3'] == 0, "cdir3"] = df['cdir3'] - df['tmp_dec']
    df.loc[df["cdir3"] < 0, "cdir3"] = df["cdir3"] + 360

    df.loc[flag['wdir'] == 0, "wdir"] = df['wdir'] - df['tmp_dec']
    df.loc[df["wdir"] < 0, "wdir"] = df["wdir"] + 360

    df.loc[flag['mwd'] == 0, "mwd"] = df['mwd'] - df['tmp_dec']
    df.loc[df["mwd"] < 0, "mwd"] = df["mwd"] + 360

    del df['tmp_dec']
    del df['sensor00']

    return df

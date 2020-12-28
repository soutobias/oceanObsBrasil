import psycopg2 as pg
from sqlalchemy import create_engine

import os
import sys

sys.path.append(os.environ['HOME'])
import user_config

import pandas as pd

def conn_qc_db():
    user = user_config.username_postgre
    passw = user_config.password_postgre
    host = user_config.host_postgre
    db = user_config.database_postgre
    engine = create_engine('postgres+psycopg2://' + user + ":" + passw + "@" + host + "/" + db)
    return engine

def select_station(columns, values):

    con = conn_qc_db()

    where = 'WHERE '
    for i in range(len(columns)):
        where = where + "%s = '%s' AND " % (columns[i], values[i])
    where = where[0:-4]
    print

    query = "SELECT * FROM stations %s" % (where)

    buoy_ids = pd.read_sql_query(query, con)

    return buoy_ids

def delete_old_data(df, station):

    con = conn_qc_db()

    query = "DELETE FROM data_stations WHERE station_id = %s AND date_time >= '%s'" % (station, df["date_time"].min())

    cur = con.connect()

    cur.execute(query)

    print("deleted old data")

def insert_new_data(df):

    con = conn_qc_db()

    df.to_sql(con=con, name='data_stations', if_exists='append', index=False)

    print("inserted new data")

def query_last_data(columns, values):

    con = conn_qc_db()

    where = 'WHERE '
    for i in range(len(columns)):
        where = where + "%s = '%s' AND " % (columns[i], values[i])
    where = where[0:-5]

    query = "SELECT * FROM data_no_stations %s ORDER BY date_time DESC LIMIT 1" % (where)

    no_stations = pd.read_sql_query(query, con)

    return no_stations

def delete_old_data_no_station(df):

    con = conn_qc_db()

    query = "DELETE FROM data_no_stations WHERE type = '%s' AND institution = '%s'  AND date_time >= '%s'" % (df.type[0], df.institution[0], df["date_time"].min())

    cur = con.connect()

    cur.execute(query)

    print("deleted old data")

def insert_new_data_no_station(df):

    con = conn_qc_db()

    df.to_sql(con=con, name='data_no_stations', if_exists='append', index=False)

    print("inserted new data")


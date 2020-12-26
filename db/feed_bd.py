import pandas as pd

from pandas.io import sql
import psycopg2 as pg
from sqlalchemy import create_engine

def conn_qc_db():

    user='oceanobsbrasil'
    passw='Marinha1@'
    host='oceanobsbrasil.postgres.uhserver.com'
    db='oceanobsbrasil'

    engine = create_engine('postgres+psycopg2://' + user + ":" + passw + "@" + host + "/" + db)

    return engine

x = pd.read_csv('stations.csv', sep = '\t')

con = conn_qc_db()

x.to_sql(con=con, name='stations', if_exists='append', index=False)

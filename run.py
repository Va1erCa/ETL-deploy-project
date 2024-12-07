import os.path
from datetime import datetime, timedelta
import pandas as pd
import configparser
from yahoo_fin.stock_info import get_data

from pgdb import PGDatabase

config = configparser.ConfigParser()
config.read('config.ini')

SALES_PATH = config['Files']['SALES_PATH']
COMPANIES = eval(config['Companies']['COMPANIES'])
DATABASE_CREDS = config['Database']

sales_df = pd.DataFrame()
if os.path.exists(SALES_PATH):
    sales_df = pd.read_csv(SALES_PATH)
    os.remove(SALES_PATH)

historical_d = {}
for company in COMPANIES:
    historical_d[company] = get_data(
        company,
        start_date=(datetime.today() - timedelta(days=1)).strftime('%m/%d/%Y'),
        end_date=datetime.today().strftime('%m/%d/%Y')
    ).reset_index()

database = PGDatabase(
    host=DATABASE_CREDS['HOST'],
    database=DATABASE_CREDS['DATABASE'],
    user=DATABASE_CREDS['USER'],
    password=DATABASE_CREDS['PASSWORD']
)

for i, row in sales_df.iterrows():
    query = 'insert into sales values (%s, %s, %s, %s)'
    database.post(query, (row['dt'], row['company'], row['transaction_type'], row['amount']))

for company, data in historical_d.items():
    for i, row in data.iterrows():
        query = 'insert into stock values (%s, %s, %s, %s)'
        database.post(query, (row['index'], row['ticker'], row['open'], row['close']))
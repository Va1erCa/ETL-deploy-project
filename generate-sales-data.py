# Module for creating fake data

import pandas as pd
from datetime import datetime, timedelta
from random import randint
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

COMPANIES = eval(config['Companies']['COMPANIES'])

today = datetime.today()
yesterday = today - timedelta(days=1)
if 1 <= today.weekday() <= 5 :
    d = {
        'dt' : [yesterday.strftime('%d/%m/%Y')] * len(COMPANIES) * 2,
        'company' : COMPANIES * 2,
        'transaction_type' : ['buy'] * len(COMPANIES) + ['sell'] * len(COMPANIES),
        'amount' : [randint(0, 1000) for _ in range(len(COMPANIES) * 2)]
    }
    df = pd.DataFrame(d)
    df.to_csv('sales_data.csv', index=False)


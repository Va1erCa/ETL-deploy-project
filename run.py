import os.path
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

SALES_PATH = config['Files']['SALES_PATH']

if os.path.exists(SALES_PATH):
    sales_df = pd.read_csv(SALES_PATH)
    print(sales_df)
    os.remove(SALES_PATH)

"""
Data Import Script: 

Python script to initialize database and load in historical data

"""

import pandas as pd
import numpy as np
import sqlite3

federal_api = 'https://api.covidtracking.com/v1/us/daily.json'
state_api = 'https://api.covidtracking.com/v1/states/daily.json'

federal_df = pd.read_json(federal_api)
state_df = pd.read_json(state_api)

# Update Date
federal_df['date'] = pd.to_datetime(federal_df['date'].astype(str), format='%Y%m%d')
state_df['date'] = pd.to_datetime(state_df['date'].astype(str), format='%Y%m%d')

# Setup SQLite3 Database
db_name = '../data/output_data/covidDB.db'
conn = sqlite3.connect(db_name)

try:
    federal_df.to_sql('federaldata', conn, index=False)
    state_df.to_sql('statedata', conn, index=False)
except:
    raise
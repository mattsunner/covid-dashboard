"""
Data Import Script: 

Python script to initialize database and load in historical data

"""

import pandas as pd
import numpy as np
import sqlite3

federal_api = 'https://api.covidtracking.com/v1/us/current.json'
state_api = 'https://api.covidtracking.com/v1/states/current.json'

federal_df = pd.read_json(federal_api)
state_df = pd.read_json(state_api)

# Update Date with Daily Values
federal_df['date'] = pd.to_datetime(federal_df['date'].astype(str), format='%Y%m%d')
state_df['date'] = pd.to_datetime(state_df['date'].astype(str), format='%Y%m%d')

db_name = '../data/output_data/covidDB.db'
conn = sqlite3.connect(db_name)

federal_df.to_sql('federaldata', conn, index=False, if_exists='append')
state_df.to_sql('statedata', conn, index=False, if_exists='append')

conn.commit()

# Check if Persistence Matches Current API

persistent_federal_df = pd.read_sql('SELECT * FROM federaldata', conn)
persistent_state_df = pd.read_sql('SELECT * FROM statedata', conn)

federal_full_api = 'https://api.covidtracking.com/v1/us/daily.json'
state_full_api = 'https://api.covidtracking.com/v1/states/daily.json'

federal_full_df = pd.read_json(federal_full_api)
state_full_df = pd.read_json(state_full_api)


conn.close()




""" 
Process: 
- Load in new day values for federal/state statistics -- cleaned and ready for storage
- Check if full federal/state datasets match the current database 
- If they match, break and save the dataset
- If they do not match, delete the persisted data and reload a new full dataset (This assumes that updates were made)
- Disconnect from the database and save it
"""


# # Custom Script Methods
# def silentremove(filename):
#     try:
#         os.remove(filename)
#     except OSError as e:
#         if e.errno != errno.ENOENT:
#             raise
"""
Data Import Script: 

Python script to initialize database and load in historical data

"""

import pandas as pd
import numpy as np
import sqlite3


def update_database(federal_api, state_api, conn):
    """update_database: Method to update the database with new COVID-19 daily data

    Args:
        federal_api (str): URL for the federal API 
        state_api (str): URL for the state API
        conn (connection): SQLite3 connection method call and database name information
    """
    conn = conn

    federal_df = pd.read_json(federal_api)
    state_df = pd.read_json(state_api)

    df_persistent_fed = pd.read_sql('SELECT * FROM federaldata', conn)
    hash_key_fed = federal_df['hash'][0]

    check_federal = df_persistent_fed['hash'][df_persistent_fed['hash'].str.contains(hash_key_fed)].count()

    if check_federal == 0:
        # Update Date Formatting
        federal_df['date'] = pd.to_datetime(federal_df['date'].astype(str), format='%Y%m%d')
        state_df['date'] = pd.to_datetime(state_df['date'].astype(str), format='%Y%m%d')
        
        federal_df.to_sql('federaldata', conn, index=False, if_exists='append')
        state_df.to_sql('statedata', conn, index=False, if_exists='append')

        conn.commit()
        conn.close()
    else:
        print('Database is already up to date.')

        conn.close()


def main():
    federal_api = 'https://api.covidtracking.com/v1/us/current.json'
    state_api = 'https://api.covidtracking.com/v1/states/current.json'
    conn = sqlite3.connect('../data/output_data/covidDB.db')

    update_database(federal_api, state_api, conn)



if __name__ == '__main__':
    main()









#import needed libraries
from sqlalchemy import create_engine
import pandas as pd
import os
from sqlalchemy.engine import URL

# Get password and username from environment variables
pwd = os.environ['PGPASS']
uid = os.environ['PGUID']
uid1 = 'postgres'
pass1 = 'Nisha%402903'
# SQL Server DB connection details
driv = "{ODBC Driver 11 for SQL Server}"  # Updated ODBC Driver
serv = "localhost\SQLEXPRESS"  # Use localhost or "localhost\SQLEXPRESS" for named instance
datab = "AdventureWorksDW2019"
serv2 = "localhost"
# print(platform.architecture())

#extract data from sql server
def extract():
    try:
        connection_string = 'DRIVER=' + driv + ';SERVER=' + serv + ';DATABASE=' + datab + ';UID=' + uid + ';PWD=' + pwd
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        src_conn = create_engine(connection_url)
        tbl_name = "DimProduct"
        #query and load save data to dataframe
        df = pd.read_sql_query(f'select * FROM {tbl_name}', src_conn)
        return df, tbl_name
    except Exception as e:
        print("Data extract error: " + str(e))

#load data to postgres
def load(df, tbl):
    try:
        rows_imported = 0
        engine = create_engine(f'postgresql://{uid1}:{pass1}@{serv2}:5432/AdventureWorks')
        print(f'importing rows {rows_imported} to {rows_imported + len(df)}... for table {tbl}')
        # save df to postgres
        df.to_sql(f'stg_{tbl}', engine, if_exists='replace', index=False)
        rows_imported += len(df)
        # add elapsed time to final print out
        print("Data imported successful")
    except Exception as e:
        print("Data load error: " + str(e))


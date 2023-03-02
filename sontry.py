#!/usr/bin/env python
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
import sqlalchemy
import mysql.connector
#connect to MySQL DB in docker
import mysql.connector

mydb = mysql.connector.connect(
  host="172.17.0.2",
  user="root",
  password="E-Kalite"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS covid_world;")

db_username = 'root'
db_password = 'E-Kalite'
db_ip       = '172.17.0.2'
db_name     = 'covid_world'
db_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                         format(db_username, db_password, db_ip, db_name))
website='https://www.worldometers.info/coronavirus/#countries'
website_url=requests.get(website).text
soup = BeautifulSoup(website_url,'html.parser')

my_table = soup.find('tbody')

table_data = []
for row in my_table.findAll('tr'):
    row_data = []
    for cell in row.findAll('td'):
        row_data.append(cell.text)
    if(len(row_data) > 0):
        data_item = {"Country": row_data[0],
                     "TotalCases": row_data[1],
                     "NewCases": row_data[2],
                     "TotalDeaths": row_data[3],
                     "NewDeaths": row_data[4],
                     "TotalRecovered": row_data[5],
                     "ActiveCases": row_data[6],
                     "CriticalCases": row_data[7],
                     "Totcase1M": row_data[8],
                     "Totdeath1M": row_data[9],
                     "TotalTests": row_data[10],
                     "Tottest1M": row_data[11],
        }
        table_data.append(data_item)

df = pd.DataFrame(table_data)

df.to_sql(con=db_connection, name='covid_world', if_exists='replace')

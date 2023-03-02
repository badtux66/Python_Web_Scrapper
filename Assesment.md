### Here it pulls the os down and automatically creates the vm
>$ sudo vagrant box add centos/7 
### installing docker
>$ sudo yum install docker
# Q1
### This command downloads the docker image from docker hub then creates the container maps port 3306 of the docker container to the same port of the localhost
>$ sudo docker run -p 127.0.0.1:3306:3306  --name ekalite-mariadb -e MARIADB_ROOT_PASSWORD=E-Kalite -d mariadb:latest<br>
# Q2
### uploading the file
>$ vagrant upload /home/badtux/covid19-table.sql
#### badtux is my home directory
### This command executes the mysql shell then runs the mysql command in the shell
> $ sudo docker exec -i ekalite-mariadb sh -c 'exec mysql -uroot -pE-Kalite' </home/vagrant/covid19-table.sql

### Here it pulls the os down and automatically creates the vm
>\$ sudo vagrant box add centos/7 install docker <br>

# Q3
### Since all the modules work on after python 3.9 releases, it didn't run on centos/7 and ubuntu 20.04 but ran on ubuntu 20.04 thus it was configured to run as a docker container in order to avoid compatibility issues
<pre>
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
</pre>
<br>

# Q4

><pre>$ sudo docker exec -i ekalite-mariadb sh -c 'CREATE TABLE challange.table1 SELECT * FROM covid_world.table1'
</pre>
<br>

# Q5

><pre> watch -n 600 $(python3 sontry.py && sudo docker exec -i ekalite-mariadb sh -c 'CREATE TABLE challange.table1 SELECT * FROM covid_world.table1')
</pre>
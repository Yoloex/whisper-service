import mysql.connector
import yaml

with open('cfg/server.yaml') as f:
    cfg = yaml.safe_load(f.read())
    db_cfg = cfg['database']

mydb = mysql.connector.connect(host=db_cfg['host'], user=db_cfg['user'], password=db_cfg['password'])
cursor = mydb.cursor(buffered=True)

found = False

cursor.execute("show databases;")

for x in cursor:
    if x[0] == 'test':
        found = True

if not found:
    cursor.execute('create database test;')

cursor.execute('select database() test;')
cursor.execute('show tables in test;')

found = False

for x in cursor:
    if x[0] == 'calldata':
        found = True

cursor.execute('Use test;')

if not found:
    sql = "CREATE TABLE calldata " + \
          "(idx INT AUTO_INCREMENT PRIMARY KEY, groupid VARCHAR(5), id VARCHAR(5), dateid DATE, timeid TIME, content TEXT);"
    cursor.execute(sql)

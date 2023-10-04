import mysql.connector
import getpass

password = getpass.getpass()

mydb = mysql.connector.connect(host='localhost', user='root', password=password)
cursor = mydb.cursor(buffered=True)

found = False

cursor.execute("show databases;")

for x in cursor:
    if x[0] == 'test':
        found = True

if not found:
    cursor.execute('create test;')

cursor.execute('select database() test;')
cursor.execute('show tables in test;')

found = False

for x in cursor:
    if x[0] == 'calldata':
        found = True

if not found:
    sql = "CREATE TABLE calldata " + \
          "(idx INT AUTO_INCREMENT PRIMARY KEY, groupid VARCHAR(5), id VARCHAR(5), dateid DATE, timeid TIME, content TEXT);"
    cursor.execute(sql)

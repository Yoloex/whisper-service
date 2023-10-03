import mysql.connector

mydb = mysql.connector.connect(host='localhost', user='root', password='notouch1234!@#$')
mycursor = mydb.cursor()

found = False

mycursor.execute("show databases;")

for x in mycursor:
    if x[0] == 'test':
        found = True

if not found:
    mycursor.execute('create test;')

mycursor.execute('select database() test;')

print([x for x in mycursor])

mycursor.execute('show tables in test;')

found = False

for x in mycursor:
    print(x)
    if x[0] == 'calldata':
        found = True

if not found:
    sql = "CREATE TABLE calldata " + \
          "(idx INT AUTO_INCREMENT PRIMARY KEY, groupid VARCHAR(5), id VARCHAR(5), dateid DATE, timeid TIME, content TEXT);"
    mycursor.execute(sql)
    print([x for x in mycursor])

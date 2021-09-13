import mysql.connector
from getpass import getpass
from mysql.connector import connect

connection = connect(host='us-cdbr-east-04.cleardb.com', 
    user='b7a35a7346aea6', 
    password='a2aa8c36', 
    database='heroku_38066fac900fae9')
cursor = connection.cursor()
f = open('leads.txt', 'w')

q = 'SELECT name from survey;'
cursor.execute(q)
results = cursor.fetchall()

for r in results:
    lead = r[0]
    url = 'https://www.similarweb.com/website/{}/'.format(lead)
    f.write(url)
f.close()
print('all done!')
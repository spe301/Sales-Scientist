import mysql.connector
from getpass import getpass
from mysql.connector import connect

connection = connect(host='localhost', user='root', password='Raptor//Kona9', database='covid19')
cursor = connection.cursor()

q = '''Show TABLES;'''
cursor.execute(q)
results = cursor.fetchall()

def getCols(table):
    q = 'SHOW COLUMNS FROM {};'.format(table)
    cursor.execute(q)
    results = cursor.fetchall()
    return results
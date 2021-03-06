import mysql.connector
from getpass import getpass
from mysql.connector import connect
from helpers import Data, Scraping
import pandas as pd


def clear(tables):
    connection = connect(host='us-cdbr-east-04.cleardb.com', 
    user='b7a35a7346aea6', 
    password='a2aa8c36', 
    database='heroku_38066fac900fae9')
    cursor = connection.cursor()
    for table in tables:
        cursor.execute('''DELETE FROM {};'''.format(table))
        connection.commit()

def insert(quiet=True):
    connection = connect(host='us-cdbr-east-04.cleardb.com', 
    user='b7a35a7346aea6', 
    password='a2aa8c36', 
    database='heroku_38066fac900fae9')
    cursor = connection.cursor()
    Data().leadsOnTwitter()
    print('done')
    if quiet == False:
        print(pd.read_sql('''SELECT * FROM social;''', connection))
    Data().globalRank()
    print('done')
    if quiet == False:
        print(pd.read_sql('''SELECT * FROM fullcontact;''', connection))
    Data().fillLanding()
    print('done')
    if quiet == False:
        print(pd.read_sql('''SELECT * FROM landingpage;''', connection))

def writeLeads():
    connection = connect(host='us-cdbr-east-04.cleardb.com', 
    user='b7a35a7346aea6', 
    password='a2aa8c36', 
    database='heroku_38066fac900fae9')
    cursor = connection.cursor()
    q = '''SELECT name FROM survey;'''
    cursor.execute(q)
    leads = cursor.fetchall()
    f = open(r"C:\Users\aacjp\Sales-Scientist\leads.txt","w")
    for lead in leads:
        f.write("https://www.similarweb.com/website/{}/,".format(lead[0]))
    f.close()

def run(quiet=True):
    tables = ['social', 'fullcontact', 'landingpage', 'similarweb']
    clear(tables)
    insert(quiet=quiet)
    writeLeads()

run()
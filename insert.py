import mysql.connector
from getpass import getpass
from mysql.connector import connect
from helpers import Data, Scraping
import pandas as pd

def insert(quiet=True):
    connection = connect(host='localhost', user='root', password='Raptor//Kona9', database='leads')
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
    connection = connect(host='localhost', user='root', password='Raptor//Kona9', database='leads')
    cursor = connection.cursor()
    q = '''SELECT name FROM survey;'''
    cursor.execute(q)
    leads = cursor.fetchall()
    f = open(r"C:\Users\aacjp\Sales-Scientist\leads.txt","w")
    for lead in leads:
        f.write("https://www.similarweb.com/website/{}/,".format(lead[0]))
    f.close()

def run(quiet=True):
    #insert(quiet=quiet)
    writeLeads()

run()
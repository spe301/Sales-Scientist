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
        print(pd.read_sql('''SELECT * FROM test;''', connection))
    Data().fillLanding()
    print('done')
    if quiet == False:
        print(pd.read_sql('''SELECT * FROM landingpage;''', connection))

insert()
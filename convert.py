import mysql.connector
from getpass import getpass
from mysql.connector import connect
import pandas as pd

class Features:
    def __init__(self, df):
        self.df = df
        
    def pp(self):
        ps = self.df['percentSocial']
        pd = self.df['percentDisplay']
        psp = self.df['percentSearchPaid']
        n = len(ps)
        percent = []
        for i in range(n):
            paid = (ps[i]+pd[i]+psp[i])/100
            percent.append(paid)
        return percent

    def sales(self, crt=0.0001):
        c = []
        for i in range(len(self.df)):
            row = self.df.iloc[i]
            disp = row['percentDisplay']/100
            sm = (row['percentSocial'] * row['percentSearchPaid'])/100
            inv = 1 - (row['bounceRate']/100)
            ads = (disp+sm) * inv
            organic = (1 - (disp+sm))*crt
            customers = ads + organic
            ncustomers = int(customers * row['visits'])
            c.append(ncustomers)
        return c
    
    def adRevenue(self):
        adRevenue = []
        for i in range(len(self.df)):
            row = self.df.iloc[i]
            disp = row['percentDisplay']/100
            sm = (row['percentSocial'] * row['percentSearchPaid'])/100
            inv = 1 - (row['bounceRate']/100)
            ads = (disp+sm) * inv
            organic = (1 - (disp+sm))/1000
            customers = ads + organic
            ar = (ads / customers) * row['revenue']
            adRevenue.append(ar)
        return adRevenue
    
    def cac(self):
        adspend = self.df['adspend']
        customers = self.df['sales']
        cac = []
        for i in range(len(adspend)):
            cac.append(adspend[i]/customers[i])
        return cac
    
    def roas(self):
        adspend = self.df['adspend']
        ar = self.df['adRevenue']
        roas = []
        for i in range(len(adspend)):
            roas.append(ar[i]/adspend[i])
        return roas
    
    def profit(self):
        return self.df['revenue'] - self.df['adspend'] - self.df['hardcosts']
    
    def lpc(self):
        return self.df['words'] * self.df['triggers'] * self.df['links']
    
    def aov(self):
        return self.df['revenue'] / self.df['sales']

class Wrappers:
    
    def db2df(self):
        connection = connect(host='localhost', user='root', password='Raptor//Kona9', database='leads')
        cursor = connection.cursor()
        survey = pd.read_sql('''SELECT * FROM survey;''', connection)
        social = pd.read_sql('''SELECT * FROM social;''', connection).drop(['name'], axis='columns')
        landing = pd.read_sql('''SELECT * FROM landingpage;''', connection).drop(['name', 'landingPage'], axis='columns')
        web = pd.read_sql('''SELECT * FROM similarweb;''', connection).drop(['id'], axis='columns')
        rank = pd.read_sql('''SELECT * FROM fullcontact;''', connection).drop(['id', 'name'], axis='columns')
        return pd.concat([survey, social, landing, web, rank], axis='columns')
    
    def addFeats(self, df):
        f = Features(df)
        df['percentPaid'] = f.pp()
        df['sales'] = f.sales()
        return df

    def aggregate(self, df):
        f = Features(df)
        df['adRevenue'] = f.adRevenue()
        df['cac'] = f.cac()
        df['roas'] = f.roas()
        df['profit'] = f.profit()
        df['profitMargin'] = df['profit']/df['revenue']
        df['lpc'] = f.lpc()
        df['averageOrderValue'] = f.aov()
        return df

    def db2csv(self, title, quiet=False, path=r'C:\Users\aacjp\Sales-Scientist\datasets'):
        df = Wrappers().db2df()
        df2 = Wrappers().addFeats(df)
        df3 = Wrappers().aggregate(df2)
        if quiet==False:
            print(df3.shape)
        df3.to_csv('{}\{}.csv'.format(path, title))
        pass

Wrappers().db2csv('check')
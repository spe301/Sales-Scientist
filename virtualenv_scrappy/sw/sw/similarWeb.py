import scrapy
import mysql.connector
from getpass import getpass
from mysql.connector import connect, Error

class Spider2Sql:
    
    def __init__(self):
        self.create_connection()
        
    def create_connection(self):
        self.conn = connect(host='us-cdbr-east-04.cleardb.com', 
    user='b7a35a7346aea6', 
    password='a2aa8c36', 
    database='heroku_38066fac900fae9')
        self.curr = self.conn.cursor()
        
    def process_item(self, item, Spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        visits = item['visits']
        deltaVisits = item['deltaVisits']
        bounceRate = item['bounceRate']
        percentSearch = item['percentSearch']
        percentSocial = item['percentSocial']
        percentDisplay = item['percentDisplay']
        percentSearchPaid = item['percentSearchPaid']
        topPlatform = item['topPlatform']
        try:
            q = '''INSERT INTO similarweb (percentSocial, percentDisplay, percentSearchPaid, percentSearch, 
            visits, monthlyVisitsChange, bounceRate, dominantPlatform) VALUES ({}, {}, {}, {}, 
            {}, {}, {}, '{}');'''.format(percentSocial, percentDisplay, percentSearchPaid, percentSearch, 
            visits, deltaVisits, bounceRate, topPlatform)
            self.curr.execute(q)
        except:
            q = '''INSERT INTO similarweb (visits) VALUES ({});'''.format(visits)
            self.curr.execute(q)
        self.conn.commit()
    
class PostsSpider(scrapy.Spider):
    name = 'posts'
    f = open(r'C:\Users\aacjp\Sales-Scientist\leads.txt').read()
    start_urls = f.split(',')[7:12] #-1
    
    '''def parse(self, response):
        return response.css('a.href').getall()'''
    
    def parse(self, response):
        overview = response.css('span.engagementInfo-valueNumber.js-countValue::text').getall()
        if len(overview):
            try:
                visits = float(overview[0].replace('K', ''))*1000
            except:
                try:
                    visits = (float(overview[0].replace('K', '').replace('<', ''))*1000)-1
                except:
                    visits = float(overview[0].replace('M', ''))*1000000
            trajectory = float(response.css('span.websitePage-relativeChangeNumber::text').get().replace('%', ''))/100
            deltaVisits = round(visits * trajectory)
            breakdown = response.css('div.trafficSourcesChart-value::text').getall()
            bounceRate = float(overview[-1].replace('%', ''))
            percentSearch = float(breakdown[2].replace('%', ''))
            percentSocial = float(breakdown[3].replace('%', ''))
            percentDisplay = float(breakdown[5].replace('%', ''))
            percentSearchPaid = float(response.css('span.searchPie-number::text').getall()[1].replace('%', ''))/100
            topPlatform = response.css('a.socialItem-title.name.link::text').get()
            #percentPaidTraffic = (percentSocial+percentDisplay) + (percentSearchPaid*percentSearch)
        else:
            visits = 9999
            deltaVisits = 0
            bounceRate = None
            percentSearch = None
            percentSocial = None
            percentDisplay = None
            percentSearchPaid = None
            topPlatform = 'Facebook'
        results = {'visits': visits, 'deltaVisits': deltaVisits, 'bounceRate': bounceRate, 
               'percentSearch': percentSearch, 'percentSocial': percentSocial, 'percentDisplay': percentDisplay, 
               'percentSearchPaid': percentSearchPaid, 'topPlatform': topPlatform}
        Spider2Sql().store_db(results)
        yield results
        

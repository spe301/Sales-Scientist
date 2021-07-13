import scrapy
import mysql.connector
from getpass import getpass
from mysql.connector import connect, Error

class Spider2Sql:
    def __init__(self, percentSocial, percentDisplay, percentSearchPaid, percentSearch, 
                 visits, deltaVisits, bounceRate, topPlatform):
        self.percentSocial = percentSocial
        self.percentDisplay = percentDisplay
        self.percentSearchPaid = percentSearchPaid
        self.percentSearch = percentSearch
        self.visits = visits
        self.deltaVisits = deltaVisits
        self.bounceRate = bounceRate
        self.topPlatform = topPlatform
        
    def writeValues(self):
        percentSocial = self.percentSocial
        percentDisplay = self.percentDisplay
        percentSearchPaid = self.percentSearchPaid
        percentSearch = self.percentSearch
        visits = self.visits
        deltaVisits = self.deltaVisits
        bounceRate = self.bounceRate
        topPlatform = self.topPlatform
        return "({}, {}, {}, {}, {}, {}, {}, '{}')".format(percentSocial, percentDisplay, percentSearchPaid, percentSearch, 
                                         visits, deltaVisits, bounceRate, topPlatform)
    
    @classmethod
    def insertionQuery(cls):
        values = cls.writeValues()
        query = '''insert into similarweb (percentSocial, percentDisplay, percentSearchPaid, percentSearch, 
                                         visits, deltaVisits, bounceRate, topPlatform) 
        values {}'''.format(values)
        return query
    
    @classmethod
    def insertValues(cls, password, host='localhost', user='root', database='sys'):
        connection = connect(host=host, user=user, password=password, database=database)
        cursor = connection.cursor()  
        q = cls.insertionQuery()
        cursor.execute(q)
        pass
    
    
class PostsSpider(scrapy.Spider):
    name = 'posts'
    f = open(r'C:\Users\aacjp\Spencer\similarWeb.txt').read()
    start_urls = f.split(' ')[:-1]
    
    '''def parse(self, response):
        page = response.url.split('/')[-1]
        filename = 'posts-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        return response.body'''
    
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
            topPlatform = None
        s2s = Spider2Sql(percentSocial, percentDisplay, percentSearchPaid, percentSearch, 
                         visits, deltaVisits, bounceRate, topPlatform)
        s2s.insertValues(input('Enter password:'))
        return None
        
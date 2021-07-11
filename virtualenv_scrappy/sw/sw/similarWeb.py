import scrapy


class PostsSpider(scrapy.Spider):
    name = 'posts'
    start_urls = ['https://www.similarweb.com/website/millionaire.it/']
    
    '''def parse(self, response):
        page = response.url.split('/')[-1]
        filename = 'posts-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        return response.body'''
    
    def parse(self, response):
        visits = float(response.css('span.engagementInfo-valueNumber.js-countValue::text').get().replace('K', ''))*1000
        trajectory = float(response.css('span.websitePage-relativeChangeNumber::text').get().replace('%', ''))/100
        deltaVisits = visits * trajectory
        breakdown = response.css('div.trafficSourcesChart-values::text').getall()
        #bounceRate = float(response.css('div.engagementInfo-line::text').get().replace('%', ''))
        percentSearch = float(breakdown[2].replace('%', ''))/100
        percentSocial = float(breakdown[3].replace('%', ''))/100
        percentDisplay = float(breakdown[5].replace('%', ''))/100
        percentSearchPaid = float(response.css('span.searchPie-number::text').getall()[1].replace('%', ''))/100
        topPlatform = response.css('a.socialItem-title.name.link::text').get()
        return visits, deltaVisits, percentSearch, percentSocial, percentDisplay, percentSearchPaid, topPlatform
    
    
        

import scrapy

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
            percentSearch = float(breakdown[2].replace('%', ''))/100
            percentSocial = float(breakdown[3].replace('%', ''))/100
            percentDisplay = float(breakdown[5].replace('%', ''))/100
            percentSearchPaid = float(response.css('span.searchPie-number::text').getall()[1].replace('%', ''))/100
            topPlatform = response.css('a.socialItem-title.name.link::text').get()
            percentPaidTraffic = (percentSocial+percentDisplay) + (percentSearchPaid*percentSearch)
        else:
            visits = 9999
            deltaVisits = 0
            bounceRate = None
            percentSearch = None
            percentSocial = None
            percentDisplay = None
            percentSearchPaid = None
            topPlatform = None
            percentPaidTraffic = None
        yield {'% paid traffic': percentPaidTraffic, 
               'visits': visits, 
               'monthly visits change': deltaVisits, 
               'bounce rate': bounceRate, 
               'dominant platform': topPlatform}
        
import pandas as pd
from fullcontact import FullContactClient
from imblearn.over_sampling import SMOTENC
from urllib.request import urlopen, Request

class individualFeatures:
    '''trigger words are words that are associated with a call to action. We are creating a list of them so that we can cout the number of trigger words a business has in their landing page. A lot of trigger words indicate multiple CTA's, this is a sign of spending too much on ads.'''
    
    def percentPaidSearch(self, percentSearch, percentPaid):
        return percentSearch * (percentPaid/100)
    
    def adSpend(self, visits, percentSocial, percentAds, percentPaidSearch):
        social = (visits * (percentSocial/100)) * 7
        display = (visits * (percentAds/100)) * 7
        paidSearch = (visits * (percentPaidSearch/100)) * 0.95
        return round(social + display + paidSearch)
    
    def percentAdTraffic(self, percentSocial, percentAds, percentPaidSearch):
        return round(percentSocial+percentAds+percentPaidSearch, 2)
    
    def nWords(self, landingPage):
        words = 0
        for lp in landingPage.split(' '):
            if lp.startswith('http') == False:
                words += 1
        return words
    
    def triggerWords(self, landingPage):
        triggerWords = ['book', 'call', 'today', 'get', 'my', 'free', 'copy', 'checklist', 
                'pdf', 'report', 'ebook', 'join', 'session', 'now', 'set', 'email',
                'free', 'list', 'attend', 'start', 'access', 'training', 'speak', 
                'expert', 'here']
        tw = 0
        for lp in landingPage.split(' '):
            if lp in triggerWords:
                tw += 1
        return tw
    
    def nLinks(self, landingPage):
        links = 0
        for lp in landingPage.split(' '):
            if lp.startswith('http') == True:
                links += 1
        return links
    
class aggregateFeatures:
    
    def estimateRevenue(self, df, key):
        fcc = FullContactClient(key)
        revenue = []
        for i in range(len(df)):
            row = df.iloc[i]
            lead = fcc.company.enrich(domain=row['lead']).json()
            try:
                if row['business model'] == 'consulting':
                    revenue.append(lead['employees'] * 15873)
                if row['business model'] == 'ecommerce':
                    revenue.append(lead['employees'] * 66666)
                if row['business model'] == 'info':
                    revenue.append(lead['employees'] * 16666)
                if row['business model'] == 'media':
                    revenue.append(lead['employees'] * 50000)
                if row['business model'] == 'restaurant':
                    revenue.append(lead['employees'] * 35714)
                if row['business model'] == 'software':
                    revenue.append(lead['employees'] * 379722)
            except:
                revenue.append(False)
        return revenue
    
    def adRevenue(self, revenue, percentAdTraffic):
        return revenue * (percentAdTraffic/100)
    
    def roas(self, adRevenue, adSpend):
        return adRevenue / adSpend
    
    def cac(self, newCustomers, adSpend):
        return adSpend / newCustomers
    
    def profit(self, revenue, adSpend, hardcosts):
        return revenue - adSpend - hardcosts
    
    def landingPageComplexity(self, links, words, triggerWords):
        return links+1 * words+1 * triggerWords+1
    
    def profitMargin(self, revenue, adSpend, hardcosts):
        af = aggregateFeatures()
        return af.profit(revenue, adSpend, hardcosts) / revenue

class Data:
    
    def doubleUp(self, df, class_size, target_col, sm):
        yes = df.loc[df[target_col] == 1]
        no = df.loc[df[target_col] == 0]
        df = pd.concat([yes, no])
        inv = len(df) - class_size - 6
        positives = df.iloc[:class_size+6]
        negatives = df.iloc[inv:]
        posX = positives.drop([target_col], axis='columns')
        posY = positives[target_col]
        posX2, posY2 = sm.fit_resample(posX, posY)
        pos2 = posX2
        pos2[target_col] = posY2
        negX = negatives.drop([target_col], axis='columns')
        negY = negatives[target_col]
        negX2, negY2 = sm.fit_resample(negX, negY)
        neg2 = negX2
        neg2[target_col] = negY2
        return pd.concat([pos2, neg2])
    
    def lpCopy(self, url, headers):
        req = Request(url=url, headers=headers) 
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'lxml')
        div = soup.findAll('div')
        p = soup.findAll('p')
        try:
            text = div[0].text + p[0].text
        except: 
            text = div[0].text
        text2 = text.replace('\n', '').replace('\'', '').replace(')', '').replace('(', '').lower()
        text3 = re.sub("([\(\[]).*?([\)\]])", '', text2)
        text4 = re.sub(r'\[(^)*\]', '', text3)
        text5 = text4.replace('-', '').replace('"', '').replace('!', ' ').replace('*', '').replace(':', ' ').replace('.', ' ')
        text6 = text5.replace('?', ' ')
        return text6
    
class Math:
    
    def cubicRoot(self, x):
        return x ** (1. / 3)

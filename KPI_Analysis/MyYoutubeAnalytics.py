import pandas as pd
from textblob import TextBlob
import numpy as np

df1 = pd.read_csv(r'C:\Users\aacjp\OneDrive\Desktop\Table0.csv')
df2 = pd.read_csv(r'C:\Users\aacjp\OneDrive\Desktop\Table data.csv')
df3 = pd.read_csv(r'C:\Users\aacjp\OneDrive\Desktop\internal_all.csv')

class myStats():
    
    def getPercentile(self, n, sample):
        sample = sorted(list(sample))
        n_lesser = 0
        n_greater = 0
        for s in sample:
            if s > n:
                n_greater += 1
            else:
                n_lesser += 1
        return (n_lesser / (n_lesser+n_greater))*100

    def getQuartile(self, percentile):
        return int(percentile/25)
    
    
class Youtube():
    
    def youtubeLingo(self, title):
        '''converts youtube titles for nlp'''
        return title.lower().replace('***', 'uck').replace('prod.', 'produced by').replace('ep.', 'episode ').replace('|', 'and').replace('@', 'at ').replace('=', 'equals')
    
    def getVideoLength(self, avd, apv):
        vd = []
        for i in range(1, len(avd)+1):
            vd.append(int((avd[i]/apv[i])*100))
        return vd

    
class myUtils():
    
    def countLinks(self, description):
        '''counts how many links are in a body of text'''
        try:
            wrds = description.replace('...', ' ').split(' ')
            links = 0
            for w in wrds:
                if w.startswith('http'):
                    links += 1
        except: 
            links = 0
        return links
    
    def stripPunct(self, string):
        '''removes punctuation from text'''
        return string.replace('(', '').replace(')', '').replace(':', '').replace('!', '').replace('?', '')
    
    def toSeconds(self, duration):
        '''converts hh:mm:ss durations to the number od seconds'''
        timesplits = duration.split(':')
        return int(timesplits[0])*3600 + int(timesplits[1])*60 + int(timesplits[2])
    
class processYoutubeReports():
    
    def convert(self, df1, df2, df3):
        df1 = df1.iloc[1:].set_index('Video')
        df2 = df2.iloc[1:]
        df3 = df3[['Address', 'Meta Description 1']]
        df3['Address'] = df3['Address'].apply(lambda x: x.split('=')[1])
        return df1, df2, df3
    
    def unite(self, df1, df2, df3):
        imp = []
        imp_crt = []
        desc = []
        for i in range(1, len(df2['Video'])+1): #adding impressions and impression click through for each video
            imp.append(df1.loc[df2['Video'][i]]['Impressions'])
            imp_crt.append(df1.loc[df2['Video'][i]]['Impressions click-through rate (%)'])
            desc.append(df3.loc[df3['Address'] == df2['Video'][i]]['Meta Description 1'])
        df2['Impressions'] = imp
        df2['Impressions click-through rate (%)'] = imp_crt
        df2['description'] = desc
        return df2
    
    def countRefrences(self, df):
        '''count the number of links refrenced for each youtube video description'''
        mu = myUtils()
        df['nlinks'] = df['description'].apply(lambda x: mu.countLinks(x.iloc[0]))
        return df
    
    def cleanTitles(self, df):
        '''gets video titles ready for tokenization'''
        y = Youtube()
        mu = myUtils()
        df['Video title'] = df['Video title'].apply(lambda x: mu.stripPunct(y.youtubeLingo(x)))
        return df
    
    def addTitleMeta(self, df):
        '''calculates the length and sentiment score of a youtube video title'''
        pyr = processYoutubeReports()
        df = pyr.cleanTitles(df)
        tl = []
        tp = []
        for title in df['Video title']:
            tl.append(len(title))
            tp.append(TextBlob(title).sentiment.polarity)
        df['title length'] = tl
        df['title polarity'] = tp
        return df
    
    def cleanDurations(self, df):
        '''returns the number of seconds a given video is'''
        mu = myUtils()
        y = Youtube()
        df['Average view duration'] = df['Average view duration'].apply(lambda x: mu.toSeconds(x)) 
        df['Video duration'] = y.getVideoLength(df['Average view duration'], df['Average percentage viewed (%)'])
        return df
    
    def bucketDurations(self, df):
        ms = myStats()
        df['duration bucket']= df['Video duration'].apply(lambda x: ms.getQuartile(ms.getPercentile(x, list(df['Video duration']))))
        return df
    
    def Wrap(self, df1, df2, df3):
        pyr = processYoutubeReports()
        a, b, c = pyr.convert(df1, df2, df3)
        df = pyr.unite(a, b, c)
        df = pyr.countRefrences(df)
        df = pyr.addTitleMeta(df)
        df = pyr.cleanDurations(df)
        df = pyr.bucketDurations(df)
        return df
    
processYoutubeReports().Wrap(df1, df2, df3).to_csv(r'C:\Users\aacjp\Spencer\KPI_Analysis\Youtube.csv')
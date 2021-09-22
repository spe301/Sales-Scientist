#from sklearn.externals import joblib
import joblib
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier

class Prediction:
	
	def test(self, X):
		path = r'C:\Users\aacjp\Sales-Scientist\clf.pkl'
		model = joblib.load(path)
		return model.predict(X)

	def Probability(self, X):
		path = r'C:\Users\aacjp\Sales-Scientist\clf.pkl'
		try:
			model = joblib.load(path)
		except:
			path = r'C:\Users\aacjp\Sales-Scientist\datasets\check6.csv'
			x = Data().Preprocess(pd.read_csv(path).drop(['customer'], axis='columns'))
			Y = pd.read_csv(path)['customer']
			model = DecisionTreeClassifier().fit(x, Y)
		print(x.columns, X.columns)
		predictions = model.predict_proba(X)[:, 1]
		temp = pd.DataFrame(predictions)
		temp.columns = ['probabilities']
		temp['probabilities'] = temp['probabilities'].apply(lambda x: round(x*5, 1))
		return temp

	def Opportunity(self, X):
		training_data = pd.read_csv(r'C:\Users\aacjp\Sales-Scientist\datasets\leadsML.csv').drop(['Unnamed: 0'], axis='columns')
		mu_cac = np.mean(training_data['cac'])
		sigma_cac = np.std(training_data['cac'])
		mu_adspend = np.mean(training_data['adspend'])
		sigma_adspend = np.std(training_data['adspend'])
		scores = []
		for i in range(len(X)):
			cacZ = (X['cac'][i]-mu_cac)/sigma_cac
			adspendZ = (X['adspend'][i]-mu_adspend)/sigma_adspend
			net = (cacZ+3) + (adspendZ+3) + (X['avg_polarity'][i]+1)
			opportunity = round((net/14)*5, 1)
			scores.append(opportunity)
		temp = pd.DataFrame(scores)
		return temp

	def ScoreLeads(self, X):
		n = len(X)
		pr = Prediction()
		try:
			X = Data().Preprocess(X)
		except:
			pass
		update = X
		probs = np.array(pr.Probability(X))
		opps = np.array(pr.Opportunity(X))
		X['score'] = probs+opps
		action = []
		priority = []
		for i in range(len(X)):
			if probs[i] <= 2.5:
				action.append('nurture')
				if opps[i] <= 2.5:
					priority.append('low')
				else:
					priority.append('high')
			if probs[i]>2.5:
				action.append('advance')
				if opps[i] > 2.5:
					priority.append('high')
				else:
					priority.append('low')
		X['action'] = action
		X['priority'] = priority
		update['customer'] = X['score'].apply(lambda x: int(round(x/10)))
		update = update.drop(['score', 'action', 'priority'], axis='columns')
		original = X.drop(['score', 'action', 'priority'], axis='columns').iloc[:n]
		X2 = pd.concat([original, update])
		return X, X2

class Data:

	def Preprocess(self, X):
		X2 = X.drop(['name', 'landingPage', 'source'], axis='columns')
		domains = pd.get_dummies(X['domain'])
		models = pd.get_dummies(X['model'])
		dominantPlatforms = pd.get_dummies(X['dominantPlatform'])
		X3 = X2.drop(['domain', 'model', 'dominantPlatform'], axis='columns')
		X4 = pd.concat([X3, domains, models, dominantPlatforms], axis='columns')
		return X4

def WrapScoring(X, data_path, leads_path):
	names = X['name']
	X = X.drop(['name'], axis='columns')
	original_path = r'C:\Users\aacjp\Sales-Scientist\datasets\check6.csv'
	leads, _ = Prediction().ScoreLeads(X)
	data = leads.drop(['score', 'action', 'priority'], axis='columns')
	df = Data().Preprocess(pd.read_csv(original_path))
	data.columns = list(df.columns)
	df2 = df.append(data)
	leads['name'] = names
	#df2.to_csv(data_path)
	#leads.to_csv(leads_path)
	return leads[['name', 'score', 'action', 'priority']]


#dp = r'C:\Users\aacjp\Sales-Scientist\datasets\check6.csv'
#lp = r'C:\Users\aacjp\Sales-Scientist\datasets\prospects.csv'
#print(WrapScoring(X, dp, lp))
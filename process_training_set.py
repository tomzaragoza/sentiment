from pymongo import MongoClient
import csv

mongo = MongoClient()
db = mongo['sentiment-analysis']
collection = db['training-set']

if True:
	with open('Sentiment_Analysis_Dataset.csv', 'rb') as csvfile:
		r = csv.reader(csvfile, delimiter=',')
		next(r, None)
		for row in r:
			print row
			doc = {
					'tweet': row[3],
					'sentiment': int(row[1])
					}
			collection.insert(doc)

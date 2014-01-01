from pymongo import MongoClient
import csv

mongo = MongoClient()
db = mongo['sentiment-analysis']
collection = db['tweets']


def process_csv(filename):
	with open(filename, 'rb') as csvfile:
		r = csv.reader(csvfile, delimiter=',')
		next(r, None)
		for row in r:
			print row
			doc = {
					'tweet': row[3],
					'sentiment': int(row[1])
					}
			collection.insert(doc)

if __name__ == "__main__":
	process_csv('Sentiment_Analysis_Dataset.csv')
''' Using Character Gram tweets to train the classifier.

	http://www.academia.edu/2306608/R_U_-_or_-_Character-_vs._Word-Gram_Feature_Selection_for_Sentiment_Classification_of_OSN_Corpora 
'''
from TwitterAPI import TwitterAPI
from pprint import pprint as pretty
from pymongo import MongoClient
from datetime import datetime
import authenticate
import json

CONSUMER_KEY = ''
CONSUMER_SECRET = ''

def positive_char_gram_tweets(api, max_tweets):
	""" Writes negative tweet to a text file while streaming. """
	print "{0}: Retrieving positive character gram tweets...".format(datetime.now())

	r = api.request('statuses/filter', {'track': ":),:-),:D,:],:')", 'language':'en'})
	f = open('positive-tweets.txt', 'w')

	max_tweets = max_tweets
	c = 0
	for item in r.get_iterator():
		
		if 'text' in item:
			print c
			f.write(item['text'].encode('utf-8') + '\n')
			if c <= max_tweets:
				c += 1
			else:
				break
	f.close()

def negative_char_gram_tweets(api, max_tweets):
	""" Writes negative tweet to a text file while streaming. """
	print "{0}: Retrieving negative character gram tweets...".format(datetime.now())

	r = api.request('statuses/filter', {'track': ":(,:-(,D:,:'(", 'language':'en'})
	f = open('negative-tweets.txt', 'w')

	max_tweets = max_tweets
	c = 0
	for item in r.get_iterator():
		
		if 'text' in item:
			print c
			f.write(item['text'].encode('utf-8') + '\n')
			if c <= max_tweets:
				c += 1
			else:
				break
	f.close()

def process_tweets(collection):
	""" Insert all positive and negative tweets into the collection """

	with open('positive-tweets.txt') as p:
		print "{0}: Inserting positive tweets into mongo...".format(datetime.now())
		for tweet in p.readlines():
			collection.insert({'tweet': tweet, 'sentiment': 1})
	p.close()

	with open('negative-tweets.txt') as n:
		print "{0}: Inserting negative tweets into mongo...".format(datetime.now())
		for tweet in n.readlines():
			collection.insert({'tweet': tweet, 'sentiment': 0})
	n.close()



if __name__ == "__main__":

	RETRIEVE_NEW_TWEETS = False
	PROCESS_TWEETS = True

	if RETRIEVE_NEW_TWEETS:
		access_tokens = authenticate.get_tokens(CONSUMER_KEY, CONSUMER_SECRET)
		api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, access_tokens['oauth_token'], access_tokens['oauth_token_secret'])

		positive_char_gram_tweets(api, 100000)
		negative_char_gram_tweets(api, 100000)

	if PROCESS_TWEETS:
		mongo = MongoClient()
		db = mongo['sentiment-analysis']
		collection = db['tweets']

		process_tweets(collection)

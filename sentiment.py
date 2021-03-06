import nltk
import pickle
import pickling as p
from pymongo import MongoClient
from pprint import pprint as pretty
from classifier import Classifier
from datetime import datetime

mongo = MongoClient()
db = mongo['sentiment-analysis']
collection = db['tweets']

# implementation
def get_positive_tweets():
	print "Retrieving positive tweets..."
	pos_tweets = []
	tweets = collection.find({'sentiment': 1})
	count = 0
	for tweet in tweets:
		if count != 30000:
			pos_tweets.append((tweet['tweet'], 'positive'))
			count += 1
		else:
			break
	return pos_tweets


def get_negative_tweets():
	print "Retrieving negative tweets..."
	neg_tweets = []
	tweets = collection.find({'sentiment': 0})
	count = 0
	for tweet in tweets:
		if count != 30000:
			neg_tweets.append((tweet['tweet'], 'negative'))
			count += 1
		else:
			break
	return neg_tweets

def contains(e):
	for chars in ['@', 'http:', 'https:']:
		if chars in e:
			return True
	return False

def process_token(e):
	token = e
	for c in ['!', '#', '.', ';', ':']:
		if c in e:
			token = e.replace(c, '')
	return token

def is_emoticon(e):
	if e in [":-(", ":'(", ":-)", ":')"]:
		return True
	return False

def process_tweets(pos_tweets, neg_tweets):
	tweets = []
	for (words, sentiment) in pos_tweets + neg_tweets:
		words_filtered = [process_token(e.lower()) for e in words.split() if len(e) >= 3 and not contains(e) and not is_emoticon(e)]
		print words_filtered
		tweets.append((words_filtered, sentiment))
	return tweets


test_tweets = [
	(['feel', 'happy', 'this', 'morning'], 'positive'),
	(['larry', 'friend'], 'positive'),
	(['not', 'like', 'that', 'man'], 'negative'),
	(['house', 'not', 'great'], 'negative'),
	(['your', 'song', 'annoying'], 'negative')]

# classifier
def get_words_in_tweets(tweets):
	all_words = []
	for(words, sentiment) in tweets:
		all_words.extend(words)
	return all_words

def get_word_features(wordlist):
	wordlist = nltk.FreqDist(wordlist)
	word_features = wordlist.keys()
	return word_features


if __name__ == "__main__":

	print "START: {0}".format(datetime.now())
	# set this to False if:
	# 	Need to create Classifier
	#	Need to update classifier with new tweets that are brought in
	#	Need to update training set (this follows after point 2)
	CLASSIFIER_MADE = False
	
	if not CLASSIFIER_MADE:
		positive_tweets = get_positive_tweets()
		negative_tweets = get_negative_tweets()

		print "Processing all retrieved tweets..."
		tweets = process_tweets(positive_tweets, negative_tweets)
		words_in_tweets = get_words_in_tweets(tweets)
		p.save(tweets, 'tweets')

		print "Retrieving word features..."
		word_features = get_word_features(words_in_tweets)
		p.save(word_features, 'word_features')

		print "Extracting features and classifiying using Naive Bayes..."
		# save the training set and the classifier

		c = Classifier(word_features, tweets)

	elif CLASSIFIER_MADE:
		print "Reloading previously created classifier..."

		c = Classifier(	word_features=p.load('word_features'),
						tweets=p.load('tweets'),
						classifier=p.load('my_classifier'),
						show_count=False
						)

	print c.classifier.show_most_informative_features(32)

	# testing it out
	print "\ntesting out the classifier"
	ts = [
			"wonderful, everything is going wrong right now",
			"The movie wasn't that bad",
			"this is a very thought provoking book",
			"my new computer was expensive, but I'm much more productive now",
			"people like john are hard to deal with",
			"I'm not happy"
			]
	for tweet in ts:
		print c.classifier.classify(c.extract_features(tweet.split())), '------>', tweet

	print "END {0}".format(datetime.now())

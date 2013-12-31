import nltk
import pickle
import pickling as p
from pymongo import MongoClient
from pprint import pprint as pretty
from classifier import Classifier


TRAIN_CLASSIFIER = True

mongo = MongoClient()
db = mongo['sentiment-analysis']
collection = db['training-set']

# implementation

def get_positive_tweets():
	pos_tweets = []
	tweets = collection.find({'sentiment': 1})
	count = 0
	for tweet in tweets:
		# pretty(tweet)
		if count != 5000:
			pos_tweets.append((tweet['tweet'], 'positive'))
			count += 1
		else:
			break
	return pos_tweets


def get_negative_tweets():
	neg_tweets = []
	tweets = collection.find({'sentiment': 0})
	count = 0
	for tweet in tweets:
		# print tweet
		if count != 5000:
			neg_tweets.append((tweet['tweet'], 'negative'))
			count +=1
		else:
			break
	return neg_tweets


def process_tweets(pos_tweets, neg_tweets):
	tweets = []
	for (words, sentiment) in pos_tweets + neg_tweets:
		words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
		tweets.append((words_filtered, sentiment))
	return tweets

# pretty(tweets)

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

	# set this to False if:
	# 	Need to create Classifier
	#	Need to update classifier with new tweets that are brought in
	#	Need to update training set (this follows after point 2)
	CLASSIFIER_MADE = False
	
	if not CLASSIFIER_MADE:
		print "Retrieving positive and negative tweets..."
		positive_tweets = get_positive_tweets()
		negative_tweets = get_negative_tweets()

		print "Processing all retrieved tweets..."
		tweets = process_tweets(positive_tweets, negative_tweets)
		words_in_tweets = get_words_in_tweets(tweets)
		p.save_tweets(tweets)

		print "Retrieving word features..."
		word_features = get_word_features(words_in_tweets)
		p.save_word_features(word_features)

		print "Extracting features and classifiying using Naive Bayes..."
		# save the training set and the classifier

		c = Classifier(word_features, tweets)

	elif CLASSIFIER_MADE:
		print "Reloading previously created classifier..."

		c = Classifier(	word_features=p.load_word_features(),
						tweets=p.load_tweets(),
						classifier=p.load_classifier()
						)

	print c.classifier.show_most_informative_features(32)

	# testing it out
	print "\ntesting out the classifier"
	ts = [
			"wonderful, everything is going wrong right now",
			"The movie wasn't that bad",
			"this is a very thought provoking book",
			"my new computer was expensive, but I'm much more productive now",
			"people like john are hard to deal with"
			]
	for tweet in ts:
		print c.classifier.classify(c.extract_features(tweet.split())), '------>', tweet

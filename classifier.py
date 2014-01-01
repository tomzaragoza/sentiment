import nltk
import pickling as p
from pprint import pprint as pretty
from datetime import datetime
import gevent
from gevent import monkey; monkey.patch_socket()
from gevent.pool import Pool


class Classifier():
	def __init__(self, word_features=None, tweets=None, training_set=None, classifier=None, show_count=True):
		self.word_features = word_features
		self.tweets = tweets
		self.overall_count = 0
		self.show_count = show_count

		if training_set:
			self.training_set = training_set
		else:
			self.training_set = []

			first_checkpoint = len(self.tweets) / 3
			second_checkpoint = first_checkpoint * 2

			first_batch = self.tweets[:first_checkpoint]
			second_batch = self.tweets[first_checkpoint:second_checkpoint]
			third_batch = self.tweets[second_checkpoint:]

			tweet_batches = [first_batch, second_batch, third_batch]

			print "{0} : Running the Map function for the features".format(datetime.now())
			pool = Pool(3)
			returned_from_pool = pool.map(self.apply_features, tweet_batches)
			# self.training_set += pool.map(self.apply_features, tweet_batches)
			self.training_set = [feature for feature_list in returned_from_pool for feature in feature_list]
			# print len(self.training_set)
			# print type(self.training_set)

			# # self.training_set = nltk.classify.apply_features(self.extract_features, self.tweets)
			

			# print
			# print
			# for i in self.training_set:
			# 	print
			# 	pretty(i)
			# 	print len(i)
			# 	print type(i)
			# print self.training_set
			print "length of training set is ", len(self.training_set)

		if classifier:
			self.classifier = classifier
		else:
			# only save classifier / pickle if no errors occur
			try:
				self.classifier = nltk.NaiveBayesClassifier.train(self.training_set)
			except:
				raise Exception()
			p.save_classifier(self.classifier)
	
	def apply_features(self, tweets):
		return nltk.classify.apply_features(self.extract_features, tweets)

	def extract_features(self, document):
		document_words = set(document)
		features = {}

		if self.show_count:
			print "{0} : {1} of out {2}".format(datetime.now(), self.overall_count, len(self.tweets))

		for word in self.word_features:
			features['contains({0})'.format(word.encode('utf-8'))] = word in document_words
		self.overall_count += 1
		return features

	def retrieve_classifier(self):
		return self.classifier

	def retrieve_training_set(self):
		return self.training_set

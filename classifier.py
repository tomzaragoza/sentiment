import nltk
import pickling as p
from pprint import pprint as pretty
from datetime import datetime

class Classifier():
	def __init__(self, word_features=None, tweets=None, training_set=None, classifier=None, show_count=True):
		self.word_features = word_features
		self.tweets = tweets
		self.overall_count = 0
		self.show_count = show_count

		if training_set:
			self.training_set = training_set
		else:
			self.training_set = nltk.classify.apply_features(self.extract_features, self.tweets)

		if classifier:
			self.classifier = classifier
		else:
			self.classifier = nltk.NaiveBayesClassifier.train(self.training_set)
			p.save_classifier(self.classifier)

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

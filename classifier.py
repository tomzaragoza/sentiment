import nltk

class Classifier():
	def __init__(self, word_features, tweets):
		self.word_features = word_features
		self.tweets = tweets

		self.training_set = nltk.classify.apply_features(self.extract_features, self.tweets)
		self.classifier = nltk.NaiveBayesClassifier.train(self.training_set)		

	def extract_features(self, document):
		document_words = set(document)
		features = {}
		for word in self.word_features:
			features['contains({0})'.format(word.encode('utf-8'))] = word in document_words
		return features

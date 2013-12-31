import pickle

# For saving the classifier
def save_classifier(classifier):
	f = open('my_classifier.pickle', 'wb')
	pickle.dump(classifier, f)
	f.close()

def load_classifier():
	f = open('my_classifier.pickle', 'rb')
	classifier = pickle.load(f)
	f.close()
	return classifier

# For saving training set
def save_training_set(training_set):
	f = open('training_set.pickle', 'wb')
	pickle.dump(training_set, f)
	f.close()

def load_training_set():
	f = open('training_set.pickle', 'rb')
	training_set = pickle.load(f)
	f.close()
	return training_set

# for saving word features
def save_word_features(classifier):
	f = open('word_features.pickle', 'wb')
	pickle.dump(classifier, f)
	f.close()

def load_word_features():
	f = open('word_features.pickle', 'rb')
	word_features = pickle.load(f)
	f.close()
	return word_features

# for saving tweets
def save_tweets(tweets):
	f = open('tweets.pickle', 'wb')
	pickle.dump(tweets, f)
	f.close()

def load_tweets():
	f = open('tweets.pickle', 'rb')
	tweets = pickle.load(f)
	f.close()
	return tweets

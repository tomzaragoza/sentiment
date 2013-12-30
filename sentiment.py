import nltk
from pprint import pprint as pretty

# implementation
pos_tweets = [('I love this car', 'positive'),
              ('This view is amazing', 'positive'),
              ('I feel great this morning', 'positive'),
              ('I am so excited about the concert', 'positive'),
              ('He is my best friend', 'positive')]


neg_tweets = [('I do not like this car', 'negative'),
              ('This view is horrible', 'negative'),
              ('I feel tired this morning', 'negative'),
              ('I am not looking forward to the concert', 'negative'),
              ('He is my enemy', 'negative')]

tweets = []
for (words, sentiment) in pos_tweets + neg_tweets:
	words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
	tweets.append((words_filtered, sentiment))

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
    # print wordlist
    word_features = wordlist.keys()
    return word_features

words_in_tweets = get_words_in_tweets(tweets)
word_features = get_word_features(words_in_tweets)
# print word_features


def extract_features(document): # document is really a list of words
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains({0})'.format(word)] = word in document_words
	return features

# pretty(extract_features(['love', 'this', 'car'], word_features))
# pretty(tweets)
training_set = nltk.classify.apply_features(extract_features, tweets)
# pretty(training_set)
# print training_set

classifier = nltk.NaiveBayesClassifier.train(training_set)

# print classifier.show_most_informative_features(32)

tweet = "Larry is my friend"
pretty(extract_features(tweet.split()))
print classifier.classify(extract_features(tweet.split()))

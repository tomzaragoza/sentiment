sentiment
=========

Building a Twitter sentiment analyzer.


Update: 01/01/2014

It seems like switching to the character n-gram tweets improved the classifier a bit. I used a smaller training set of positive and negative tweets, so now trying it on a larger training set. These New Years tweets should be good!

To do
* Speed up training somehow. It seems like the extract feature function in Classifier() is pretty slow. Must investigate further
* Better tweet text cleaning. So, possible remove punctuations, or whatever needs to be done to have cleaner data. Read up on this, son.

Update 2: 01/01/2014

Managed to use gevent for speeding up the creation of the training set. Must look further into this to see if it is the right solution. Also managed to clean up the tweets that are coming in.

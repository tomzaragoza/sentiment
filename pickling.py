import pickle

def save(obj, name):
	f = open(name + '.pickle', 'wb')
	pickle.dump(obj, f)
	f.close()

def load(name):
	f = open(name + '.pickle', 'wb')
	unpickled_obj = pickle.load(f)
	f.close()
	return unpickled_obj

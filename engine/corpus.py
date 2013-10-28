import nltk, os
from nltk.corpus import movie_reviews
from random import randrange, sample

class Corpus:

	def __init__(self):
		path_to_nltk_data = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'nltk_data'
		)
		nltk.data.path.append(path_to_nltk_data)

		return

	"""
	category is 'positive' or 'negative'
	"""
	def getRandomMovieReview(self, category):
		ret = ''
		if category != 'positive' and category != 'negative':
			return ret
		return self.movieReviews(category, 1)[0]

	def wordDictHelper(self, path):
		ret = {}
		with open(path, 'r') as f:
			for line in f:
				word = line.rstrip()
				if word not in ret:
					ret[word] = True
		return ret

	def positiveWordDict(self):
		path = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'lib',
			'positive-words.txt'
		)
		return self.wordDictHelper(path)

	def negativeWordDict(self):
		path = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'lib',
			'negative-words.txt'
		)
		return self.wordDictHelper(path)

	def stopWordDict(self):
		path = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'lib',
			'stop-words-small.txt'
		)
		return self.wordDictHelper(path)

	"""
	category is 'positive' or 'negative'
	Returns a list of strings
	"""
	def movieReviews(self, category, count):
		ret = []
		if category != 'positive' and category != 'negative':
			return ret
		fileids = []
		if category == 'positive':
			fileids = movie_reviews.fileids('pos')
		elif category == 'negative':
			fileids = movie_reviews.fileids('neg')
		sampleFileIds = sample(fileids, count)
		for sampleFileId in sampleFileIds:
			ret.append(movie_reviews.raw(sampleFileId))
		return ret
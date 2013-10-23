from nltk.corpus import movie_reviews
from random import randrange

class Corpus:

	def __init__(self):
		return

	"""
	category is 'positive' or 'negative'
	"""
	@staticmethod
	def getRandomMovieReview(category):
		ret = ''
		if category != 'positive' and category != 'negative':
			return ret
		fileids = []
		if category == 'positive':
			fileids = movie_reviews.fileids('pos')
		elif category == 'negative':
			fileids = movie_reviews.fileids('neg')
		index = randrange(len(fileids))
		fileid = fileids[index]
		ret = movie_reviews.raw(fileid)
		print(ret)
		return ret
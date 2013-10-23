import nltk, os
from nltk.corpus import movie_reviews
from random import randrange

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
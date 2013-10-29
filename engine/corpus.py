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

	####################
	# Word Dict
	####################
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

	####################
	# Movie Reviews
	####################		

	"""
	category is 'positive' or 'negative'
	"""
	def getRandomMovieReview(self, category):
		ret = ''
		if category != 'positive' and category != 'negative':
			return ret
		return self.movieReviews(category, 1)[0]

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

	####################
	# James Data
	###################
	"""
	category is 'positive' or 'negative'
	"""
	def getArticleHelper(self, category, topic):
		articles = self.getArticlesHelper(category, topic)
		l = len(articles)
		index = randrange(l)
		return articles[index]

	"""
	category is 'positive' or 'negative'
	"""
	def getArticlesHelper(self, category, topic):
		ret = []
		dirPath = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'james_data',
			topic
		)
		if category == 'positive':
			dirPath = os.path.join(dirPath, 'pos')
		elif category == 'negative':
			dirPath = os.path.join(dirPath, 'neg')
		filenames = os.listdir(dirPath)
		for filename in filenames:
			path = os.path.join(dirPath, filename)
			with open(path, 'r') as f:
				fileString = f.read()
				ret.append(fileString)
		return ret

	def celebrityArticle(self, category):
		return self.getArticleHelper(category, 'bieber')

	def celebrityArticles(self, category):
		return self.getArticlesHelper(category, 'bieber')


	def ufoArticle(self, category):
		return self.getArticleHelper(category, 'ufo')

	def ufoArticles(self, category):
		return self.getArticlesHelper(category, 'ufo')


	def syriaArticle(self, category):
		return self.getArticleHelper(category, 'syria')

	def syriaArticles(self, category):
		return self.getArticlesHelper(category, 'syria')


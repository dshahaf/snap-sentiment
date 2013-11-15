import nltk, os
from nltk.corpus import movie_reviews
from random import randrange, sample
from gensim.corpora.dictionary import Dictionary
from gensim.corpora.mmcorpus import MmCorpus
from gensim.corpora.textcorpus import TextCorpus
from nltk.tokenize import word_tokenize, sent_tokenize

class Corpus:

	def __init__(self):
		path_to_nltk_data = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'nltk_data'
		)
		nltk.data.path.append(path_to_nltk_data)

		return

	####################
	# Helpers
	####################
	def combineStrings(self, listOfStrings):
		return "\n\n\n\n\n".join(listOfStrings)

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
		if category == 'positive' or category == 'negative':
			ret = self.movieReviews(category, 1)[0]
		elif category == 'combined':
			positiveList = self.movieReviews('positive', 10)
			negativeList = self.movieReviews('negative', 10)
			ret = self.combineStrings(positiveList) + "\n\n\n\n\n" + self.combineStrings(negativeList)
		return ret

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

	def tokensFromText(self, text):
		ret = []
		sentences = sent_tokenize(text)
		for s in sentences:
			words = word_tokenize(s)
			for w in words:
				ret.append(w)
		return ret

	def saveGensim(self, name):
		if name == 'movie':
			self.saveMovieReviewsGensim()

	"""
	"""
	def saveMovieReviewsGensim(self, count = 100):
		posReviews = self.movieReviews('positive', count)
		negReviews = self.movieReviews('negative', count)
	
		listOfTokens = [] # dictionary	
		docs = [] # corpus

		for pr in posReviews:
			tokens = self.tokensFromText(pr)
			listOfTokens.append(tokens)
			prWithoutNewlines = pr.replace('\n', ' ')
			docs.append(prWithoutNewlines)
		for nr in negReviews:
			tokens = self.tokensFromText(nr)
			listOfTokens.append(tokens)
			nrWithoutNewlines = nr.replace('\n', ' ')
			docs.append(nrWithoutNewlines)

		dictionaryFilename = 'movie_reviews_gensim_dictionary.txt'
		corpusFilename = 'movie_reviews_gensim_corpus.mm'

		# make destination files if they don't exist
		dictionaryPath = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'james_data',
			'movie_reviews',
			dictionaryFilename
		)

		if not os.path.exists(dictionaryPath):
			with open(dictionaryPath, 'w') as f:
				f.write(' ')

		corpusPath = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'james_data',
			'movie_reviews',
			corpusFilename
		)

		if not os.path.exists(corpusPath):
			with open(corpusPath, 'w') as f:
				f.write(' ')

		# save
		d = Dictionary(listOfTokens)
		d.save(dictionaryPath)

		corpus = MyTextCorpus('\n'.join(docs))
		corpus.save(corpusPath)

		return

	######################
	# James Data Helpers
	######################
	"""
	category is 'positive' or 'negative'
	Returns a string
	"""
	def getArticleHelper(self, category, topic):
		ret = ''
		if category == 'combined':
			dirPath = os.path.join(
				os.path.dirname(os.path.abspath(__file__)),
				'james_data',
				topic
			)
			combinedFilePath = os.path.join(dirPath, 'all')

			if os.path.exists(combinedFilePath):
				# use existing file
				ret = ''
				with open(combinedFilePath, 'r') as f:
					ret = f.read()
			else:
				positiveList = self.getArticlesHelper('positive', topic)
				negativeList = self.getArticlesHelper('negative', topic)
				ret = self.combineStrings(positiveList) + "\n\n\n\n\n" + self.combineStrings(negativeList)
				with open(combinedFilePath, 'w') as f:
					# save as 'all' in the topic directory
					f.write(ret)
		else:
			articles = self.getArticlesHelper(category, topic)
			l = len(articles)
			index = randrange(l)
			ret = articles[index]

		return ret

	"""
	category is 'positive' or 'negative'
	Returns a list of strings
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

	######################
	# James Data Getters
	######################
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

class MyTextCorpus(TextCorpus):
	def get_text(self):
		dictionary = self.dictionary
		print('dictionary')
		print(dictionary)
		return
		docs = []
		with open(path, 'r') as f:
			docs.append(f.read())
		for doc in docs:
			tokens = []
			sentences = sent_tokenize(doc)
			for s in sentences:
				words = word_tokenize(s)
				for w in words:
					tokens.append(w)
			yield(tokens)
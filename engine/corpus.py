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

	def saveGensim(self, topic):
		if topic is None:
			# generate all
			self.saveGensim('movie')
			self.saveGensim('celebrity')
			self.saveGensim('syria')
			self.saveGensim('ufo')
			return

		posReviews = []
		negReviews = []

		if topic == 'movie':
			topic = 'movie_reviews'
		elif topic == 'celebrity':
			topic = 'bieber'

		if topic == 'movie_reviews':
			count = 100
			posReviews = self.movieReviews('positive', count)
			negReviews = self.movieReviews('negative', count)
		else:
			posDocs = self.getArticlesHelper('positive', topic)
			negDocs = self.getArticlesHelper('negative', topic)

		listOfTokens = [] # dictionary
		docs = [] # corpus

		for posDoc in posDocs:
			processed = self.processDocForGensim(posDoc)
			tokens = self.tokensFromText(processed)
			listOfTokens.append(tokens)
			docs.append(processed)
		for negDoc in negDocs:
			processed = self.processDocForGensim(negDoc)
			tokens = self.tokensFromText(processed)
			listOfTokens.append(tokens)
			docs.append(processed)

		dictionaryFilename = 'gensim_dictionary.txt'
		corpusFilename = 'gensim_corpus.mm'

		# make destination files if they don't exist
		dictionaryPath = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'james_data',
			topic,
			dictionaryFilename
		)

		corpusPath = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'james_data',
			topic,
			corpusFilename
		)

		corpusTempPath = corpusPath + '.tmp'

		if os.path.exists(dictionaryPath):
			os.remove(dictionaryPath)

		if os.path.exists(corpusPath):
			os.remove(corpusPath)

		if os.path.exists(corpusTempPath):
			os.remove(corpusTempPath)

		with open(dictionaryPath, 'w') as f:
			f.write(' ')

		with open(corpusPath, 'w') as f:
			f.write(' ')

		# save dictionary and corpus
		d = Dictionary(listOfTokens)
		d.save(dictionaryPath)

		with open(corpusTempPath, 'w') as f:
			f.write('\n'.join(docs))

		corpus = TextCorpus(corpusTempPath)
		MmCorpus.save_corpus(corpusPath, corpus)

		return

	def isAlphanumeric(self, c):
		return ('0' <= c and c <= '9') or ('a' <= c and c <= 'z') or ('A' <= c and c <= 'Z')

	def processDocForGensim(self, doc):
		withoutNewlines = doc.replace('\n', ' ')
		lowered = withoutNewlines.lower()
		ret = ''
		# replace non-ascii letters with ' '
		for c in lowered:
			if (ord(c) < 128):
				ret += c
			else:
				ret += ' '
		tokens = self.tokensFromText(ret)
		filtered = []
		for token in tokens:
			# remove single letter tokens
			l = len(token)
			if l == 1:
				continue
			# remove non alphanumeric tokens
			isAlphanumeric = True
			for c in token:
				if not self.isAlphanumeric(c):
					isAlphanumeric = False
					break
			if not isAlphanumeric:
				continue
			filtered.append(token)

		return ' '.join(filtered)

	######################
	# James Data Helpers
	######################
	"""
	category is 'positive' or 'negative'
	topic is one of ['bieber', 'syria', 'ufo']
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

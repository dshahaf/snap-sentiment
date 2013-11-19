import nltk, os
from nltk.corpus import movie_reviews
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from random import randrange, sample
from gensim import utils
from gensim.corpora.dictionary import Dictionary
from gensim.corpora.mmcorpus import MmCorpus
from gensim.corpora.textcorpus import TextCorpus
from gensim.models.ldamodel import LdaModel

class Corpus:

	def __init__(self):
		path_to_nltk_data = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'nltk_data'
		)
		nltk.data.path.append(path_to_nltk_data)
		self.stopwords = self.stopWordDict()
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
		# nltk english stop words
		ret = {}
		sws = stopwords.words('english')
		for sw in sws:
			ret[sw] = True
		return ret
		'''
		# stanford nlp small stop words
		path = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'lib',
			'stop-words-small.txt'
		)
		return self.wordDictHelper(path)
		'''

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

		posDocs = []
		negDocs = []

		if topic == 'movie':
			topic = 'movie_reviews'
		elif topic == 'celebrity':
			topic = 'bieber'

		if topic == 'movie_reviews':
			count = 100
			posDocs = self.movieReviews('positive', count)
			negDocs = self.movieReviews('negative', count)
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
			# remove stop words
			if token in self.stopwords:
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

	########################
	## LDA using SNAP data
	########################

	"""
	Command order:
	from corpus import Corpus
	c = Corpus()
	c.SNAP_ldaTopicsForTopic('bieber')

	Once:
	c.SNAP_generateGensimDictionaryForSNAP()
	c.SNAP_generateMmCorpus('all')
	c.SNAP_generateLDAForTopic('all')
	"""


	"""
	1. (LDA) To run LDA, we need 1) id2word mapping (gensim Dictionary), 2) MmCorpus.
	2. (id2word) For all SNAP data, id2word mapping is shared. This can be generated by going through RepresentativeTokens, and just feeding in all the words to gensim.
	3. (corpus) Each document is a list of (word_id, word_weight) tuples.

	To summarize,
	1) (id2word) Generate a gensim dictionary by going through RepresentativeTokens.txt, and feeding in [[word1, word2, ...]]. Save it as gensim_snap_dict.txt
	2) (corpus) For each topic (e.g., bieber), generate a corpus of [[(word_id, tfidf score), ... ], ...], and save it as MmCorpus named gensim_snap_mmcorpus_bieber.mm
	3) (lda) For each topic (e.g., bieber), generate the lda result as,
	lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=10, update_every=1, chunksize=10000, passes=1)
	"""

	"""
	Creates gensim_snap_dict.txt in snap_data.
	TODO: handle document frequency. Currently all set to 1
	"""
	def SNAP_generateGensimDictionaryForSNAP(self):
		inputFilePath = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'snap_data',
			'RepresentativeTokens.txt'
		)
		outputFilepath = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'snap_data',
			'gensim_snap_dict.txt'
		)
		# format: id[TAB]word_utf8[TAB]document frequency[NEWLINE].
		linesToWrite = []
		with open(inputFilePath, 'r') as f:
			for line in f:
				line = line.rstrip()
				tokens = line.split()
				wordID = tokens[0]
				word = tokens[1]
				linesToWrite.append("%s\t%s\t%d" % (wordID, word, 1)) # TODO handle doc freq better
		textToWrite = "\n".join(linesToWrite) + "\n"
		with open(outputFilepath, 'w') as f:
			f.write(textToWrite)
		return

	"""
	topic is one of "bieber", "cyrus", "syria", "ufo"
	Generates gensim_snap_mmcorpus_<topic>.mm in snap_data
	"""
	def SNAP_generateMmCorpus(self, topic):
		if topic == 'all':
			topics = ['bieber', 'cyrus', 'syria', 'ufo']
			for t in topics:
				self.SNAP_generateMmCorpus(t)
			return
		corpus = self.SNAP_corpusForTopic(topic)
		outputPath = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'snap_data',
			"gensim_snap_mmcorpus_%s.mm" % topic
		)
		id2word = self.SNAP_id2word()
		MmCorpus.save_corpus(outputPath, corpus, id2word)
		return

	"""
	HELPER
	topic is one of "bieber", "cyrus", "syria", "ufo"
	Returns [
		[
			(word_id, tfidf), ...
		],
		...
	]
	"""
	def SNAP_corpusForTopic(self, topic):
		dirPath = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'snap_data',
			topic
		)
		filenames = os.listdir(dirPath)
		ret = []
		for filename in filenames:
			if len(filename.split('-')) == 2:
				filepath = os.path.join(
					os.path.dirname(os.path.abspath(__file__)),
					'snap_data',
					topic,
					filename
				)
				with open(filepath, 'r') as f:
					flagInDoc = False
					docData = []
					for line in f:
						line = line.rstrip()
						tokens = line.split()
						numTokens = len(tokens)

						flagNewDoc = (numTokens > 2)
						flagEndDoc = (numTokens == 0)

						if (flagInDoc and flagEndDoc):
							# finished reading the current doc
							ret.append(docData)
							docData = []
							flagInDoc = False
						elif (flagInDoc and (not flagEndDoc)):
							# need to read (word_id, tfidf)
							wordID = (int)(tokens[0])
							tfidf = (float)(tokens[1])
							docData.append((wordID, tfidf))
						elif ((not flagInDoc) and flagNewDoc):
							# just read the doc header
							flagInDoc = True
		return ret

	def SNAP_id2word(self):
		path = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'snap_data',
			'gensim_snap_dict.txt'
		)
		# self.myLoadFromText(path)
		ret = Dictionary.load_from_text(path)
		return ret

	"""
	Saves the file to,
	"snap_data/gensim_snap_lda_<topic>_<numTopics>"
	"""
	def SNAP_generateLDAForTopic(self, topic, numTopics = 5):
		if (topic == 'all'):
			topics = ['syria', 'ufo', 'movie', 'celebrity', 'russia'] # bieber, cyrus
			for t in topics:
				for nt in [5, 10]:
					self.SNAP_generateLDAForTopic(t, nt)
			return
		id2word = self.SNAP_id2word()
		mmPath = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'snap_data',
			"gensim_snap_mmcorpus_%s.mm" % topic
		)
		outPath = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'snap_data',
			"gensim_snap_lda_%s_%d" % (topic, numTopics)
		)
		mm = MmCorpus(mmPath)
		lda = LdaModel(corpus=mm, id2word=id2word, num_topics=numTopics, update_every=1, chunksize=10000, passes=1)
		lda.save(outPath)
		return

	"""
	Returns a list of strings
	"""
	def SNAP_ldaTopicsForTopic(self, topic, numTopics = 10):
		if numTopics not in [10, 20, 30]:
			print("[ERROR] Invalid numTopics")
			return
		inPath = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'snap_data',
			"gensim_snap_lda_%s_%d" % (topic, numTopics)
		)
		lda = LdaModel.load(inPath)
		return lda.print_topics(numTopics)
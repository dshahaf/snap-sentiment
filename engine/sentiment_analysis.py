#!/usr/bin/env python
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
import nltk, os
from nltk import pos_tag
from text_processor import TextProcessor
from corpus import Corpus
from math import log
from lib.porter2 import stem

class SentimentAnalysis:

	controversyScoreCache = {}

	def __init__(self, text = ''):
		# prepare to use nltk_data
		path_to_nltk_data = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			'nltk_data'
		)
		nltk.data.path.append(path_to_nltk_data)

		# pre-processing
		tp = TextProcessor(text)
		self.text = tp.getProcessedText()

		# setup dictionaries
		corpus = Corpus()
		words = {}
		words['positive'] = corpus.positiveWordDict()
		words['negative'] = corpus.negativeWordDict()
		self.dictionaries = words

	def setText(self, text):
		tp = TextProcessor(text)
		self.text = tp.getProcessedText()

	##########################################
	# Simple Analysis
	##########################################
	"""
	Returns array of tokens
	"""
	def tokensFromText(self, text):
		ret = []
		sentences = sent_tokenize(text)
		for sentence in sentences:
			words = word_tokenize(sentence)
			for word in words:
				ret.append(word)
		return ret

	"""
	Returns array of,
	{
		value: <token>
		sentiment: "positive" or "negative" or "neither"
	}
	"""
	def getTaggedTokens(self):
		tokens = self.tokensFromText(self.text)
		ret = []
		for token in tokens:
			entry = {
				'value' : token,
				'sentiment' : 'neither'
			}
			if token in self.dictionaries['positive']:
				entry['sentiment'] = 'positive'
			elif token in self.dictionaries['negative']:
				entry['sentiment'] = 'negative'
			ret.append(entry)
		return ret

	"""
	Returns 1 if sentiment is determined positive, -1 if negative, 0 if neither
	"""
	def simpleAnalysisInt(self):
		ret = 0
		taggedTokens = self.getTaggedTokens()
		posCount = 0;
		negCount = 0;
		for taggedToken in taggedTokens:
			sentiment = taggedToken['sentiment']
			if sentiment == "positive":
				posCount += 1
			elif sentiment == "negative":
				negCount += 1
		if posCount > negCount:
			ret = 1
		elif posCount < negCount:
			ret = -1
		return ret

	"""
	Returns,
	{
		'words' : array of { 'value': str, 'sentiment': 'positive' or 'negative' or 'neither' },
		'overall_sentiment' : 'positive' or 'negative' or 'neither',
		'sentimental_words' : {
			'positive' : array of { 'value': str, 'count': int },
			'negative' : array of { 'value': str, 'count': int },
			'count': {
				'positive' : int,
				'negative' : int,
			}
		},
	}
	"""
	def simpleAnalysis(self):
		ret = {
			'words' : [],
			'overall_sentiment' : '',
			'sentimental_words' : {
				'positive' : [],
				'negative' : [],
				'count': {
					'positive': 0,
					'negative': 0,
				},
			},
		}

		positiveWords = {} # word -> count
		negativeWords = {} # word -> count
		taggedTokens = self.getTaggedTokens()

		# ret['words']
		for taggedToken in taggedTokens:
			ret['words'].append(taggedToken)
			token = taggedToken['value']
			sentiment = taggedToken['sentiment']
			if sentiment == 'positive':
				if token not in positiveWords:
					positiveWords[token] = 0
				positiveWords[token] += 1
			elif sentiment == 'negative':
				if token not in negativeWords:
					negativeWords[token] = 0
				negativeWords[token] += 1
		
		pcount = 0
		ncount = 0

		# ret['sentimental_words']['positive']
		for pword in sorted(positiveWords.keys()):
			count = positiveWords[pword]
			pcount += count
			ret['sentimental_words']['positive'].append({
				'value' : pword,
				'count' : count	
			})

		# ret['sentimental_words']['negative']
		for nword in sorted(negativeWords.keys()):
			count = negativeWords[nword]
			ncount += count
			ret['sentimental_words']['negative'].append({
				'value' : nword,
				'count' : count	
			})

		# ret['sentimental_words']['count']
		ret['sentimental_words']['count']['positive'] = pcount
		ret['sentimental_words']['count']['negative'] = ncount

		# ret['overall_sentiment']
		if pcount > ncount:
			ret['overall_sentiment'] = 'positive'
		elif pcount < ncount:
			ret['overall_sentiment'] = 'negative'
		else:
			ret['overall_sentiment'] = 'neither'

		return ret

	##########################################
	# Noun Analysis
	##########################################

	def isNounToken(self, taggedToken):
		word = taggedToken['value']
		t = taggedToken['type']
		return (word.isalpha()) and len(word) > 1 and (t[:2] == "NN")

	def isAdjectiveToken(self, taggedToken):
		t = taggedToken['type']
		return t[:2] == "JJ"

	"""
	Returns,
	[
		# sentence
		[
			# tagged token
			{
				'value': string,
				'type': string,
			},
			...
		],
		...
	]
	"""
	def getParseTaggedSentences(self):
		text = self.text
		ret = []
		sentences = sent_tokenize(text)
		for sentence in sentences:
			currList = []
			tokens = word_tokenize(sentence)
			taggedTokens = pos_tag(tokens)
			for taggedToken in taggedTokens:
				currList.append({
					'value': taggedToken[0],
					'type': taggedToken[1],
				})
			ret.append(currList)
		return ret

	# returns 'positive', 'negative', or 'neither'
	def sentimentFromWord(self, word):
		ret = 'neither'
		if word in self.dictionaries['positive']:
			ret = 'positive'
		elif word in self.dictionaries['negative']:
			ret = 'negative'
		return ret

	# returns 'positive', 'negative', or 'neither'
	def sentimentFromCounts(self, posCount, negCount):
		ret = 'neither'
		if posCount > negCount:
			ret = 'positive'
		elif posCount < negCount:
			ret = 'negative'
		return ret

	def getOrderedPair(self, a, b):
		if a < b:
			return (a, b)
		else:
			return (b, a)

	def getControversyScoreFromCounts(self, posCount, negCount, scaleFactor = 2):
		cacheKey = self.getOrderedPair(posCount, negCount)
		if cacheKey in self.controversyScoreCache:
			return self.controversyScoreCache[cacheKey]
		p = posCount
		n = negCount
		t1 = posCount + negCount + 1
		d = abs(posCount - negCount)
		totalCountFactor = log(t1) # [0, inf]
		diffCountFactor = (1 - (d * 1.0 / t1)) # [0, 1]
		diffCountFactorScaled = 1 + (scaleFactor - 1.0) * diffCountFactor # [1, k] 
		ret = totalCountFactor * diffCountFactorScaled

		self.controversyScoreCache[cacheKey] = ret
		return ret

	"""
	Helper for nounAnalysis
	Returns,
	[
		{
			'sentiment': string,
			'words': [
				{
					'value': string,
					'type': string,
					'sentiment': string,
					'isNoun': string, ('true' or 'false'),
					'isAdjective': string, ('true' or 'false')
				}
			],
			...
		},
		...
	]
	"""
	def getProcessedSentences(self, nounsWithCounts):
		ret = []
		parseTaggedSentences = self.getParseTaggedSentences()

		for parseTaggedSentence in parseTaggedSentences:
			currObj = { 'sentiment': '', 'words': [] }
			posCount = 0
			negCount = 0
			currNouns = {} # noun => True

			# first, register the nouns in the current sentence
			for taggedToken in parseTaggedSentence:
				v = taggedToken['value']
				t = taggedToken['type']
				if not self.isNounToken(taggedToken): continue

				currNouns[v] = True
				if v not in nounsWithCounts:
					nounsWithCounts[v] = { 'positive': {}, 'negative': {} }

			for taggedToken in parseTaggedSentence:
				v = taggedToken['value']
				t = taggedToken['type']

				currWord = {
					'value': v,
					'type': t,
					'sentiment': self.sentimentFromWord(v) if self.isAdjectiveToken(taggedToken) else 'neither',
					'isNoun': 'true' if self.isNounToken(taggedToken) else 'false',
					'isAdjective': 'true' if self.isAdjectiveToken(taggedToken) else 'false'
				}

				currObj['words'].append(currWord)

				if currWord['sentiment'] == 'positive':
					posCount += 1
					for k in currNouns.keys():
						if v not in nounsWithCounts[k]['positive']:
							nounsWithCounts[k]['positive'][v] = 0
						nounsWithCounts[k]['positive'][v] += 1

				elif currWord['sentiment'] == 'negative':
					negCount += 1
					for k in currNouns.keys():
						if v not in nounsWithCounts[k]['negative']:
							nounsWithCounts[k]['negative'][v] = 0
						nounsWithCounts[k]['negative'][v] += 1

			currObj['sentiment'] = self.sentimentFromCounts(posCount, negCount)
			ret.append(currObj)

		return ret

	"""
	Helper for nounsWithCountsListFromDict

	@param
	nounsWithCounts: {
		noun : {
			'positive' : {
				neighbor : int,
				...
			}
			'negative' : {
				neighbor : int,
				...
			}
		},
		...
	}

	@return
	[
		{
			'values': [] # list of strings with the same stem
			'positive': {
				neighbor: int,
				...
			},
			'negative': {
				neighbor: int,
				...
			}
		},
		...
	]
	"""
	def groupNounsWithCounts(self, nounsWithCounts):
		ret = []
		stemToNouns = {} # stem => { noun => True }

		# populate stemToNouns
		for noun in nounsWithCounts.keys():
			currStem = stem(noun)
			if currStem not in stemToNouns:
				stemToNouns[currStem] = {}
			if noun not in stemToNouns[currStem]:
				stemToNouns[currStem][noun] = True

		# populate ret
		for currStem in stemToNouns.keys():
			nounToTrue = stemToNouns[currStem]
			currObj = {
				'values': [],
				'positive': {},
				'negative': {},
			}
			for noun in sorted(nounToTrue.keys()):
				currObj['values'].append(noun)
				positiveCountDict = nounsWithCounts[noun]['positive']
				negativeCountDict = nounsWithCounts[noun]['negative']
				for neighbor in positiveCountDict.keys():
					if neighbor not in currObj['positive']:
						currObj['positive'][neighbor] = 0
					currObj['positive'][neighbor] += positiveCountDict[neighbor]
				for neighbor in negativeCountDict.keys():
					if neighbor not in currObj['negative']:
						currObj['negative'][neighbor] = 0
					currObj['negative'][neighbor] += negativeCountDict[neighbor]
			ret.append(currObj)

		return ret

	"""
	Helper for nounAnalysis

	@param
	nounsWithCounts: {
		noun : {
			'positive' : {
				neighbor : int,
				...
			}
			'negative' : {
				neighbor : int,
				...
			}
		},
		...
	}

	@return
	[
		{
			'values': [], # list of strings
			'sentiment': string,
			'sentiment_score': int,
			'controversy_score': float,
			'positive_neighbors': [
				{
					'value': string,
					'count': int,
				},
				...
			]
			'negative_neighbors': [
				{
					'value': string,
					'count': int,
				},
				...
			]
		},
		...
	]
	"""
	def nounsWithCountsListFromDict(self, nounsWithCounts):
		ret = []

		'''
		nounsWithCountsGrouped:
		[
			{
				'values': [] # list of strings with the same stem
				'positive': {
					neighbor: int,
					...
				},
				'negative': {
					neighbor: int,
					...
				}
			},
			...
		]
		'''
		nounsWithCountsGrouped = self.groupNounsWithCounts(nounsWithCounts)

		for obj in nounsWithCountsGrouped:
			entry = {
				'values': obj['values'],
				'sentiment': '',
				'positive_neighbors': [],
				'negative_neighbors': [],
				'sentiment_score': 0,
				'controversy_score': 0,
			}

			positiveNeighborsDict = obj['positive']
			negativeNeighborsDict = obj['negative']
			posCount = 0
			negCount = 0

			for positiveNeighbor in positiveNeighborsDict.keys():
				currCount = positiveNeighborsDict[positiveNeighbor]
				posCount += currCount
				entry['positive_neighbors'].append({
					'value': positiveNeighbor, 'count': currCount
				})

			for negativeNeighbor in negativeNeighborsDict.keys():
				currCount = negativeNeighborsDict[negativeNeighbor]
				negCount += currCount
				entry['negative_neighbors'].append({
					'value': negativeNeighbor, 'count': currCount	
				})

			entry['positive_neighbors'] = sorted(entry['positive_neighbors'], key = lambda k : -k['count'])
			entry['negative_neighbors'] = sorted(entry['negative_neighbors'], key = lambda k : -k['count'])
			entry['positive_neighbors'].insert(0, {'value': 'TOTAL', 'count': posCount	})
			entry['negative_neighbors'].insert(0, {'value': 'TOTAL', 'count': negCount	})

			entry['sentiment'] = self.sentimentFromCounts(posCount, negCount)
			entry['sentiment_score'] = posCount - negCount
			entry['controversy_score'] = self.getControversyScoreFromCounts(posCount, negCount)


			ret.append(entry)

		return ret

	"""
	Returns,
	{
		'sentences': [
			{
				'sentiment': string,
				'words': [
					{
						'value': string,
						'type': string,
						'sentiment': string,
						'isNoun': string, ('true' or 'false'),
						'isAdjective': string, ('true' or 'false')
					}
				],
				...
			},
			...
		],

		'words': [
			{
				'values': [], # list of strings
				'sentiment': string,
				'sentiment_score': int,
				'controversy_score': float,
				'positive_neighbors': [
					{
						'value': string,
						'count': int,
					},
					...
				]
				'negative_neighbors': [
					{
						'value': string,
						'count': int,
					},
					...
				]
			},
			...
		]
	}
	"""
	def nounAnalysis(self):
		ret = { 'sentences': [], 'words': [], }
		nounsWithCounts = {} # word => { 'positive' : { word => int }, 'negative': { word => int } }
		ret['sentences'] = self.getProcessedSentences(nounsWithCounts)
		nounsWithCountsList = self.nounsWithCountsListFromDict(nounsWithCounts)
		ret['words'] = sorted(nounsWithCountsList, key = lambda k : -k['controversy_score'])
		return ret
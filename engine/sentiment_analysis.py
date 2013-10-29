#!/usr/bin/env python
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
import nltk, os
from nltk import pos_tag
from text_processor import TextProcessor
from corpus import Corpus

class SentimentAnalysis:

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

	###################
	# Simple Analysis
	###################
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

	##################
	# Noun Analysis
	##################

	def isNounToken(self, token):
		return (token[:2] == "NN")

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
						'isNoun': string, ('true' or 'false')
					}
				],
				...
			},
			...
		],

		'words': [
			{
				'value': string,
				'sentiment': string,
				'score': int,
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
		ret = {
			'sentences': [],
			'words': [],
		}

		# word => { 'positive' : { word => int }, 'negative': { word => int } }
		nounsWithCounts = {}

		parseTaggedSentences = self.getParseTaggedSentences()

		for parseTaggedSentence in parseTaggedSentences:
			currObj = {
				'sentiment': '',
				'words': []
			}
			posCount = 0
			negCount = 0
			currNouns = {}

			for taggedToken in parseTaggedSentence:
				print(taggedToken)
				v = taggedToken['value']
				t = taggedToken['type']
				if not self.isNounToken(t):
					continue
				currNouns[v] = True
				if v not in nounsWithCounts:
					nounsWithCounts[v] = {
						'positive': {},
						'negative': {},
					}

			for taggedToken in parseTaggedSentence:
				v = taggedToken['value']
				t = taggedToken['type']

				wordSentiment = 'neither'
				if v in self.dictionaries['positive']:
					wordSentiment = 'positive'
				elif v in self.dictionaries['negative']:
					wordSentiment = 'negative'
				isNounString = 'false'
				if self.isNounToken(t):
					isNounString = 'true'
				currObj['words'].append({
					'value': v,
					'type': t,
					'sentiment': wordSentiment,
					'isNoun': isNounString,
				})

				if v in self.dictionaries['positive']:
					posCount += 1
					for k in currNouns.keys():
						if v not in nounsWithCounts[k]['positive']:
							nounsWithCounts[k]['positive'][v] = 0
						nounsWithCounts[k]['positive'][v] += 1

				elif v in self.dictionaries['negative']:
					negCount += 1
					for k in currNouns.keys():
						if v not in nounsWithCounts[k]['negative']:
							nounsWithCounts[k]['negative'][v] = 0
						nounsWithCounts[k]['negative'][v] += 1

			if posCount > negCount:
				currObj['sentiment'] = 'positive'
			elif posCount < negCount:
				currObj['sentiment'] = 'negative'
			else:
				currObj['sentiment'] = 'neither'
			ret['sentences'].append(currObj)

		# process nounsWithCounts
		nounsWithCountsList = []
		for noun in nounsWithCounts.keys():
			entry = {
				'value': noun,
				'sentiment': '',
				'positive_neighbors': [],
				'negative_neighbors': [],
				'score': 0,
			}
			obj = nounsWithCounts[noun]
			positiveNeighborsDict = obj['positive']
			negativeNeighborsDict = obj['negative']
			posCount = 0
			negCount = 0
			for positiveNeighbor in positiveNeighborsDict.keys():
				currCount = positiveNeighborsDict[positiveNeighbor]
				posCount += currCount
				entry['positive_neighbors'].append({
					'value': positiveNeighbor,
					'count': currCount
				})
			for negativeNeighbor in negativeNeighborsDict.keys():
				currCount = negativeNeighborsDict[negativeNeighbor]
				negCount += currCount
				entry['negative_neighbors'].append({
					'value': negativeNeighbor,
					'count': currCount	
				})
			if posCount > negCount:
				entry['sentiment'] = 'positive'
			elif posCount < negCount:
				entry['sentiment'] = 'negative'
			else:
				entry['sentiment'] = 'neither'
			entry['score'] = posCount - negCount
			nounsWithCountsList.append(entry)
		ret['words'] = sorted(nounsWithCountsList, key = lambda k : -k['score'])
		return ret
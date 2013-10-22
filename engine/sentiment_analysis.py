#!/usr/bin/env python
from lib.words import Words
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
import nltk
from nltk import pos_tag


class SentimentAnalysis:

	def __init__(self, text):
		nltk.data.path.append('./nltk_data/')

		# pre-processing
		text = text.replace('"', ' ')
		text = text.replace('-', ' ')

		self.text = text
		w = Words()
		words = {}
		words['positive'] = w.positiveWords()
		words['negative'] = w.negativeWords()
		self.dictionaries = words

	###################
	# Simple Analysis
	###################
	def tokenize(self, text):
		ret = []
		sentences = sent_tokenize(text)
		for sentence in sentences:
			words = word_tokenize(sentence)
			for word in words:
				ret.append(word)
		return ret

	def simpleAnalysis(self):
		ret = {
			'words' : [],  # { 'value' : ?, 'count' : ? }
			'overall_sentiment' : '', # positive or negative
			'sentimental_words' : {
				'positive' : [], # { 'value' : ?, 'count' : ? }
				'negative' : [],
				'count': {
					'positive': 0,
					'negative': 0
				},
			},
		}

		arr = self.tokenize(self.text)
		positiveWords = {}
		negativeWords = {}

		for word in arr:
			if word in self.dictionaries['positive']:
				ret['words'].append({
					'value' : word,
					'sentiment' : 'positive'	
				})
				if word not in positiveWords:
					positiveWords[word] = 0
				positiveWords[word] += 1

			elif word in self.dictionaries['negative']:
				ret['words'].append({
					'value' : word,
					'sentiment' : 'negative'
				})
				if word not in negativeWords:
					negativeWords[word] = 0
				negativeWords[word] += 1
			else:
				ret['words'].append({
					'value' : word,
					'sentiment' : 'neither'
				})

		for positiveWord in positiveWords.keys():
			count = positiveWords[positiveWord]
			ret['sentimental_words']['positive'].append({
				'value' : positiveWord,
				'count' : count
			})
			ret['sentimental_words']['count']['positive'] += count

		for negativeWord in negativeWords.keys():
			count = negativeWords[negativeWord]
			ret['sentimental_words']['negative'].append({
				'value' : negativeWord,
				'count' : count
			})
			ret['sentimental_words']['count']['negative'] += count

		pcount = ret['sentimental_words']['count']['positive']
		ncount = ret['sentimental_words']['count']['negative']
		if pcount > ncount:
			ret['overall_sentiment'] = 'Positive'
		elif pcount < ncount:
			ret['overall_sentiment'] = 'Negative'
		else:
			ret['overall_sentiment'] = 'Neither'

		return ret

	##################
	# Noun Analysis
	##################

	"""
	{
		'sentences': [
			{
				'sentiment' : '' # positive, negative, or neither
				'words': [
					{
						'value' : ''
						'sentiment' : '' # positive, negative, or neither
						'isNoun': 'true' or 'false'
					},
					...
				]
			},
			...
		]
	}
	"""
	def nounAnalysis(self):
		ret = {}
		ret['sentences'] = []
		sentences = sent_tokenize(self.text)
		for sentence in sentences:
			entry = {
				'sentiment' : '',
				'words': []
			}
			numPos = 0
			numNeg = 0
			words = word_tokenize(sentence)
			tagged_words = pos_tag(words)
			for tagged_word in tagged_words:
				value = tagged_word[0]
				sentiment = ''
				if value in self.dictionaries['positive']:
					sentiment = 'positive'
					numPos += 1
				elif value in self.dictionaries['negative']:
					sentiment = 'negative'
					numNeg += 1
				else:
					sentiment = 'neither'
				wordType = tagged_word[1]
				isNoun = 'false'
				if (wordType == 'NN') or (wordType == 'NNS'):
					isNoun = 'true'
				entry['words'].append({
					'value' : value,
					'sentiment' : sentiment,
					'isNoun' : isNoun
				})
			if numPos > numNeg:
				entry['sentiment'] = 'positive'
			elif numPos < numNeg:
				entry['sentiment'] = 'negative'
			else:
				entry['sentiment'] = 'neither'
			ret['sentences'].append(entry)
		return ret
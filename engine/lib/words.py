#!/usr/bin/env python

class Words:
	positiveWordsPath = 'positive-words.txt'
	negativeWordsPath = 'negative-words.txt'
	stopWordsSmallPath = 'stop-words-small.txt'

	def arrayToDict(arr):
		ret = {}
		for s in arr:
			if s not in ret:
				ret[s] = True
		return ret

	def positiveWords(self):
		ret = []
		with open(self.positiveWordsPath, 'r') as f:
			for line in f:
				ret.append(line.rstrip())
		return arrayToDict(ret)

	def negativeWords(self):
		ret = []
		with open(self.negativeWordsPath, 'r') as f:
			for line in f:
				ret.append(line.rstrip())
		return arrayToDict(ret)

	def stopWords(self):
		ret = []
		with open(self.stopWordsSmallPath, 'r') as f:
			for line in f:
				ret.append(line.rstrip())
		return arrayToDict(ret)
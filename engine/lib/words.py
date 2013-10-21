#!/usr/bin/env python

import os

class Words:
	dirPath = os.path.dirname(os.path.abspath(__file__))
	positiveWordsPath = os.path.join(dirPath, 'positive-words.txt')
	negativeWordsPath = os.path.join(dirPath, 'negative-words.txt')
	stopWordsSmallPath = os.path.join(dirPath, 'stop-words-small.txt')

	
	def arrayToDict(self, arr):
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
		return self.arrayToDict(ret)

	def negativeWords(self):
		ret = []
		with open(self.negativeWordsPath, 'r') as f:
			for line in f:
				ret.append(line.rstrip())
		return self.arrayToDict(ret)

	def stopWords(self):
		ret = []
		with open(self.stopWordsSmallPath, 'r') as f:
			for line in f:
				ret.append(line.rstrip())
		return self.arrayToDict(ret)
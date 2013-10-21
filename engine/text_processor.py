#!/usr/bin/env python
from lib.porter2 import stem as pstem
from lib.words import Words

class TextProcessor:

	def __init__(self, text):
		self.text = text
		w = Words()
		words = {}
		words['positive'] = w.positiveWords()
		words['negative'] = w.negativeWords()
		words['stop'] = w.stopWords()
		self.dictionaries = words

	def stemArray(arr):
		stemCache = {}
		ret = []
		for w in arr:
			if w not in stemCache:
				stemCache[w] = pstem(w)
			ret.append(stemCache[w])
		return ret

	def extractAlphabetWords(text):
		arr = text.split()
		retArr = []
		for word in arr:
			if word.isalpha():
				retArr.append(word)
		return ' '.join(retArr)

	def process(self, lower, removeStop, alphabetsOnly):
		if alphabetsOnly:
			self.text = extractAlphabetWords(self.text)
		if lower:
			self.text = self.text.lower()
		arr = self.text.split()
		if removeStop:
			tmp = []
			for w in arr:
				if w not in self.dictionaries.stop:
					tmp.append(w)
			arr = tmp
		self.text = ' '.join(arr)


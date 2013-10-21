#!/usr/bin/env python
from lib.porter2 import stem as pstem
from lib.words import Words

class TextProcessor:

	def __init__(self, text):
		self.text = text
		w = Words()
		words = {}
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

	def process(self, lower, alphabetsOnly, removeStop):
		if lower:
			self.text = self.text.lower()
		if alphabetsOnly:
			tmp = ''
			for c in self.text:
				if c.isalpha():
					tmp += c
				else:
					tmp += ' '
			self.text = tmp
		arr = self.text.split()
		if removeStop:
			tmp = []
			for w in arr:
				if w not in self.dictionaries['stop']:
					tmp.append(w)
			arr = tmp
		self.text = ' '.join(arr)

	def get(self):
		return self.text
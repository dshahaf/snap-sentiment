#!/usr/bin/env python

import nltk, os
from nltk import pos_tag
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from lib.porter2 import stem
from clean_corpus import CleanCorpus
from math import log, sqrt

"""
Parent class for sentiment analysis classes

Useful Methods:
def getControversyScoreFromCounts(self, posCount, negCount)

"""
class CleanSentimentAnalysis:

  ##################
  # Public Methods
  ##################

  def __init__(self):
    return

  def getControversialWords(self, text, max = 10):
    

  def getControversyScoreFromCounts(self, posCount, negCount):
    # cacheKey = self.getOrderedPair(posCount, negCount)
    # if cacheKey in self.controversyScoreCache:
    #   return self.controversyScoreCache[cacheKey]

    p = posCount
    n = negCount

    s = posCount + negCount # sum
    sN = s + 1 # sum Normalized
    d = abs(posCount - negCount) # diff
    dR = 1.0 * d / sN # diff Ratio
    dF = 1 - dR * dR * (1 - 1.0 / sqrt(sN)) # diff Factor

    ret = log(sN * dF)
    # self.controversyScoreCache[cacheKey] = ret
    return ret

  ##################
  # Helpers
  ##################

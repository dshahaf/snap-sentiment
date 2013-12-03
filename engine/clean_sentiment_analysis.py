#!/usr/bin/env python

"""
Useful methods of class CleanSentimentAnalysis:

def getScoresFromRawText(self, rawText, detailed = False)
def getControversyScoreFromCounts(self, posCount, negCount)
"""

import nltk, os
from nltk import pos_tag
from lib.porter2 import stem
from math import log, sqrt
from clean_corpus import CleanCorpus
from clean_text_processor import CleanTextProcessor
from clean_tagger import CleanTagger

class CleanSentimentAnalysis:

  """
  ivars:

  tp = CleanTextProcessor()
  corpus = CleanCorpus()
  tagger = CleanTagger()
  """

  ##################
  # Public Methods
  ##################

  def __init__(self):
    self.tp = CleanTextProcessor()
    self.corpus = CleanCorpus()
    self.tagger = CleanTagger()
    return

  """
  @param rawText, detailed
  @return
  case 1) detailed is False
  [
    # word group 1 begins
    {
      'words' : [string, ...], # group of equivalent words (currently determined by stems),
      'scores' : {
        'controversy' : float,
        'sentiment' : float,
      },
    },
    ...
  ]
  case 2) detailed is True
  [
    # word group 1 begins
    {
      'words' : [string, ...], # group of equivalent words (currently determined by stems),

    },
    ...
  ]

  """
  def getScoresFromRawText(self, rawText, detailed = False):
    return

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

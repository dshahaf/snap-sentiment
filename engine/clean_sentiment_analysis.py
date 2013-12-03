#!/usr/bin/env python

"""
Useful methods of class CleanSentimentAnalysis:

def getScoresFromRawText(self, rawText, detailed = False)
def getControversyScoreFromCountsWithCache(self, posCount, negCount, cache = {})
def getControversyScoreFromCounts(self, posCount, negCount)
"""

# import nltk, os
# from nltk import pos_tag
# from lib.porter2 import stem
import os
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
    # noun group 1 begins
    {
      'equivalent_nouns' : [string, ...], # group of equivalent nouns (currently determined by stems),
      'scores' : {
        'controversy' : float,
        'sentiment' : float,
      },
    },
    ...
  ]

  case 2) detailed is True
  [
    # noun group 1 begins
    {
      'equivalent_nouns' : [string, ...], # group of equivalent nouns (currently determined by stems),
      'scores' : {
        'controversy' : float,
        'sentiment' : float,
      },
      'descriptors' : {
        'pos_count' : int,
        'neg_count' : int,
        'pos_descriptors' : [
          {
            'descriptor' : string,
            'count' : int,
            'sentences' : [string, ...] # sentences
          },
          ...
        ],
        'neg_descriptors' : [
          ... # same as in pos
        ],
      },
    },
    ...
  ]

  """
  def getScoresFromRawText(self, rawText, detailed = False):
    preprocessedText = self.tp.preprocessedText(rawText)

    taggedSentences = self.tagger.getTaggedSentencesFromPreprocessedText(preprocessedText, True)

    simpleSentences = self.getSimpleSentencesFromTaggedSentences(taggedSentences)

    if not detailed:
      return self.getScoresFromSimpleSentencesNotDetailed(simpleSentences)
    else:
      return self.getScoresFromSimpleSentencesDetailed(simpleSentences)
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

  def getControversyScoreFromCountsWithCache(self, posCount, negCount, cache = {}):
    smallerCount = min(posCount, negCount)
    biggerCount = max(posCount, negCount)
    tup = (smallerCount, biggerCount)
    if tup in cache:
      return cache[tup]
    ret = self.getControversyScoreFromCounts(posCount, negCount)
    cache[tup] = ret
    return ret

  ##################
  # Helpers
  ##################

  """
  @param taggedSentences is the result of CleanTagger.getTaggedSentencesFromPreprocessedText() with detailed = True

  @returnVal:
  [
    # sentence 1 begins
    {
      'sentenceString' : string,
      'nouns' : [
        # noun 1 begins
        {
          'word' : string,
          'stem' : string,
        },
        ...
      ],
      'pos_descriptors' : [string, ...],
      'neg_descriptors' : [string, ...],
    },
    ...
  ]

  """
  def getSimpleSentencesFromTaggedSentences(self, taggedSentences):
    ret = []
    for taggedSentence in taggedSentences:
      entry = {
        'sentenceString' : '',
        'nouns' : [],
        'pos_descriptors' : [],
        'neg_descriptors' : [],
      }
      entry['sentenceString'] = taggedSentences['sentenceString']

      for wordData in taggedSentence['sentenceData']:
        # 1. get fields from data
        tag = wordData['tag']
        word = wordData['word']
        isAdjective = wordData['isAdjective']
        isNoun = wordData['isNoun']
        isStopWord = wordData['isStopWord']
        isPositive = wordData['isPositive']
        isNegative = wordData['isNegative']
        stem = wordData['stem']

        # 2. fill in the rest of the entry
        if isNoun:
          entry['nouns'].append({
            'word' : word,
            'stem' : stem,
          })
        elif isAdjective:
          if isPositive:
            entry['pos_descriptors'].append(word)
          elif isNegative:
            entry['neg_descriptors'].append(word)

      ret.append(entry)

    return ret

  """
  Helper for getScoresFromRawText
  """
  def getScoresFromSimpleSentencesNotDetailed(self, simpleSentences):

    stemToEntry = {}

    # 1. stemToEntry: get equivalent_nouns (in dict form) and counts
    for simpleSentence in simpleSentences:
      sentenceString = simpleSentence['sentenceString']
      nouns = simpleSentence['nouns'] # { 'word' : string, 'stem' : string }
      posDescriptors = simpleSentence['pos_descriptors']
      negDescriptors = simpleSentence['neg_descriptors']
      numPosDescriptors = len(posDescriptors)
      numNegDescriptors = len(negDescriptors)

      for noun in nouns:
        stem = noun['stem']
        word = noun['word']
        # 1. create an entry if it doesn't exist
        if stem not in stemToEntry:
          stemToEntry[stem] = {
            'equivalent_nouns' : {}, # word => True
            'scores' : {
              'controversy' : 0.0,
              'sentiment' : 0.0,
            },
            'counts' : {
              'pos' : 0,
              'neg' : 0,
            }
          }
        entry = stemToEntry[stem]
        # 2. update the entry
        if word not in entry['equivalent_nouns']:
          entry['equivalent_nouns'][word] = True
        entry['counts']['pos'] += numPosDescriptors
        entry['counts']['neg'] += numNegDescriptors

    # 2. stemToEntry: get scores
    controversyScoreCache = {}
    for stem in stemToEntry.keys():
      entry = stemToEntry[stem]
      posCount = entry['counts']['pos']
      negCount = entry['counts']['neg']
      entry['scores']['sentiment'] = posCount - negCount
      entry['scores']['controversy'] = self.getControversyScoreFromCountsWithCache(posCount, negCount, controversyScoreCache)

    # 3. change format & order
    ret = []

    for stem in stemToEntry.keys():
      entry = stemToEntry[stem]
      retEntry = {
        'equivalent_nouns' : sorted(entry['equivalent_nouns'].keys()),
        'scores' : entry['scores']
      }
      ret.append(retEntry)

    return ret

  """
  Helper for getScoresFromRawText
  """
  def getScoresFromSimpleSentencesDetailed(self, simpleSentences):

    stemToEntry = {}

    # 1. stemToEntry: get equivalent_nouns (in dict form) and counts
    for simpleSentence in simpleSentences:
      sentenceString = simpleSentence['sentenceString']
      nouns = simpleSentence['nouns'] # { 'word' : string, 'stem' : string }
      posDescriptors = simpleSentence['pos_descriptors']
      negDescriptors = simpleSentence['neg_descriptors']
      numPosDescriptors = len(posDescriptors)
      numNegDescriptors = len(negDescriptors)

      for noun in nouns:
        stem = noun['stem']
        word = noun['word']
        # 1. create an entry if it doesn't exist
        if stem not in stemToEntry:
          stemToEntry[stem] = {
            'equivalent_nouns' : {}, # word => True
            'scores' : {
              'controversy' : 0.0,
              'sentiment' : 0.0,
            },
            'counts' : {
              'pos' : 0,
              'neg' : 0,
            }
          }
        entry = stemToEntry[stem]
        # 2. update the entry
        if word not in entry['equivalent_nouns']:
          entry['equivalent_nouns'][word] = True
        entry['counts']['pos'] += numPosDescriptors
        entry['counts']['neg'] += numNegDescriptors

    # 2. stemToEntry: get scores
    controversyScoreCache = {}
    for stem in stemToEntry.keys():
      entry = stemToEntry[stem]
      posCount = entry['counts']['pos']
      negCount = entry['counts']['neg']
      entry['scores']['sentiment'] = posCount - negCount
      entry['scores']['controversy'] = self.getControversyScoreFromCountsWithCache(posCount, negCount, controversyScoreCache)

    # 3. change format & order
    ret = []

    for stem in stemToEntry.keys():
      entry = stemToEntry[stem]
      retEntry = {
        'equivalent_nouns' : sorted(entry['equivalent_nouns'].keys()),
        'scores' : entry['scores']
      }
      ret.append(retEntry)

    return ret
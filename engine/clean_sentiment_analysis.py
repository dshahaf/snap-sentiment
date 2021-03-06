#!/usr/bin/env python

"""
Useful methods of class CleanSentimentAnalysis:

def getMostControversialWordsFromTopic(self, topic, maxCount = 5)
def getMostControversialWordsFromRawText(self, rawText, maxCount = 5)
def getScoresFromTopic(self, topic, detailed = False)
def getScoresFromRawText(self, rawText, detailed = False)
"""

# import nltk, os
# from nltk import pos_tag
# from lib.porter2 import stem
import os
from math import log, sqrt
from clean_corpus import CleanCorpus
from clean_text_processor import CleanTextProcessor
from clean_tagger import CleanTagger
from clean_util import CleanUtil
from clean_console import CleanConsole

class CleanSentimentAnalysis:

  """
  ivars:

  tp = CleanTextProcessor()
  corpus = CleanCorpus()
  tagger = CleanTagger()
  util = CleanUtil()
  cc = CleanConsole()
  """

  ##############################################
  # Public Methods
  ##############################################

  def __init__(self):
    self.tp = CleanTextProcessor()
    self.corpus = CleanCorpus()
    self.tagger = CleanTagger()
    self.util = CleanUtil()
    self.cc = CleanConsole()
    return

  """
  See getScoresFromRawText() for the return value
  """
  def getScoresFromTopic(self, topic, detailed = False):
    rawDocsCombined = self.corpus.getRawDocuments(topic, combined = True)
    if not rawDocsCombined:
      self.cc.error('CleanSentimentAnalysis.getScoresFromTopic: Unsuppored topic %s. See CleanCorpus.getSupportedTopics' % topic)
      return []
    return self.getScoresFromRawText(rawDocsCombined, detailed)

  """
  See getMostControversialWordsFromRawText() for the return value
  """
  def getMostControversialWordsFromTopic(self, topic, maxCount = 5):
    rawDocsCombined = self.corpus.getRawDocuments(topic, combined = True)
    if not rawDocsCombined:
      # unsupported topic
      # see CleanCorpus.getSupportedTopics
      return []
    return self.getMostControversialWordsFromRawText(rawDocsCombined, maxCount)

  """
  @returnVal
  [
    # equivalent noun group 1 begins
    {
      'equivalent_nouns' : [],
      'controversy_score' : float,
    }
  ]

  """
  def getMostControversialWordsFromRawText(self, rawText, maxCount = 5):
    scoresNotDetailed = self.getScoresFromRawText(rawText)
    scoresNotDetailedTrimmed = self.util.getBeginningOfList(scoresNotDetailed, maxCount)
    ret = []
    for entry in scoresNotDetailedTrimmed:
      retEntry = {}
      retEntry['equivalent_nouns'] = entry['equivalent_nouns']
      retEntry['controversy_score'] = entry['scores']['controversy']
      ret.append(retEntry)
    return ret

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
        'sentiment' : float, # probably an int
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
    preprocessedText = self.tp.preprocessText(rawText)

    taggedSentences = self.tagger.getTaggedSentencesFromPreprocessedText(preprocessedText, True)

    simpleSentences = self.getSimpleSentencesFromTaggedSentences(taggedSentences)

    if not detailed:
      return self.getScoresFromSimpleSentencesNotDetailed(simpleSentences)
    else:
      return self.getScoresFromSimpleSentencesDetailed(simpleSentences)
    return

  ##############################################
  # Helpers
  ##############################################

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
      entry['sentenceString'] = taggedSentence['sentenceString']

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

      currNounStems = {}
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
        if stem not in currNounStems:
          entry['counts']['pos'] += numPosDescriptors
          entry['counts']['neg'] += numNegDescriptors
          currNounStems[stem] = True

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

    return sorted(ret, key = lambda elem : elem['scores']['controversy'], reverse = True)

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
      posDescriptorsCountDict = self.util.getCountDictFromList(posDescriptors)
      negDescriptorsCountDict = self.util.getCountDictFromList(negDescriptors)
      numPosDescriptors = len(posDescriptors)
      numNegDescriptors = len(negDescriptors)

      currNounStems = {}

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
            'descriptors' : {
              'pos_count' : 0,
              'neg_count' : 0,
              'pos_descriptors' : {
                # descriptor => { 'count' : 0, 'sentences' : [string, ... ] }
              },
              'neg_descriptors' : {
                # ...
              },
            }
          }
        entry = stemToEntry[stem]

        # 2. update the entry
        if word not in entry['equivalent_nouns']:
          entry['equivalent_nouns'][word] = True

        if stem not in currNounStems:
          currNounStems[stem] = True
          entry['descriptors']['pos_count'] += numPosDescriptors
          entry['descriptors']['neg_count'] += numNegDescriptors

          currPosDescriptorsDict = entry['descriptors']['pos_descriptors']
          for posDescriptor in posDescriptorsCountDict.keys():
            posDescriptorCount = posDescriptorsCountDict[posDescriptor]
            if posDescriptor not in currPosDescriptorsDict:
              currPosDescriptorsDict[posDescriptor] = {
                'count' : 0,
                'sentences' : [],
              }
            currPosDescriptorsDict[posDescriptor]['count'] += posDescriptorCount
            currPosDescriptorsDict[posDescriptor]['sentences'].append(sentenceString)

          currNegDescriptorsDict = entry['descriptors']['neg_descriptors']
          for negDescriptor in negDescriptorsCountDict.keys():
            negDescriptorCount = negDescriptorsCountDict[negDescriptor]
            if negDescriptor not in currNegDescriptorsDict:
              currNegDescriptorsDict[negDescriptor] = {
                'count' : 0,
                'sentences' : [],
              }
            currNegDescriptorsDict[negDescriptor]['count'] += negDescriptorCount
            currNegDescriptorsDict[negDescriptor]['sentences'].append(sentenceString)

      # end of for noun in nouns:

    # 2. stemToEntry: get scores
    controversyScoreCache = {}
    for stem in stemToEntry.keys():
      entry = stemToEntry[stem]
      posCount = entry['descriptors']['pos_count']
      negCount = entry['descriptors']['neg_count']
      entry['scores']['sentiment'] = posCount - negCount
      entry['scores']['controversy'] = self.getControversyScoreFromCountsWithCache(posCount, negCount, controversyScoreCache)

    # 3. change format & order
    ret = []

    for stem in stemToEntry.keys():
      entry = stemToEntry[stem]

      retEntry = {
        'equivalent_nouns' : sorted(entry['equivalent_nouns'].keys()),
        'scores' : entry['scores'],
        'descriptors' : {
          'pos_count' : entry['descriptors']['pos_count'],
          'neg_count' : entry['descriptors']['neg_count'],
          'pos_descriptors' : [],
          'neg_descriptors' : [],
        },
      }

      posDescriptorsSorted = sorted(entry['descriptors']['pos_descriptors'].keys())
      for posDescriptor in posDescriptorsSorted:
        retEntry['descriptors']['pos_descriptors'].append({
          'descriptor' : posDescriptor,
          'count' : entry['descriptors']['pos_descriptors'][posDescriptor]['count'],
          'sentences' : entry['descriptors']['pos_descriptors'][posDescriptor]['sentences'],
        })

      negDescriptorsSorted = sorted(entry['descriptors']['neg_descriptors'].keys())
      for negDescriptor in negDescriptorsSorted:
        retEntry['descriptors']['neg_descriptors'].append({
          'descriptor' : negDescriptor,
          'count' : entry['descriptors']['neg_descriptors'][negDescriptor]['count'],
          'sentences' : entry['descriptors']['neg_descriptors'][negDescriptor]['sentences'],
        })

      ret.append(retEntry)

    return sorted(ret, key = lambda elem : elem['scores']['controversy'], reverse = True)
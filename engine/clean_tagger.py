#!/usr/bin/env python

"""
Useful methods of class CleanTagger:

def isPositive(self, word)
def isNegative(self, word)
def isStopWord(self, word)
def isNounWordTag(self, word, tag)
def isAdjectiveWordTag(self, word, tag)
def tagPreprocessedText(self, preprocessedText, detailed = False)
def stem(self, word)
def stemWithCache(self, word, cache = {})
"""

import os
from lib.porter2 import stem as pstem
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk import pos_tag

class CleanTagger:

  """
  ivars:

  posWords = {} # { posWord : True }
  negWords = {} # { negWord : True }
  stopWords = {} # { stopWord : True } # light version
  """

  #########################
  # Public Methods
  #########################

  def __init__(self):
    # 1. create empty variables
    self.posWords = {}
    self.negWords = {}
    self.stopWords = {}

    # 2. fill variables with data
    data = [
      { 'variable' : self.posWords, 'path' : 'words/positive-words.txt' },
      { 'variable' : self.negWords, 'path' : 'words/negative-words.txt' },
      { 'variable' : self.stopWords, 'path' : 'words/stop-words-small.txt' },
    ]

    for entry in data:
      fullPath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        entry['path']
      )
      self.initDictHelper(entry['variable'], fullPath)
    return

  def isPositive(self, word):
    return word in self.posWords

  def isNegative(self, word):
    return word in self.negWords

  def isStopWord(self, word):
    return word in self.stopWords

  def isNounTag(self, tag):
    return tag[:2] == 'NN'

  def isAdjectiveTag(self, tag):
    return tag[:2] == 'JJ'

  def isNounWordTag(self, word, tag):
    return self.isNounTag(tag) and len(word) > 1

  def isAdjectiveWordTag(self, word, tag):
    return self.isAdjectiveTag(tag)

  def stem(self, word):
    return pstem(word)

  def stemWithCache(self, word, cache = {}):
    if word in cache:
      return cache[word]
    ret = self.stem(word)
    cache[word] = ret
    return ret

  """
  @param
  @return
    case 1) detailed = False
    [
      # sentence 1 begins
      [
        # word 1 begins
        { 'tag' : string, 'word' : string, },
        ...
      ]
      ,
      ...
    ],
    case 2) detailed = True
    [
      # sentence 1 begins
      [
        # word 1 begins
        {
          'tag' : string,
          'word' : string,
          'isAdjective' : boolean,
          'isNoun' : boolean,
          'isStopWord' : boolean,
          'isPositive' : boolean,
          'isNegative' : boolean,
          'stem' : string,
        },
        ...
      ]
      ,
      ...
    ]

  """
  def tagPreprocessedText(self, preprocessedText, detailed = False):
    ret = []
    sentences = sent_tokenize(preprocessedText)
    for sentence in sentences:
      sentenceData = []
      words = word_tokenize(sentence)
      taggedWords = pos_tag(words)
      for taggedWord in taggedWords:
        sentenceData.append({
          'word': taggedWord[0],
          'tag': taggedWord[1],
        })
      ret.append(sentenceData)

    if not detailed:
      print('detailed is False')
      return ret

    print('detailed is True')
    # details requested. add the following infos:
    #   isAdjective, isNoun, isStopWord, isPositive, isNegative, stem

    newRet = []

    stemCache = {}
    for sentence in ret:
      newSentence = []
      for wordData in sentence:
        word = wordData['word']
        tag = wordData['tag']
        newWordData = {
          'tag' : wordData['tag'],
          'word' : wordData['word'],
          'isAdjective' : self.isAdjectiveWordTag(word, tag),
          'isNoun' : self.isNounWordTag(word, tag),
          'isStopWord' : self.isStopWord(word),
          'isPositive' : self.isPositive(word),
          'isNegative' : self.isNegative(word),
          'stem' : self.stemWithCache(word, stemCache)
        }
        newSentence.append(newWordData)
      newRet.append(newSentence)

    return newRet

  #########################
  # Helpers
  #########################

  def initDictHelper(self, dictVar, path):
    if (not os.path.exists(path)) or os.path.isdir(path):
      # bad
      return

    # ret = {}
    with open(path, 'r') as f:
      for line in f:
        word = line.rstrip() # \n
        if word not in dictVar:
          dictVar[word] = True

    # dictVar = ret
    return
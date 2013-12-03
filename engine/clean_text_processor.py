#!/usr/bin/env python

"""
Useful methods of class CleanTextProcessor:
def preprocessText(self, text, doLowercase = True)
def stem(self, word)
def stemWithCache(self, word, cache = {})
def tagText(self, text, detailed = False) # call preprocessText before
"""

from lib.porter2 import stem as pstem
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from clean_tagger import CleanTagger
from nltk import pos_tag

class CleanTextProcessor:

  """
  tagger = CleanTagger()
  """

  ##################
  # Public Methods
  ##################

  def __init__(self):
    self.tagger = CleanTagger()
    return

  def preprocessText(self, text, doLowercase = True):
    ret = text
    if doLowercase:
      ret = ret.lower()
    return ret

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
    text is (preferrably) preprocessed before being passed
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
  def tagText(self, text, detailed = False):
    ret = []
    sentences = sent_tokenize(text)
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
      return ret

    # detailed => add the following infos:
    # isAdjective, isNoun, isStopWord, isPositive, isNegative, stem

    stemCache = {}
    for sentence in ret:
      for wordData in sentence:
        word = wordData['word']
        tag = wordData['tag']
        wordData = {
          'tag' : wordData['tag'],
          'word' : wordData['word'],
          'isAdjective' : self.tagger.isAdjectiveWordTag(word, tag),
          'isNoun' : self.tagger.isNounWordTag(word, tag),
          'isStopWord' : self.tagger.isStopWord(word),
          'isPositive' : self.tagger.isPositive(word),
          'isNegative' : self.tagger.isNegative(word),
          'stem' : self.stemWithCache(word, stemCache)
        }

    return ret

  ##################
  # Helpers
  ##################

#!/usr/bin/env python

"""
Useful methods of class CleanTagger:

def isPositive(self, word)
def isNegative(self, word)
def isStopWord(self, word)
def isNounWordTag(self, word, tag)
def isAdjectiveWordTag(self, word, tag)
"""

import os

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
    return word in posWords

  def isNegative(self, word):
    return word in negWords

  def isStopWord(self, word):
    return word in stopWords

  def isNounTag(self, tag):
    return tag[:2] == 'NN'

  def isAdjectiveTag(self, tag):
    return tag[:2] == 'JJ'

  def isNounWordTag(self, word, tag):
    return self.isNounTag(tag) and len(word) > 1

  def isAdjectiveWordTag(self, word, tag):
    return self.isAdjectiveTag(tag)

  #########################
  # Helpers
  #########################

  def initDictHelper(self, dictVar, path):
    if (not os.path.exists(path)) or os.path.isdir(path):
      # bad
      return

    ret = {}
    with open(path, 'r') as f:
      for line in f:
        word = line.rstrip() # \n
        if word not in ret:
          ret[word] = True

    dictVar = ret
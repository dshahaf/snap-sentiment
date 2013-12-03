#!/usr/bin/env python

class CleanCorpus:
  def __init__(self):
    return

  """
  @param
    topic is one of the following:
    ['movie', 'celebrity', 'syria', 'ufo']
  @return
    1) withSentiment is False
    [string, ...] # each entry is the content of the doc
    2) withSentiment is True
    [
      {
        'sentiment' : string, # 'pos' or 'neg'
        'value' : string, # document
      },
      ...
    ]
  """
  @staticmethod
  def getDocuments(topic, maxCount = 50, withSentiment = False):
    
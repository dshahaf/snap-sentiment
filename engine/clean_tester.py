#!/usr/bin/env python

"""
Useful methods of class CleanTester:

def run(self)
"""

"""
Command to run on python interpreter:

from engine.clean_tester import CleanTester; tester = CleanTester(); tester.run()
"""

import pprint
from clean_sentiment_analysis import CleanSentimentAnalysis
from clean_text_processor import CleanTextProcessor
from clean_corpus import CleanCorpus
from clean_tagger import CleanTagger
from clean_console import CleanConsole

class CleanTester:

  """
  ivars:

  tagger = CleanTagger()
  corpus = CleanCorpus()
  tp = CleanTextProcessor()
  sa = CleanSentimentAnalysis()
  cc = CleanConsole()
  """

  ##################
  # Public methods
  ##################

  def __init__(self):
    self.tagger = CleanTagger()
    self.corpus = CleanCorpus()
    self.tp = CleanTextProcessor()
    self.sa = CleanSentimentAnalysis()
    self.cc = CleanConsole()
    return

  def run(self):
    self.testCleanTextProcessor()
    self.testCorpus()
    return

  def testCorpus(self):
    self.cc.console('Testing CleanCorpus...')
    self.cc.console('TEST BEGINS')
    self.askForContinuation()
    topics = self.corpus.getSupportedTopics()
    maxCount = 2
    for topic in topics:
      self.cc.console("topic %s's sample documents:" % topic)
      docs = self.corpus.getRawDocuments(topic, maxCount)
      for doc in docs:
        self.cc.console('DOCUMENT BEGINS (topic:%s)' % topic)
        self.cc.printObject(doc)
        self.cc.console('DOCUMENT ENDS')
    self.cc.console('TEST ENDS')
    return

  def testCleanTextProcessor(self):
    self.cc.console('Testing CleanTextProcessor...')
    self.cc.console('TEST BEGINS')
    self.askForContinuation()
    rawText = 'Yesterday was terribly bad. Today is a good day.'
    preprocessedText = self.tp.preprocessText(rawText)
    detailedTagResult = self.tagger.tagPreprocessedText(preprocessedText, True)
    self.cc.console('processed text:'); self.cc.printObject(preprocessedText)
    self.cc.console('detailedTagResult'); self.cc.printObject(detailedTagResult)
    self.cc.console('TEST ENDS')
    return

  ##################
  # Helpers
  ##################
  def askForContinuation(self):
    ret = self.cc.askYesOrNo('Continue?')
    if not ret:
      exit()
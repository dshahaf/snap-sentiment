#!/usr/bin/env python

"""
Useful methods of class CleanTester:

def run(self)
"""

"""
Commands for copying and pasting:
from clean_tester import CleanTester; tester = CleanTester(); tester.run()
"""

import pprint
from clean_sentiment_analysis import CleanSentimentAnalysis
from clean_text_processor import CleanTextProcessor
from clean_corpus import CleanCorpus
from clean_tagger import CleanTagger
from clean_console import CleanConsole()

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

  ##################
  # Helpers
  ##################

  def testCorpus(self):
    
    return

  def testCleanTextProcessor(self):
    self.cc.console('Testing CleanTextProcessor...')
    text = 'I went to the school. It was pretty fun. I learned a lot.'
    processedText = self.tp.preprocessText(text)
    detailedTagResult = self.tp.tagText(processedText)
    self.cc.console('processed text:'); self.cc.printObject(processedText)
    self.cc.console('detailedTagResult'); self.cc.printObject(detailedTagResult)
    return
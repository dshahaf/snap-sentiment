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

class CleanTester:

  """
  tagger = CleanTagger()
  corpus = CleanCorpus()
  tp = CleanTextProcessor()
  sa = CleanSentimentAnalysis()
  pp = pprint.PrettyPrinter(indent = 4)
  """

  ##################
  # Public methods
  ##################

  def __init__(self):
    self.tagger = CleanTagger()
    self.corpus = CleanCorpus()
    self.tp = CleanTextProcessor()
    self.sa = CleanSentimentAnalysis()
    self.pp = pprint.PrettyPrinter(indent = 4)
    return

  def run(self):
    self.testCleanTextProcessor()
    return

  ##################
  # Helpers
  ##################

  def testCleanTextProcessor(self):
    self.console('Testing CleanTextProcessor...')
    text = 'I went to the school. It was pretty fun. I learned a lot.'
    processedText = self.tp.preprocessText(text)
    detailedTagResult = self.tp.tagText(processedText)
    self.console('processed text:'); self.printObject(processedText)
    self.console('detailedTagResult'); self.printObject(detailedTagResult)
    return

  def console(self, s):
    print("\n>> %s" % s)

  def printObject(self, obj):
    self.pp.pprint(obj)
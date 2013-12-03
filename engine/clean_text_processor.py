#!/usr/bin/env python

from lib.porter2 import stem as pstem

"""
Useful Methods:
def processText(self, text, doLowercase = True)
def stem(self, word)
"""

class CleanTextProcessor:
  def __init__(self):
    return

  def processText(self, text, doLowercase = True):
    ret = text
    if doLowercase:
      ret = ret.lower()
    return ret

  def stem(self, word):
    return pstem(word)


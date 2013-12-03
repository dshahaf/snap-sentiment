#!/usr/bin/env python

"""
Useful methods of class CleanTextProcessor:

def preprocessText(self, rawText, doLowercase = True)
"""

class CleanTextProcessor:

  """
  ivars:

  """

  ##################
  # Public Methods
  ##################

  def __init__(self):
    return

  def preprocessText(self, rawText, doLowercase = True):
    ret = rawText
    if doLowercase:
      ret = ret.lower()
    ret = ret.replace('<br />', '\n')
    return ret

  ##################
  # Helpers
  ##################

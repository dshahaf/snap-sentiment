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

  # TODO perhaps add asciiOnly?
  def preprocessText(self, rawText, doLowercase = True):
    ret = rawText
    if doLowercase:
      ret = ret.lower()
    return ret

  ##################
  # Helpers
  ##################

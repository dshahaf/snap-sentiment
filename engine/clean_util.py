#!/usr/bin/env python

"""
Useful methods of class CleanUtil:

def getCountDictFromList(self, l)
"""

class CleanUtil:

  def __init__(self):
    return

  def getCountDictFromList(self, l):
    ret = {}
    for elem in l:
      if elem not in ret:
        ret[elem] = 0
      ret[elem] += 1
    return ret

  def getBeginningOfList(self, l, maxCount):
    length = len(l)
    if length <= maxCount:
      return l
    else:
      return l[:maxCount]
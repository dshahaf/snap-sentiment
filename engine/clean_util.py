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
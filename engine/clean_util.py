#!/usr/bin/env python

from math import sqrt
from clean_console import CleanConsole

"""
Useful methods of class CleanUtil:

def getListFromDict(self, dict)
def getCountDictFromList(self, l)
def getBeginningOfList(self, l, maxCount)

def vectorDictMagnitude(self, vd)
def vectorDictDot(self, vd1, vd2)
def vectorDictNormalize(self, vd)

def vectorMagnitude(self, v)
def vectorDot(self, v1, v2)
def vectorNormalize(self, v)

"""

class CleanUtil:

  """
  ivars

  cc = CleanConsole()
  """

  def __init__(self):
    self.cc = CleanConsole()
    return

  def getListFromDict(self, dict):
    ret = []
    for k in sorted(dict.keys()):
      v = dict[k]
      ret.append(v)
    return ret

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

  def vectorDictMagnitude(self, vd):
    ret = 0
    for k in vd.keys():
      v = vd[k]
      ret += v * v
    return sqrt(ret)

  def vectorDictDot(self, vd1, vd2):
    ret = 0
    if len(vd1.keys()) != len(vd2.keys()):
      self.cc.error('CleanUtil.vectorDictDot: lengths do not match')
      return ret
    for k1 in vd1:
      if k1 not in vd2:
        self.cc.error('CleanUtil.vectorDictDot: key %s does not exist in vd2' % k1)
        return ret
      v1 = vd1[k1]
      v2 = vd2[k1]
      ret += v1 * v2
    return ret  

  def vectorDictNormalize(self, vd):
    mag = self.vectorDictMagnitude(vd)
    ret = {}
    for k in vd:
      v = vd[k]
      if mag > 0:
        ret[k] = v / mag
      else:
        ret[k] = v
    return ret

  def vectorMagnitude(self, v):
    ret = 0
    for elem in v:
      ret += elem * elem
    return sqrt(ret)

  def vectorDot(self, v1, v2):
    ret = 0
    if len(v1) != len(v2):
      self.cc.error('CleanUtil.vectorDot: lengths do not match')
      return ret
    l = len(v1)
    for i in range(l):
      ret += v1[i] * v2[i]
    return ret

  def vectorNormalize(self, v):
    ret = []
    l = len(v)
    mag = self.vectorMagnitude(v)
    for i in range(l):
      elem = v[i]
      if mag > 0:
        ret.append(elem / mag)
      else:
        ret.append(elem)
    return ret
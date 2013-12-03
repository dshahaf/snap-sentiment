#!/usr/bin/env python

"""
Useful methods of class CleanConsole:

def console(self, s)
def printObject(self, obj)
def isDirPath(self, path)
def getFilesFromDirectory(self, pathToDir)
"""

import os, pprint

class CleanConsole:

  """
  ivars:

  pp = pprint.PrettyPrinter(indent = 4)
  """

  def __init__(self):
    self.pp = pprint.PrettyPrinter(indent = 4)
    return

  def console(self, s):
    print("\n>> %s" % s)

  def printObject(self, obj):
    self.pp.pprint(obj)

  def isDirPath(self, path):
    return os.path.exists(path) and os.path.isdir(path)

  """
  @return list of documents immediately below pathToDir, [] if none found
  """
  def getFilesFromDirectory(self, pathToDir):
    if not self.isDirPath(pathToDir):
      return []
    ret = []
    filenames = os.listdir(pathToDir)
    for filename in filenames:
      path = os.path.join(pathToDir, filename)
      with open(path, 'r') as f:
        content = f.read()
        ret.append(content)
    return ret
#!/usr/bin/env python

"""
Useful methods of class CleanCorpus:

def getDocuments(self, topic, maxCount = 50)
"""

import os
from clean_console import CleanConsole

class CleanCorpus:

  """
  ivars:

  cc = CleanConsole()
  """

  #############################
  # Public Methods
  #############################

  def __init__(self):
    self.cc = CleanConsole()
    return

  """
  @param
    topic is one of the following:
    ['movie', 'celebrity', 'syria', 'ufo']
    The topic should match the name of the directory within engine/clean_data
  @return
    [
      {
        'sentiment' : string, # 'pos', 'neg', or 'any'
        'document' : string, # document content
      },
      ...
    ]
    3) error (can't find directory, etc)
    False
  @notes
    maxCount applies to each sentiment ('pos', 'neg', 'any'), not these combined

  """
  def getDocuments(self, topic, maxCount = 50):
    pathToDir = os.path.join(
      os.path.dirname(os.path.abspath(__file__)),
      'clean_data',
      topic
    )

    if not self.cc.isDirPath(pathToDir):
      # bad
      return False

    subdirs = ['pos', 'neg', 'any']
    data = [] # each entry is { 'subdir' : string, 'docs' : [] }
    for subdir in subdirs:
      data.append({
        'subdir' : subdir,
        'docs' : [],
      })

    for entry in data:
      entry['docs'] = self.cc.getFilesFromDirectory(
        os.path.join(pathToDir, entry['subdir'])
      )
      if len(entry['docs']) > maxCount:
        entry['docs'] = entry['docs'][:maxCount]

    ret = []
    for entry in data:
      for doc in entry['docs']:
        ret.append({
          'sentiment' : entry['subdir'],
          'document' : doc,
        })

    return ret

  #############################
  # Helpers
  #############################

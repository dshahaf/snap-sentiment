#!/usr/bin/env python

"""
Useful methods of class CleanCorpus:

def getRawDocuments(self, topic, maxCount = 50)
def getSupportedTopics(self)
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
    topic should be supported (see getSupportedTopics)
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
  def getRawDocuments(self, topic, maxCount = 50):
    if topic not in self.getSupportedTopics():
      # unsupported topic
      return False

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

  """
  @return list of topics that are supported
  Each supported topic should match the name of the directory within engine/clean_data
  """
  def getSupportedTopics(self):
    return ['movie', 'celebrity', 'syria', 'ufo']

  #############################
  # Helpers
  #############################

#!/usr/bin/env python

"""
Useful methods of class CleanCorpus:
def getDocuments(self, topic, maxCount = 50)
"""

import os

class CleanCorpus:

  #############################
  # Public Methods
  #############################

  def __init__(self):
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

    if not self.isDirPath(pathToDir):
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
      entry['docs'] = self.getFilesFromDirectory(
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

  """
  @return list of documents, [] if none found
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

  def isDirPath(self, path):
    return os.path.exists(path) and os.path.isdir(path)
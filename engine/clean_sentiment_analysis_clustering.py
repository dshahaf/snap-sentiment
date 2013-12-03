#!/usr/bin/env python

"""
Useful methods of class CleanSentimentAnalysisClustering:

def getClusterResultsFromTopic(self, topic, detailed = False)
"""

from clean_sentiment_analysis import CleanSentimentAnalysis

class CleanSentimentAnalysisClustering(CleanSentimentAnalysis):

  ##########################################
  # Public Methods
  ##########################################

  """
  @returnVal
  1) detailed is False
  [
    # cluster 1 begins
    [
      # cluster 1's document 1 begins
      {
        'head' : string, # first 3 sentences
      },
      ...
    ]
    ,
    # cluster 2 begins
    [
      ...
    ],
  ]
  2) detailed is True
  TODO

  """
  def getClusterResultsFromTopic(self, topic, detailed = False):
    controversialWordStems = self.getControversialWordStemsFromTopic(topic)
    if not detailed:
      return self.getClusterResultsFromTopicNotDetailed(topic, controversialWordStems)
    else:
      return self.getClusterResultsFromTopicDetailed(topic, controversialWordStems)

  ##########################################
  # Helpers
  ##########################################

  def getClusterResultsFromTopicNotDetailed(self, topic, controversialWordStems):
    rawDocuments = self.corpus.getRawDocuments(topic)
    vectors = []
    heads = []

    for rawDocument in rawDocuments:
      countVectorDict = self.getCountVectorDictFromRawDocument(rawDocument, controversialWordStems)
      countVector = self.util.getListFromDict(countVectorDict)
      normalizedVector = self.util.vectorNormalize(countVector)
      head = self.getHeadFromRawDocument(rawDocument)
      vectors.append(normalizedVector)
      heads.append(head)

    self.util.doKmeans(vectors)

    # TODO
    return []

  # TODO
  def getClusterResultsFromTopicDetailed(self, topic, controversialWordStems):
    return []

  def getControversialWordStemsFromTopic(self, topic):
    controversialWordsList = self.getMostControversialWordsFromTopic(topic) # this has scores too
    equivalentNounsList = [elem['equivalent_nouns'] for elem in controversialWordsList]
    ret = []
    for equivalentNouns in equivalentNounsList:
      if len(equivalentNouns) > 0:
        stem = self.tagger.stem(equivalentNouns[0])
        ret.append(stem)
    return ret

  def getCountVectorDictFromRawDocument(self, rawDocument, controversialWordStems):
    ret = {}
    for controversialWordStem in controversialWordStems:
      ret[controversialWordStem] = 0
    scores = self.getScoresFromRawText(rawDocument)
    for entry in scores:
      equivalentNouns = entry['equivalent_nouns']
      if len(equivalentNouns) > 0:
        currStem = self.tagger.stem(equivalentNouns[0])
        if currStem in ret:
          currScore = entry['scores']['sentiment']
          ret[currStem] = currScore
    return ret

  def getHeadFromRawDocument(self, rawDocument):
    preprocessedDocument = self.tp.preprocessText(rawDocument)
    sentences = self.tagger.getSentencesFromPreprocessedText(preprocessedDocument)
    head = ' '.join(sentences[:3])
    return head
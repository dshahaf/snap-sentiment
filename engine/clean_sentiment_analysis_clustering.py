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
  {
    'stems' : [],
    'center1' : [],
    'center2' : [],
    'cluster1_num_pos' : int,
    'cluster1_num_neg' : int,
    'cluster2_num_pos' : int,
    'cluster2_num_neg' : int,

    'cluster1' : [
      {
        'head' : string, # first 3 sentences
        'sentiment' : string, # 'pos' or 'neg',
        'vector' : [],
      },
      ...
    ],
    'cluster2' : [
      ...
    ]
  }

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

  # TODO
  def getClusterResultsFromTopicDetailed(self, topic, controversialWordStems):
    return []

  def getClusterResultsFromTopicNotDetailed(self, topic, controversialWordStems):
    rawDocuments = self.corpus.getRawDocuments(topic)

    vectors = []
    heads = []
    sentiments = []

    for rawDocumentWrapper in rawDocuments:
      rawDocument = rawDocumentWrapper['document']

      countVectorDict = self.getCountVectorDictFromRawDocument(rawDocument, controversialWordStems)
      countVector = [countVectorDict[stem] for stem in controversialWordStems]

      normalizedVector = self.util.vectorNormalize(countVector)
      head = self.getHeadFromRawDocument(rawDocument)
      sentiment = rawDocumentWrapper['sentiment']

      vectors.append(normalizedVector)
      heads.append(head)
      sentiments.append(sentiment)

    l = len(vectors)

    if False:
      # debugging
      self.cc.console('stems:')
      self.cc.printObject(controversialWordStems)

      for i in range(l):
        self.cc.console('sentiment:')
        self.cc.printObject(sentiments[i])
        self.cc.console('head:')
        self.cc.printObject(heads[i])
        self.cc.console('vector:')
        self.cc.printObject(vectors[i])

    res = self.util.doKmeans2(vectors)
    center1 = res[0][0]
    center2 = res[0][1]
    distortion = res[1]

    cluster1Indexes = []
    cluster2Indexes = []

    for i in range(l):
      vector = vectors[i]
      distToCenter1 = self.util.vectorDist(vector, center1)
      distToCenter2 = self.util.vectorDist(vector, center2)
      if distToCenter1 < distToCenter2:
        cluster1Indexes.append(i)
      else:
        cluster2Indexes.append(i)

    ret = {
      'stems' : controversialWordStems,
      'center1' : center1,
      'center2' : center2,
      'cluster1' : [],
      'cluster2' : [],
      'cluster1_num_pos' : 0,
      'cluster1_num_neg' : 0,
      'cluster2_num_pos' : 0,
      'cluster2_num_neg' : 0,
    }

    for index in cluster1Indexes:
      entry = {
        'head' : heads[index],
        'sentiment' : sentiments[index],
        'vector' : vectors[index],
      }
      ret['cluster1'].append(entry)
      if sentiments[index] == 'pos':
        ret['cluster1_num_pos'] += 1
      elif sentiments[index] == 'neg':
        ret['cluster1_num_neg'] += 1

    for index in cluster2Indexes:
      entry = {
        'head' : heads[index],
        'sentiment' : sentiments[index],
        'vector' : vectors[index],
      }
      ret['cluster2'].append(entry)
      if sentiments[index] == 'pos':
        ret['cluster2_num_pos'] += 1
      elif sentiments[index] == 'neg':
        ret['cluster2_num_neg'] += 1

    return ret

  """
  @returnVal
  list of controversial word stems
  """
  def getControversialWordStemsFromTopic(self, topic):
    controversialWordsList = self.getMostControversialWordsFromTopic(topic) # this has scores too
    equivalentNounsList = [elem['equivalent_nouns'] for elem in controversialWordsList]
    ret = []
    for equivalentNouns in equivalentNounsList:
      if len(equivalentNouns) > 0: # just in case
        stem = self.tagger.stem(equivalentNouns[0])
        ret.append(stem)
    return ret

  """
  @returnVal
  {
    stem => sentimentScore,
    ...
  }
  """
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
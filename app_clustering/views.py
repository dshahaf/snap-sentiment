"""
Clustering
"""
from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms
from engine.sentiment_analysis import SentimentAnalysis
from engine.corpus import Corpus
from engine.clean_sentiment_analysis_clustering import CleanSentimentAnalysisClustering

"""

"""
def index(request):
  context = {}

  if request.method == 'POST':
    form = request.POST
    action = form.get('action')
    context['action'] = action
    actionTokens = action.split('-')

    if actionTokens[0] == 'clustering': # sanity check
      # one of ['movie', 'celebrity', 'ufo', 'syria']
      topic = actionTokens[1]

      sa = CleanSentimentAnalysisClustering()
      result = sa.cluster(topic)
      print "result: %s" % result
      context['result'] = result
    else:
      print 'sanity check failed'

  return render(request, 'clustering.html', context)

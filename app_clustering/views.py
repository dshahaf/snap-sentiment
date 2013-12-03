"""
Clustering
"""
from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms
from engine.sentiment_analysis import SentimentAnalysis
from engine.corpus import Corpus

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
      print 'sanity check passed'
      topic = actionTokens[1]

      sa = SentimentAnalysis()
      result = sa.cluster(topic)
      context['result'] = result
    else:
      print 'sanity check failed'

  return render(request, 'clustering.html', context)

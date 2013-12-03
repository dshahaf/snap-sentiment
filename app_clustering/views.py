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
    pass
    form = request.POST
    action = form.get('action')
    context['action'] = action

    if action[:3] == 'lda':
      words = action.split('-')
      topic = words[1]
      numTopics = (int)(words[2])
      sa = SentimentAnalysis()
      ldaTopics = sa.ldaTopics(topic, numTopics)
      context['result'] = {}
      context['result']['topics'] = ldaTopics

  return render(request, 'clustering.html', context)

# Create your views here.
from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms
from engine.sentiment_analysis import SentimentAnalysis
from engine.corpus import Corpus

"""
See sentiment_analysis.py for the content of context.
{
	'text' : string,
	'action': string,
	'result' :  {
		'sentences': [
			...
		],
		'words': [
			...
		]
	}
}
"""
def index(request):
	context = {}
	if request.method == 'POST':
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

	return render(request, 'lda.html', context)

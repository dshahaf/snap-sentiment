# Create your views here.
from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms
from engine.sentiment_analysis import SentimentAnalysis
import nltk

"""
{
	'text' : ""
	'result' : {
		'words': []
	}
}
"""
def index(request):
	context = {}
	if request.method == 'POST':
		form = request.POST
		value = form.get('textarea')
		context['text'] = value
		sa = SentimentAnalysis(value)
		context['result'] = sa.nounAnalysis()
	return render(request, 'noun.html', context)

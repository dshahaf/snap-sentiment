# Create your views here.
from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms
from engine.text_processor import TextProcessor
from engine.sentiment_analysis import SentimentAnalysis

def index(request):
	context = {}
	if request.method == 'POST':
		form = request.POST		
		value = form.get('textarea')
		context['text'] = value
		sa = SentimentAnalysis(value)
		context['result'] = sa.simpleAnalysis()

	return render(request, 'simple.html', context)
# Create your views here.
from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms
from engine.sentiment_analysis import SentimentAnalysis

def index(request):
	context = {}

	if request.method == 'POST':
		form = request.POST
		action = form.get('action')
		context['action'] = action

		if action == 'user-input':
			value = form.get('textarea')
			context['text'] = value
			context['result'] = value

	return render(request, 'sentence.html', context)
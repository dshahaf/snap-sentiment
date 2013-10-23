# Create your views here.
from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms
from engine.text_processor import TextProcessor
from engine.sentiment_analysis import SentimentAnalysis
from engine.corpus import Corpus

def index(request):
	context = {}
	if request.method == 'POST':
		form = request.POST
		sampleData = form.get('sample-data')

		if sampleData is None:
			# not using sample data
			value = form.get('textarea')
			context['text'] = value
			sa = SentimentAnalysis(value)
			context['result'] = sa.simpleAnalysis()

		else:
			# using sample data
			category = ''
			if sampleData == 'positive-movie-review':
				category = 'positive'
				context['sample_data'] = 'positive-movie-review'
			elif sampleData == 'negative-movie-review':
				category = 'negative'
				context['sample_data'] = 'negative-movie-review'
			corpus = Corpus()
			text = corpus.getRandomMovieReview(category)
			context['text'] = text
			sa = SentimentAnalysis(text)
			context['result'] = sa.simpleAnalysis()

	return render(request, 'simple.html', context)
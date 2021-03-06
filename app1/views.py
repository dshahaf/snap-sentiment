"""
Simple Analysis
"""

from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms
from engine.sentiment_analysis import SentimentAnalysis
from engine.corpus import Corpus
from engine.tester import Tester

def index(request):
	context = {}

	if request.method == 'POST':
		form = request.POST
		action = form.get('action')
		context['action'] = action
		if action == 'user-input':
			value = form.get('textarea')
			context['text'] = value
			sa = SentimentAnalysis(value)
			context['result_single'] = sa.simpleAnalysis()

		elif action[:6] == 'sample':
			words = action.split('-')
			category = words[1]
			dataset = words[2]

			corpus = Corpus()
			text = ''

			if dataset == 'movie':
				text = corpus.getRandomMovieReview(category)
			elif dataset == 'celebrity':
				text = corpus.celebrityArticle(category)

			context['text'] = text
			sa = SentimentAnalysis(text)
			context['result_single'] = sa.simpleAnalysis()

		elif action[:4] == 'test':
			words = action.split('-')
			dataset = words[1]
			if dataset == 'movie':
				tester = Tester()
				count = 200
				context['result_test'] = tester.test('simple', 'movie', count)
			elif dataset == 'celebrity':
				tester = Tester()
				context['result_test'] = tester.test('simple', 'celebrity', None)

	return render(request, 'simple.html', context)
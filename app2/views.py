# Create your views here.
from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms
from engine.sentiment_analysis import SentimentAnalysis
from engine.corpus import Corpus

"""
{
	'text' : string,
	'result' :  {
		'sentences': [
			{
				'sentiment': string,
				'words': [
					{
						'value': string,
						'type': string,
						'sentiment': string,
						'isNoun': string, # 'true' or 'false'
					}
				],
				...
			},
			...
		],

		'words': [
			{
				'value': string,
				'sentiment': string,
				'score': int,
				'positive_neighbors': [
					{
						'value': string,
						'count': int,
					},
					...
				]
				'negative_neighbors': [
					{
						'value': string,
						'count': int,
					},
					...
				]
			},
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

		if action == 'user-input':
			value = form.get('textarea')
			context['text'] = value
			sa = SentimentAnalysis(value)
			context['result'] = sa.nounAnalysis()

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
			context['result'] = sa.nounAnalysis()

	return render(request, 'noun.html', context)

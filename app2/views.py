# Create your views here.
from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms
from engine.sentiment_analysis import SentimentAnalysis

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
		value = form.get('textarea')
		context['text'] = value
		sa = SentimentAnalysis(value)
		context['result'] = sa.nounAnalysis()
	return render(request, 'noun.html', context)

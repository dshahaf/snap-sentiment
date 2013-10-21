# Create your views here.
from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms

"""
result = {
	'words': [
		{'value' : 'love', 'sentiment' : 'positive'},
		{'value' : 'is', 'sentiment' : 'neither'},
		{'value' : 'bad', 'sentiment' : 'negative'},
		{'value' : 'love', 'sentiment' : 'positive'},
		{'value' : 'is', 'sentiment' : 'neither'},
		{'value' : 'good', 'sentiment' : 'positive'},
	],
	'overall_sentiment' : 'positive',
	'sentimental_words': {
		'positive': [
			{
				'value' : 'love',
				'count' : 2
			},
			{
				'value' : 'good',
				'count' : 1
			},
				
		],
		'negative': [
			{
				'value' : 'bad',
				'count' : 1
			},	
		],				
		'count': {
			'positive' : 3,
			'negative' : 1,
		}
	},
}
"""

def index(request):
	context = {}
	if request.method == 'POST':
		form = request.POST
		value = form.get('textarea')
		result = {}
		context = {'text': value, 'result': result}
	return render(request, 'word.html', context)

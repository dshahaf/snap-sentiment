# Create your views here.
from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms
from engine.text_processor import TextProcessor

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
		removeStop = (form.get('checkbox-remove-stop-words') is not None)
		result = {}
		tp = TextProcessor(value)
		tp.process(lower = True, alphabetsOnly = True, removeStop = removeStop)
		result['test'] = tp.get()
		context = {'text': value, 'result': result, 'setup': {}}
		if removeStop:
			context['setup']['remove_stop_words_value'] = 'checked'
	return render(request, 'word.html', context)

# Create your views here.
from django.shortcuts import render
from django.template import RequestContext, loader
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
		context['result'] = {}
		context['result']['words'] = nltk.word_tokenize(value)
	return render(request, 'noun.html', context)

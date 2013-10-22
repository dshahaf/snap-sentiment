# Create your views here.
from django.shortcuts import render
from django.template import RequestContext, loader

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
		context['result']['words'] = value.split()
	return render(request, 'noun.html', context)

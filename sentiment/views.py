# Create your views here.
from django.shortcuts import render
from django.template import RequestContext, loader

def index(request):
	template = loader.get_template('sentiment/index.html')
	context = {}
	return render(request, 'sentiment/index.html', context)
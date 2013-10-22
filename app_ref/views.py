# Create your views here.
from django.shortcuts import render
from django.template import RequestContext, loader

def index(request):
	context = {}
	return render(request, 'ref.html', context)

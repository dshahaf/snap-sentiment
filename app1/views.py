# Create your views here.
from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms

def index(request):
	context = {}
	if request.method == 'POST':
		form = request.POST
		value = form.get('textarea')
		context = {'orig': value, 'result': 'hahaha'}
	return render(request, 'word.html', context)

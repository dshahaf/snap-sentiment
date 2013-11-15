Sentiment Analysis (SNAP)
===

Links
---
###Most Useful
- <a href="http://127.0.0.1:8000/" target="_blank">Local Application</a>
- <a href="http://snap-sentiment.herokuapp.com/" target="_blank">Deployed Application</a>
- <a href="https://www.heroku.com" target="_blank">Heroku Main Page</a>
- <a href="http://getbootstrap.com/2.3.2/" target="_blank">Twitter Bootstrap 2</a>
- <a href="https://github.com/namejames91/snap-sentiment/wiki/TODO" target="_blank">TODO</a>
- <a href="http://nltk.org/" target="_blank">NLTK documentation</a>

###Sentiment Analysis
- <a href="http://andybromberg.com/sentiment-analysis-python/?goback=%2Egde_115439_member_223217943#%21" target="_blank">Andy Bromberg</a>
- <a href="http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/" target="_blank">Laurent Luce</a>
- <a href="http://www.sjwhitworth.com/sentiment-analysis-in-python-using-nltk/" target="_blank">Stephen Whitworth</a>
- <a href="http://radimrehurek.com/gensim/" target="_blank">Gensim Documentation</a>


###Django Documentation
- <a href="https://devcenter.heroku.com/articles/getting-started-with-django" target="_blank">Heroku - Getting Started with Django</a>
- <a href="https://docs.djangoproject.com/en/1.5/contents/" target="_blank">Long Index</a>
- <a href="https://docs.djangoproject.com/en/1.5/" target="_blank">Everything you need to know about Django</a>
- <a href="https://docs.djangoproject.com/en/1.5/intro/" target="_blank">Getting Started</a>
- <a href="https://docs.djangoproject.com/en/1.5/topics/" target="_blank">Using Django</a>
- <a href="https://devcenter.heroku.com/categories/python" target="_blank">Herok - Python</a>

###Related Repositories
- <a href="https://github.com/snap-stanford/MetroMaps" target="_blank">SNAP - MetroMaps</a>
- <a href="https://github.com/namejames91/django" target="_blank">Django Practice</a>
- <a href="https://github.com/dyve/django-bootstrap-toolkit" target="_blank">Django Bootstrap Toolkit</a>

Commands
---

Activating virtualenv
	
	source venv/bin/activate

Generating Gensim dictionaries and corpuses

	python
	from engine.corpus import Corpus
	c = Corpus()
	c.saveGensim('movie')
	c.saveGensim('celebrity')
	c.saveGensim('syria')
	c.saveGensim('ufo')

Getting the LDA from a dictionary and corpus (example topic: ufo)

	python
	import logging, gensim, bz2
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	id2word = gensim.corpora.Dictionary.load('engine/james_data/ufo/gensim_dictionary.txt')
	mm = gensim.corpora.MmCorpus('engine/james_data/ufo/gensim_corpus.mm')
	lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=10, update_every=1, chunksize=10000, passes=1)
	lda.print_topics(20)

Running Django server

	python manage.py runserver

Creating Django project

	python manage.py startproject <project-name>

Creating Django app (run in the same directory as manage.py)

	python manage.py startapp <app-name>

Collect static files

	python manage.py collectstatic

Syncing DB

	python manage.py syncdb

Shell

	python manage.py shell

Compile Less

	npm install -g less

Archive
---
###Django advice
- If you plan to use a database, edit the DATABASES setting in sentiment/settings.py.
- Start your first app by running python manage.py startapp [appname].
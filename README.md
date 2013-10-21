Sentiment Analysis (SNAP)
===
TODO
---
- positive, negative words ratio
- sentiment analysis
- new approach

Links
---
###Most Useful
- <a href="http://127.0.0.1:8000/" target="_blank">Local Application</a>
- <a href="http://snap-sentiment.herokuapp.com/" target="_blank">Deployed Application</a>
- <a href="https://www.heroku.com" target="_blank">Heroku Main Page</a>

###Django Documentation
- <a href="https://devcenter.heroku.com/articles/getting-started-with-django" target="_blank">Heroku - Getting Started with Django</a>
- <a href="https://docs.djangoproject.com/en/1.5/contents/" target="_blank">Long Index</a>
- <a href="https://docs.djangoproject.com/en/1.5/" target="_blank">Everything you need to know about Django</a>
- <a href="https://docs.djangoproject.com/en/1.5/intro/" target="_blank">Getting Started</a>
- <a href="https://docs.djangoproject.com/en/1.5/topics/" target="_blank">Using Django</a>

###Related Repositories
- <a href="https://github.com/namejames91/django" target="_blank">SNAP - MetroMaps</a>
- <a href="https://github.com/namejames91/django" target="_blank">Django Practice</a>

Commands
---

Activating virtualenv
	
	source venv/bin/activate

Running Django server

	python manage.py runserver

Creating Django project

	python manage.py startproject <project-name>

Creating Django app (run in the same directory as manage.py)

	python manage.py startapp <app-name>

Syncing DB

	python manage.py syncdb

Shell

	python manage.py shell

Archive
---
###Django advice
- If you plan to use a database, edit the DATABASES setting in sentiment/settings.py.
- Start your first app by running python manage.py startapp [appname].
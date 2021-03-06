from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'sentiment.views.home', name='home'),
	# url(r'^sentiment/', include('sentiment.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	# url(r'^admin/', include(admin.site.urls)),

	url(r'^$', 'sentiment.views.index', name='index'),
	url(r'^simple/', include('app1.urls')),
	url(r'^noun/', include('app2.urls')),
	url(r'^lda/', include('app_lda.urls')),
	url(r'^clustering/', include('app_clustering.urls')),
)
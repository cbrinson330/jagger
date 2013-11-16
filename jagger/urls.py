from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
	url(r'^$', 'jagger.views.home', name='home'),
	url('^create', 'jagger.views.create', name='create'),
	url('^entry', 'jagger.views.entry', name='entry'),
	url('^api/interest/create/$', 'jagger.views.APIInterestCreate' , name='APIInterestCreate'),
	url('^api/interest/delete/$', 'jagger.views.APIInterestDelete' , name='APIInterestDelete'),
	url('^api/interest/update/$', 'jagger.views.APIInterestUpdate' , name='APIInterestUpdate'),
	url('^api/interest/getValues/', 'jagger.views.APIInterestGetValues' , name='APIInterestGetValues'),


    # url(r'^jagger/', include('jagger.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)

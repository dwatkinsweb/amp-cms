from django.conf.urls.defaults import patterns, url

from ampcms.lib.application_mapper import application_mapper
application_mapper.autodiscover()

urlpatterns = patterns('ampcms.views',
    url(r'^login/?$',
        view='login', name='login'),
    url(r'^logout/?$',
        view='logout', name='logout'),
    url(r'^page/(?P<module>[a-zA-Z0-9]+)/(?P<page>[a-zA-Z0-9]+)/?$', 
        view='page', name='page'),
    url(r'^pagelet/(?P<module>[a-zA-Z0-9]+)/(?P<page>[a-zA-Z0-9]+)/(?P<pagelet>[a-zA-Z0-9]+)/?(?P<url>[a-zA-Z0-9\/\-_]+)?', 
        view='pagelet', name='pagelet'),
    url(r'^css/(?P<module>[a-zA-Z0-9]+)/(?P<page>[a-zA-Z0-9]+)/?$', 
        view='css', name='css'),
    url(r'^(?P<module>[a-zA-Z0-9]+)/?(?P<page>[a-zA-Z0-9]+)?/?$', 
        view='full_page', name='full_page'),
    url(r'^$', 
        view='index', name='index')
)
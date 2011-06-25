from django.conf.urls.defaults import *
from cassad import views

urlpatterns = patterns('cassad',
    (r'^$', views.index, { 'template_name': 'cassad_index.html', }),
    (r'^search/(?P<last>.*)$', views.search, {}),
    (r'^addtags/?$', views.addtags, {}),
    (r'^tags/$', views.tags, { 'template_name': 'cassad_tags.html' }),
    (r'^tags/(?P<tag>.+)/(?P<last>.*)$', views.showtags, { 'template_name': 'cassad_index.html', }),
)

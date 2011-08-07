from django.conf.urls.defaults import *
from cassad import views

urlpatterns = patterns('cassad',
    (r'^not-tagged/?$', views.tagmeview,
        { 'template_name': 'cassad_index.html', 'callback': 'show/' }),
    (r'^not-tagged/show/(?P<last>.*)$', views.tagme, {}),
    (r'^addtags/?$', views.addtags, {}),
    (r'^tags/$', views.tags, { 'template_name': 'cassad_tags.html' }),
    (r'^tags/(?P<tag>[^\/]+)/$', views.showtagview,
        { 'template_name': 'cassad_index.html', 'callback': 'show/' }),
    (r'^tags/(?P<tag>[^\/]+)/show/(?P<last>.*)$', views.showtag, {}),
    (r'^delete/?$', views.delete, {}),
    (r'^image/(?P<id>.*)/$', views.image, {})
)

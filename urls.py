from django.conf.urls.defaults import *
from cassad import views

urlpatterns = patterns('cassad',
    (r'^$', views.index, { 'template_name': 'cassad_index.html', }),
)

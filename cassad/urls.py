from django.conf.urls.defaults import *
from cassad import views
import settings

urlpatterns = patterns('',
    (r'^not-tagged/?$', views.tagmeview,
        { 'template_name': 'cassad_index.html', 'callback': 'show/' }),
    (r'^not-tagged/show/(?P<last>.*)$', views.tagme, {}),
    (r'^all/?$', views.tagmeview, { 'template_name': 'cassad_index.html',
        'callback': 'show/' }),
    (r'^all/show/(?P<last>.*)$', views.whole, {}),
    (r'^addtags/?$', views.addtags, {}),
    (r'^tags/$', views.tags, { 'template_name': 'cassad_tags.html' }),
    (r'^tags/(?P<tag>[^\/]+)/$', views.showtagview,
        { 'template_name': 'cassad_index.html', 'callback': 'show/' }),
    (r'^tags/(?P<tag>[^\/]+)/show/(?P<last>.*)$', views.showtag, {}),
    (r'^delete/?$', views.delete, {}),
    (r'^image/(?P<id>.*)/$', views.showimage, { 'template_name': 'cassad_wp.html' }, 'image-display'),
    (r'^image-content/(?P<id>.*)/$', views.image, {}, 'image-content'),
    url(r"^thumbnails/(?P<path>.*)$", "django.views.static.serve", { "document_root":settings.THUMBNAIL_DIR }),
)

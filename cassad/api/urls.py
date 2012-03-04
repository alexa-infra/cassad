from django.conf.urls.defaults import *
from piston.resource import Resource
from cassad.api.handlers import PictureNotTagged, PictureTagged, PictureNotDeleted

not_tagged = Resource(PictureNotTagged)
tagged = Resource(PictureTagged)
not_deleted = Resource(PictureNotDeleted)

urlpatterns = patterns('',
    url(r'^not_tagged/$', not_tagged),
    url(r'^tag/(?P<tag>[^/]+)/', tagged),
    url(r'^not_deleted/$', not_deleted),
)

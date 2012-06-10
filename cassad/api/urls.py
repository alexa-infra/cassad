from django.conf.urls.defaults import *
from piston.resource import Resource
from cassad.api.handlers import PictureNotTagged, PictureTagged, PictureNotDeleted, TagsBulk

not_tagged = Resource(PictureNotTagged)
tagged = Resource(PictureTagged)
not_deleted = Resource(PictureNotDeleted)
tags_bulk = Resource(TagsBulk)

urlpatterns = patterns('',
    url(r'^not-tagged/$', not_tagged),
    url(r'^tags/(?P<tag>[^/]+)/', tagged),
    url(r'^not-deleted/$', not_deleted),
    url(r'^tags-bulk/$', tags_bulk),
)

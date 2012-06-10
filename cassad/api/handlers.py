from piston.handler import BaseHandler
from cassad.entries import Picture
from serializer import SerializedObject
from piston.utils import rc
from mongoengine import *
from django.utils import simplejson
from bson.objectid import ObjectId


class PictureNotTagged(BaseHandler):
    allowed_methods = ('GET',)
    fields = ('id', 'tags', 'creation', 'width', 'height', 'size', 'thumbnail')

    def read(self, request):
        from_value = request.GET.get('from', None)
        show_number = request.GET.get('num', 30)
        res_list = Picture.ranged(Q(tags__size=0) | Q(tags__exists=False), from_value, show_number, "-creation")
        return SerializedObject(res_list, fields=self.fields).to_python()


class PictureNotDeleted(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        from_value = request.GET.get('from', None)
        show_number = request.GET.get('num', 30)
        res_list = Picture.ranged(Q(tags__nin=["deleted"]), from_value, show_number, "-creation")
        return SerializedObject(res_list).to_python()


class PictureTagged(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, tag):
        from_value = request.GET.get('from', None)
        show_number = request.GET.get('num', 30)
        if tag == 'deleted':
            res_list = Picture.ranged(Q(tags__in=[tag]), from_value, show_number, "-creation")
        else:
            res_list = Picture.ranged(Q(tags__in=[tag]) & Q(tags__nin=["deleted"]), from_value, show_number, "-creation")
        return SerializedObject(res_list).to_python()


class TagsBulk(BaseHandler):
    allowed_methods = ('POST')

    def create(self, request):
        data = simplejson.load(request)
        selected = data["selected"]
        tags = data["tags"]
        if not selected:
            return rc.NOT_FOUND
        objs = [ObjectId(x) for x in selected]
        entry_list = Picture.objects(id__in=objs)

        for p in entry_list:
            p.tags = tags
            p.save()
        return rc.ALL_OK

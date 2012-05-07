from piston.handler import BaseHandler
from cassad.entries import Picture
from serializer import SerializedObject
from piston.utils import rc
from mongoengine import *

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


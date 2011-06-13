from mongoengine import *
from datetime import datetime
import os

class Picture(Document):
    path = StringField(required=True) # path to picture
    hashcode = StringField()  # hash (SHA1) of file
    tags = ListField(StringField())
    thumbnail = StringField()
    width = IntField(min_value=0)   # width of picture
    height = IntField(min_value=0)  # height of picture
    size = IntField(min_value=0)    # filesize in bytes
    creation = DateTimeField(default=datetime.now) # time of file creation

    meta = {
        'indexes': ['creation', 'tags'],
    }

    def __unicode__(self):
        return u"%s the picture" % self.path

    def ThumbnailName(self):
        if not self.thumbnail:
            return ""
        return os.path.basename(self.thumbnail)

    @queryset_manager
    def objects(doc_cls, queryset):
        return queryset.order_by('creation')

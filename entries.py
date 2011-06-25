from mongoengine import *
from datetime import datetime
import os, re

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

    def save(self):
        def convert_tag(tag):
            tag = tag.strip().lower().replace(' ', '-')
            return re.sub('[^a-z0-9_-]', '', tag)
        self.tags = [convert_tag(tag) for tag in self.tags]
        self.tags = [tag for tag in self.tags if tag.strip()]
        super(Picture, self).save()

    @staticmethod
    def ranged(request, fr=None, num=30, order='creation'):
        query = Q(**request)
        asc = order[0] != '-'
        if fr:
            if asc:
                fromreq = { '%s__gt' % order : fr }
            else:
                fromreq = { '%s__lt' % order[1:] : fr }
            query = Q(**fromreq) & query

        if asc:
            startsort = '-%s' % order
            endsort = order
        else:
            startsort = order[1:]
            endsort = order

        return Picture.objects.order_by(startsort).filter(query).order_by(endsort).limit(num)



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
    def ranged(request, last=None, num=30, order='creation', last_field=None):
        query = Q(**request)

        if order[0] == '-':
            asc = False
            order = order[1:]
        elif order[0] == '+':
            asc = True
            order = order[1:]
        else:
            asc = True

        if last:
            if not last_field:
                last_field = order

            if asc:
                fromreq = { '%s__gt' % last_field : last }
            else:
                fromreq = { '%s__lt' % last_field : last }
            query = Q(**fromreq) & query

        if asc:
            startsort = '-%s' % order
            endsort = order
        else:
            startsort = order
            endsort = '-%s' % order

        return Picture.objects.order_by(startsort).filter(query).order_by(endsort).limit(num)



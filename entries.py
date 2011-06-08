from mongoengine import *
from datetime import datetime

class Picture(Document):
    path = StringField(required=True) # path to picture
    hashcode = StringField()  # hash (SHA1) of file
    tags = ListField(StringField())
    thumbnail = StringField()
    width = IntField(min_value=0)   # width of picture
    height = IntField(min_value=0)  # height of picture
    size = IntField(min_value=0)    # filesize in bytes
    creation = DateTimeField(default=datetime.now) # time of file creation

    def __unicode__(self):
        return u"%s the picture" % self.path


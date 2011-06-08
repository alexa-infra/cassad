from django.db import models
import base64

class Picture(models.Model):
    path = models.CharField('local path to picture', max_length=200)
    hashcode = models.CharField('hash of file', max_length=200, blank=True)
    timestamp = models.DateTimeField('time of file creation')
    tags = models.ManyToManyField('Tag')
    thumbnail = models.OneToOneField('Thumbnail')

    def __unicode__(self):
        return u"%s the picture" % self.path

class Thumbnail(models.Model):
    _data = models.TextField(blank=True)
    width = models.IntegerField()
    height = models.IntegerField()

    def set_data(self, data):
        self._data = base64.encodestring(data)

    def get_data(self):
        return base64.decodestring(self._data)

    data = property(get_data, set_data)

    def __unicode__(self):
        return u"%s the thumbnail" % self.picture.path

class Tag(models.Model):
    name = models.CharField('tag name', max_length=50, primary_key=True)

    def __unicode__(self):
        return u"%s the name" % self.name

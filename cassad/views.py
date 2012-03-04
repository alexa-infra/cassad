import entries
import os
from django.http import HttpResponse
from django.utils import simplejson
from bson.objectid import ObjectId
from datetime import datetime
import time
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.core.urlresolvers import reverse

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        defaults = {
            'content_type': 'application/json',
        }
        defaults.update(kwargs)
        super(JSONResponse, self).__init__(simplejson.dumps(data), defaults)

def tagmeview(request, template_name, callback):
    tags = entries.Picture.objects.item_frequencies('tags')
    return render(request, template_name, { 'callback': callback, 'tags': tags })

def addtags(request):
    selected = request.GET.get("selected", None)
    tags = request.GET.get("tags", "")
    if not selected:
        return JSONResponse({})
    ids = selected.split(',')
    objs = [ObjectId(x) for x in ids]
    entry_list = entries.Picture.objects(id__in=objs)

    taglist = tags.split(',')

    for p in entry_list:
        p.tags = taglist
        p.save()
    return JSONResponse({ "res": "OK" })

def tags(request, template_name):
    res = entries.Picture.objects.item_frequencies('tags')
    return render(request, template_name,  { 'tags': res })

def showtagview(request, template_name, tag, callback):
    tags = entries.Picture.objects.item_frequencies('tags')
    return render(request, template_name, { 'callback': callback + tag, 'tag': tag, 'tags': tags })

def delete(request):
    selected = request.GET.get("selected", None)
    if not selected:
        return JSONResponse({})
    ids = selected.split(',')
    objs = [ObjectId(x) for x in ids]
    entry_list = entries.Picture.objects(id__in=objs)

    for p in entry_list:
        p.tags.append("deleted")
        p.save()
    return JSONResponse({ "res": "OK" })

def showimage(request, template_name, id):
    p = entries.Picture.objects.get(id=ObjectId(id))
    return render(request, template_name, { 'image': p,
            'wpurl': reverse('image-content', args=[id,])
        })

def image(request, id):
    p = entries.Picture.objects.get(id=ObjectId(id))
    image_data = open(p.path, "rb").read()
    return HttpResponse(image_data, mimetype="image/jpeg")

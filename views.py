import entries
import os
from django.http import HttpResponse
from django.utils import simplejson
from bson.objectid import ObjectId
from datetime import datetime
import time
from django.views.decorators.http import require_POST
from django.shortcuts import render

from mongoengine import *
connect("cassad")

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        defaults = {
            'content_type': 'application/json',
        }
        defaults.update(kwargs)
        super(JSONResponse, self).__init__(simplejson.dumps(data), defaults)

def convert(entry_list):
    res = {
        'pictures' : [ {
            "thumb":p.ThumbnailName(),
            "id": str(p.id),
            "width": p.width,
            "height":p.height,
            "tags": ",".join(p.tags)
            } for p in entry_list if p.thumbnail ]

    }
    if len(res['pictures']) > 0:
        res["last"] = res['pictures'][-1]['id']
    else:
        res["last"] = ""
    return res

def tagmeview(request, template_name, callback):
    return render(request, template_name, { 'callback': callback })

def tagme(request, last=None, num=30):
    if not last:
        from_value = None
        show_number = 80
    else:
        last_el = entries.Picture.objects.get(id=ObjectId(last))
        from_value = last_el.creation
        show_number = num

    res_list = entries.Picture.ranged({ 'tags__size': 0 }, from_value, show_number, "-creation")

    res = convert(res_list)

#    last_entries = entries.Picture.objects.filter(hashcode=res["last"])
#    if len(last_entries) > 1:
#        conv_last = convert(last_entries)
#        for p in conv_last['pictures']:
#            if p not in res['pictures']:
#                res['pictures'].append(p)

    return JSONResponse(res)

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
    return render(request, template_name, { 'callback': callback, 'tag': tag })

def showtag(request, tag, last=None, num=30):
    if not last:
        from_value = None
        show_number = 80
    else:
        last_el = entries.Picture.objects.get(id=ObjectId(last))
        from_value = last_el.creation
        show_number = num

    if tag == 'deleted':
        res_list = entries.Picture.ranged({ "tags__in" : [tag] },
            from_value, show_number, "-creation")
    else:
        res_list = entries.Picture.ranged({ "tags__in" : [tag], "tags__nin": ["deleted"] },
            from_value, show_number, "-creation")
    res = convert(res_list)

#    last_entries = entries.Picture.objects.filter(hashcode=res["last"])
#    if len(last_entries) > 1:
#        conv_last = convert(last_entries)
#        for p in conv_last['pictures']:
#            if p not in res['pictures']:
#                res['pictures'].append(p)

    return JSONResponse(res)

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


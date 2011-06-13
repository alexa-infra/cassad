import entries
import os
from django.http import HttpResponse
from django.utils import simplejson
from bson.objectid import ObjectId
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import datetime
import time

from mongoengine import *
connect("cassad")

def render_to_response(request, template_name, context_dict, **kwargs):
    from django.template import RequestContext
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict)
    return _render_to_response(template_name, context_instance=context, **kwargs)

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
            "creation":time.mktime(p.creation.timetuple())
            } for p in entry_list if p.thumbnail ]

    }
    res["last"] = res['pictures'][-1]['id']
    return res


def index(request, template_name, num=30):
    res_list = entries.Picture.objects.order_by("-creation").limit(num)
    res = convert(res_list)
    return render_to_response(request, template_name, res)

def search(request, last, num=30):
#    try:
    last_el = entries.Picture.objects.get(id=ObjectId(last))
    res_list = entries.Picture.objects(creation__lt=last_el.creation).order_by("-creation").limit(num)
#    except:
#        res_list = entry_list.limit(num)
    res = convert(res_list)

    return JSONResponse(res)

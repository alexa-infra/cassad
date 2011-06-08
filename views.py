import entries

from mongoengine import *
connect("cassad")

def render_to_response(request, template_name, context_dict, **kwargs):
    from django.template import RequestContext
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict)
    return _render_to_response(template_name, context_instance=context, **kwargs)

def index(request, template_name):
    pictures = entries.Picture.objects.all()
    return render_to_response(request, template_name, {
            'pictures': pictures
        })


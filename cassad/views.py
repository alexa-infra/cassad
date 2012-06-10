import entries
from django.http import HttpResponse
from bson.objectid import ObjectId
from django.shortcuts import render
from django.core.urlresolvers import reverse


def tagmeview(request, template_name, callback):
    tags = entries.Picture.objects.item_frequencies('tags')
    return render(request, template_name, {'callback': callback, 'tags': tags})


def tags(request, template_name):
    res = entries.Picture.objects.item_frequencies('tags')
    return render(request, template_name,  {'tags': res})


def showtagview(request, template_name, tag, callback):
    tags = entries.Picture.objects.item_frequencies('tags')
    return render(request, template_name, {'callback': callback + tag, 'tag': tag, 'tags': tags})


def showimage(request, template_name, id):
    p = entries.Picture.objects.get(id=ObjectId(id))
    return render(request, template_name, {'image': p,
            'wpurl': reverse('image-content', args=[id])
        })


def image(request, id):
    p = entries.Picture.objects.get(id=ObjectId(id))
    image_data = open(p.path, "rb").read()
    return HttpResponse(image_data, mimetype="image/jpeg")

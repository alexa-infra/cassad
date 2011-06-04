# -*- coding:utf-8 -*-
from django.template import Library
from django.conf import settings
import urlparse
import os
from django.contrib.sites.models import Site

register = Library()

def _absolute_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        return url
    domain = Site.objects.get_current().domain
    return 'http://%s%s' % (domain, url)

@register.simple_tag
def media(filename, flags=''):
    flags = set(f.strip() for f in flags.split(','))
    url = urlparse.urljoin(settings.MEDIA_URL, filename)
    if 'absolute' in flags:
        url = _absolute_url(url)
    if (filename.endswith('.css') or filename.endswith('.js')) and 'no-timestamp' not in flags or \
            'timestamp' in flags:
        fullname = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(fullname):
        url += '?%d' % os.path.getmtime(fullname)
    return url

@register.simple_tag
def today(timeformat):
    from datetime import datetime
    return datetime.now().strftime(timeformat)

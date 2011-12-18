from cassad.entries import Picture
import os
import sys
import Image
import hashlib
from datetime import datetime
from django.conf import settings

thumbdir = getattr(settings, 'THUMBNAIL_DIR', None)
tsize = 250

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from mprogress import ProgressBar

class Command(BaseCommand):
    help = 'Help text goes here'

    def handle(self, *args, **options):
        for p in args:
            self.process_path(p)

    def shahash(self, filename):
        sha = hashlib.sha1()
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(128*sha.block_size), ''):
                sha.update(chunk)
        return sha.hexdigest()

    def process_path(self, rootdir):
        count_files = 0
        for root, subfolders, files in os.walk(rootdir):
            count_files += len(files)
        prog = ProgressBar(0, count_files, 77, mode='fixed')
        oldprog = str(prog)

        for root, subfolders, files in os.walk(rootdir):
            for f in files:
                filename = os.path.join(root, f)
                try:
                    if Picture.objects.filter(path=filename).count() == 0:
                       self.process_file(filename)
                except:
                    print 'ERROR with %s' % filename
                    pass
                prog.increment_amount()
                print prog, "\r",
                sys.stdout.flush()

    def process_file(self, filename):
        img = Image.open(filename)
        ts = os.path.getctime(filename)
        creation = datetime.fromtimestamp(ts)
        size = os.path.getsize(filename)
        sha = self.shahash(filename)

        p = Picture()
        p.path = filename.decode('utf-8')
        p.hashcode = sha
        p.creation = creation
        p.width, p.height = img.size
        p.size = size

        if Picture.objects.filter(hashcode=sha).count() > 0:
            p.tags = ['deleted']

        p.save()

        fname = os.path.basename(filename)
        name, ext = os.path.splitext(fname)
        name = str(p.id)
        tname = os.path.join(thumbdir, name + ext)

        w, h = img.size
        factor = min(tsize / float(w), tsize / float(h))
        w = int(w * factor)
        h = int(h * factor)

        mode = img.format
        s = (w, h)
        img.thumbnail(s)
        img.save(tname, mode)

        p.thumbnail = tname
        p.save()

        print filename, size, img.format, img.size, img.mode, creation, sha

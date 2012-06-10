from cassad.entries import Picture
import os
import sys
import Image
import hashlib
from datetime import datetime
from django.conf import settings

thumbdir = getattr(settings, 'THUMBNAIL_DIR', None)
tsize = 250

from django.core.management.base import BaseCommand
from mprogress import ProgressBar


class Command(BaseCommand):
    help = 'Help text goes here'

    def handle(self, *args, **options):
        for p in args:
            self.process_path(p)

    def shahash(self, filename):
        sha = hashlib.sha1()
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(128 * sha.block_size), ''):
                sha.update(chunk)
        return sha.hexdigest()

    def process_path(self, rootdir):
        count_files = 0
        for _, _, files in os.walk(rootdir):
            count_files += len(files)
        prog = ProgressBar(0, count_files, 77, mode='fixed')

        processed = 0
        errors = 0
        for root, subfolders, files in os.walk(rootdir):
            for f in files:
                filename = os.path.join(root, f)
                try:
                    if self.process_file(filename):
                        processed += 1
                except:
                    print 'ERROR with %s' % filename
                    print 'Exception', sys.exc_info()[0]
                    errors += 1
                prog.increment_amount()
                print prog, "\r",
                sys.stdout.flush()
        print "\n"
        print "total files: %d, added: %d, errors: %d \n" % (count_files, processed, errors)

    def process_file(self, filename):
        if Picture.objects.filter(path=filename).count() != 0:
            return False
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

        try:
            p.thumbnail = self.generate_thumbnail(img, filename, str(p.id))
        except:
            p.delete()
            raise

        p.save()
        print filename, size, img.format, img.size, img.mode, creation, sha
        return True

    def generate_thumbnail(self, img, filename, thumbnailname):
        fname = os.path.basename(filename)
        _, ext = os.path.splitext(fname)
        tname = os.path.join(thumbdir, thumbnailname + ext)

        w, h = img.size
        factor = min(tsize / float(w), tsize / float(h))
        w, h = int(w * factor), int(h * factor)
        s = (w, h)

        thumbnail = img.resize(s, Image.ANTIALIAS)
        thumbnail.save(tname, img.format)

        return tname

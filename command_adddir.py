import entries
from mongoengine import *
import os
import sys
import Image
import hashlib
from datetime import datetime

connect("cassad")

rootdir = sys.argv[1]
thumbdir = sys.argv[2]
tsize = 250

def shahash(filename):
    sha = hashlib.sha1()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128*sha.block_size), ''):
            sha.update(chunk)
    return sha.hexdigest()

for root, subfolders, files in os.walk(rootdir):
    for f in files:
        filename = os.path.join(root, f)
        try:
            img = Image.open(filename)
            ts = os.path.getctime(filename)
            creation = datetime.fromtimestamp(ts)
            size = os.path.getsize(filename)
            sha = shahash(filename)

            p = entries.Picture(path=filename)
            p.hashcode = sha
            p.creation = creation
            p.width, p.height = img.size
            p.size = size
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
        except:
            pass

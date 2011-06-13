import entries
from mongoengine import *
import os
import sys
import Image
from mprogress import ProgressBar

connect("cassad")

root = sys.argv[1]
size = 250

allpictures = entries.Picture.objects.all()

limit = allpictures.count()
prog = ProgressBar(0, limit, 77, mode='fixed')
oldprog = str(prog)

for pic in allpictures:
    try:
        if pic.thumbnail:
            if os.path.exists(pic.thumbnail):
                prog.increment_amount()
                print prog, "\r",
                sys.stdout.flush()
                continue
        filename = os.path.basename(pic.path)
        name, ext = os.path.splitext(filename)
        name = str(pic.id)
        filename = os.path.join(root, name + ext)

        w, h = pic.width, pic.height
        factor = min(size / float(w), size / float(h))
        w = int(w * factor)
        h = int(h * factor)

        img = Image.open(pic.path)
        mode = img.format
        s = (w, h)
        img.thumbnail(s)
        img.save(filename, mode)

        pic.thumbnail = filename
        pic.save()

        prog.increment_amount()
        print prog, "\r",
        sys.stdout.flush()
    except:
        print pic.path


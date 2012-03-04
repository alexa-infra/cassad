from cassad import entries
from mongoengine import *
connect("cassad")
import shutil, os

root = "/home/alexa/cassad/duplicate"

pp = entries.Picture.objects(tags='deleted')
for p in pp:
  fname = os.path.basename(p.path)
  name, ext = os.path.splitext(fname)
  name = str(p.id)
  tname = os.path.join(root, name + ext)
  shutil.move(p.path, tname)
  os.remove(p.thumbnail)
  p.delete()


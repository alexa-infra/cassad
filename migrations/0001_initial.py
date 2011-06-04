# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Picture'
        db.create_table('cassad_picture', (
            ('path', self.gf('django.db.models.fields.CharField')(max_length=200, primary_key=True)),
            ('hashcode', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('thumbnail', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cassad.Thumbnail'], unique=True)),
        ))
        db.send_create_signal('cassad', ['Picture'])

        # Adding M2M table for field tags on 'Picture'
        db.create_table('cassad_picture_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('picture', models.ForeignKey(orm['cassad.picture'], null=False)),
            ('tag', models.ForeignKey(orm['cassad.tag'], null=False))
        ))
        db.create_unique('cassad_picture_tags', ['picture_id', 'tag_id'])

        # Adding model 'Thumbnail'
        db.create_table('cassad_thumbnail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_data', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cassad', ['Thumbnail'])

        # Adding model 'Tag'
        db.create_table('cassad_tag', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
        ))
        db.send_create_signal('cassad', ['Tag'])

    def backwards(self, orm):
        
        # Deleting model 'Picture'
        db.delete_table('cassad_picture')

        # Removing M2M table for field tags on 'Picture'
        db.delete_table('cassad_picture_tags')

        # Deleting model 'Thumbnail'
        db.delete_table('cassad_thumbnail')

        # Deleting model 'Tag'
        db.delete_table('cassad_tag')

    models = {
        'cassad.picture': {
            'Meta': {'object_name': 'Picture'},
            'hashcode': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cassad.Tag']", 'symmetrical': 'False'}),
            'thumbnail': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cassad.Thumbnail']", 'unique': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'cassad.tag': {
            'Meta': {'object_name': 'Tag'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'})
        },
        'cassad.thumbnail': {
            'Meta': {'object_name': 'Thumbnail'},
            '_data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['cassad']

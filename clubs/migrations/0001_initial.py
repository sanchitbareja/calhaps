# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Club'
        db.create_table(u'clubs_club', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('typeOfOrganization', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('founded', self.gf('django.db.models.fields.TextField')()),
            ('urlPersonal', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('image', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'clubs', ['Club'])


    def backwards(self, orm):
        # Deleting model 'Club'
        db.delete_table(u'clubs_club')


    models = {
        u'clubs.club': {
            'Meta': {'object_name': 'Club'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'founded': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'typeOfOrganization': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'urlPersonal': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['clubs']
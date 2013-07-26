# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EventType'
        db.create_table(u'events_eventtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'events', ['EventType'])

        # Deleting field 'Event.typeOfEvent'
        db.delete_column(u'events_event', 'typeOfEvent')

        # Deleting field 'Event.advertise'
        db.delete_column(u'events_event', 'advertise')

        # Adding field 'Event.readyForDisplay'
        db.add_column(u'events_event', 'readyForDisplay',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding M2M table for field typeOfEvent on 'Event'
        m2m_table_name = db.shorten_name(u'events_event_typeOfEvent')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'events.event'], null=False)),
            ('eventtype', models.ForeignKey(orm[u'events.eventtype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'eventtype_id'])


    def backwards(self, orm):
        # Deleting model 'EventType'
        db.delete_table(u'events_eventtype')

        # Adding field 'Event.typeOfEvent'
        db.add_column(u'events_event', 'typeOfEvent',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Event.advertise'
        db.add_column(u'events_event', 'advertise',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Event.readyForDisplay'
        db.delete_column(u'events_event', 'readyForDisplay')

        # Removing M2M table for field typeOfEvent on 'Event'
        db.delete_table(db.shorten_name(u'events_event_typeOfEvent'))


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
        },
        u'events.event': {
            'Meta': {'object_name': 'Event'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clubs.Club']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Location']", 'null': 'True', 'blank': 'True'}),
            'readyForDisplay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'typeOfEvent': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['events.EventType']", 'null': 'True', 'blank': 'True'})
        },
        u'events.eventtype': {
            'Meta': {'object_name': 'EventType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'events.location': {
            'Meta': {'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['events']
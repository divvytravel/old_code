# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AirportIATA'
        db.create_table(u'geo_airportiata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iata', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100, blank=True)),
            ('coordinates', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('parent_name_en', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100, blank=True)),
        ))
        db.send_create_signal(u'geo', ['AirportIATA'])

        # Adding model 'UploadIATA'
        db.create_table(u'geo_uploadiata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('csv_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('result', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('error_details', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'geo', ['UploadIATA'])

        # Adding model 'Country'
        db.create_table(u'geo_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('name_en', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'geo', ['Country'])

        # Adding model 'City'
        db.create_table(u'geo_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Country'])),
            ('iata', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
        ))
        db.send_create_signal(u'geo', ['City'])

        # Adding unique constraint on 'City', fields ['name', 'country']
        db.create_unique(u'geo_city', ['name', 'country_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'City', fields ['name', 'country']
        db.delete_unique(u'geo_city', ['name', 'country_id'])

        # Deleting model 'AirportIATA'
        db.delete_table(u'geo_airportiata')

        # Deleting model 'UploadIATA'
        db.delete_table(u'geo_uploadiata')

        # Deleting model 'Country'
        db.delete_table(u'geo_country')

        # Deleting model 'City'
        db.delete_table(u'geo_city')


    models = {
        u'geo.airportiata': {
            'Meta': {'object_name': 'AirportIATA'},
            'coordinates': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'iata': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'parent_name_en': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'geo.city': {
            'Meta': {'ordering': "('country__name', 'name')", 'unique_together': "(('name', 'country'),)", 'object_name': 'City'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geo.Country']"}),
            'iata': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'geo.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'geo.uploadiata': {
            'Meta': {'object_name': 'UploadIATA'},
            'csv_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'error_details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['geo']
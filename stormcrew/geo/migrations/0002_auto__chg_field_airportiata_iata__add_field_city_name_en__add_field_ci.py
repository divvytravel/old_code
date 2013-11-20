# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AirportIATA.iata'
        db.alter_column(u'geo_airportiata', 'iata', self.gf('django.db.models.fields.CharField')(max_length=3))
        # Adding field 'City.name_en'
        db.add_column(u'geo_city', 'name_en',
                      self.gf('django.db.models.fields.CharField')(max_length=100, unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'City.iata'
        db.add_column(u'geo_city', 'iata',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=3, blank=True),
                      keep_default=False)

        # Adding field 'Country.name_en'
        db.add_column(u'geo_country', 'name_en',
                      self.gf('django.db.models.fields.CharField')(max_length=100, unique=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'AirportIATA.iata'
        db.alter_column(u'geo_airportiata', 'iata', self.gf('django.db.models.fields.CharField')(max_length=100))
        # Deleting field 'City.name_en'
        db.delete_column(u'geo_city', 'name_en')

        # Deleting field 'City.iata'
        db.delete_column(u'geo_city', 'iata')

        # Deleting field 'Country.name_en'
        db.delete_column(u'geo_country', 'name_en')


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
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'geo.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'})
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
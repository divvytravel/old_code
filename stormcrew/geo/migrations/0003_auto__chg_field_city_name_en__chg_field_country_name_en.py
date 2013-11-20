# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'City.name_en'
        db.alter_column(u'geo_city', 'name_en', self.gf('django.db.models.fields.CharField')(default='-', unique=True, max_length=100))

        # Changing field 'Country.name_en'
        db.alter_column(u'geo_country', 'name_en', self.gf('django.db.models.fields.CharField')(default='-', unique=True, max_length=100))

    def backwards(self, orm):

        # Changing field 'City.name_en'
        db.alter_column(u'geo_city', 'name_en', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, null=True))

        # Changing field 'Country.name_en'
        db.alter_column(u'geo_country', 'name_en', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, null=True))

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
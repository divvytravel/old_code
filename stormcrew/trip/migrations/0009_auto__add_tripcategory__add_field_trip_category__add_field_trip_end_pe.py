# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TripCategory'
        db.create_table(u'trip_tripcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'trip', ['TripCategory'])

        # Adding field 'Trip.category'
        db.add_column(u'trip_trip', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trip.TripCategory'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Trip.end_people_date'
        db.add_column(u'trip_trip', 'end_people_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 11, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Trip.people_max_count'
        db.add_column(u'trip_trip', 'people_max_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=50),
                      keep_default=False)

        # Adding field 'Trip.price_type'
        db.add_column(u'trip_trip', 'price_type',
                      self.gf('django.db.models.fields.CharField')(default='noncom', max_length=10),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'TripCategory'
        db.delete_table(u'trip_tripcategory')

        # Deleting field 'Trip.category'
        db.delete_column(u'trip_trip', 'category_id')

        # Deleting field 'Trip.end_people_date'
        db.delete_column(u'trip_trip', 'end_people_date')

        # Deleting field 'Trip.people_max_count'
        db.delete_column(u'trip_trip', 'people_max_count')

        # Deleting field 'Trip.price_type'
        db.delete_column(u'trip_trip', 'price_type')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'geo.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'trip.trip': {
            'Meta': {'ordering': "('start_date',)", 'object_name': 'Trip'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trip.TripCategory']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geo.Country']", 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'euro'", 'max_length': '10'}),
            'descr_additional': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'descr_company': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'descr_main': ('django.db.models.fields.TextField', [], {}),
            'descr_share': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'end_people_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'includes': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'approved_trips'", 'blank': 'True', 'to': u"orm['users.User']"}),
            'people_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'people_max_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'price_type': ('django.db.models.fields.CharField', [], {'default': "'noncom'", 'max_length': '10'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'trip_type': ('django.db.models.fields.CharField', [], {'default': "'open'", 'max_length': '10'})
        },
        u'trip.tripcategory': {
            'Meta': {'object_name': 'TripCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'trip.trippicture': {
            'Meta': {'object_name': 'TripPicture'},
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['trip.Trip']"})
        },
        u'trip.triprequest': {
            'Meta': {'ordering': "('-date_created',)", 'object_name': 'TripRequest'},
            'approved_by_owner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'denied_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'denied_trip_requests'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '10'}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_requests'", 'to': u"orm['trip.Trip']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'users_approved': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'approved_trip_requests'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.User']"})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'avatar_url': ('django.db.models.fields.CharField', [], {'default': "'/static/img/no-avatar.jpg'", 'max_length': '200'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'social_auth_response': ('social_auth.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['trip']
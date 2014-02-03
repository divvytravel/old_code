# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tags'
        db.create_table(u'trip_tags', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'trip', ['Tags'])

        # Adding model 'TripCategory'
        db.create_table(u'trip_tripcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('applicable', self.gf('django.db.models.fields.CharField')(default='all', max_length=10)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trip_category', to=orm['trip.Tags'])),
        ))
        db.send_create_signal(u'trip', ['TripCategory'])

        # Adding model 'Trip'
        db.create_table(u'trip_trip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='trips', null=True, to=orm['trip.TripCategory'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('end_people_date', self.gf('django.db.models.fields.DateField')()),
            ('price', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.City'])),
            ('currency', self.gf('django.db.models.fields.CharField')(default='euro', max_length=10)),
            ('includes', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('people_count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('people_max_count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('descr_main', self.gf('django.db.models.fields.TextField')()),
            ('descr_share', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('descr_additional', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('descr_company', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('trip_type', self.gf('django.db.models.fields.CharField')(default='open', max_length=10)),
            ('price_type', self.gf('django.db.models.fields.CharField')(default='noncom', max_length=10)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
        ))
        db.send_create_signal(u'trip', ['Trip'])

        # Adding M2M table for field people on 'Trip'
        m2m_table_name = db.shorten_name(u'trip_trip_people')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('trip', models.ForeignKey(orm[u'trip.trip'], null=False)),
            ('user', models.ForeignKey(orm[u'users.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['trip_id', 'user_id'])

        # Adding M2M table for field tags on 'Trip'
        m2m_table_name = db.shorten_name(u'trip_trip_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('trip', models.ForeignKey(orm[u'trip.trip'], null=False)),
            ('tags', models.ForeignKey(orm[u'trip.tags'], null=False))
        ))
        db.create_unique(m2m_table_name, ['trip_id', 'tags_id'])

        # Adding model 'TripPointType'
        db.create_table(u'trip_trippointtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('point_title_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('many', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='point_types', to=orm['trip.TripCategory'])),
        ))
        db.send_create_signal(u'trip', ['TripPointType'])

        # Adding model 'TripPoint'
        db.create_table(u'trip_trippoint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('p_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trip.TripPointType'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('price', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('trip', self.gf('django.db.models.fields.related.ForeignKey')(related_name='points', to=orm['trip.Trip'])),
        ))
        db.send_create_signal(u'trip', ['TripPoint'])

        # Adding model 'TripPicture'
        db.create_table(u'trip_trippicture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('trip', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['trip.Trip'])),
        ))
        db.send_create_signal(u'trip', ['TripPicture'])

        # Adding model 'TripRequest'
        db.create_table(u'trip_triprequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trip', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_requests', to=orm['trip.Trip'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=10)),
            ('approved_by_owner', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'trip', ['TripRequest'])

        # Adding M2M table for field users_approved on 'TripRequest'
        m2m_table_name = db.shorten_name(u'trip_triprequest_users_approved')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('triprequest', models.ForeignKey(orm[u'trip.triprequest'], null=False)),
            ('user', models.ForeignKey(orm[u'users.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['triprequest_id', 'user_id'])

        # Adding M2M table for field denied_by on 'TripRequest'
        m2m_table_name = db.shorten_name(u'trip_triprequest_denied_by')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('triprequest', models.ForeignKey(orm[u'trip.triprequest'], null=False)),
            ('user', models.ForeignKey(orm[u'users.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['triprequest_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'Tags'
        db.delete_table(u'trip_tags')

        # Deleting model 'TripCategory'
        db.delete_table(u'trip_tripcategory')

        # Deleting model 'Trip'
        db.delete_table(u'trip_trip')

        # Removing M2M table for field people on 'Trip'
        db.delete_table(db.shorten_name(u'trip_trip_people'))

        # Removing M2M table for field tags on 'Trip'
        db.delete_table(db.shorten_name(u'trip_trip_tags'))

        # Deleting model 'TripPointType'
        db.delete_table(u'trip_trippointtype')

        # Deleting model 'TripPoint'
        db.delete_table(u'trip_trippoint')

        # Deleting model 'TripPicture'
        db.delete_table(u'trip_trippicture')

        # Deleting model 'TripRequest'
        db.delete_table(u'trip_triprequest')

        # Removing M2M table for field users_approved on 'TripRequest'
        db.delete_table(db.shorten_name(u'trip_triprequest_users_approved'))

        # Removing M2M table for field denied_by on 'TripRequest'
        db.delete_table(db.shorten_name(u'trip_triprequest_denied_by'))


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
        u'trip.tags': {
            'Meta': {'object_name': 'Tags'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'trip.trip': {
            'Meta': {'ordering': "('start_date',)", 'object_name': 'Trip'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'trips'", 'null': 'True', 'to': u"orm['trip.TripCategory']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geo.City']"}),
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
            'price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price_type': ('django.db.models.fields.CharField', [], {'default': "'noncom'", 'max_length': '10'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'trips'", 'blank': 'True', 'to': u"orm['trip.Tags']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'trip_type': ('django.db.models.fields.CharField', [], {'default': "'open'", 'max_length': '10'})
        },
        u'trip.tripcategory': {
            'Meta': {'object_name': 'TripCategory'},
            'applicable': ('django.db.models.fields.CharField', [], {'default': "'all'", 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trip_category'", 'to': u"orm['trip.Tags']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'trip.trippicture': {
            'Meta': {'object_name': 'TripPicture'},
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['trip.Trip']"})
        },
        u'trip.trippoint': {
            'Meta': {'object_name': 'TripPoint'},
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'p_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trip.TripPointType']"}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'points'", 'to': u"orm['trip.Trip']"})
        },
        u'trip.trippointtype': {
            'Meta': {'object_name': 'TripPointType'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'point_types'", 'to': u"orm['trip.TripCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'many': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'point_title_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
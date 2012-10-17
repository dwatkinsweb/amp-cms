# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Pagelet.private'
        db.add_column('ampcms_pagelet', 'private',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Pagelet.private'
        db.delete_column('ampcms_pagelet', 'private')


    models = {
        'ampcms.ampcmssite': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'AmpCmsSite', 'db_table': "'ampcms_site'", '_ormbases': ['sites.Site']},
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True', 'primary_key': 'True'}),
            'skin': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'ampcms.group': {
            'Meta': {'object_name': 'Group', '_ormbases': ['auth.Group']},
            'acl_pagelets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ampcms.Pagelet']", 'symmetrical': 'False', 'blank': 'True'}),
            'acl_pages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ampcms.Page']", 'symmetrical': 'False', 'blank': 'True'}),
            'group_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.Group']", 'unique': 'True', 'primary_key': 'True'})
        },
        'ampcms.module': {
            'Meta': {'ordering': "['site', 'order']", 'unique_together': "(('name', 'site'), ('site', 'order'))", 'object_name': 'Module'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'order': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ampcms.AmpCmsSite']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'ampcms.page': {
            'Meta': {'ordering': "['module__order', 'order']", 'unique_together': "(('module', 'name'), ('module', 'order'))", 'object_name': 'Page'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages'", 'to': "orm['ampcms.Module']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'page_class': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'pagelet_layout': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'ampcms.pagelet': {
            'Meta': {'ordering': "['page__module__order', 'page__order', 'order']", 'unique_together': "(('page', 'name'), ('page', 'order'))", 'object_name': 'Pagelet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'application': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'classes': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pagelets'", 'to': "orm['ampcms.Page']"}),
            'pagelet_class': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'starting_url': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'ampcms.pageletattribute': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('pagelet', 'name'),)", 'object_name': 'PageletAttribute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'pagelet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attributes'", 'to': "orm['ampcms.Pagelet']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ampcms.user': {
            'Meta': {'object_name': 'User', '_ormbases': ['auth.User']},
            'acl_pagelets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ampcms.Pagelet']", 'symmetrical': 'False', 'blank': 'True'}),
            'acl_pages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ampcms.Page']", 'symmetrical': 'False', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['ampcms']
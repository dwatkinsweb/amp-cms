# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AmpCmsSite'
        db.create_table('ampcms_site', (
            ('site_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True, primary_key=True)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('skin', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('ampcms', ['AmpCmsSite'])

        # Adding model 'Module'
        db.create_table('ampcms_module', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=1024, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ampcms.AmpCmsSite'])),
        ))
        db.send_create_signal('ampcms', ['Module'])

        # Adding unique constraint on 'Module', fields ['name', 'site']
        db.create_unique('ampcms_module', ['name', 'site_id'])

        # Adding unique constraint on 'Module', fields ['site', 'order']
        db.create_unique('ampcms_module', ['site_id', 'order'])

        # Adding model 'Page'
        db.create_table('ampcms_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=1024, null=True, blank=True)),
            ('page_class', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pages', to=orm['ampcms.Module'])),
            ('pagelet_layout', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal('ampcms', ['Page'])

        # Adding unique constraint on 'Page', fields ['module', 'name']
        db.create_unique('ampcms_page', ['module_id', 'name'])

        # Adding unique constraint on 'Page', fields ['module', 'order']
        db.create_unique('ampcms_page', ['module_id', 'order'])

        # Adding model 'Pagelet'
        db.create_table('ampcms_pagelet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('pagelet_class', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('application', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('starting_url', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('classes', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pagelets', to=orm['ampcms.Page'])),
        ))
        db.send_create_signal('ampcms', ['Pagelet'])

        # Adding unique constraint on 'Pagelet', fields ['page', 'name']
        db.create_unique('ampcms_pagelet', ['page_id', 'name'])

        # Adding unique constraint on 'Pagelet', fields ['page', 'order']
        db.create_unique('ampcms_pagelet', ['page_id', 'order'])

        # Adding model 'PageletAttribute'
        db.create_table('ampcms_pageletattribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('pagelet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attributes', to=orm['ampcms.Pagelet'])),
        ))
        db.send_create_signal('ampcms', ['PageletAttribute'])

        # Adding unique constraint on 'PageletAttribute', fields ['pagelet', 'name']
        db.create_unique('ampcms_pageletattribute', ['pagelet_id', 'name'])

        # Adding model 'Group'
        db.create_table('ampcms_group', (
            ('group_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.Group'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('ampcms', ['Group'])

        # Adding M2M table for field acl_pages on 'Group'
        db.create_table('ampcms_group_acl_pages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['ampcms.group'], null=False)),
            ('page', models.ForeignKey(orm['ampcms.page'], null=False))
        ))
        db.create_unique('ampcms_group_acl_pages', ['group_id', 'page_id'])

        # Adding M2M table for field acl_pagelets on 'Group'
        db.create_table('ampcms_group_acl_pagelets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['ampcms.group'], null=False)),
            ('pagelet', models.ForeignKey(orm['ampcms.pagelet'], null=False))
        ))
        db.create_unique('ampcms_group_acl_pagelets', ['group_id', 'pagelet_id'])

        # Adding model 'User'
        db.create_table('ampcms_user', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('ampcms', ['User'])

        # Adding M2M table for field acl_pages on 'User'
        db.create_table('ampcms_user_acl_pages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['ampcms.user'], null=False)),
            ('page', models.ForeignKey(orm['ampcms.page'], null=False))
        ))
        db.create_unique('ampcms_user_acl_pages', ['user_id', 'page_id'])

        # Adding M2M table for field acl_pagelets on 'User'
        db.create_table('ampcms_user_acl_pagelets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['ampcms.user'], null=False)),
            ('pagelet', models.ForeignKey(orm['ampcms.pagelet'], null=False))
        ))
        db.create_unique('ampcms_user_acl_pagelets', ['user_id', 'pagelet_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'PageletAttribute', fields ['pagelet', 'name']
        db.delete_unique('ampcms_pageletattribute', ['pagelet_id', 'name'])

        # Removing unique constraint on 'Pagelet', fields ['page', 'order']
        db.delete_unique('ampcms_pagelet', ['page_id', 'order'])

        # Removing unique constraint on 'Pagelet', fields ['page', 'name']
        db.delete_unique('ampcms_pagelet', ['page_id', 'name'])

        # Removing unique constraint on 'Page', fields ['module', 'order']
        db.delete_unique('ampcms_page', ['module_id', 'order'])

        # Removing unique constraint on 'Page', fields ['module', 'name']
        db.delete_unique('ampcms_page', ['module_id', 'name'])

        # Removing unique constraint on 'Module', fields ['site', 'order']
        db.delete_unique('ampcms_module', ['site_id', 'order'])

        # Removing unique constraint on 'Module', fields ['name', 'site']
        db.delete_unique('ampcms_module', ['name', 'site_id'])

        # Deleting model 'AmpCmsSite'
        db.delete_table('ampcms_site')

        # Deleting model 'Module'
        db.delete_table('ampcms_module')

        # Deleting model 'Page'
        db.delete_table('ampcms_page')

        # Deleting model 'Pagelet'
        db.delete_table('ampcms_pagelet')

        # Deleting model 'PageletAttribute'
        db.delete_table('ampcms_pageletattribute')

        # Deleting model 'Group'
        db.delete_table('ampcms_group')

        # Removing M2M table for field acl_pages on 'Group'
        db.delete_table('ampcms_group_acl_pages')

        # Removing M2M table for field acl_pagelets on 'Group'
        db.delete_table('ampcms_group_acl_pagelets')

        # Deleting model 'User'
        db.delete_table('ampcms_user')

        # Removing M2M table for field acl_pages on 'User'
        db.delete_table('ampcms_user_acl_pages')

        # Removing M2M table for field acl_pagelets on 'User'
        db.delete_table('ampcms_user_acl_pagelets')


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
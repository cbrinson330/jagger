# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'intrest'
        db.create_table(u'jagger_intrest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('minVal', self.gf('django.db.models.fields.IntegerField')()),
            ('maxVal', self.gf('django.db.models.fields.IntegerField')()),
            ('dateVals', self.gf('django.db.models.fields.CharField')(max_length=800)),
        ))
        db.send_create_signal(u'jagger', ['intrest'])


    def backwards(self, orm):
        # Deleting model 'intrest'
        db.delete_table(u'jagger_intrest')


    models = {
        u'jagger.intrest': {
            'Meta': {'object_name': 'intrest'},
            'dateVals': ('django.db.models.fields.CharField', [], {'max_length': '800'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maxVal': ('django.db.models.fields.IntegerField', [], {}),
            'minVal': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['jagger']
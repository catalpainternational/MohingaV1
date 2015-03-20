# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'activity.is_draft'
        db.add_column(u'aims_activity', 'is_draft',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'transaction.is_draft'
        db.add_column(u'aims_transaction', 'is_draft',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'activity.is_draft'
        db.delete_column(u'aims_activity', 'is_draft')

        # Deleting field 'transaction.is_draft'
        db.delete_column(u'aims_transaction', 'is_draft')


    models = {
        u'IATI.activity': {
            'Meta': {'object_name': 'activity'},
            'activity_status': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.activity_status']", 'null': 'True', 'blank': 'True'}),
            'collaboration_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.collaboration_type']", 'null': 'True', 'blank': 'True'}),
            'default_aid_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.aid_type']", 'null': 'True', 'blank': 'True'}),
            'default_currency': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'default_currency'", 'null': 'True', 'to': u"orm['IATI.currency']"}),
            'default_finance_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.finance_type']", 'null': 'True', 'blank': 'True'}),
            'default_flow_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.flow_type']", 'null': 'True', 'blank': 'True'}),
            'default_tied_status': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.tied_status']", 'null': 'True', 'blank': 'True'}),
            'end_actual': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'end_planned': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'hierarchy': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'iati_identifier': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '150', 'primary_key': 'True'}),
            'last_updated_datetime': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'linked_data_uri': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'participating_organisation': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['IATI.organisation']", 'null': 'True', 'through': u"orm['IATI.activity_participating_organisation']", 'blank': 'True'}),
            'policy_marker': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['IATI.policy_marker']", 'null': 'True', 'through': u"orm['IATI.activity_policy_marker']", 'blank': 'True'}),
            'recipient_country': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['geodata.country']", 'through': u"orm['IATI.activity_recipient_country']", 'symmetrical': 'False'}),
            'recipient_region': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['geodata.region']", 'through': u"orm['IATI.activity_recipient_region']", 'symmetrical': 'False'}),
            'reporting_organisation': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'activity_reporting_organisation'", 'null': 'True', 'blank': 'True', 'to': u"orm['IATI.organisation']"}),
            'sector': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['IATI.sector']", 'null': 'True', 'through': u"orm['IATI.activity_sector']", 'blank': 'True'}),
            'start_actual': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'start_planned': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'total_budget': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'default': 'None', 'max_digits': '15', 'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'total_budget_currency': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'total_budget_currency'", 'null': 'True', 'blank': 'True', 'to': u"orm['IATI.currency']"}),
            'xml_source_ref': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'IATI.activity_date_type': {
            'Meta': {'object_name': 'activity_date_type'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'IATI.activity_participating_organisation': {
            'Meta': {'object_name': 'activity_participating_organisation'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.organisation']", 'null': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.organisation_role']", 'null': 'True'})
        },
        u'IATI.activity_policy_marker': {
            'Meta': {'object_name': 'activity_policy_marker'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            'alt_policy_marker': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'policy_marker': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.policy_marker']", 'null': 'True'}),
            'policy_significance': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.policy_significance']", 'null': 'True'}),
            'vocabulary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.vocabulary']", 'null': 'True'})
        },
        u'IATI.activity_recipient_country': {
            'Meta': {'object_name': 'activity_recipient_country'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geodata.country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage': ('django.db.models.fields.DecimalField', [], {'default': 'None', 'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'})
        },
        u'IATI.activity_recipient_region': {
            'Meta': {'object_name': 'activity_recipient_region'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage': ('django.db.models.fields.DecimalField', [], {'default': 'None', 'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geodata.region']"})
        },
        u'IATI.activity_sector': {
            'Meta': {'object_name': 'activity_sector'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            'alt_sector_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage': ('django.db.models.fields.DecimalField', [], {'default': 'None', 'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.sector']", 'null': 'True'}),
            'vocabulary': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.vocabulary']", 'null': 'True'})
        },
        u'IATI.activity_status': {
            'Meta': {'object_name': 'activity_status'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'IATI.activity_website': {
            'Meta': {'object_name': 'activity_website'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'IATI.aid_type': {
            'Meta': {'object_name': 'aid_type'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.aid_type_category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'IATI.aid_type_category': {
            'Meta': {'object_name': 'aid_type_category'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'IATI.budget': {
            'Meta': {'object_name': 'budget'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.currency']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period_end': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'period_start': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.budget_type']", 'null': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'value_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'})
        },
        u'IATI.budget_type': {
            'Meta': {'object_name': 'budget_type'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'IATI.collaboration_type': {
            'Meta': {'object_name': 'collaboration_type'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'IATI.condition': {
            'Meta': {'object_name': 'condition'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.condition_type']", 'null': 'True'})
        },
        u'IATI.condition_type': {
            'Meta': {'object_name': 'condition_type'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'IATI.contact_info': {
            'Meta': {'object_name': 'contact_info'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            'email': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailing_address': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'organisation': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'person_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'IATI.currency': {
            'Meta': {'object_name': 'currency'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'IATI.description': {
            'Meta': {'object_name': 'description'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.language']", 'null': 'True'}),
            'rsr_description_type_id': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'description_type'", 'null': 'True', 'to': u"orm['IATI.description_type']"})
        },
        u'IATI.description_type': {
            'Meta': {'object_name': 'description_type'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'IATI.disbursement_channel': {
            'Meta': {'object_name': 'disbursement_channel'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        u'IATI.document_category': {
            'Meta': {'object_name': 'document_category'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'category_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'IATI.document_link': {
            'Meta': {'object_name': 'document_link'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            'document_category': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.document_category']", 'null': 'True'}),
            'file_format': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.file_format']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'IATI.file_format': {
            'Meta': {'object_name': 'file_format'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'IATI.finance_type': {
            'Meta': {'object_name': 'finance_type'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.finance_type_category']"}),
            'code': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '220'})
        },
        u'IATI.finance_type_category': {
            'Meta': {'object_name': 'finance_type_category'},
            'code': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'IATI.flow_type': {
            'Meta': {'object_name': 'flow_type'},
            'code': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'IATI.gazetteer_agency': {
            'Meta': {'object_name': 'gazetteer_agency'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'IATI.geographical_precision': {
            'Meta': {'object_name': 'geographical_precision'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'IATI.indicator_measure': {
            'Meta': {'object_name': 'indicator_measure'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'IATI.language': {
            'Meta': {'object_name': 'language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'IATI.location': {
            'Meta': {'object_name': 'location'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            'adm_country_adm1': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'adm_country_adm2': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'adm_country_iso': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['geodata.country']", 'null': 'True'}),
            'adm_country_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'description_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.description_type']", 'null': 'True'}),
            'gazetteer_entry': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '70', 'null': 'True'}),
            'gazetteer_ref': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.gazetteer_agency']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '70', 'null': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '70', 'null': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': 'None', 'max_length': '1000', 'null': 'True'}),
            'percentage': ('django.db.models.fields.DecimalField', [], {'default': 'None', 'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'precision': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.geographical_precision']", 'null': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.location_type']", 'null': 'True'}),
            'type_description': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True'})
        },
        u'IATI.location_type': {
            'Meta': {'object_name': 'location_type'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'IATI.organisation': {
            'Meta': {'object_name': 'organisation'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'null': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True'}),
            'reported_by_organisation': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.organisation_type']", 'null': 'True'})
        },
        u'IATI.organisation_identifier': {
            'Meta': {'object_name': 'organisation_identifier'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'null': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True'})
        },
        u'IATI.organisation_role': {
            'Meta': {'object_name': 'organisation_role'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'IATI.organisation_type': {
            'Meta': {'object_name': 'organisation_type'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'IATI.other_identifier': {
            'Meta': {'object_name': 'other_identifier'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'owner_ref': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'})
        },
        u'IATI.planned_disbursement': {
            'Meta': {'object_name': 'planned_disbursement'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.currency']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period_end': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'period_start': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'value_date': ('django.db.models.fields.DateField', [], {'null': 'True'})
        },
        u'IATI.policy_marker': {
            'Meta': {'object_name': 'policy_marker'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'IATI.policy_significance': {
            'Meta': {'object_name': 'policy_significance'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'IATI.publisher_type': {
            'Meta': {'object_name': 'publisher_type'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'IATI.related_activity': {
            'Meta': {'object_name': 'related_activity'},
            'current_activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'current_activity'", 'to': u"orm['IATI.activity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ref': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.related_activity_type']", 'null': 'True', 'max_length': '200'})
        },
        u'IATI.related_activity_type': {
            'Meta': {'object_name': 'related_activity_type'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'IATI.result': {
            'Meta': {'object_name': 'result'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.result_type']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'IATI.result_type': {
            'Meta': {'object_name': 'result_type'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'IATI.sector': {
            'Meta': {'object_name': 'sector'},
            'code': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'IATI.sector_category': {
            'Meta': {'object_name': 'sector_category'},
            'code': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'IATI.tied_status': {
            'Meta': {'object_name': 'tied_status'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'IATI.title': {
            'Meta': {'object_name': 'title'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.language']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        u'IATI.transaction': {
            'Meta': {'object_name': 'transaction'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.activity']"}),
            'aid_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.aid_type']", 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.currency']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'description_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.description_type']", 'null': 'True', 'blank': 'True'}),
            'disbursement_channel': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.disbursement_channel']", 'null': 'True', 'blank': 'True'}),
            'finance_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.finance_type']", 'null': 'True', 'blank': 'True'}),
            'flow_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.flow_type']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider_activity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'provider_organisation': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'transaction_providing_organisation'", 'null': 'True', 'blank': 'True', 'to': u"orm['IATI.organisation']"}),
            'provider_organisation_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'receiver_organisation': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'transaction_receiving_organisation'", 'null': 'True', 'blank': 'True', 'to': u"orm['IATI.organisation']"}),
            'receiver_organisation_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ref': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tied_status': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.tied_status']", 'null': 'True', 'blank': 'True'}),
            'transaction_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'transaction_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['IATI.transaction_type']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'value_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'IATI.transaction_type': {
            'Meta': {'object_name': 'transaction_type'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'IATI.value_type': {
            'Meta': {'object_name': 'value_type'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'IATI.verification_status': {
            'Meta': {'object_name': 'verification_status'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'IATI.vocabulary': {
            'Meta': {'object_name': 'vocabulary'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'aims.activity': {
            'Meta': {'object_name': 'activity', '_ormbases': [u'IATI.activity']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.activity']"})
        },
        u'aims.activity_date_type': {
            'Meta': {'object_name': 'activity_date_type', '_ormbases': [u'IATI.activity_date_type']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.activity_date_type']"})
        },
        u'aims.activity_participating_organisation': {
            'Meta': {'object_name': 'activity_participating_organisation', '_ormbases': [u'IATI.activity_participating_organisation']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.activity_participating_organisation']"})
        },
        u'aims.activity_policy_marker': {
            'Meta': {'object_name': 'activity_policy_marker', '_ormbases': [u'IATI.activity_policy_marker']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.activity_policy_marker']"})
        },
        u'aims.activity_recipient_country': {
            'Meta': {'object_name': 'activity_recipient_country', '_ormbases': [u'IATI.activity_recipient_country']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.activity_recipient_country']"})
        },
        u'aims.activity_recipient_region': {
            'Meta': {'object_name': 'activity_recipient_region', '_ormbases': [u'IATI.activity_recipient_region']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.activity_recipient_region']"})
        },
        u'aims.activity_sector': {
            'Meta': {'object_name': 'activity_sector', '_ormbases': [u'IATI.activity_sector']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.activity_sector']"})
        },
        u'aims.activity_status': {
            'Meta': {'object_name': 'activity_status', '_ormbases': [u'IATI.activity_status']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.activity_status']"})
        },
        u'aims.activity_website': {
            'Meta': {'object_name': 'activity_website', '_ormbases': [u'IATI.activity_website']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.activity_website']"})
        },
        u'aims.activitytotalbudgetusd': {
            'Meta': {'object_name': 'ActivityTotalBudgetUSD', 'db_table': "'aims_activity_total_budget_usd'"},
            'activity': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'total_budget_in'", 'unique': 'True', 'to': u"orm['IATI.activity']"}),
            'dollars': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aims.CurrencyExchangeRate']", 'null': 'True', 'blank': 'True'})
        },
        u'aims.aid_type': {
            'Meta': {'object_name': 'aid_type', '_ormbases': [u'IATI.aid_type']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.aid_type']"})
        },
        u'aims.aid_type_category': {
            'Meta': {'object_name': 'aid_type_category', '_ormbases': [u'IATI.aid_type_category']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.aid_type_category']"})
        },
        u'aims.budget': {
            'Meta': {'object_name': 'budget', '_ormbases': [u'IATI.budget']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.budget']"})
        },
        u'aims.budget_type': {
            'Meta': {'object_name': 'budget_type', '_ormbases': [u'IATI.budget_type']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.budget_type']"})
        },
        u'aims.collaboration_type': {
            'Meta': {'object_name': 'collaboration_type', '_ormbases': [u'IATI.collaboration_type']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.collaboration_type']"})
        },
        u'aims.condition': {
            'Meta': {'object_name': 'condition', '_ormbases': [u'IATI.condition']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.condition']"})
        },
        u'aims.condition_type': {
            'Meta': {'object_name': 'condition_type', '_ormbases': [u'IATI.condition_type']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.condition_type']"})
        },
        u'aims.contact_info': {
            'Meta': {'object_name': 'contact_info', '_ormbases': [u'IATI.contact_info']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.contact_info']"})
        },
        u'aims.currency': {
            'Meta': {'object_name': 'currency', '_ormbases': [u'IATI.currency']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.currency']"})
        },
        u'aims.currencyexchangerate': {
            'Meta': {'object_name': 'CurrencyExchangeRate', 'db_table': "'aims_currency_exchange_rate'"},
            'base_currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'base_currencies'", 'to': u"orm['IATI.currency']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'exchange_currencies'", 'to': u"orm['IATI.currency']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '8'})
        },
        u'aims.description': {
            'Meta': {'object_name': 'description', '_ormbases': [u'IATI.description']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.description']"})
        },
        u'aims.description_type': {
            'Meta': {'object_name': 'description_type', '_ormbases': [u'IATI.description_type']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.description_type']"})
        },
        u'aims.difference': {
            'Meta': {'object_name': 'Difference'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'difference_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'field_value': ('django.db.models.fields.CharField', [], {'max_length': '600', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'aims.disbursement_channel': {
            'Meta': {'object_name': 'disbursement_channel', '_ormbases': [u'IATI.disbursement_channel']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.disbursement_channel']"})
        },
        u'aims.document_category': {
            'Meta': {'object_name': 'document_category', '_ormbases': [u'IATI.document_category']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.document_category']"})
        },
        u'aims.document_link': {
            'Meta': {'object_name': 'document_link', '_ormbases': [u'IATI.document_link']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.document_link']"})
        },
        u'aims.file_format': {
            'Meta': {'object_name': 'file_format', '_ormbases': [u'IATI.file_format']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.file_format']"})
        },
        u'aims.finance_type': {
            'Meta': {'object_name': 'finance_type', '_ormbases': [u'IATI.finance_type']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.finance_type']"})
        },
        u'aims.finance_type_category': {
            'Meta': {'object_name': 'finance_type_category', '_ormbases': [u'IATI.finance_type_category']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.finance_type_category']"})
        },
        u'aims.flow_type': {
            'Meta': {'object_name': 'flow_type', '_ormbases': [u'IATI.flow_type']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.flow_type']"})
        },
        u'aims.gazetteer_agency': {
            'Meta': {'object_name': 'gazetteer_agency', '_ormbases': [u'IATI.gazetteer_agency']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.gazetteer_agency']"})
        },
        u'aims.geographical_precision': {
            'Meta': {'object_name': 'geographical_precision', '_ormbases': [u'IATI.geographical_precision']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.geographical_precision']"})
        },
        u'aims.indicator_measure': {
            'Meta': {'object_name': 'indicator_measure', '_ormbases': [u'IATI.indicator_measure']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.indicator_measure']"})
        },
        u'aims.language': {
            'Meta': {'object_name': 'language', '_ormbases': [u'IATI.language']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.language']"})
        },
        u'aims.location': {
            'Meta': {'object_name': 'location', '_ormbases': [u'IATI.location']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.location']"})
        },
        u'aims.location_type': {
            'Meta': {'object_name': 'location_type', '_ormbases': [u'IATI.location_type']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.location_type']"})
        },
        u'aims.organisation': {
            'Meta': {'object_name': 'organisation', '_ormbases': [u'IATI.organisation']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.organisation']"})
        },
        u'aims.organisation_identifier': {
            'Meta': {'object_name': 'organisation_identifier', '_ormbases': [u'IATI.organisation_identifier']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.organisation_identifier']"})
        },
        u'aims.organisation_role': {
            'Meta': {'object_name': 'organisation_role', '_ormbases': [u'IATI.organisation_role']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.organisation_role']"})
        },
        u'aims.organisation_type': {
            'Meta': {'object_name': 'organisation_type', '_ormbases': [u'IATI.organisation_type']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.organisation_type']"})
        },
        u'aims.other_identifier': {
            'Meta': {'object_name': 'other_identifier', '_ormbases': [u'IATI.other_identifier']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.other_identifier']"})
        },
        u'aims.planned_disbursement': {
            'Meta': {'object_name': 'planned_disbursement', '_ormbases': [u'IATI.planned_disbursement']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.planned_disbursement']"})
        },
        u'aims.policy_marker': {
            'Meta': {'object_name': 'policy_marker', '_ormbases': [u'IATI.policy_marker']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.policy_marker']"})
        },
        u'aims.policy_significance': {
            'Meta': {'object_name': 'policy_significance', '_ormbases': [u'IATI.policy_significance']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.policy_significance']"})
        },
        u'aims.publisher_type': {
            'Meta': {'object_name': 'publisher_type', '_ormbases': [u'IATI.publisher_type']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.publisher_type']"})
        },
        u'aims.related_activity': {
            'Meta': {'object_name': 'related_activity', '_ormbases': [u'IATI.related_activity']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.related_activity']"})
        },
        u'aims.related_activity_type': {
            'Meta': {'object_name': 'related_activity_type', '_ormbases': [u'IATI.related_activity_type']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.related_activity_type']"})
        },
        u'aims.result': {
            'Meta': {'object_name': 'result', '_ormbases': [u'IATI.result']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.result']"})
        },
        u'aims.result_type': {
            'Meta': {'object_name': 'result_type', '_ormbases': [u'IATI.result_type']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.result_type']"})
        },
        u'aims.sector': {
            'Meta': {'object_name': 'sector', '_ormbases': [u'IATI.sector']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.sector']"})
        },
        u'aims.sector_category': {
            'Meta': {'object_name': 'sector_category', '_ormbases': [u'IATI.sector_category']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.sector_category']"})
        },
        u'aims.tied_status': {
            'Meta': {'object_name': 'tied_status', '_ormbases': [u'IATI.tied_status']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.tied_status']"})
        },
        u'aims.title': {
            'Meta': {'object_name': 'title', '_ormbases': [u'IATI.title']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.title']"})
        },
        u'aims.transaction': {
            'Meta': {'object_name': 'transaction', '_ormbases': [u'IATI.transaction']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.transaction']"})
        },
        u'aims.transaction_type': {
            'Meta': {'object_name': 'transaction_type', '_ormbases': [u'IATI.transaction_type']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.transaction_type']"})
        },
        u'aims.transactionvaluelocation': {
            'Meta': {'object_name': 'TransactionValueLocation', 'db_table': "'aims_transaction_value_location'"},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'transaction_value_for_location'", 'null': 'True', 'to': u"orm['IATI.activity']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['IATI.currency']", 'null': 'True', 'blank': 'True'}),
            'dollars': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'transaction_value_for_location'", 'null': 'True', 'to': u"orm['IATI.location']"}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'transaction_value_for_location'", 'null': 'True', 'to': u"orm['IATI.transaction']"}),
            'value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'aims.transactionvalueusd': {
            'Meta': {'object_name': 'TransactionValueUSD', 'db_table': "'aims_transaction_value_usd'"},
            'dollars': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aims.CurrencyExchangeRate']", 'null': 'True', 'blank': 'True'}),
            'transaction': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'value_in'", 'unique': 'True', 'to': u"orm['IATI.transaction']"})
        },
        u'aims.userorganisation': {
            'Meta': {'object_name': 'UserOrganisation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organisations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'users'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['IATI.organisation']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'aims.value_type': {
            'Meta': {'object_name': 'value_type', '_ormbases': [u'IATI.value_type']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.value_type']"})
        },
        u'aims.verification_status': {
            'Meta': {'object_name': 'verification_status', '_ormbases': [u'IATI.verification_status']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.verification_status']"})
        },
        u'aims.vocabulary': {
            'Meta': {'object_name': 'vocabulary', '_ormbases': [u'IATI.vocabulary']},
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remote_data': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'local_data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['IATI.vocabulary']"})
        },
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'geodata.city': {
            'Meta': {'object_name': 'city'},
            'alt_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ascii_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geodata.country']", 'null': 'True', 'blank': 'True'}),
            'geoname_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'namepar': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'geodata.country': {
            'Meta': {'object_name': 'country'},
            'alpha3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'capital_city': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'capital_city'", 'null': 'True', 'to': u"orm['geodata.city']"}),
            'center_longlat': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'dac_country_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fips10': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'iso3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'numerical_code_un': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'polygon': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geodata.region']", 'null': 'True', 'blank': 'True'}),
            'un_region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'un_region'", 'null': 'True', 'to': u"orm['geodata.region']"})
        },
        u'geodata.region': {
            'Meta': {'object_name': 'region'},
            'code': ('django.db.models.fields.SmallIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'parental_region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geodata.region']", 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['aims']